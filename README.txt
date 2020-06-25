SETUP
------------

Install Python 3.7.x (https://www.python.org/downloads/release/python-370/)

Install python module dependencies by navigating to the project root directory (e.g: cd C:\Users\Ross\Desktop\Master\Python\AmazonQ1)
and execute:  ‘pip install -r requirements.txt’

Additionally you'll need to make sure you've got GhostScript installed for Camelot (https://www.ghostscript.com/download/gsdnld.html)


EXECUTION
------------

To execute a single script navigate to the respective 'site' folder and execute the python script, for example:

py amd_script.py

After execution has finialized a JSON file with the site name (AMD.json) will be generated within the /results/ directory.

To execute ALL scripts navigate to the root folder within the project and execute the runner.py file, e.g:

py runner.py

After which each script will sequentially run, again with results generated within the /results/ directory.