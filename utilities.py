import random

# This class provides utility functions for data loading, ID generation, PDF creation, and email sending.

class Utilities:    
    @staticmethod
    def generate_random_id() -> str:
        """Generates a random 14-character ID as a string."""
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        # Compact form of generating a random string from the specified characters
        # The probability of collision is very low for our use case, we won't check for duplicates here.
        return ''.join(random.choice(chars) for _ in range(14))
    
    @staticmethod
    def export_ranking_pdf(ranked_list, filepath: str):
        """Write the top-10 entries from ranked_list to a simple PDF file."""
        from fpdf import FPDF

        pdf = FPDF()
        pdf.add_page()
        from datetime import date

        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", "B", 16)
        today = date.today().strftime("%Y-%m-%d")
        pdf.cell(0, 10, f"{today} Ranking", ln=True, align="C")
        pdf.ln(4)
        pdf.set_font("Arial", "", 12)
        for idx, (uni, score) in enumerate(ranked_list[:10], start=1):
            name = uni.get_uni_att('name') or 'Unknown'
            pdf.cell(0, 8, f"{idx}. {name} - {score:.2f}", ln=True)
        pdf.output(filepath)
