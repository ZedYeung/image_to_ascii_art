from PIL import Image
import argparse
import os
from os.path import splitext

# commandline args
parser = argparse.ArgumentParser(description="transform image to ascii art", formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('file', help="input image")
parser.add_argument('-o', '--output', help="output file")
parser.add_argument('-w', '--width', type=int,  help="width to resize image, without height the image will be scaled base on width")
parser.add_argument('--height', type=int, help="height to resize image")
parser.add_argument('-s', '--scheme', type=int, default=70,
help="""choose a color scheme, the more colors--which means the more char, the more gradation
70--default color scheme: ($@B%%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. )
16--(MNHQ$OC?7>!:-;. )
15--['##', '@@', '%%%%', 'QQ', 'SS', 'UU', 'OO', '??', '**', 'oo', '++', '--', '::', '..', '  ']
3--(#: )
2--(# )""")

# get args
args = parser.parse_args()

IMG = args.file
WIDTH = args.width
HEIGHT = args.height
OUTPUT = args.output
SCHEME = args.scheme

# color scheme--ascii char to draw the picture
# 15: ['##', '@@', '%%', 'QQ', 'SS', 'UU', 'OO', '??', '**', 'oo', '++', '--', '::', '..', '  ']
color_scheme = {
70: list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "),
16: list('MNHQ$OC?7>!:-;. '),
15: list('#@%QSUO?*o+-:. '),
3: list('#: '),
2: list('# ')}


def resize_image(image, new_width=200):
	"""
	Resizes an image preserving the aspect ratio.
	"""
	(original_width, original_height) = image.size
	aspect_ratio = original_height / original_width
	new_height = int(aspect_ratio * new_width)
	new_image = image.resize((new_width, new_height))
	return new_image


def image_to_ascii(image, scheme=color_scheme[SCHEME]):
	(new_width, new_height) = image.size
	image = image.convert('L')
	colors = len(scheme)
	# unit = 255 / (colors - 1)
	unit = 256 / colors
	txt = ""

	for i in range(new_height):
		for j in range(new_width):
			gray = image.getpixel((j, i))
			txt += scheme[int(gray // unit)]
		txt += '\n'
	return txt


def main():
	image = Image.open(IMG)
	img_file = os.path.splitext(IMG)[0]
	# resize image
	if WIDTH:
		if HEIGHT:
			image = image.resize((WIDTH, HEIGHT), Image.NEAREST)
		else:
			image = resize_image(image, new_width=WIDTH)
	(width, height) = image.size
	# 0.4 is the weight/height of font, it depends.
	image = image.resize((width, int(height * 0.4)), Image.NEAREST)
	# transfer img to ascii art
	txt = image_to_ascii(image, scheme=color_scheme[SCHEME])

	# output ascii picture
	if OUTPUT:
		with open(OUTPUT, 'w') as f:
			f.write(txt)
	else:
		with open('{img}_{scheme}_ascii_art.txt'.format(img=img_file, scheme=SCHEME), 'w') as f:
			f.write(txt)

if __name__ == '__main__':
	main()
