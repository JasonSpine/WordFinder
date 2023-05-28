# Requires Python 3.5+ and PyQt5 installed!
# pip install PyQt5

import sys
from collections import Counter

from PyQt5.QtWidgets import (
	QApplication,
	QMainWindow,
	QWidget,
	QFormLayout,
	QLineEdit,
	QSpinBox,
	QPlainTextEdit,
	QPushButton,
	QMessageBox,
)

from PyQt5.QtCore import (
	Qt,
)

from PyQt5.QtGui import (
	QFont,
)

def filter_words(dictionary_file, char_set, char_count):
	char_counts = Counter(char_set)
	filtered_words = []
	with open(dictionary_file, 'r', encoding='utf-8') as file:
		for line in file:
			word = line.strip()
			if len(word) == char_count and all(char_counts[char] >= word.count(char) for char in set(word)):
				filtered_words.append(word)
	return filtered_words

class WordFinder(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Word Finder")
		self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint) #| Qt.WindowStaysOnTopHint)
		self.setStyleSheet("font-size: 16pt;")
		
		centralWidget = QWidget(self)
		self.setCentralWidget(centralWidget)
		windowLayout = QFormLayout()
		centralWidget.setLayout(windowLayout)
		
		self.charactersEdit = QLineEdit("talżye")
		self.charactersEdit.textChanged.connect(self.charactersEditTextChanged)
		
		self.charCountEdit = QSpinBox()
		self.charCountEdit.setSingleStep(1)
		self.charactersEditTextChanged(self.charactersEdit.text())
		self.charCountEdit.setValue(4)
		
		f = QFont("unexistent")
		f.setStyleHint(QFont.Monospace)
		f.setWeight(90)
		#f.setPointSize(12)
		
		self.outputArea = QPlainTextEdit()
		self.outputArea.setFixedHeight(550)
		self.outputArea.setFixedWidth(300)
		self.outputArea.setFont(f)
		
		self.findButton = QPushButton("Find!")
		self.findButton.clicked.connect(self.findWords)
		
		windowLayout.addRow("Word characters", self.charactersEdit)
		windowLayout.addRow("Word characters count", self.charCountEdit)
		windowLayout.addRow("Confirm", self.findButton)
		windowLayout.addRow("Output", self.outputArea)
	
	def charactersEditTextChanged(self, text):
		l = len(text)
		if l > 1:
			self.charCountEdit.setRange(2, l)
	
	def findWords(self):
		dictionary_file = 'dictionary.txt'  # Zmień na nazwę pliku ze słownikiem
		char_set = self.charactersEdit.text()  # Zmień na zestaw znaków, które chcesz użyć
		char_count = self.charCountEdit.value()  # Ile dokładnie znaków mają mieć zwracane słowa?

		filtered_words = filter_words(dictionary_file, char_set, char_count)
		
		self.outputArea.clear()
		
		for word in filtered_words:
			self.outputArea.insertPlainText(f"{word}\n")
			
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
			self.findWords()
		

app = QApplication(sys.argv)

window = WordFinder()
window.show()

sys.exit(app.exec_())
