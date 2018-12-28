import os

numbers = ["one", "two", "three"]

print(numbers)

for x in numbers:
    print(x)

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

def pairme(source):
        result = []
        for p1 in range(len(source)):
                for p2 in range(p1+1,len(source)):
                        result.append([source[p1],source[p2]])
        return result

pairings = pairme(imagelist)
print("%d pairings" % len(pairings))
for pair in pairings:
        print(pair)
