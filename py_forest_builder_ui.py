# ***********************************************************************
# Forest Builder Tool
# Gives the user the ability to populate a geometry in Houdini with L-System "trees" and export it
#
#   
# Author: Ximena Jaramillo 
# ***********************************************************************

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from node_operations import NodeOperations

class ForestBuilderUI(QDialog):
    def __init__(self):
        super(ForestBuilderUI, self).__init__()

        self.setGeometry(100, 100, 400, 500)
        self.setWindowTitle('Forest Builder')
        self.clickFunc = ClickFunctionality()

        self.mainLayout = QVBoxLayout(self)
        spacer = QSpacerItem(40, 50)

        self.setUpCreationLayout()
        self.setUpEditLayout()
        self.mainLayout.addItem(spacer)
        self.setUpExportLayout()

    def setUpCreationLayout(self):
        creationLayout = QVBoxLayout()
        self.mainLayout.addLayout(creationLayout)
        spacer = QSpacerItem(40, 50)

        welcomeLabel = QLabel('Welcome to Forest Builder!')
        welcomeLabel.setFont(QFont('Roboto', 16))
        welcomeLabel.setAlignment(Qt.AlignCenter)
        creationLayout.addWidget(welcomeLabel)
        creationLayout.addItem(spacer)

        chooseLabel = QLabel('Choose a geometry to populate with trees')
        chooseLabel.setFont(QFont('Roboto', 10))
        chooseLabel.setAlignment(Qt.AlignCenter)

        # Geometry options dropdown
        dropdown = QComboBox()
        dropdownOptions = ['Curve', 'Box', 'Sphere', 'Tube', 'Torus', 'Grid']
        for option in dropdownOptions:
            dropdown.addItem(option)
        dropdown.activated.connect(self.clickFunc.selectionChange)
        
        createButton = QPushButton('Create Nodes')
        createButton.clicked.connect(self.clickFunc.createBtnClicked)

        self.addComponentsToLayout([chooseLabel, dropdown, createButton], creationLayout)

    def setUpEditLayout(self):
        editLayout = QVBoxLayout()
        self.mainLayout.addLayout(editLayout)

        densityLabel = QLabel('Adjust density of trees')
        densityLabel.setFont(QFont('Roboto', 10))
        densityLabel.setAlignment(Qt.AlignCenter)
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(1)
        slider.setMaximum(10)
        slider.valueChanged.connect(self.clickFunc.sliderChanged)
        
        self.addComponentsToLayout([densityLabel, slider], editLayout)

    def setUpExportLayout(self):
        exportLayout = QVBoxLayout()
        self.mainLayout.addLayout(exportLayout)
 
        titleLabel = QLabel('Export to USD')
        titleLabel.setFont(QFont('Roboto', 10))
        titleLabel.setAlignment(Qt.AlignCenter)
        nameLabel = QLabel('Name your USD file: ')

        # Add horizontal layout for file name line edit 
        fileNameHLayout = QHBoxLayout()
        fileNameLineEdit = QLineEdit()
        fileNameFileExtLabel = QLabel('.usd')
        fileNameSetButton = QPushButton('Set file name')
        fileNameLineEdit.textChanged.connect(self.clickFunc.fileNameTextChanged)

        pathLabel = QLabel('Path to export')
        self.addComponentsToLayout([fileNameLineEdit, fileNameFileExtLabel, fileNameSetButton], fileNameHLayout)
        self.addComponentsToLayout([titleLabel, nameLabel], exportLayout)
        exportLayout.addLayout(fileNameHLayout)
        exportLayout.addWidget(pathLabel)

        exportPathLayout = QHBoxLayout()
        pathLineEdit = QLineEdit()
        pathLineEdit.textChanged.connect(self.clickFunc.exportPathTextChanged)
        exportButton = QPushButton('Export')
        exportButton.clicked.connect(self.clickFunc.exportPathSet)
        self.addComponentsToLayout([pathLineEdit, exportButton], exportPathLayout)
        exportLayout.addLayout(exportPathLayout)
        
    def getlabel(self):
        return self.exportSuccessLabel
    def addComponentsToLayout(self, uiComponents, layout):
        for component in uiComponents:
            layout.addWidget(component)
        
class ClickFunctionality:
    def __init__(self):
        self.nodeOps = NodeOperations()
        self.exportPath = ''
        self.fileName = ''
        self.isSuccessLabelVisible = False
    
    def getPath(self):
        return self.exportPath

    def selectionChange(self, user_selection):
        dropdown_options = {
            0 : 'Curve',
            1 : 'Box',
            2 : 'Sphere',
            3 : 'Tube',
            4 : 'Torus',
            5 : 'Grid'
        }

        # Convert user selection to lowercase to match Houdini params
        self.nodeOps.user_selected_geo = dropdown_options[user_selection].lower() 
        
        return str(self.nodeOps.user_selected_geo)
    
    def createBtnClicked(self):
        self.nodeOps.set_up_base_nodes()
        self.nodeOps.configure_selected()
      
        self.nodeOps.add_trees()        
        
        # Layout network view in clean tree view
        self.nodeOps.base_obj.moveToGoodPosition()
        self.nodeOps.base_obj.layoutChildren()

        # Reset slider value for new geo
        # self.ui.slider_density.setValue(1) - still need to do this
        self.nodeOps.set_slider_value(1)

    def sliderChanged(self, sliderValue):
        self.nodeOps.set_slider_value(sliderValue)
        self.nodeOps.adjust_tree_density()

    def fileNameTextChanged(self, text):
        self.fileName = text

    def exportPathTextChanged(self, pathText):
        self.exportPath = pathText

    def exportPathSet(self):
        finalPath = ''
        if not self.exportPath and self.nodeOps.base_obj:
            print('Please enter an export path')
        if not self.fileName:
            self.fileName = 'forest'
        elif self.exportPath and self.fileName:
            finalPath = self.exportPath + '/' + self.fileName + '.usd'
        
        self.nodeOps.export_to_usd(finalPath)
        
        
dialog = ForestBuilderUI()
dialog.show()

