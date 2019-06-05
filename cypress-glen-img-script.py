import urllib.request, shutil, glob, os
from PIL import Image

x = 0
y = 0
i = 0
maxx=19
maxy=11

# Pulls down the image files from the grid on the website.
# It does it row by row and names the files according to
# an index, so 0,0 is 0.jpg, 1,0 is 1.jpg etc.
# Saves them to the current directory.

while y <= maxy:
	x = 0
	while x <= maxx:
		url = "https://cypressglen.org/client/cypressglen.org/files/map/tiles/20/map_tile_" + str(x) + "_" + str(y) + ".jpg"
		filename = "./" + str(i) + ".jpg"
		
		request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		with urllib.request.urlopen(request) as response, open(filename, 'wb') as out_file:
			shutil.copyfileobj(response, out_file)
		x += 1
		i += 1
	y += 1

# Grabs a list of all the filenames in the current directory
files = glob.glob("./*.jpg")

# The list is initially sorted alphabetically, so ['0.jpg','1.jpg','10.jpg'...]
# We can't sort by int because of the .jpg in the filename, so we have to write
# a lambda function to extract the number from the filename and use that as the
# key to sort the list.
files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

# Create a new blank image large enough to store all the individual images
# we downloaded (20x12 grid of images).
result = Image.new("RGB", (256*20, 256*12))

# For each file, paste it at a specific point in the blank image according to its size
# and how many files pasted previously.
for index, file in enumerate(files):
	path = os.path.expanduser(file)
	img = Image.open(path)
	img.thumbnail((256, 256), Image.ANTIALIAS)
	x = index % 20 * 256
	y = index // 20 * 256
	w, h = img.size
	print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
	result.paste(img, (x, y, x+w, y+h))

# Save the resulting image to a file.
result.save(os.path.expanduser('./final.jpg'))