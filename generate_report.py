import csv
from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Internship Performance Report", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Generated on {datetime.now().strftime('%d-%m-%Y')}", 0, 0, "C")

def read_data(file_path):
    with open(file_path, newline="") as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data

def analyze_data(data):
    total_hours = sum(float(row["Hours Worked"]) for row in data)
    avg_score = sum(float(row["Performance Score"]) for row in data) / len(data)
    return total_hours, avg_score

def generate_pdf(data, total_hours, avg_score, end_date):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)

    # Summary
    pdf.cell(0, 10, f"Total Interns: {len(data)}", ln=True)
    pdf.cell(0, 10, f"Total Hours Worked: {total_hours}", ln=True)
    pdf.cell(0, 10, f"Average Performance Score: {avg_score:.2f}", ln=True)
    pdf.ln(10)

    # Table Header
    pdf.set_font("Arial", "B", 12)
    pdf.cell(40, 10, "Name", 1)
    pdf.cell(50, 10, "Project", 1)
    pdf.cell(40, 10, "Hours Worked", 1)
    pdf.cell(50, 10, "Performance Score", 1)
    pdf.ln()

    # Table Data
    pdf.set_font("Arial", "", 12)
    for row in data:
        pdf.cell(40, 10, row["Name"], 1)
        pdf.cell(50, 10, row["Project"], 1)
        pdf.cell(40, 10, row["Hours Worked"], 1)
        pdf.cell(50, 10, row["Performance Score"], 1)
        pdf.ln()

    # Certificate Section
    pdf.ln(20)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Completion Certificate", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, f"""
This is to certify that the interns listed above have successfully completed their internship at CODTECH.

Completion certificates will be issued on the internship end date: {end_date}.
""")
    
    pdf.output("report.pdf")
    print("PDF generated: report.pdf")

# Main Execution
if __name__ == "__main__":
    data = read_data("data.csv")
    total_hours, avg_score = analyze_data(data)
    internship_end_date = "31-07-2025"
    generate_pdf(data, total_hours, avg_score, internship_end_date)
