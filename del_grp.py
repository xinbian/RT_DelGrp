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
offset=10
mylist = [parentDir,'/',inFile]
delimiter = ''
filepath = delimiter.join(mylist)

variable = ['PVz','PVy','PVx','PPress','Prho']
H5File = h5py.File(filepath,'r+')
Fields = H5File.get('Fields').values()

def get_timestepstr(dset):

    return os.path.split(dset.name)[1]

def get_LatestTime(Fields):

    maxtstep = 0

    for grp in Fields:
        dsets = grp.values()

        for dset in dsets:
            dTimestep = int(get_timestepstr(dset))
            if dTimestep > maxtstep:
                maxtstep = dTimestep

    return maxtstep

        
timestep = get_LatestTime(Fields)
step=[str(timestep).zfill(6)]
stepRht=timestep/specout

for i in range(stepRht-offset,stepRht):
	step.append(str((i+1)*specout).zfill(6))

for istep in step:
 for variable1 in variable:
	delimiter = ''
	mylist = ['Fields/',variable1,'/',istep]
	filepath = delimiter.join(mylist)	
#	del H5File[filepath]


H5File.close()
