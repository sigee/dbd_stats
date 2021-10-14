from PIL import Image

from os import listdir
from os.path import isfile, join

myPath = 'D:\\DBD\\EndResults\\_base_'
myPath = 'D:\\DBD\\EndResults\\to_improve'
onlyFiles = [f for f in listdir(myPath) if isfile(join(myPath, f))]
print(onlyFiles)

myRanksPath = 'D:\\DBD\EndResults\\ranks'
myPerksPath = 'D:\\DBD\EndResults\\perks'
myKillersPath = 'D:\\DBD\EndResults\\killers'
mySurvivorStatusPath = 'D:\\DBD\EndResults\\survivor_statuses'

index = 1
for f in onlyFiles:
    im = Image.open(myPath + "\\" + f)
    im = im.convert("RGB")

    rank = im.crop((80, 700, 180, 810))
    rank.save(myRanksPath + "\\rank_" + str(index) + ".jpg", quality=100)

    perk1 = im.crop((180, 740, 240, 795))
    perk1.save(myPerksPath + "\\perk1_" + str(index) + ".jpg", quality=100)

    perk2 = im.crop((235, 740, 295, 795))
    perk2.save(myPerksPath + "\\perk2_" + str(index) + ".jpg", quality=100)

    perk3 = im.crop((290, 740, 355, 795))
    perk3.save(myPerksPath + "\\perk3_" + str(index) + ".jpg", quality=100)

    perk4 = im.crop((345, 740, 405, 795))
    perk4.save(myPerksPath + "\\perk4_" + str(index) + ".jpg", quality=100)

    killer = im.crop((480, 740, 530, 795))
    killer.save(myKillersPath + "\\killer_" + str(index) + ".jpg", quality=100)

    surv1 = im.crop((810, 295, 870, 345))
    surv1.save(mySurvivorStatusPath + "\\surv1_" + str(index) + ".jpg", quality=100)
    surv2 = im.crop((810, 407, 870, 457))
    surv2.save(mySurvivorStatusPath + "\\surv2_" + str(index) + ".jpg", quality=100)
    surv3 = im.crop((810, 519, 870, 569))
    surv3.save(mySurvivorStatusPath + "\\surv3_" + str(index) + ".jpg", quality=100)
    surv4 = im.crop((810, 628, 870, 678))
    surv4.save(mySurvivorStatusPath + "\\surv4_" + str(index) + ".jpg", quality=100)

    index = index + 1
