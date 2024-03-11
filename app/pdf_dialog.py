# from PyQt5.QtWidgets import QDialog, QVBoxLayout, QMessageBox
# from PyQt5.QtCore import QUrl
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# import os
# import subprocess

# class PDFDialog(QDialog):
#     def __init__(self,_file):
#         super().__init__()
#         self.setWindowTitle("PDF Viewer")
#         self.setGeometry(100, 100, 800, 600)

#         self.web_view = QWebEngineView()
#         layout = QVBoxLayout()
#         layout.addWidget(self.web_view)
#         self.setLayout(layout)

#         self.open_pdf(_file)

#     def open_pdf(self,_file):
#         try:
#             file_path = "generated/user_info.pdf"
#             self.web_view.setUrl(QUrl.fromLocalFile(_file))
#         except FileNotFoundError:
#             QMessageBox.critical(self, "Error", "PDF file not found.")

#         # Open the PDF file using the default application
#         if os.path.exists(_file):
#             try:
#                 subprocess.Popen(['xdg-open', _file])  # For Linux
#             except FileNotFoundError:
#                 try:
#                     subprocess.Popen(['open', _file])  # For macOS
#                 except FileNotFoundError:
#                     try:
#                         subprocess.Popen(['start', '', _file], shell=True)  # For Windows
#                     except FileNotFoundError:
#                         QMessageBox.critical(self, "Error", "Failed to open PDF file.")
#         else:
#             QMessageBox.critical(self, "Error", "PDF file not found.")






from PyQt5.QtWidgets import QDialog, QVBoxLayout, QMessageBox
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os
import subprocess

class PDFDialog(QDialog):
    def __init__(self, pdf_path):
        super().__init__()
        self.setWindowTitle("PDF Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.web_view = QWebEngineView()
        layout = QVBoxLayout()
        layout.addWidget(self.web_view)
        self.setLayout(layout)

        self.open_pdf(pdf_path)

    def open_pdf(self, pdf_path):
        try:
            self.web_view.setUrl(QUrl.fromLocalFile(pdf_path))
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "PDF file not found.")

        # Open the PDF file using the default application
        if os.path.exists(pdf_path):
            try:
                subprocess.Popen(['xdg-open', pdf_path])  # For Linux
            except FileNotFoundError:
                try:
                    subprocess.Popen(['open', pdf_path])  # For macOS
                except FileNotFoundError:
                    try:
                        subprocess.Popen(['start', '', pdf_path], shell=True)  # For Windows
                    except FileNotFoundError:
                        QMessageBox.critical(self, "Error", "Failed to open PDF file.")
        else:
            QMessageBox.critical(self, "Error", "PDF file not found.")
