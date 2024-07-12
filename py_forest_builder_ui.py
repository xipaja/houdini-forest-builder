from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class ForestBuilderUI(QDialog):
    def __init__(self):
        super(ForestBuilderUI, self).__init__()

        self.setGeometry(100, 100, 400, 500)
        self.setWindowTitle('Forest Builder')

        self.setUpCreationLayout()
        self.setUpEditLayout()

    def setUpCreationLayout(self):
        creationLayout = QVBoxLayout(self)

        welcomeLabel = QLabel('Welcome to Forest Builder!', self)
        welcomeLabel.setFont(QFont('Arial', 18))
        welcomeLabel.setAlignment(Qt.AlignCenter)

        chooseLabel = QLabel('Choose a geometry to populate with trees', self)
        chooseLabel.setFont(QFont('Arial', 12))
        chooseLabel.setAlignment(Qt.AlignCenter)

        dropdown = QComboBox(self)
        
        creationComponents = [welcomeLabel, chooseLabel, dropdown]
        self.addComponentsToLayout(creationLayout, creationComponents)

    def setUpEditLayout(self):
        editLayout = QVBoxLayout(self)

        label = QLabel('Adjust density of trees', self)

    def setUpExportLayout(self):
        pass

    def addComponentsToLayout(self, layout, uiComponents):
        for component in uiComponents:
            layout.addWidget(component)
        

dialog = ForestBuilderUI()
dialog.show()

