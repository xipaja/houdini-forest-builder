from platform import node
import hou
from PySide2 import QtCore, QtUiTools, QtWidgets

class ForestCreator(QtWidgets.QWidget):
    
    def __init__(self):
        super(ForestCreator,self).__init__()
        ui_file = 'C:/hou_temp/uiForestCreator.ui'
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        self.user_selected_geo = 'curve'

        # SIGNALS
        self.ui.dropdown.activated.connect(self.selectionChange)
        self.ui.btn_create.clicked.connect(self.btnClicked)

    def selectionChange(self, user_selection):
        print("user selection :", user_selection)
        
        dropdown_options = {
            0 : 'Curve',
            1 : 'Box',
            2 : 'Sphere',
            3 : 'Tube',
            4 : 'Torus',
            5 : 'Grid'
        }
        
        # Convert user selection to lowercase to match Houdini params
        self.user_selected_geo = dropdown_options[user_selection].lower() 
        
        return str(self.user_selected_geo)

    def btnClicked(self):

        base_obj = hou.node('/obj').createNode('geo', f'p_{self.user_selected_geo}_object')
        p_base_geo = base_obj.createNode(self.user_selected_geo, f'p_{self.user_selected_geo}')
    
        p_resample = base_obj.createNode('resample', 'p_resample')
        p_resample.setInput(0, p_base_geo, 0)

        # If a 3D geo, need to add a grouprange node for editing forest density
        if self.user_selected_geo != 'curve':
            p_connector = base_obj.createNode('grouprange', 'p_grouprange')
            p_connector.setInput(0, p_resample, 0)

        p_copy_to_points = base_obj.createNode('copytopoints::2.0', 'p_copy_to_points')
        p_copy_to_points.setInput(1, p_resample, 0)
    
        p_lsystem = base_obj.createNode('lsystem', 'p_lsystem')
        p_copy_to_points.setInput(0, p_lsystem, 0)
        p_copy_to_points.setDisplayFlag(True)


win = ForestCreator()
win.show()

 # have a slider or text input for number of trees you want to do
        # ^ corresponds to 'length' parm of resample node
        #   if user chosen geo is 1D (curve, etc), add resample node between geo and copy to pts nodes
    # slider to adjust density of trees
        # create grouprange node, connect it to chosen shape ('torus', 'curve', whatever user chooses)
        # Make sure grouprange Group Type is 'Points' ('grouptype1')
        # change Range Filter Select # of # (second parm - 'selecttotal1') based on UI slider
        # In copytopoints node, change Target Points parm ('targetgroup') to be the name of group in 
            # the grouprange node ('groupname1')
