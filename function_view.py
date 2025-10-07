import sys
import sympy as sp
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QColorDialog
)
from PyQt6 import uic
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from function_model import FonctionModel
from mpl_canvas import MplCanvas


class FonctionView(QMainWindow):
    def __init__(self):
        super().__init__()

        # Interface pas encore faite :(
        uic.loadUi("ui/function_view.ui", self)


        self.model = FonctionModel()

        self.canvas = MplCanvas(self)
        self.layout_canvas.addWidget(NavigationToolbar(self.canvas, self))
        self.layout_canvas.addWidget(self.canvas)


        self.button_draw.clicked.connect(self.on_draw_clicked)
        self.text_function.editingFinished.connect(self.on_function_changed)
        self.text_title.editingFinished.connect(self.on_title_changed)
        self.checkbox_grid.stateChanged.connect(self.on_grid_changed)

        # Menu couleur
        self.actionCouleur.triggered.connect(self.on_color_menu)

        # Ajustement dynamique de la taille
        self.canvas.setMinimumSize(400, 300)


        # Les boutons et tout
    def on_function_changed(self):
        f_str = self.text_function.toPlainText().strip()
        if self.model.set_function(f_str):
            # fonction valide
            return
        else:
            # fonction invalide  = message d'erreur
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Expression fonctionnelle invalide.")
            msg.setWindowTitle("Erreur")
            msg.exec()

    def on_title_changed(self):
        title = self.text_title.toPlainText().strip()
        self.model.set_title(title)

    def on_grid_changed(self, state):
        show_grid = (state == 2)  # 2 = Checked dans Qt
        self.model.set_grid(show_grid)

    def on_color_menu(self):
        qcolor = QColorDialog.getColor()
        if qcolor.isValid():
            self.model.set_color(qcolor)

    def on_draw_clicked(self):

        f = self.model.get_callable_function()
        title = self.model.title
        show_grid = self.model.show_grid
        color = self.model.color

        if f is None:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Veuillez entrer une fonction valide avant de dessiner.")
            msg.setWindowTitle("Erreur")
            msg.exec()
            return

        # Dessine la fonction
        import numpy as np
        x_vals = np.linspace(-10, 10, 400)
        try:
            y_vals = f(x_vals)
        except Exception:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Erreur lors de l'évaluation de la fonction.")
            msg.setWindowTitle("Erreur")
            msg.exec()
            return

        self.canvas.axes.clear()
        self.canvas.axes.plot(x_vals, y_vals, color=color)
        self.canvas.axes.set_title(title)
        self.canvas.axes.grid(show_grid)
        self.canvas.draw()