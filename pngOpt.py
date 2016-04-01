#! /usr/bin/python -B

###############################################################
########                  pngOpt.py                   ######## 
########             Made by Thomas Roberts            ######## 
########                  01/04/2016                   ########
###############################################################
from __future__ import division
import os
import sys
import logging
from PIL import Image


# Optimise jpeg function
# Input :- Source DIR
# Input :- Destination DIR
# Output :- Boolean
# Description:- This function will optimise pngs
def pngOpt(source, destination):
    # Return Value initialisations
    returnValue = True
    
    logging.info("Scanning %s for pngs", source)
    # Scan the sour DIR to find all png's init
    pngs = [f for f in os.listdir(source) if f.endswith('png')]
    
    if (len(pngs) > 0):
        logging.info("Found %d pngs to optimise", len(pngs))
        for i in range(len(pngs)):
            # Start optimising jepg's
            src = os.path.abspath(source + "/" + pngs[i])
            dest =  os.path.abspath(destination + "/" + pngs[i])
            if not os.path.isdir(destination):
                os.mkdir(destination)
            image = Image.open(src)
            image.save(dest,optimize=True)
            srcSize = os.path.getsize(src)
            destSize = os.path.getsize(dest)
            percentDiff = ((srcSize - destSize) / srcSize) * 100
            logging.info("Reduced image %d by %.2f %%", i + 1 , percentDiff)
    else:
        # We didn't find any png's
        logging.error("Found no png's in %s", source)
        returnValue = False

    return returnValue

# Check Arguments
# Input:- Source directory
# Input:- Destination directory
# Output:- Boolean, True is everything is ok
# This function will check the source and destination directory
def checkArgs(source, destination):

    returnValue = True
    
    if not os.path.isdir(source):
        logging.error("Source directory %s doesn't exist", source)
        returnValue = False

    if not os.path.isdir(destination):
        logging.warning("Destination %s doesn't exist", destination)
        logging.info("Making destination directory as it doesn't exists")
        os.makedirs(destination)
        

    return returnValue

# Yes No Prompt
# Input:- Question
# Input:- default answer (default is yes unless changed)
# Output:- Boolean
# Description :- Prompt the user with a yes no question and return boolean.
def queryYesNo(question, default="yes"):

    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


# Clear shell script
# Input:- None
# Output:- None
# Description: This function will clear the shell 
def cls():
    os.system(['clear','cls'][os.name == 'nt'])

# Main
if __name__ == "__main__":
    # Initialise all logging configuration, only levels equal to info or above will be logged, the stream will be stdout and message will appear as the following:
    # DEBUG: This is DEBUG (only if configured)
    # INFO: This is information
    # Warning: This is a warning
    # Error: This is a error
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(levelname)s: %(message)s')

    # Clean the shell
    cls()

    # Check arguments
    if len(sys.argv) > 1:
        if len(sys.argv) < 3 or len(sys.argv) > 3:
            logging.error("*** usage: %s <source directory> <destination directory>\n",sys.argv[0])
        else:
            if (checkArgs(sys.argv[1], sys.argv[2])):
                pngOpt(sys.argv[1], sys.argv[2])
            else:
                logging.error("Failed when checking arguments")
    else:
        # We have no arguments pass to use we will prompt the user
        src = raw_input("Please enter a source directory: ")
        dest = raw_input("Please enter a destination directory: ")

        if (checkArgs(src, dest)):
            pngOpt(src, dest)
        else:
            logging.error("Failed when checking arguments")
    
    end = raw_input("\nDone! Press any key to exit....")