![Sample](/movies/Skyfall.png "Skyfall")


## How it works

1. Get video length (in seconds) using `ffprobe`
2. Calculate frame rate (`video_length / desired_image_width`)
3. Initialize `output_image` and `temporary_image`
	* `output_image` will be the final barcode image
	* `temporary_image` will be a 1x1 bitmap containing the average color of the current frame
4. Extract frame from video using `ffmpeg` and save in `temporary_image`
5. Draw line on `output_image` using color from `temporary_image`
6. Repeat step 4 until we've reached the final frame
7. Save `output_image`


## Usage

	positional arguments:
	  file                  file to process

	optional arguments:
	  -h, --help            show this help message and exit
	  --output OUTPUT       output file
	  --width WIDTH         output image width  (default=1280)
	  --height HEIGHT       output image height (default=720)
	  --thickness THICKNESS frame thickness     (default=10)
		

## Requirements

* [Python3](https://www.python.org/)
* [Pillow](https://github.com/python-pillow/Pillow/)
* [FFmpeg](https://github.com/FFmpeg/FFmpeg/)
* [progress](https://github.com/verigak/progress/) (optional)


## Info

* small videos should finish within 1 minute (for default settings)
* large video files are slow (movies can take from 1-5 mintues depending on file size and total length)
* resolution is irrelevant (no need for 4K video files)
* `thickness` should be a multiple of `width` but is not enforced
* `output_image` will be automatically named based on input
	- if `--output` option is provided with trailing slash then the image will still be automatically named but place in to that directory
	