def createCurve():
    obj = hou.node('/obj')
    geo_node = obj.createNode('geo', 'curve_geo')
    
    curve_node = geo_node.createNode('drawcurve', 'new_curve')
    
    # Set input from box node to be curve node
    # boxNode.setInput(0, curveNode, 0)
    
    # Set display flag to true for curve node
    curve_node.setDisplayFlag(True)
    # curveNode.setRenderFlag(1)
    
    curve_node.setCurrent(True)
    
    tree_node = geo_node.createNode('lsystem', 'tree')
    tree_node.setDisplayFlag(1)
    
    # Set merge node to see both curve and trees
    # hou.node('/obj/curve_geo').createNode('merge')
    
    # TODO: set show handles (left toolbar) = true to let user draw curve on creation
    parentLSystem(curve_node, tree_node)
    
def parentLSystem(parent_node, child_node):
    parent_node.setInput(0, child_node,0)     

            