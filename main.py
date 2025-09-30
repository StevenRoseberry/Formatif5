import sys
from PyQt6.QtWidgets import QApplication, QWidget
from function_view import FonctionView
from function_model import FonctionModel

def main():
    app = QApplication(sys.argv)
    model = FonctionModel()
    view = FonctionView(model)
    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()