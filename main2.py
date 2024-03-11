# import sys
# from PyQt5.QtWidgets import QApplication
# from app.login_page import LoginPage

# def main():
#     app = QApplication(sys.argv)
#     login_page = LoginPage()
#     login_page.show()
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()


from PyQt5.QtWidgets import QApplication
from app.login_page import LoginPage

if __name__ == "__main__":
    app = QApplication([])
    login_page = LoginPage()
    login_page.show()
    app.exec_()
