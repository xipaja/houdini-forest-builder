# Forest Builder for Python Advanced Masterclass

  ![Houdini Viewport with Vine Curve](https://github.com/xipaja/python-advanced-tool/blob/main/tool_screenshots/forest_builder.PNG)

Create a forest with the geometry of your choice! Draw a curve and see trees populated on it, or create a torus for a round, strange forest. 

This tool is able to be integrated into the Houdini toolshelf.


## How it works

This tool creates different node trees depending on the geometry the user selects, and retrieves the data from specific nodes in order to perform the UI's functionality.

#### Curves
For curves, it uses a Resample node (resample into even segments) and then copies l-system trees to each point on the curve.
 
<p>How the density change works:
    <ul>
      <li>The slider adjusts the "Length" parameter of the Resample node</li>
    </ul>
</p>

#### 3D Geometry
For any other geometry, it uses a Group Range node (group points or prims by a range) and an Attribute Expression (Modify attributes with VEX expressions) node in addition to the resample node. 
  <p>This ensures that the user can change the density of the geometry with the slider, but abstracts the logic that makes this magic happen for the more complex geometry.</p>
  
  <p>How the density change works:
  <ul>
    <li> The code sets up what needs to be connected between nodes, such as setting the Group Name, Group Type, and where the range should start from </li>
    <li> The slider is connected to the "Range Filter" parameter of the Group Range node. This parameter allows the user to select "every 1 of [n] points", which increases or decreases density </li> 
  </ul>
  </p>
The tool also internally cleans up the nodes so they are laid out evenly in the Network View and are easy for the user to access in this view if they ever want to edit them.

