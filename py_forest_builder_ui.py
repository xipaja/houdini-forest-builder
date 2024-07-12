from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class ForestBuilderUI(QDialog):
    def __init__(self):
        super(ForestBuilderUI, self).__init__()

        self.setGeometry(100, 100, 400, 500)
        self.setWindowTitle('Forest Builder')

        self.mainLayout = QVBoxLayout(self)

        self.setUpCreationLayout()
        self.setUpEditLayout()
        self.setUpExportLayout()

    def setUpCreationLayout(self):
        creationLayout = QVBoxLayout()
        self.mainLayout.addLayout(creationLayout)

        welcomeLabel = QLabel('Welcome to Forest Builder!')
        welcomeLabel.setFont(QFont('Arial', 16))
        welcomeLabel.setAlignment(Qt.AlignCenter)

        chooseLabel = QLabel('Choose a geometry to populate with trees')
        chooseLabel.setAlignment(Qt.AlignCenter)

        dropdown = QComboBox()
        dropdownOptions = ['Curve', 'Box', 'Sphere', 'Tube', 'Torus', 'Grid']
        for option in dropdownOptions:
            dropdown.addItem(option)
        
        createButton = QPushButton('Create Nodes')

        creationComponents = [welcomeLabel, chooseLabel, dropdown, createButton]
        self.addComponentsToLayout(creationLayout, creationComponents)

    def setUpEditLayout(self):
        editLayout = QVBoxLayout()
        self.mainLayout.addLayout(editLayout)

        label = QLabel('Adjust density of trees')
        slider = QSlider(Qt.Horizontal)

        editComponents = [label, slider]
        self.addComponentsToLayout(editLayout, editComponents)

    def setUpExportLayout(self):
        exportLayout = QVBoxLayout()
        self.mainLayout.addLayout(exportLayout)

        titleLabel = QLabel('Export to USD')
        pathLabel = QLabel('Path to export')

        exportComponents = [titleLabel, pathLabel]
        self.addComponentsToLayout(exportLayout, exportComponents)


    def addComponentsToLayout(self, layout, uiComponents):
        for component in uiComponents:
            layout.addWidget(component, stretch=1)
        

dialog = ForestBuilderUI()
dialog.show()

