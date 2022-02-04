# type: ignore
import os
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
from collections import deque

load_dotenv()

FA_SOLID = ImageFont.truetype(
    "fonts/fontawesome-free-6.0.0-beta3-desktop/otfs/Font Awesome 6 Free-Solid-900.otf",
    30,
)
BITTER_40 = ImageFont.truetype(
    "fonts/BitterPro-Regular.ttf",
    40,
)
BITTER_20 = ImageFont.truetype(
    "fonts/BitterPro-Regular.ttf",
    20,
)
NOTO = ImageFont.truetype(
    "fonts/NotoSans-Regular.ttf",
    10,
)


def utf(b: bytes) -> str:
    return b.decode("unicode-escape")


THERMOMETER = [
    utf(b"\\uf2cb"),
    utf(b"\\uf2ca"),
    utf(b"\\uf2c9"),
    utf(b"\\uf2c8"),
    utf(b"\\uf2c7"),
]
SENSOR_1 = 22.1
SENSOR_2 = (22.3, 45.4)


class Display:
    def __init__(self):
        self.height = 250
        self.width = 122

    def displayPartial(self, image: Image.Image):
        image.save("test.png")

    def getbuffer(self, image: Image.Image) -> Image.Image:
        return image


DISPLAY = Display()

if os.getenv("ENV") == "production":
    from waveshare_epd import epd2in13_V2  # type: ignore

    DISPLAY: Display = epd2in13_V2.EPD()  # type: ignore


IMAGE = Image.new("1", (DISPLAY.width, DISPLAY.height), 255)
DRAW = ImageDraw.Draw(IMAGE)


def draw():
    DISPLAY.displayPartial(DISPLAY.getbuffer(IMAGE))


# DRAW.rectangle(((DISPLAY.width - w)//2, h*line, ((DISPLAY.width - w)//2)+w, h*(line+1)))

# for idx, icon in enumerate(THERMOMETER):
#     DRAW.text((30 * idx, 0), icon, font=FA_SOLID)  # type: ignore
# DRAW.rounded_rectangle((5, 5, 50, 50), width=4, radius=10)
# DRAW.rounded_rectangle((5, 55, 50, 100), width=4, radius=10)

DRAW.text(
    (12, 0),
    f"{SENSOR_2[0]:0.1f}",
    font=BITTER_40,
)
DRAW.text((90, 26), "°C", font=BITTER_20)
DRAW.line((3, 60, DISPLAY.width - 3, 60))
for i in range(38):
    DRAW.line((2 + (i * 3), 65, 7 + (i * 3), 60))


DRAW.text(
    (12, 50),
    f"{SENSOR_1:0.1f}",
    font=BITTER_40,
)
DRAW.text((90, 76), "°C", font=BITTER_20)


DRAW.text(
    (35, 105),
    f"{SENSOR_2[1]:0.0f}",
    font=BITTER_40,
)
DRAW.text((82, 128), "%", font=BITTER_20)

# DRAW.line(((DISPLAY.width // 2), 0, (DISPLAY.width // 2), DISPLAY.height))
# DRAW.line((0, (DISPLAY.height // 2), DISPLAY.width, (DISPLAY.height // 2)))

DRAW.text((10, 180), "Topení", font=NOTO)

DRAW.rounded_rectangle((27, 200, 57, 214), radius=7, fill=0)
DRAW.text((35, 200), "On", fill=1, font=NOTO)
DRAW.rounded_rectangle((65, 200, 95, 214), radius=7)
DRAW.text((72, 200), "Off", font=NOTO)

# DRAW.rounded_rectangle((1,1,120,110), radius=8)

a = deque(
    [
        20.1,
        20.3,
        20.6,
        21.0,
        22.1,
        23.3,
        23.6,
        23.0,
        23.1,
        23.3,
        23.6,
        23.0,
        23.1,
        23.3,
        24.6,
        24.0,
        24.1,
        25.3,
        25.6,
        25.0,
        24.1,
        24.3,
        24.6,
        24.0,
        24.1,
        24.3,
        24.6,
        24.0,
        24.1,
        24.3,
        24.6,
        24.0,
        24.1,
        24.3,
        23.6,
        23.0,
        23.1,
        23.3,
        23.6,
        23.0,
        23.1,
        23.3,
        23.6,
        23.0,
        23.1,
        23.3,
        24.6,
        24.0,
        24.1,
        24.3,
        24.6,
        24.0,
        24.1,
        24.3,
        24.6,
        24.0,
        24.1,
        24.3,
        24.6,
        24.0,
        24.1,
        25.3,
        25.6,
        25.0,
        25.1,
        25.3,
        25.6,
        25.0,
        25.1,
        25.3,
        25.6,
        25.0,
        25.1,
        25.3,
        25.6,
        26.0,
        26.1,
        26.3,
        26.6,
        26.0,
        26.1,
        26.3,
        26.6,
        26.0,
        26.1,
        26.3,
        26.6,
        26.0,
        26.1,
        26.3,
        26.6,
        26.0,
        27.1,
        27.3,
        27.6,
        27.0,
        27.1,
        27.3,
        27.6,
        27.0,
        27.3,
        27.6,
        27.0,
        27.1,
        27.3,
        27.6,
        27.0,
        27.5,
        27.5,
        27.2,
    ],
    maxlen=100,
)


BASE = 250

for idx, i in enumerate(a):
    DRAW.point((idx + 10, BASE - round((i - 10))))


draw()
