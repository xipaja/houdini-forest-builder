# Forest Builder

Create a forest with the primitive geometry of your choice! Draw a curve and see trees populated on it, or create a 3D geometry for a different forest. 
<p align="center">
  <img src="https://github.com/xipaja/python-advanced-tool/blob/main/tool_screenshots/curve.gif" width=700 height=350 />
</p>

## How to use it

<p>To integrate into Houdini</p>
<ul>
  <li>First, run the generate_houdini_integration Python script to get the snippet you will paste into Houdini</li>
    <ul>To run script:
      <li>Open a terminal (for example, Command Prompt on Windows)</li>
      <li>Navigate to where you cloned/downloaded this project. For example, mine is on my Desktop, so I would cd to Desktop</li>
      <li>Once you're in the houdini-forest-builder folder, type "python generate_houdini_integration.py"</li>
      <li>The script will give you a snippet of code that you'll paste into Houdini soon</li>
      <li>See next steps</li>
    </ul>
  <li>Create a new tool in the shelf by right clicking on the shelf and selecting "New Tool"</li>
  <li>Navigate to the "Scripts" tab</li>
  <li>Paste that snippet you got from the generate_houdini_integration script, click "Apply" and "Accept"</li>
  <li>Click on your tool icon in the shelf, and the Forest Builder UI should appear</li>
</ul>

take the code and put it in Houdini's Python Source Editor (Windows -> Python Source Editor) and click Apply - the UI should open.
This tool is also able to be integrated into the Houdini toolshelf by right-clicking on the toolshelf, selecting "New Tool," navigating to the "Script" tab, and opening this code there.

<p>In the UI, the user can select a curve or 3D geometry from the dropdown list, and press "Create Nodes."</p>
<ul>
  <li> If the user selects a curve, they can draw the curve point by point in the viewport, and trees will automatically populate the curve
  <li> If the user selects a 3D geo, it will be populated by trees and they can play with the density slider to increase/decrease tree coverage
</ul>


  ![Houdini Viewport with Various Geometries](https://github.com/xipaja/python-advanced-tool/blob/main/tool_screenshots/forest_builder.PNG)


## How it works (behind the scenes)

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

