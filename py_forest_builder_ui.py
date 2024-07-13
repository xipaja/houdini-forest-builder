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
        welcomeLabel.setFont(QFont('Roboto', 16))
        welcomeLabel.setAlignment(Qt.AlignCenter)

        chooseLabel = QLabel('Choose a geometry to populate with trees')
        chooseLabel.setFont(QFont('Roboto', 11))
        chooseLabel.setAlignment(Qt.AlignCenter)

        dropdown = QComboBox()
        dropdownOptions = ['Curve', 'Box', 'Sphere', 'Tube', 'Torus', 'Grid']
        for option in dropdownOptions:
            dropdown.addItem(option)
        
        createButton = QPushButton('Create Nodes')

        creationComponents = [welcomeLabel, chooseLabel, dropdown, createButton]
        self.addComponentsToLayout(creationComponents, creationLayout)

    def setUpEditLayout(self):
        editLayout = QVBoxLayout()
        self.mainLayout.addLayout(editLayout)

        densityLabel = QLabel('Adjust density of trees')
        densityLabel.setFont(QFont('Roboto', 11))
        densityLabel.setAlignment(Qt.AlignCenter)
        slider = QSlider(Qt.Horizontal)

        editComponents = [densityLabel, slider]
        self.addComponentsToLayout(editComponents, editLayout)

    def setUpExportLayout(self):
        exportLayout = QVBoxLayout()
        self.mainLayout.addLayout(exportLayout)
 
        titleLabel = QLabel('Export to USD')
        titleLabel.setFont(QFont('Roboto', 11))
        titleLabel.setAlignment(Qt.AlignCenter)
        nameLabel = QLabel('Name your USD file: ')

        # Add horizontal layout for file name line edit 
        fileNameHLayout = QHBoxLayout()
        fileNameLineEdit = QLineEdit()
        fileNameFileExtLabel = QLabel('.usd')

        pathLabel = QLabel('Path to export')
        exportComponents = [titleLabel, nameLabel]
        self.addComponentsToLayout([fileNameLineEdit, fileNameFileExtLabel], fileNameHLayout)
        self.addComponentsToLayout(exportComponents, exportLayout)
        exportLayout.addLayout(fileNameHLayout)
        exportLayout.addWidget(pathLabel)

        exportPathLayout = QHBoxLayout()
        pathLineEdit = QLineEdit()
        exportButton = QPushButton('Export')
        self.addComponentsToLayout([pathLineEdit, exportButton], exportPathLayout)
        exportLayout.addLayout(exportPathLayout)
    
    def addComponentsToLayout(self, uiComponents, layout):
        for component in uiComponents:
            layout.addWidget(component, stretch=1)
        

dialog = ForestBuilderUI()
dialog.show()

