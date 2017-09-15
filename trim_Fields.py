import sys
import os.path
import getopt
import h5py

def print_usage():

    print ("usage: python trim_Fields.py [-t <timestep>] <inputfile>")
    print ("")
    print ("    If no timestep is given, timestep value is taken from the latest CheckPoint")

def parse_args(argv):

    inputfile = ''

    try:
        opts, args = getopt.getopt(argv, "ht:", ["help","timestep="])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_usage()
            sys.exit()
        if opt in ("-t", "--timestep"):
            timestep = arg

    if len(argv) not in (1,3):
        print_usage()
        sys.exit(2)
    else:
        inputfile = args[0]

    if len(opts) is 0:
        timestep = -1

    return inputfile, timestep


def get_timestepstr(dset):

    return os.path.split(dset.name)[1]


def get_LatestTime(ChkPoints):

    maxtstep = 0

    for grp in ChkPoints:
        dsets = grp.values()

        for dset in dsets:
            dTimestep = int(get_timestepstr(dset))
            if dTimestep > maxtstep:
                maxtstep = dTimestep

    return maxtstep


def trim_Fields(Fields, timestep):

    for grp in Fields:
        dsets = grp.values()

        for dset in dsets:
            if int(timestep) < int(get_timestepstr(dset)):
                del grp[dset.name]


if __name__ == "__main__":

    inputfile, timestep = parse_args(sys.argv[1:])

    H5File = h5py.File(inputfile, 'r+')
    H5Groups = H5File.get('Fields').values() + H5File.get('CheckPoints').values()+H5File.get('Refine').values()

    if timestep == -1:
        ChkPoints = H5File.get('CheckPoints').values()
        timestep = get_LatestTime(ChkPoints)

    trim_Fields(H5Groups, timestep)

    H5File.close()
