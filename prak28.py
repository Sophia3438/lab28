"""PyCalc: Simple calculator built with Python and PyQt."""

import sys
from functools import partial
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QGridLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QWidget,
)

# Константи
WINDOW_SIZE = 235
DISPLAY_HEIGHT = 35
BUTTON_SIZE = 40
ERROR_MSG = "ERROR"


class PyCalcWindow(QMainWindow):
    """Головне вікно калькулятора (GUI або view)."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyCalc")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)

        # Головне розташування
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)

        # Створення дисплея і кнопок
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        """Створення дисплея для калькулятора."""
        self.display = QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        """Створення кнопок калькулятора."""
        self.buttonMap = {}
        buttonsLayout = QGridLayout()
        keyBoard = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", "("],
            ["1", "2", "3", "-", ")"],
            ["0", "00", ".", "+", "%"],
            ["=", "//"],
        ]
        for row, keys in enumerate(keyBoard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                buttonsLayout.addWidget(self.buttonMap[key], row, col)
        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        """Встановити текст дисплея."""
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        """Отримати текст із дисплея."""
        return self.display.text()

    def clearDisplay(self):
        """Очистити дисплей."""
        self.setDisplayText("")


def evaluateExpression(expression):
    """Оцінити математичний вираз."""
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG
    return result


class PyCalc:
    """Контролер калькулятора."""

    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()

    def _calculateResult(self):
        """Обчислити результат і відобразити його."""
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, subExpression):
        """Побудувати математичний вираз."""
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
        expression = self._view.displayText() + subExpression
        self._view.setDisplayText(expression)

    def _connectSignalsAndSlots(self):
        """Підключити кнопки до дій."""
        for key, button in self._view.buttonMap.items():
            if key not in {"=", "C"}:
                button.clicked.connect(partial(self._buildExpression, key))
        self._view.buttonMap["="].clicked.connect(self._calculateResult)
        self._view.buttonMap["C"].clicked.connect(self._view.clearDisplay)


def main():
    """Головна функція PyCalc."""
    app = QApplication(sys.argv)
    view = PyCalcWindow()
    view.show()
    PyCalc(model=evaluateExpression, view=view)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
