#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import argparse

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


def process_line(line_text, text_font):
    line_text = line_text.strip().upper()
    text_width, text_height = draw.textsize(line_text, font=text_font)
    done_split = True

    while text_width > width and done_split:
        done_split = False
        lines = []
        for line in line_text.split('\n'):
            if (split_index := find_best_space(line)) > 0:
                done_split = True
                line = replace_char(line, split_index, '\n')
            lines.append(line)
        line_text = '\n'.join(lines)
        text_width, text_height = draw.textsize(line_text, font=text_font)

    return line_text, text_width, text_height


parser = argparse.ArgumentParser(description='Add text to the top and bottom of an image.')
parser.add_argument('input_image', type=str, help='The path to the input image file.')
parser.add_argument('-t', '--top_text', type=str, default='', help='The text to add to the top of the image.')
parser.add_argument('-b', '--bottom_text', type=str, default='', help='The text to add to the bottom of the image.')
parser.add_argument('output_image', type=str, help='The path where the output image will be saved.')
args = parser.parse_args()

input_image = args.input_image
image = Image.open(input_image)
width, height = image.size
draw = ImageDraw.Draw(image)
font_size = width // 10
font = ImageFont.truetype('impact.ttf', size=font_size)

top_text = args.top_text
top_text, top_text_width, top_text_height = process_line(top_text, font)
top_text_position = ((width - top_text_width) // 2, width // 20)
draw.text(top_text_position, top_text, fill=WHITE, font=font, stroke_width=font_size // 10, stroke_fill=BLACK,
          align="center")

bottom_text = args.bottom_text
bottom_text, bottom_text_width, bottom_text_height = process_line(bottom_text, font)
bottom_text_position = ((width - bottom_text_width) // 2, height - width // 20 - bottom_text_height)
draw.text(bottom_text_position, bottom_text, fill=WHITE, font=font, stroke_width=font_size // 10, stroke_fill=BLACK,
          align="center")

output_image = args.output_image
image.save(output_image)
