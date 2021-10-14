from os import listdir, rename

myPath = 'data'
index = 1
for directory in listdir(myPath):
    for f in listdir(myPath + "/" + directory):
        if f.endswith('.jpg'):
            print(myPath + "/" + directory + "/" + f)
            rename(myPath + "/" + directory + "/" + f, myPath + "/" + directory + "/" + str(index) + '.jpg')
            index = index + 1
