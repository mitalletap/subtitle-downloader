import os
from os import listdir
import zipfile
path = '/Users/mital/Downloads/Subtitles/'
list_of_zips = os.listdir(path)
for zip in list_of_zips:
    print(zip)
    try:
        folderName = zip[0:len(zip) - 4]
        with zipfile.ZipFile(path + zip, 'r') as myZip:
            list_of_files = myZip.namelist()
            print(list_of_files)
            for fileName in list_of_files:
                if fileName.endswith('.srt'):
                    print("extracting: " + path+zip)
                    print(myZip.extract(fileName, path+'{}/'.format(folderName)))
    except Exception:
        print("Not a Zip File")
