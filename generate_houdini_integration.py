'''
Script to generate the Houdini integration code for the forest builder tool
'''

print('\n')

print('Please enter the path to where you cloned/downloaded Forest Builder\n')
print('For example: C:/Users/Ximena/Desktop/houdini-forest-builder\n\n')

print('Enter path: ')
user_path = input()

print('\n')
print('------- Paste the following snippet into Houdini\'s tool script tab: ------- \n')
houdini_integration_script = f'''
from importlib import reload
import sys
sys.path.append("{user_path.strip()}")
import py_forest_builder_ui as ui
reload(ui)

window = ui.ForestBuilderUI()
window.show()
'''

print(houdini_integration_script)