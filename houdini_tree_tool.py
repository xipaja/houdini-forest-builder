from sqlite3 import connect


def createCurve():
    obj = hou.node('/obj')
    geo_node = createNode(obj, 'geo', 'curve_geo_node')
    
    curve_node = createNode(geo_node, 'curve', 'new_curve')

    # Set input from box node to be curve node
    # boxNode.setInput(0, curveNode, 0)
    resample_node = createNode(geo_node, 'resample', 'resample_node')

    connectNodes(curve_node, resample_node)

    box_node = createNode(geo_node, 'box', 'box_node')
    
    copy_node = createNode(geo_node, 'copytopoints::2.0', 'copy_pts')

    connectNodes(box_node, copy_node)
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
    

# class Node
#   self.name = name
#   self.input = input
# This func would go in class Node
def createNode(parent_node, node_type, name):
    new_node = parent_node.createNode(node_type, name)
    new_node.setDisplayFlag(True)

    return new_node

# This func also goes in Node class
def connectNodes(parent_node, child_node):
    parent_node.setInput(0, child_node, 0)

def parentLSystem(parent_node, child_node):
    parent_node.setInput(0, child_node,0)     

# TODO: create func to create L-System node - call it multiple times in the shell
# 
# When you build UI, have a slider or text input for number of trees you want to do
# Loop through textInput from ^ and parent to curve node