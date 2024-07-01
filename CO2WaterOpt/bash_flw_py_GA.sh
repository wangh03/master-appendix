#!/bin/bash

#a base bash file to be modified.

# Parameter 1: Work directory.
# Parameter 2: Path to .DATA file

cd $1

/usr/bin/flow $2 >/dev/null
/usr/bin/python3 /home/wangh/Documents/FieldOpt/examples/Flow/CO2WaterOpt/PythonDir/ObjFunCal.py 
