import os
import getopt

#inp = 'hi'
#argv = inp.split()
#arguments
# -r recursive yes or no
# --type dir * txt
# find, replace

# renamer find replace -r --type dir
# renamer find replace -r --type dir txt docx
# renamer find replace -r 
# renamer find replace --type txt

while(True):
    argv = input('enter').lower().split()
    try:
        opts, args = getopt.getopt(argv, "r", ["type"])
        print(opts)
        print(args)
    except getopt.GetoptError as err:
        pass
    