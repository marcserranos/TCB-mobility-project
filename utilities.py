import random

# This class provides utility functions for data loading, ID generation, PDF creation, and email sending.
class Utilities:
    # Public methods (+)
    
    # We decided to try and use @staticmethods, as these methods do not require any instance-specific data.
    # In the case of Utility funcions, we won't need to create an instance of Utilities to use them.

    @staticmethod
    def generate_random_id() -> str:
        """Generates a random 14-character ID as a string."""
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        # Compact form of generating a random string from the specified characters
        # The probability of collision is very low for our use case, thus we won't check for duplicates here.
        return ''.join(random.choice(chars) for _ in range(14))

    @staticmethod
    def choose_random_id(): pass
    
    @staticmethod
    def create_pdf(): pass
    
    @staticmethod
    def export_ranking_pdf(ranked_list, filepath: str):
        """Write the top-10 entries from ranked_list to a simple PDF file.

        ``ranked_list`` should be a sequence of ``(university, score)`` tuples.
        A basic text-based layout is generated using fpdf2 (already in
        requirements.txt).
        """
        try:
            from fpdf import FPDF
        except ImportError:
            raise RuntimeError("fpdf library is required for PDF export")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "University Ranking", ln=True, align="C")
        pdf.ln(4)
        pdf.set_font("Arial", "", 12)
        for idx, (uni, score) in enumerate(ranked_list[:10], start=1):
            name = uni.get_uni_att('name') or 'Unknown'
            pdf.cell(0, 8, f"{idx}. {name} - {score:.2f}", ln=True)
        pdf.output(filepath)

    
    @staticmethod
    def send_mail(): pass