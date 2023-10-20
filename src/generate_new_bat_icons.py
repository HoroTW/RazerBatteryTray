#!/usr/bin/env python3
# generate icons for the battery level

import os
from PIL import Image, ImageDraw, ImageFont

PATH = "icons"

def generate_icons(color_percent_dict, charging=False):
    for bat_level in range(0, 101):
        SIZE = 256
        BORDER = 1/16

        size = SIZE, SIZE
        border = int(BORDER * SIZE)

        font_size = int(0.56*SIZE)
        if bat_level >= 100:
            font_size = int(0.42*SIZE)
        font = ImageFont.truetype("DejaVuSans.ttf", font_size)

        # border color lookup using the color_percent_dict and the bat_level
        border_color = None
        for percent_range, color in color_percent_dict.items():
            if bat_level >= percent_range[0] and bat_level <= percent_range[1]:
                border_color = color
                break

        if charging:
            # bright blue
            border_color = (0, 255, 255, 255)

        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # draw a circle with a white outline
        draw.ellipse((0, 0, size[0]-1, size[1]-1), fill=(0, 0, 0, 128), outline=(255, 255, 255, 32), width=border)

        color_percent_dict
        draw.pieslice((0, 0, size[0]-1, size[1]-1), -90, -90+int(360*bat_level/100), fill=border_color)
        draw.ellipse((0+border, 0+border, size[0]-1-border, size[1]-1-border), fill=(0, 0, 0, 128))

        # draw text centered
        text = str(bat_level)
        text_size = draw.textbbox((0, 0), text, font=font)
        font = ImageFont.truetype("DejaVuSans.ttf", font_size)

        text_pos = (
            (size[0] - text_size[2]) / 2,
            (size[1] - text_size[3]) / 2 - int(0.047*SIZE),
        )
        draw.text(text_pos, text, font=font, fill=(255, 255, 255, 255))

        # create the directory if it doesn't exist
        if not os.path.exists(PATH):
            os.makedirs(PATH)
        
        # save the image
        save_path = f"{PATH}/bat_{bat_level}_c.png" if charging else f"{PATH}/bat_{bat_level}.png"
        img.save(save_path)


color_percent_dict = {
    (50,101): (0, 255, 0, 200), # green for 50% to 100%
    (20,50): (255, 255, 0, 200), # yellow for 20% to 50%
    (0,20): (255, 0, 0, 255), # red for 0% to 20%
}

generate_icons(color_percent_dict, charging=False)
generate_icons(color_percent_dict, charging=True)
