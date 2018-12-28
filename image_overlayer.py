from PIL import Image, ExifTags, ImageChops
import exifread
import os
import sys
import random
import shutil

root = os.getcwd()

print("Currently in: " + root)

image_folder = root + "\\images\\"

print("Target folder is: " + image_folder)

imagelist = []

for root, dirs, files in os.walk(image_folder):
    for filename in files:
        print(filename)
        imagelist.append(filename)
    else:
        print("No files in " + image_folder)

print(imagelist)

#Thanks to the following link for this chunk of pairing code:
#http://www.wellho.net/resources/ex.php4?item=y104/tessapy

def pairme(source):
        result = []
        for p1 in range(len(source)):
                for p2 in range(p1+1,len(source)):
                        result.append([source[p1],source[p2]])
        return result

pairings = pairme(imagelist)
print("%d pairings" % len(pairings))

print(pairings)

for pair in pairings:
        print(pair)
        img1 = Image.open(image_folder + pair[0], mode='r')
        img2 = Image.open(image_folder + pair[1], mode='r')
        print(img1)
        print(img2)

        width=img1.width
        height=img1.height

        widthheight = 2000

        print(str(width) + " x " + str(height))
        aspectratio = width / height
        print(aspectratio)

        try:
                for orientation in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation]=='Orientation':
                                break
                exif=dict(img1._getexif().items())
                
                if exif[orientation] == 3:
                        img1 = img1.rotate(180, expand=True)
                elif exif[orientation] == 6:
                        img1 = img1.rotate(270, expand=True)
                elif exif[orientation] == 8:
                        img1 = img1.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
                pass
                
        try:
                for orientation in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation]=='Orientation':
                                break
                exif=dict(img2._getexif().items())
                
                if exif[orientation] == 3:
                        img2 = img2.rotate(180, expand=True)
                elif exif[orientation] == 6:
                        img2 = img2.rotate(270, expand=True)
                elif exif[orientation] == 8:
                        img2 = img2.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
                pass
        if img1.width == img1.height:
            img1r = img1.resize((2000,2000))
        else:
            if img1.width > img1.height:
                img1r = img1.resize((2000, 1500))
            else:
                img1r = img1.resize((1500,2000))
            print((aspectratio/img1.height))

        if img2.width == img2.height:
            img2r = img2.resize((2000,2000))
        else:
            if img2.width > img2.height:
                img2r = img2.resize((2000, 1500))
            else:
                img2r = img2.resize((1500,2000))
            print((aspectratio/img2.height))

        img1a = img1r
        img2a = img2r
        img1a.putalpha(64)
        img2a.putalpha(64)

        bga = Image.new('RGBA', (2000, 2000), (255, 255, 255, 255))
        bga.paste(img1a, ((int(round((bga.width/2 - img1a.width/2)))),(int(round((bga.height/2 - img1a.height/2))))))
        bg2a = Image.new('RGBA', (2000, 2000), (255, 255, 2555, 255))
        bg2a.paste(img2a, ((int(round((bg2a.width/2 - img2a.width/2)))),(int(round((bg2a.height/2 - img2a.height/2))))))

        bg = Image.new('RGBA', (2000, 2000), (255, 255, 255, 255))
        bg.paste(img1r, ((int(round((bg.width/2 - img1r.width/2)))),(int(round((bg.height/2 - img1r.height/2))))))
        bg2 = Image.new('RGBA', (2000, 2000), (255, 255, 2555, 255))
        bg2.paste(img2r, ((int(round((bg2.width/2 - img2r.width/2)))),(int(round((bg2.height/2 - img2r.height/2))))))

        alpha = Image.alpha_composite(bga, bg2a)
        alpha.save("result\\" + pair[0] + '_' + pair[1] + "_" + "alpha.png")

        add = ImageChops.add(bg, bg2, scale=1.0, offset=0)
        add.save("result\\" + pair[0] + '_' + pair[1] + "_" + "add.png")

        lighter = ImageChops.lighter(bg, bg2)
        lighter.save("result\\" + pair[0] + '_' + pair[1] + "_" + "lighter.png")

        multiply = ImageChops.multiply(bg, bg2)
        multiply.save("result\\" + pair[0] + '_' + pair[1] + "_" + "multiply.png")
