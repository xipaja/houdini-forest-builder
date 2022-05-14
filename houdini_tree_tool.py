def createCurve():
    obj = hou.node('/obj')
    geo_node = Node(obj, 'geo', 'geo_node')
    geo_node.createNode()
    
    curve_node = Curve(geo_node, 'curve', 'curve1', True, 3)
    curve_node.createNode()

    # Set input from box node to be curve node
    # boxNode.setInput(0, curveNode, 0)
    # resample_node = createNode(geo_node, 'resample', 'resample_node')

    # connectNodes(curve_node, resample_node)

    # box_node = createNode(geo_node, 'box', 'box_node')
    
    # copy_node = createNode(geo_node, 'copytopoints::2.0', 'copy_pts')

    # connectNodes(box_node, copy_node)
    # Set display flag to true for curve node
    # curve_node.setDisplayFlag(True)
    # curveNode.setRenderFlag(1)
    
    # curve_node.setCurrent(True)
    
    # tree_node = geo_node.createNode('lsystem', 'tree')
    # tree_node.setDisplayFlag(1)
    
    # Set merge node to see both curve and trees
    # hou.node('/obj/curve_geo').createNode('merge')
    
    # TODO: set show handles (left toolbar) = true to let user draw curve on creation
    # parentLSystem(curve_node, tree_node)
    

class Node:
    """
    Node class for creating any kind of node in Houdini


    """

    def __init__(self, parent_node, node_type, name, display=True):
        self.parent_node = parent_node
        self.node_type = node_type
        self.name = name
        self.display = display
        # self.inputs = inputs

    def createNode(self):
        new_node = self.parent_node.createNode(self.node_type, self.name)
        new_node.setDisplayFlag(self.display)

        return new_node
    
    def connectNodes(self, child_node):
        self.parent_node.setInput(0, child_node, 0)

class Curve(Node):
    """
    Curve class, subclassed from Node class to have node data and also custom Curve data 


    """
    
    def __init_(self, parent_node, node_type, name, display, num_points):
        self.num_points = num_points

        super().__init__(self, parent_node, node_type, name, display)

    def createNode(self):
        new_node = self.parent_node.createNode(self.node_type, self.name)
        new_node.setDisplayFlag(self.display)

        # Set param 'Order' to user-determined num_points
        new_node.parm('order').eval(self.num_points)

        # Set curve to be NURBS curve for ease of use
        new_node.parm('outputtype').eval('NURBS Curve')
        
        return new_node
        

def parentLSystem(parent_node, child_node):
    parent_node.setInput(0, child_node,0)     

# TODO: create func to create L-System node - call it multiple times in the shell
# 
# When you build UI, have a slider or text input for number of trees you want to do
# Loop through textInput from ^ and parent to curve node