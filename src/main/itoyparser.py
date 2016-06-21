from translator.translatorimpl import IToYTranslator 
import os
import re

__INPUT_DIRECTORY = "ITOYInput"
__OUTPUT_DIRECTORY = "ITOYOutput"


if __name__ == '__main__':
    try:
        print(os.getcwd())
        print("Starting parser. Input folder is " + __INPUT_DIRECTORY + "; Output folder is " + __OUTPUT_DIRECTORY)
        print("Checking if input directory exists")
        if not os.path.isdir(__INPUT_DIRECTORY):
            print("Input directory does not exist. Please create directory "+ __INPUT_DIRECTORY+ " in order to continue")
            raise Exception("No INPUT directory")
        print("Done.\nChecking if output directory exists")
        if not os.path.isdir(__OUTPUT_DIRECTORY):
            print("Output directory does not exist. Please create directory "+ __OUTPUT_DIRECTORY + " in order to continue")
            raise Exception("No OUTPUT directory")
        print("Done.")
        in_files = [item for item in os.listdir(__INPUT_DIRECTORY) if re.search("\.txt", item)]
        item_count = len(in_files)
        print("Number of .txt files in input directory: %d" % item_count)
        if item_count == 0:
            print("No files to process")
            exit(1)
        translator = IToYTranslator(__INPUT_DIRECTORY,__OUTPUT_DIRECTORY)
        for item in in_files:
            print("Parsing file %s" % item)
            translator.initialize(item)
            if translator.parse():
                print("Done. Converted file saved: %s/%s"% (__OUTPUT_DIRECTORY, item+"_converted"))
            else:
                print("Failed to parse file")
    finally:
        input("Done. Press any key to continue")
        
        
    
#     print(os.getcwd())
#     test_data = open(__filename, 'r').read()
#     trans = IToYTranslator(__filename)
#     trans._parse()