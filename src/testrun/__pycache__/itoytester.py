import os
from translator.translatorimpl import IToYTranslator

def test():
    print(os.getcwd())
    test_data = open('C:/Users/a554180/gitrepository/misc/pythonDev/IToY/src/testrun/t.txt', 'r').read()
    trans = IToYTranslator(test_data)
    return trans

if __name__ == '__main__':
    print(os.getcwd())
    test_data = open('C:/Users/a554180/gitrepository/misc/pythonDev/IToY/src/testrun/t.txt', 'r').read()
    trans = IToYTranslator(test_data)
