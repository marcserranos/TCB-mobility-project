#!/usr/bin/env python3
"""Generate a PlantUML class diagram for all Python classes in the repository."""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = REPO_ROOT / "uml" / "project_class_diagram.puml"


@dataclass
class MethodInfo:
    name: str
    args: List[str] = field(default_factory=list)
    returns: Optional[str] = None


@dataclass
class AttributeInfo:
    name: str
    typ: str = "Any"


@dataclass
class ClassInfo:
    name: str
    module: str
    bases: List[str] = field(default_factory=list)
    attributes: Dict[str, AttributeInfo] = field(default_factory=dict)
    methods: Dict[str, MethodInfo] = field(default_factory=dict)


class UMLVisitor(ast.NodeVisitor):
    def __init__(self, module: str) -> None:
        self.module = module
        self.classes: Dict[str, ClassInfo] = {}
        self.class_calls: List[Tuple[str, str, str, str]] = []
        self.param_assignments: List[Tuple[str, str, str]] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        class_name = node.name
        bases = [self._expr_to_text(base) for base in node.bases]
        info = ClassInfo(name=class_name, module=self.module, bases=bases)

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method = self._extract_method(item)
                info.methods[method.name] = method
                self._extract_self_attributes(class_name, item, info)

        self.classes[class_name] = info
        self.generic_visit(node)

    def _extract_method(self, node: ast.FunctionDef) -> MethodInfo:
        args: List[str] = []
        all_args = [*node.args.posonlyargs, *node.args.args]
        defaults_offset = len(all_args) - len(node.args.defaults)

        for index, arg in enumerate(all_args):
            if arg.arg == "self":
                continue
            label = arg.arg
            if arg.annotation is not None:
                label += f": {self._expr_to_text(arg.annotation)}"
            if index >= defaults_offset:
                default_value = node.args.defaults[index - defaults_offset]
                label += f" = {self._expr_to_text(default_value)}"
            args.append(label)

        if node.args.vararg:
            args.append(f"*{node.args.vararg.arg}")
        for kwarg, default in zip(node.args.kwonlyargs, node.args.kw_defaults):
            label = kwarg.arg
            if kwarg.annotation is not None:
                label += f": {self._expr_to_text(kwarg.annotation)}"
            if default is not None:
                label += f" = {self._expr_to_text(default)}"
            args.append(label)
        if node.args.kwarg:
            args.append(f"**{node.args.kwarg.arg}")

        returns = self._expr_to_text(node.returns) if node.returns is not None else None
        return MethodInfo(name=node.name, args=args, returns=returns)

    def _extract_self_attributes(self, class_name: str, fn: ast.FunctionDef, info: ClassInfo) -> None:
        param_names = {arg.arg for arg in [*fn.args.posonlyargs, *fn.args.args]}

        for node in ast.walk(fn):
            if not isinstance(node, ast.Assign):
                continue

            value_repr = self._expr_to_text(node.value)
            for target in node.targets:
                if not isinstance(target, ast.Attribute) or not isinstance(target.value, ast.Name):
                    continue
                if target.value.id != "self":
                    continue

                attr_name = target.attr
                inferred_type = self._infer_type(node.value)
                info.attributes[attr_name] = AttributeInfo(name=attr_name, typ=inferred_type)

                if isinstance(node.value, ast.Call):
                    called = self._expr_to_text(node.value.func)
                    self.class_calls.append((class_name, attr_name, called, inferred_type))
                elif isinstance(node.value, ast.Name) and node.value.id in param_names:
                    self.param_assignments.append((class_name, attr_name, node.value.id))

    def _infer_type(self, value: ast.AST) -> str:
        if isinstance(value, ast.Call):
            return self._expr_to_text(value.func)
        if isinstance(value, ast.Constant):
            return type(value.value).__name__
        if isinstance(value, ast.List):
            return "list"
        if isinstance(value, ast.Dict):
            return "dict"
        if isinstance(value, ast.Tuple):
            return "tuple"
        if isinstance(value, ast.Name):
            return value.id
        return "Any"

    def _expr_to_text(self, expr: Optional[ast.AST]) -> str:
        if expr is None:
            return ""
        try:
            return ast.unparse(expr)
        except Exception:
            return expr.__class__.__name__


def visibility(symbol_name: str) -> str:
    if symbol_name.startswith("__") and not symbol_name.endswith("__"):
        return "-"
    if symbol_name.startswith("_") and not symbol_name.startswith("__"):
        return "#"
    return "+"


