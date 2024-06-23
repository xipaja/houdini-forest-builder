'''
Script to generate the Houdini integration code for the forest builder tool
'''

print('\n')
print('------- Hello! Paste the following snippet into Houdini\'s tool script tab: ------- \n')
houdini_integration_script = f'''
from importlib import reload
import sys
from pathlib import Path
sys.path.append(Path.cwd())

import forest_builder
reload(forest_builder)

forest = forest_builder.ForestCreator()
'''

print(houdini_integration_script)