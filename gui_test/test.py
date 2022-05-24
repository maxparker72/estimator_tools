import sys
from gooey import Gooey
@Gooey 

def main(argv):
    print(argv)

if __name__ == "__main__":
   main(sys.argv[1:])