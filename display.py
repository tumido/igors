import sys
from time import sleep
from typing import Callable, Any
from PIL import Image, ImageDraw, ImageFont
from collections import deque
from utils.environment import DISPLAY_REFRESH, is_rpi
from waveshare_epd import epd2in13_V2
from utils.logging import assert_mode, get_logger
import signal

LOGGER = get_logger("display")

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


class Display:
    FULL_UPDATE = epd2in13_V2.EPD.FULL_UPDATE
    PART_UPDATE = epd2in13_V2.EPD.PART_UPDATE

    def __init__(self):
        self.height = epd2in13_V2.EPD_HEIGHT
        self.width = epd2in13_V2.EPD_WIDTH

    def init(self, _mode: int):
        pass

    def display(self, _image: Image.Image):
        pass

    def displayPartBaseImage(self, _image: Image.Image):
        pass

    def displayPartial(self, image: Image.Image):
        image.save("test.png")

    def getbuffer(self, image: Image.Image) -> Image.Image:
        return image

    def Clear(self, _color: int):
        pass

    def sleep(self):
        pass


DISPLAY = epd2in13_V2.EPD() if is_rpi() else Display()


IMAGE = Image.new("1", (DISPLAY.width, DISPLAY.height), 255)
DRAW = ImageDraw.Draw(IMAGE)


def exit(_signal: int = 0, _frame: Any = None):
    LOGGER.info("Powering down display.")
    DISPLAY.init(DISPLAY.FULL_UPDATE)  # type: ignore
    DISPLAY.Clear(0xFF)  # type: ignore
    DISPLAY.sleep()  # type: ignore
    sys.exit(0)


signal.signal(signal.SIGTERM, exit)
signal.signal(signal.SIGINT, exit)


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


def main():
    DISPLAY.init(DISPLAY.FULL_UPDATE)  # type: ignore
    DISPLAY.Clear(0xFF)  # type: ignore
    DISPLAY.displayPartBaseImage(DISPLAY.getbuffer(IMAGE))  # type: ignore
    DISPLAY.init(DISPLAY.PART_UPDATE)  # type: ignore

    LOGGER.info("Drawing template")
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

    LOGGER.info("Serving content")
    ds_temp, dht_temp, dht_humidity, heat = (0, 0, 0, None)
    try:
        while True:
            ds_temp_new = get_sensor_data("/tmp/ds/temp")
            dht_temp_new = get_sensor_data("/tmp/dht/temp")
            dht_humidity_new = get_sensor_data("/tmp/dht/humidity")
            history = get_sensor_data("/tmp/dht/hist", lambda m: deque(m, maxlen=100))
            heat_new = get_sensor_data("/tmp/relay/on", val=lambda m: m == "true\n")

            if dht_temp != dht_temp_new:
                DRAW.rectangle((12, 5, 88, 48), fill=1)
                dht_temp = dht_temp_new
                DRAW.text(  # type: ignore
                    (12, -10),
                    f"{dht_temp:0.1f}",
                    font=BITTER_40,
                )

            if ds_temp != ds_temp_new:
                DRAW.rectangle((12, 65, 88, 108), fill=1)
                ds_temp = ds_temp_new
                DRAW.text(  # type: ignore
                    (12, 48),
                    f"{ds_temp:0.1f}",
                    font=BITTER_40,
                )

            if dht_humidity != dht_humidity_new:
                dht_humidity = dht_humidity_new
                DRAW.rectangle((35, 125, 80, 155), fill=1)
                DRAW.text(  # type: ignore
                    (35, 105),
                    f"{dht_humidity:0.0f}",
                    font=BITTER_40,
                )

            if heat != heat_new:
                heat = heat_new
                DRAW.rounded_rectangle(
                    (27, 200, 57, 214), radius=7, outline=0, fill=not heat
                )
                DRAW.text((35, 200), "On", font=NOTO, fill=heat)  # type: ignore
                DRAW.rounded_rectangle(
                    (65, 200, 95, 214), radius=7, outline=0, fill=heat
                )
                DRAW.text((72, 200), "Off", font=NOTO, fill=not heat)  # type: ignore

            for idx, i in enumerate(history):
                DRAW.point((idx + 10, 250 - round((i - 10))))

            LOGGER.info(
                f"above={dht_temp:0.1f} °C, below={ds_temp:0.1f} °C, humidity={dht_humidity:0.0f} %, heat={heat}, history={len(history)}"
            )
            DISPLAY.displayPartial(DISPLAY.getbuffer(IMAGE))  # type: ignore
            sleep(DISPLAY_REFRESH)

    except KeyboardInterrupt:
        LOGGER.info("exiting")

    except Exception as e:
        LOGGER.error(e)


if __name__ == "__main__":
    assert_mode(LOGGER)
    main()
