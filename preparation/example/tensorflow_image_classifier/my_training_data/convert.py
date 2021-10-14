from PIL import Image

from os import listdir, remove
# from os.path import isfile, join

myPath = 'data'
for directory in listdir(myPath):
    for f in listdir(myPath + "/" + directory):
        if f.endswith('.png'):
            print(myPath + "/" + directory + "/" + f)
            im1 = Image.open(myPath + "/" + directory + "/" + f)
            im1 = im1.convert("RGB")
            im1.save(myPath + "/" + directory + "/" + f.replace('.png', '.jpg'), quality=100)
            remove(myPath + "/" + directory + "/" + f)
