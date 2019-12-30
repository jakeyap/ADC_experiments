Author: yyk

To use icarus, install the prepackaged windows installers from this website
http://bleyer.org/icarus/
The full guide is at 
http://codeitdown.com/icarus-verilog-on-windows/

2 pieces of software have to be installed
iverilog is the verilog intepreter tool
gtkwave is the GUI to view the results

let's say you have a file called testbench.v and there are 2 modules called moduleA.v and moduleB.v that are instantiated inside testbench.

the command to run the simulation is as follows.

============Command============
iverilog -o <output-file-name> <list of verilog files to compile>
===============================

In our example, the relevant command would be 
iverilog -o outputfile testbench.v moduleA.v moduleB.v

This will spit out a raw text file called outputfile.
The next step is to actually run the simulation using a software called vvp.

============Command============
vvp outputfile
===============================
This spits out another file that can be interpreted by the GUI.

============Command============
gtkwave outputfile.vcd
===============================
Enjoy.

