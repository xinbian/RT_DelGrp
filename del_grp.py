#this code delete some fields from hdf5 file
#this can be used to delete "blow up results"

import h5py
import os
import os.path

curfilePath = os.path.abspath(__file__)
curDir = os.path.abspath(os.path.join(curfilePath,os.pardir))
parentDir = os.path.abspath(os.path.join(curDir,os.pardir)) 

inFile='tests_single_new.h5'
specout=1000

mylist = [parentDir,'/',inFile]
delimiter = ''
filepath = delimiter.join(mylist)

variable = ['PVz','PVy','PVx','PPress','Prho']
H5File = h5py.File(filepath,'r+')
step=['191000','192000','193000','194000','195000','196000','197000','198000','199000','200000','201000','202000','203000','204000','204272']

for i in range(651,718):
	step.append(str((i+1)*specout).zfill(6))

for istep in step:
 for variable1 in variable:
	delimiter = ''
	mylist = ['Fields/',variable1,'/',istep]
	filepath = delimiter.join(mylist)	
	del H5File[filepath]
