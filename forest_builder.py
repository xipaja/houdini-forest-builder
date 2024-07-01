# ***********************************************************************
# Forest Builder Tool
# Gives the user the ability to populate a geometry in Houdini with L-System "trees"
#
# How to use:
#   In Houdini, open this in Windows -> Python Source Editor 
#   Click "Apply" and UI will pop up
#   * Can also create a shelf tool in Houdini and place this code there
#   
# Author: Ximena Jaramillo 
# ***********************************************************************

import hou
from pathlib import Path
from PySide2 import QtCore, QtUiTools, QtWidgets 
from node_operations import NodeOperations

class ForestCreator(QtWidgets.QWidget):
    
    def __init__(self):
        super(ForestCreator,self).__init__()

        # Get UI file path
        ui_absolute_path = Path(__file__).with_name('uiForestBuilder.ui').absolute()
        ui_file = str(ui_absolute_path.as_posix())

        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        self.nodeOps = NodeOperations()

        # Signals
        self.ui.dropdown.activated.connect(self.selectionChange)
        self.ui.btn_create.clicked.connect(self.createBtnClicked)
        self.ui.slider_density.valueChanged.connect(self.sliderChanged)
        self.ui.export_btn.clicked.connect(self.exportBtnClicked)

    # -------------------------- UI event methods --------------------------
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
        self.ui.slider_density.setValue(1)


    def sliderChanged(self):
        self.nodeOps.set_slider_value(self.ui.slider_density.value())

        self.nodeOps.adjust_tree_density()
    
    def exportBtnClicked(self):
        exportPath = self.ui.path_edit.text()
        self.nodeOps.export_to_usd(exportPath)

        # once exported, print ("Export complete!" - try to do it in the UI itself)
        # label that once clicked appears in Qt

win = ForestCreator()
win.show()
