import os
from translator.translatorimpl import IToYTranslator

__PROJ_DIR = "C:/Users/a554180/gitrepository/misc/pythonDev/IToY"
__INPUT_DIRECTORY = os.path.join(__PROJ_DIR,"ITOYInput")
__OUTPUT_DIRECTORY = os.path.join(__PROJ_DIR,"ITOYOutput")

def test(filename):
    trans = IToYTranslator(__INPUT_DIRECTORY, __OUTPUT_DIRECTORY)
    trans.initialize(filename)
    return trans

if __name__ == '__main__':
    t = test("test.txt")
    t.parse()
    #test_data = open(__filename, 'r').read()
    #trans = IToYTranslator()
    #trans.initialize(__filename)
    #trans._parse()
    
    