from email.mime import base
import hou 
import json 

json_path = "C:\Users\xipaj\Desktop\python_advanced_tool\python-advanced-tool"

base_shape_data = {
    'Torus SOP': 'torus',
    'Box SOP': 'box',
    'Grid SOP': 'grid',
    'Draw Curve SOP': 'drawcurve',
    'Curve SOP': 'curve'
}

"""
This config will help with the UI later, as I plan to give the user options of shapes they can use to
populate trees on top of
"""
with open(json_path, 'w') as outFile:
    json.dump(base_shape_data, outFile, indent=4)

class Node:
    """
    Node class for creating any kind of node in Houdini

    Args:
        parent_node(hou node): parent_node this node will be nested in
        node_type(str): Houdini node type for this node
        given_name(str): User-given name for this node
        display(bool): Displays this node (or not)
    """

    def __init__(self, parent_node, node_type, given_name, display=True):
        self.parent_node = parent_node
        self.node_type = node_type
        self.given_name = given_name
        self.display = display

        self.parent_node.createNode(self.node_type, self.given_name)
        # new_node.setDisplayFlag(self.display)

    def print_node_status(self, incoming_func):
        def wrapper(*args):
            print('Creating Node...')
            incoming_func(args)
            print(f'Node {self.given_name} of type {self.node_type} created!')
        return wrapper

    @print_node_status
    def create_node(self):
        new_node = self.parent_node.createNode(self.node_type, self.name)
        new_node.setDisplayFlag(self.display)

        return new_node

    def connect_nodes(self, child_node):
        self.parent_node.setInput(0, child_node, 0)

class CurveNode(Node):
    """
    Curve class, derived from Node class to have node data and also custom Curve data 

    Args:
        parent_node(hou node): parent_node this node will be nested in
        node_type(str): Houdini node type for this node
        given_name(str): User-given name for this node
        num_points(int): Num of points for this node - will eventually be a slider in UI

    This is useful as a class because I would like it to be like the Node class, but have
    its own custom values, such as the number of points (entered by user)
    """
    
    def __init__(self, parent_node, node_type, given_name, num_points):
        super().__init__(parent_node, node_type, given_name)

        self.num_points = num_points

        new_node = self.createNode(self.parent_node, self.node_type, self.given_name)
        new_node.setDisplayFlag(self.display)

        # Set param 'Order' to user-determined num_points
        new_node.parm('order').set(self.num_points)

        # Set curve to be Bezier curve for ease of use
        new_node.parm('outputtype').set('Bezier Curve')

def main():
    obj = hou.node('/obj')

    curve_node = CurveNode(parent_node=obj, node_type='curve', given_name='p_curve', num_points=4)
    
    # curve_obj = hou.node('/obj').createNode('geo', 'p_curve_objects')
    # p_curve1 = curve_obj.createNode('curve', 'p_curve1')
    
    # p_resample = curve_obj.createNode('resample', 'p_resample')
    # p_resample.setInput(0, p_curve1, 0)
    
    # p_copy_to_points = curve_obj.createNode('copytopoints::2.0', 'p_copy_to_points')
    # p_copy_to_points.setInput(1, p_resample, 0)
    
    # p_lsystem = curve_obj.createNode('lsystem', 'p_lsystem')
    # p_copy_to_points.setInput(0, p_lsystem, 0)
    # p_copy_to_points.setDisplayFlag(True)

    # Upcoming TOOOs
        # if not exist, create
        # from.to architecture instead of Houdini's to.from (builder) for setInput 
        # translation layer for (0, p_curve1, 0) - what are the 0 inputs? Add useful var names for user
        # spread out network view - not have to manually drag the nodes around to see    them all

    # UI TODOs
    # have a slider or text input for number of trees you want to do
        # ^ corresponds to 'length' parm of resample node
        #   if user chosen geo is 1D (curve, etc), add resample node between geo and copy to pts nodes
    # slider to adjust density of trees
        # create grouprange node, connect it to chosen shape ('torus', 'curve', whatever user chooses)
        # change Range Filter Select # of # (second parm - 'selecttotal1') based on UI slider
        # In copytopoints node, change Target Points parm ('targetgroup') to be the name of group in 
            # the grouprange node ('groupname1')
        # Make sure grouprange Group Type is 'Points' ('grouptype1')
