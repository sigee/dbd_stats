from PIL import Image

im = Image.open(r"original.jpg")

rank = im.crop((80, 700, 180, 810))
rank.save("rank.jpg")
#rank.show()

perk1 = im.crop((180, 740, 240, 795))
perk1.save("perk1.jpg")
#perk1.show()

perk2 = im.crop((235, 740, 295, 795))
perk2.save("perk2.jpg")
#perk2.show()

perk3 = im.crop((290, 740, 355, 795))
perk3.save("perk3.jpg")
#perk3.show()

perk4 = im.crop((345, 740, 405, 795))
perk4.save("perk4.jpg")
#perk4.show()

killer = im.crop((480, 740, 530, 795))
killer.save("killer.jpg")
#killer.show()
