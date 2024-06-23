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
        self.ui.btn_create.clicked.connect(self.btnClicked)
        self.ui.slider_density.valueChanged.connect(self.sliderChanged)

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

    def btnClicked(self):
  
        self.nodeOps.set_up_base_nodes()
        self.nodeOps.config_selected()
      
        self.nodeOps.add_trees()        
        
        # Layout network view in clean tree view
        self.nodeOps.base_obj.moveToGoodPosition()
        self.nodeOps.base_obj.layoutChildren()

        # Reset slider value for new geo
        self.ui.slider_density.setValue(1)


    def sliderChanged(self):
        self.nodeOps.slider_value = self.ui.slider_density.value()

        self.nodeOps.adjust_tree_density()

win = ForestCreator()
win.show()
