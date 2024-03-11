from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QMessageBox
from fpdf import FPDF
from .pdf_dialog import PDFDialog  # Import the PDFDialog class

class UserInfoPage(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("User Information")
        self.setGeometry(100, 100, 400, 200)

        self.label_username = QLabel(f"Username: {user[0]}", self)
        self.label_username.move(50, 30)

        self.label_email = QLabel(f"Email: {user[1]}", self)
        self.label_email.move(50, 70)

        self.button_generate_pdf = QPushButton("Generate PDF", self)
        self.button_generate_pdf.setGeometry(50, 110, 100, 30)
        self.button_generate_pdf.clicked.connect(lambda: self.generate_pdf(user))

    def generate_pdf(self, user):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="User Information", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Username: {user[0]}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Email: {user[1]}", ln=True, align="L")

        # Save PDF to a file
        pdf_output_path = "generated/user_info.pdf"
        pdf.output(pdf_output_path)

        # Open the PDF file in a dialog
        pdf_dialog = PDFDialog(pdf_output_path)
        pdf_dialog.exec_()