def collect_classes(repo_root: Path) -> Tuple[Dict[str, ClassInfo], List[Tuple[str, str, str, str]], List[Tuple[str, str, str]]]:
    classes: Dict[str, ClassInfo] = {}
    calls: List[Tuple[str, str, str, str]] = []
    params: List[Tuple[str, str, str]] = []

    for py_file in sorted(repo_root.rglob("*.py")):
        if ".git" in py_file.parts or "__pycache__" in py_file.parts:
            continue
        if py_file.relative_to(repo_root).parts[0] in {"tools", "uml"}:
            continue
        source = py_file.read_text(encoding="utf-8")
        module = py_file.relative_to(repo_root).as_posix().replace(".py", "")
        visitor = UMLVisitor(module=module)
        visitor.visit(ast.parse(source))
        for name, info in visitor.classes.items():
            classes[name] = info
        calls.extend(visitor.class_calls)
        params.extend(visitor.param_assignments)

    return classes, calls, params


def build_plantuml(classes: Dict[str, ClassInfo], calls: List[Tuple[str, str, str, str]], params: List[Tuple[str, str, str]]) -> str:
    lines: List[str] = [
        "@startuml",
        "title TCB Mobility Project - Class Diagram",
        "skinparam classAttributeIconSize 0",
        "hide empty members",
        "",
    ]

    sorted_classes = sorted(classes.values(), key=lambda c: c.name)
    for class_info in sorted_classes:
        lines.append(f'class "{class_info.name}" as {class_info.name} <<{class_info.module}>> {{')

        for attr in sorted(class_info.attributes.values(), key=lambda a: a.name):
            vis = visibility(attr.name)
            lines.append(f"  {vis} {attr.name}: {attr.typ}")

        if class_info.attributes and class_info.methods:
            lines.append("  --")

        for method in sorted(class_info.methods.values(), key=lambda m: m.name):
            vis = visibility(method.name)
            signature = ", ".join(method.args)
            returns = f": {method.returns}" if method.returns else ""
            lines.append(f"  {vis} {method.name}({signature}){returns}")

        lines.append("}")
        lines.append("")

    # Inheritance
    for class_info in sorted_classes:
        for base in class_info.bases:
            if base in classes:
                lines.append(f"{base} <|-- {class_info.name}")

    # Composition/aggregation from instantiated class assignments
    seen_rel: Set[Tuple[str, str, str]] = set()
    for owner, attr_name, called, _ in calls:
        target = called.split(".")[-1]
        if target in classes:
            rel = (owner, target, attr_name)
            if rel in seen_rel:
                continue
            seen_rel.add(rel)
            lines.append(f'{owner} "1" *-- "1" {target} : {attr_name}')

    # Associations based on parameter storage when parameter name hints object relationship
    for owner, attr_name, param_name in params:
        hint = f"{attr_name} {param_name}".lower()
        if not any(token in hint for token in ("_obj", "object", "instance", "loc", "location")):
            continue
        matches = [cls for cls in classes if cls.lower() in hint and cls != owner]
        for target in matches:
            rel = (owner, target, attr_name)
            if rel in seen_rel:
                continue
            seen_rel.add(rel)
            lines.append(f'{owner} "1" o-- "0..1" {target} : {attr_name}')

    # Dependencies from method arguments (annotations or naming conventions)
    for class_info in sorted_classes:
        for method in class_info.methods.values():
            for arg in method.args:
                name_part = arg.split(":", 1)[0].strip()
                ann = arg.split(":", 1)[1].strip() if ":" in arg else ""
                ann_base = ann.split("=")[0].strip()
                ann_cls = ann_base.split("[")[-1].replace("]", "")
                ann_cls = ann_cls.split("|")[0].strip()

                candidate_targets = set()
                if ann_cls in classes and ann_cls != class_info.name:
                    candidate_targets.add(ann_cls)

                lowered_name = name_part.lower()
                if any(token in lowered_name for token in ("_obj", "object", "instance")):
                    for cls in classes:
                        if cls.lower() in lowered_name and cls != class_info.name:
                            candidate_targets.add(cls)

                for target in sorted(candidate_targets):
                    rel = (class_info.name, target, method.name)
                    if rel in seen_rel:
                        continue
                    seen_rel.add(rel)
                    lines.append(f"{class_info.name} ..> {target} : uses {method.name}")

    lines.append("")
    lines.append("legend left")
    lines.append("  + public")
    lines.append("  # protected (by convention)")
    lines.append("  - private (name-mangled convention)")
    lines.append("  *-- composition")
    lines.append("  o-- aggregation")
    lines.append("  <|-- inheritance")
    lines.append("endlegend")
    lines.append("@enduml")
    return "\n".join(lines)


def main() -> None:
    classes, calls, params = collect_classes(REPO_ROOT)
    plantuml = build_plantuml(classes, calls, params)
    OUTPUT_PATH.write_text(plantuml, encoding="utf-8")
    print(f"Wrote UML diagram code to: {OUTPUT_PATH}")
    print(f"Classes included: {len(classes)}")


if __name__ == "__main__":
    main()
