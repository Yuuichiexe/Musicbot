import os
import re

import aiofiles
import aiohttp
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch

from AnonXMusic import app, LOGGER
from config import YOUTUBE_IMG_URL


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


def circle(img):
    h, w = img.size
    a = Image.new("L", [h, w], 0)
    b = ImageDraw.Draw(a)
    b.pieslice([(0, 0), (h, w)], 0, 360, fill=255, outline="white")
    c = np.array(img)
    d = np.array(a)
    e = np.dstack((c, d))
    return Image.fromarray(e)


def clear(text):
    lst = text.split(" ")
    title = ""
    for i in lst:
        if len(title) + len(i) < 60:
            title += " " + i
    return title.strip()


async def get_thumb(videoid, user_id, chat_id):
    if os.path.isfile(f"cache/{videoid}_{user_id}.png"):
        return f"cache/{videoid}_{user_id}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        # Download user's profile picture
        try:
            user_profile_pic = await app.get_chat(user_id)
            user_pic_path = f"cache/user_{user_id}.jpg"
            await app.download_media(user_profile_pic.photo.big_file_id, file_name=user_pic_path)
        except:
            user_pic_path = "AnonXMusic/utils/unknown.jpg"  # Default profile picture

        user_pic = Image.open(user_pic_path)
        user_pic_resized = changeImageSize(190, 190, circle(user_pic))

        # Download group photo
        try:
            group_photo = await app.get_chat(chat_id)
            group_pic_path = f"cache/group_{chat_id}.jpg"
            await app.download_media(group_photo.photo.big_file_id, file_name=group_pic_path)
        except:
            group_pic_path = "AnonXMusic/utils/default_group.jpg"  # Default group picture

        group_pic = Image.open(group_pic_path)
        group_pic_resized = changeImageSize(352, 352, circle(group_pic))

        youtube = Image.open(f"cache/thumb{videoid}.png")
        bg = Image.open("AnonXMusic/assets/gcpfp.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(ImageFilter.BoxBlur(12))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.7)

        image3 = changeImageSize(1280, 720, bg)
        image5 = image3.convert("RGBA")
        image5 = image5.filter(ImageFilter.GaussianBlur(radius=0.2))

        # Draw a rectangular background for profile pics
        draw = ImageDraw.Draw(background)
        rect_bg_color = (0, 0, 0, 130)  # Semi-transparent black
        draw.rectangle([(30, 130), (440, 580)], fill=rect_bg_color, outline="white", width=2)

        background.paste(group_pic_resized, (50, 150), mask=group_pic_resized)
        background.paste(user_pic_resized, (290, 400), mask=user_pic_resized)

        background.paste(image5, (0, 0), mask=image5)

        # Draw text
        arial = ImageFont.truetype("AnonXMusic/assets/title.ttf", 35)
        dur = ImageFont.truetype("AnonXMusic/assets/title.ttf", 30)
        onfont = ImageFont.truetype("AnonXMusic/assets/font.ttf", 30)
        font = ImageFont.truetype("AnonXMusic/assets/Cloudb.otf", 38)

        draw.text((1047, 10), unidecode(app.name), fill="white", font=onfont)
        draw.text(
            (540, 308),
            f"Channel - {channel}",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (540, 340),
            f"Views - {views[:23]}",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (50, 670),
            clear(title),
            (255, 255, 255),
            font=font,
        )
        draw.text(
            (537, 400),
            "00:00",
            (255, 255, 255),
            font=dur,
        )
        draw.text(
            (1159, 400),
            f"{duration[:23]}",
            (255, 255, 255),
            font=dur,
        )

        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
        background.save(f"cache/{videoid}_{user_id}.png")
        return f"cache/{videoid}_{user_id}.png"
    except Exception as e:
        LOGGER("AnonXMusic").error(f"Error generating thumbnail: {e}")
        return YOUTUBE_IMG_URL
