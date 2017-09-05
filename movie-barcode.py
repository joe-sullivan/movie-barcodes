#!/usr/bin/env python3

from PIL import Image, ImageDraw
from subprocess import call, check_output
from tempfile import NamedTemporaryFile
try: # optional progress bar
	from progress.bar import ChargingBar
except ImportError:
	ChargingBar = None
import argparse, os

def get_time(file): # returns length of video in seconds
	args = ['ffprobe',
	        '-i', file,
	        '-show_entries', 'format=duration',
	        '-v', 'quiet',
	        '-of', 'csv=%s' % ("p=0")]
	return float(check_output(args).decode())

def make_barcode(srcfile, filename='barcode', width=1280, height=720, thickness=10):
	w = width // thickness
	time = get_time(srcfile)

	im = Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
	barcode = ImageDraw.Draw(im)

	tmpfile = NamedTemporaryFile(suffix='.bmp')

	if ChargingBar: bar = ChargingBar(max=w)
	for frame in range(w):
		position = '%f' % (time / w * frame)
		args = ['ffmpeg',
		        '-ss', position,      # seek
		        '-i', srcfile,        # input video file
		        '-s', '1:1',          # scale to 1 pixel
		        '-loglevel', 'quiet', # suppress output
		        '-frames:v', '1',     # extract 1 frame
		        '-y',                 # force overwrite
		        tmpfile.name]         # output file
		call(args) # grab frame

		try:
			tmp_im = Image.open(tmpfile.name)
		except: # leave transparent
			pass
		else:
			color = tmp_im.load()[0, 0]
			f = frame * thickness + (thickness // 2) - 1
			barcode.line([(f, 0), (f, height)], fill=color, width=thickness)

		if ChargingBar: bar.next()
	if ChargingBar: bar.finish()

	im.save('%s.png' % filename)

def main():
	parser = argparse.ArgumentParser(description='Create a video palette barcode')
	parser.add_argument('file', help='file to process')
	parser.add_argument('--output',
	                    help='output file')
	parser.add_argument('--width',
	                    type=int,
	                    default=1280,
	                    help='output image width  (default=1280)')
	parser.add_argument('--height',
	                    type=int,
	                    default=720,
	                    help='output image height (default=720)')
	parser.add_argument('--thickness',
	                    type=int,
	                    default=10,
	                    help='frame thickness     (default=10)')
	args = parser.parse_args()

	filename = args.output or ''
	if not filename or filename.endswith(os.path.sep):
		filename += os.path.basename(args.file).rsplit('.', 1)[0]
	make_barcode(args.file,
	             filename=filename,
	             width=args.width,
	             height=args.height,
	             thickness=args.thickness)

if __name__ == '__main__':
	main()
