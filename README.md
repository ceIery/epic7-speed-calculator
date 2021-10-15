# Epic Seven Speed Calculator
An Epic Seven arena/guild wars speed calculator bot for Discord

## Current features
- Uses OpenCV and Tesseract to read percentages from screenshots
- Requires no image processing by user (crops images to fit)
- Trims notch from screenshots taken on phones

***Note:** this is more of a proof of concept than an actual utility, as there are significant issues that need to be fixed to get it to a properly usable state.*

## Requirements

## Usage
Install requirements from `requirements.txt`. Specify bot token in `config.py` and run `main.py`.

    .status <base speed> [image URL]

The URL parameter is not required if the image is uploaded with the message. 

This repository also includes the files necessary for deploying to a Heroku dyno.

## Example
### Input
2400x1080 (20:9) jpg image with notch on left side, base speed of 263

![Input image](/ex/input_ex.jpg)
### Output
![Output](/ex/output_ex.png)
