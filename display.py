import os
from time import sleep
from typing import Callable, Any
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
from collections import deque
from waveshare_epd import epd2in13_V2

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


class Display:
    def __init__(self):
        self.height = epd2in13_V2.EPD_HEIGHT
        self.width = epd2in13_V2.EPD_WIDTH

    def displayPartial(self, image: Image.Image):
        image.save("test.png")

    def getbuffer(self, image: Image.Image) -> Image.Image:
        return image


DISPLAY = epd2in13_V2.EPD() if os.getenv("ENV") == "production" else Display()


IMAGE = Image.new("1", (DISPLAY.width, DISPLAY.height), 255)
DRAW = ImageDraw.Draw(IMAGE)


def draw():
    DISPLAY.displayPartial(DISPLAY.getbuffer(IMAGE))  # type: ignore


def get_sensor_data(
    path: str,
    cast: Callable[[Any], Any] = next,
    val: Callable[[str], Any] = lambda x: float(x),
):
    try:
        with open(path) as f:
            return cast(map(val, list(f.readlines())))
    except:
        return cast(map(val, [0]))  # type: ignore


DRAW.text((90, 16), "°C", font=BITTER_20)  # type: ignore
DRAW.line((3, 50, DISPLAY.width - 3, 50))
for i in range(37):
    DRAW.line((-10 + (i * 4), 60, 0 + (i * 4), 50))
DRAW.line((0, 0, 0, 100), fill=1)
DRAW.line((121, 0, 121, 110), fill=1)
DRAW.rounded_rectangle((1, 1, 120, 110), radius=8)
DRAW.text((90, 74), "°C", font=BITTER_20)  # type: ignore
DRAW.text((82, 128), "%", font=BITTER_20)  # type: ignore
DRAW.text((10, 180), "Topení", font=NOTO)  # type: ignore


draw()

sensor_1_temp, sensor_2_temp, sensor_2_humidity, heat = (0, 0, 0, False)
while True:
    sensor_1_temp_new = get_sensor_data("/tmp/sensor_1/temp")
    sensor_2_temp_new = get_sensor_data("/tmp/sensor_2/temp")
    sensor_2_humidity_new = get_sensor_data("/tmp/sensor_2/hum")
    history = get_sensor_data("/tmp/sensor_2/hist", lambda m: deque(m, maxlen=100))
    heat_new = get_sensor_data("/tmp/sensor_3/heat", val=lambda m: m == "true\n")

    if sensor_2_temp != sensor_2_temp_new:
        DRAW.rectangle((12, 5, 88, 48), fill=1)
        sensor_2_temp = sensor_2_temp_new
        DRAW.text(  # type: ignore
            (12, -10),
            f"{sensor_2_temp:0.1f}",
            font=BITTER_40,
        )

    if sensor_1_temp != sensor_1_temp_new:
        DRAW.rectangle((12, 65, 88, 108), fill=1)
        sensor_1_temp = sensor_1_temp_new
        DRAW.text(  # type: ignore
            (12, 48),
            f"{sensor_1_temp:0.1f}",
            font=BITTER_40,
        )

    if sensor_2_humidity != sensor_2_humidity_new:
        sensor_2_humidity = sensor_2_humidity_new
        DRAW.rectangle((35, 125, 80, 155), fill=1)
        DRAW.text(  # type: ignore
            (35, 105),
            f"{sensor_2_humidity:0.0f}",
            font=BITTER_40,
        )

    if heat != heat_new:
        heat = heat_new
        DRAW.rounded_rectangle((27, 200, 57, 214), radius=7, outline=0, fill=not heat)
        DRAW.text((35, 200), "On", font=NOTO, fill=heat)  # type: ignore
        DRAW.rounded_rectangle((65, 200, 95, 214), radius=7, outline=0, fill=heat)
        DRAW.text((72, 200), "Off", font=NOTO, fill=not heat)  # type: ignore

    for idx, i in enumerate(history):
        DRAW.point((idx + 10, 250 - round((i - 10))))

    print(
        f"above={sensor_2_temp:0.1f} °C, below={sensor_1_temp:0.1f} °C, humidity={sensor_2_humidity:0.0f} %, heat={heat}, history={len(history)}"
    )
    draw()
    sleep(60)
