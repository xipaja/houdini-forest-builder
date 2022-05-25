class NodeOperations():
    def __init__(self):
        # Nodes
        self.base_obj = None
        self.base_geo = None
        self.resample_node = None
        self.copy_to_points_node = None
        self.group_range_node = None
        self.l_system_node = None
        self.attr_exp_node = None

        self.user_selected_geo = 'curve'
        self.slider_value = 5


 # --------------------- Node operations methods ---------------------
    def set_up_base_nodes(self):
        '''
         Sets up base nodes that all geos need 

         base_obj is the /obj level node
         base_geo is what will become the base geometry node - for example, 'curve' node
        '''
        
        # Outer geo nodes
        self.base_obj = hou.node('/obj').createNode('geo', f'p_{self.user_selected_geo}_object')
        self.base_geo = self.base_obj.createNode(self.user_selected_geo, f'p_{self.user_selected_geo}')
    
        # Resample to equal surface segments for cleaner distribution of trees later
        self.resample_node = self.base_obj.createNode('resample', 'p_resample')
        self.resample_node.setInput(0, self.base_geo, 0)
                
        # Create copy_to_points node that will copy trees to geo points
        self.copy_to_points_node = self.base_obj.createNode('copytopoints::2.0', 'p_copy_to_points')

    def config_selected(self):
        '''
        Logic for handling different node setup depending on user selected geo
        
        '''
         # If user selects curve, change length of resample node for editing tree density
        if self.user_selected_geo == 'curve':
            self.copy_to_points_node.setInput(1, self.resample_node, 0)
            self.resample_node.parm('length').set(4.5)
            self.base_geo.setCurrent(True)

        # If a 3D geo, need to add a grouprange node instead of resample for editing forest density
        elif self.user_selected_geo != 'curve':
            # Adjust slider value to work with 3D geos
            self.slider_value = 10

            # Houdini auto set up length of resulting resample - avoids accidental user error & visual bugs 
            self.resample_node.parm('dolength').set(0)
            self.set_up_density_nodes()
        
    def add_trees(self):
        '''
        Add the nodes necessary to add l-system "trees" to the geos
        '''
        self.l_system_node = self.base_obj.createNode('lsystem', 'p_lsystem')
        self.copy_to_points_node.setInput(0, self.l_system_node, 0)
        self.copy_to_points_node.setDisplayFlag(True)

    def set_up_density_nodes(self):
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

        self.set_trees_upright()

        group_name = self.group_range_node.parm('groupname1')
        self.group_range_node.parm('selecttotal1').set(10)
            
        # Set up group type to be 'Points'
        self.group_range_node.parm('grouptype1').set(0)         
        self.copy_to_points_node.parm('targetgroup').set(group_name)

        self.group_range_node.parm('selecttotal1').set(10)

    def adjust_tree_density(self):
        '''
        Adjust tree density on slider change
        '''
         
        # Set select every 1 of {slider_value} points in geo
        if self.user_selected_geo == 'curve':
            self.resample_node.parm('length').set(5 - (self.slider_value/2))
        else:
            self.group_range_node.parm('selecttotal1').set(11 - self.slider_value)

    def set_trees_upright(self):
        '''
        Rotates trees to be along ZX plane on surface normals to give appearance of standing upright
        '''
        self.attr_exp_node = self.base_obj.createNode('attribexpression', 'p_attr_exp')
        self.attr_exp_node.setInput(0, self.group_range_node, 0)
        self.copy_to_points_node.setInput(1, self.attr_exp_node, 0)

        # Set attr exp to Normals and Flatten to ZX plane
        self.attr_exp_node.parm('preset1').set(6)
        self.attr_exp_node.parm('snippet1').set('set(self.x, 0, self.z)')
