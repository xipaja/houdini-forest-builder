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
        self.slider_value = 1
    
        # Nodes
        self.base_obj = None
        self.base_geo = None
        self.resample_node = None
        self.copy_to_points_node = None
        self.group_range_node = None
        self.l_system_node = None

        # Signals
        self.ui.dropdown.activated.connect(self.selectionChange)
        self.ui.btn_create.clicked.connect(self.btnClicked)
        self.ui.slider_density.valueChanged.connect(self.sliderChanged)

    # -------------------------- UI methods --------------------------
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
        self.user_selected_geo = dropdown_options[user_selection].lower() 
        
        return str(self.user_selected_geo)

    def btnClicked(self):

        self.setUpBaseNodes()
       
       # If user selects curve, change length of resample node for editing tree density
        if self.user_selected_geo == 'curve':
            self.copy_to_points_node.setInput(1, self.resample_node, 0)

        # If a 3D geo, need to add a grouprange node instead of resample for editing forest density
        elif self.user_selected_geo != 'curve':
            self.setUpGeoDensityNodes()
        
        self.addTrees()        
        
        self.group_range_node.parm('selecttotal1').set(10)
        
        # Layout network view in clean tree view
        self.base_obj.moveToGoodPosition()
        self.base_obj.layoutChildren()

    def sliderChanged(self):
        self.slider_value = self.ui.slider_density.value()

        # Adjust tree density on slider change
        # Set select every 1 of {slider_value} points in geo
        if self.user_selected_geo == 'curve':
            self.resample_node.parm('length').set(self.slider_value)
        else:
            self.group_range_node.parm('selecttotal1').set(self.slider_value)
    
    # --------------------- Node operations methods ---------------------
    def setUpBaseNodes(self):
        '''
         Sets up base nodes that all geos need 
        '''
        
        # Outer geo nodes
        self.base_obj = hou.node('/obj').createNode('geo', f'p_{self.user_selected_geo}_object')
        self.base_geo = self.base_obj.createNode(self.user_selected_geo, f'p_{self.user_selected_geo}')
    
        # Resample to equal surface segments for cleaner distribution of trees later
        self.resample_node = self.base_obj.createNode('resample', 'p_resample')
        self.resample_node.setInput(0, self.base_geo, 0)
        
        # Houdini auto set up length of resulting resample - avoids accidental user error & visual bugs 
        self.resample_node.parm('dolength').set(0)
        
        # Create copy_to_points node that will copy trees to geo points
        self.copy_to_points_node = self.base_obj.createNode('copytopoints::2.0', 'p_copy_to_points')

    def addTrees(self):
        '''
        Add the nodes necessary to add l-system "trees" to the geos
        '''
        self.l_system_node = self.base_obj.createNode('lsystem', 'p_lsystem')
        self.copy_to_points_node.setInput(0, self.l_system_node, 0)
        self.copy_to_points_node.setDisplayFlag(True)

    def setUpGeoDensityNodes(self):
        '''
        Set up the nodes for changing the density for 3D non-curve geos

        GR = Group Range
        C2P = Copy to Points

        This workflow in Houdini looks like:
            - GR node connected to Resample output and C2P input
            - GR "Group Name" = group1 (this is used later in workflow!)
            - Group "Type" changed to Points (allows for C2P to work with it)
            - GR "Range Filter" changes to "Select 1 of [slider value]", depending on user changed slider
            - C2P "Target Points" set to 'group1' - aforementioned "Group Name"
        '''

        # Group range node groups points/prims by specified ranges
        self.group_range_node = self.base_obj.createNode('grouprange', 'p_grouprange')
        self.group_range_node.setInput(0, self.resample_node, 0)

        self.copy_to_points_node.setInput(1, self.group_range_node, 0)            

        group_name = self.group_range_node.parm('groupname1')
            
        # Set up group type to be 'Points'
        self.group_range_node.parm('grouptype1').set(0)         
        self.copy_to_points_node.parm('targetgroup').set(group_name)



win = ForestCreator()
win.show()
