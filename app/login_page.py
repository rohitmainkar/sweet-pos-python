from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import mysql.connector
import configparser
from app.user_info_page import UserInfoPage  # Corrected import statement

class LoginPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 200)

        self.label_username = QLabel("Username:", self)
        self.label_username.move(50, 30)
        self.entry_username = QLineEdit(self)
        self.entry_username.setGeometry(150, 30, 200, 20)
        
        

        self.label_password = QLabel("Password:", self)
        self.label_password.move(50, 70)
        self.entry_password = QLineEdit(self)
        self.entry_password.setGeometry(150, 70, 200, 20)
        self.entry_password.setEchoMode(QLineEdit.Password)

        self.button_login = QPushButton("Login", self)
        self.button_login.setGeometry(150, 110, 100, 30)
        self.button_login.clicked.connect(self.login)

    def login(self):
        username = self.entry_username.text()
        password = self.entry_password.text()

        # Connect to MySQL database
        config = read_config()
        try:
            conn = mysql.connector.connect(
                host=config['host'],
                user=config['user'],
                password=config['password'],
                database=config['database']
            )
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()

            if user:
                QMessageBox.information(self, "Login Successful", f"Welcome, {username}")
                self.show_user_info(user)
            else:
                QMessageBox.critical(self, "Login Failed", "Invalid username or password")

            conn.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "MySQL Error", str(err))

    def show_user_info(self, user):
        self.user_info_window = UserInfoPage(user).show()
        self.user_info_window.show()
        self.hide()

def read_config(filename='config.ini.template'):
    config = configparser.ConfigParser()
    config.read(filename)
    return config['mysql']
