# freecad-scripted-object

A simple example of a freecad parametric scripted object.

The code shows how to create such an object which will survive saving/opening
the document and keeps being editable using it's parameters.

If the complete python scripted object code would be in the macro, after
saving/reloading the document the created object will not be editable
anymore due to the fact that free-cad won't find the python class.

Once the class is moved in a python module on the normal python path,
free-cad will find the class and the scripted object remains editable.

# Installation

Install the fcso module (you should know how to do it on your platform, this is just a hint):

python setup.py install

Copy the hex_head_screw.FCMacro file to the free-cad macro directory, and run it !

Then edit the "data" parameters of the HexHeadScrew object, and watch it changing accordingly.

