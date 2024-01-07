#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import argparse
import os


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def find_best_space(text: str) -> int:
    middle = len(text) // 2
    left = right = middle

    while left > 0 or right < len(text):
        if left > 0 and text[left] == ' ':
            return left
        if right < len(text) and text[right] == ' ':
            return right

        left -= 1
        right += 1
    return -1


def replace_char(text: str, index: int, new_char: chr) -> str:
    char_list = list(text)
    char_list[index] = new_char
    return ''.join(char_list)


def process_part(part_text, text_font, img_width):
    part_text = part_text.strip().upper()
    text_width, text_height = draw.textsize(part_text, font=text_font)
    done_split = True

    while text_width > img_width and done_split:
        done_split = False
        widest = 0
        widest_index = 0
        lines = part_text.split('\n')
        for idx, line in enumerate(lines):
            line_width, _ = draw.textsize(line, font=text_font)
            if line_width > widest:
                widest_index = idx
                widest = line_width
        if (split_index := find_best_space(lines[widest_index])) > 0:
            done_split = True
            lines[widest_index] = replace_char(lines[widest_index], split_index, '\n')
        part_text = '\n'.join(lines)
        text_width, text_height = draw.textsize(part_text, font=text_font)

    return part_text, text_width, text_height


def confirm_overwrite(filename):
    while True:
        response = input(f"Are you sure you want to overwrite {filename}? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False


parser = argparse.ArgumentParser(description='Add text to the top and bottom of an image.')
parser.add_argument('input_image', type=str, help='The path to the input image file.')
parser.add_argument('-t', '--top_text', type=str, default='', help='The text to add to the top of the image.')
parser.add_argument('-b', '--bottom_text', type=str, default='', help='The text to add to the bottom of the image.')
parser.add_argument('output_image', type=str, help='The path where the output image will be saved.')
args = parser.parse_args()

output_image = args.output_image
if os.path.exists(output_image) and not confirm_overwrite(output_image):
    exit(-1)

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

input_image = args.input_image
image = Image.open(input_image)
width, height = image.size
draw = ImageDraw.Draw(image)
font_size = min(width, height) // 15
font = ImageFont.truetype(script_dir+'/memeg_res/impact.ttf', size=font_size)

top_text = args.top_text
top_text, top_text_width, top_text_height = process_part(top_text, font, width)
top_text_position = ((width - top_text_width) // 2, min(width, height) // 20)
draw.text(top_text_position, top_text, fill=WHITE, font=font, stroke_width=font_size // 10, stroke_fill=BLACK,
          align="center")

bottom_text = args.bottom_text
bottom_text, bottom_text_width, bottom_text_height = process_part(bottom_text, font, width)
bottom_text_position = ((width - bottom_text_width) // 2, height - min(width, height) // 20 - bottom_text_height * 1.1)
draw.text(bottom_text_position, bottom_text, fill=WHITE, font=font, stroke_width=font_size // 10, stroke_fill=BLACK,
          align="center")

image.save(output_image)
