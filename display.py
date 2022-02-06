from dataclasses import dataclass
import sys
from time import sleep
from datetime import datetime
from typing import Callable, Any, Optional
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
MATERIAL_ICONS = ImageFont.truetype(
    "fonts/MaterialIconsOutlined-Regular.otf",
    13,
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


@dataclass
class SensorOnDisplay:
    position: int
    path: str
    value: Optional[float] = None


SENSORS = [
    SensorOnDisplay(4, "/tmp/ds/temp"),
    SensorOnDisplay(61, "/tmp/dht/temp"),
    SensorOnDisplay(119, "/tmp/dht/humidity"),
]


def update_sensor(s: SensorOnDisplay):
    new_value = get_sensor_data(s.path)
    if not s.value or new_value != s.value:
        DRAW.rectangle((4, 15 + s.position, 89, 58 + s.position), fill=1)
        s.value = new_value
        length = DRAW.textlength(f"{s.value:0.1f}", font=BITTER_40)
        DRAW.text(  # type: ignore
            (89 - length, s.position),
            f"{s.value:0.1f}",
            font=BITTER_40,
        )


WIFI = [b"\ue1da", b"\uebe4", b"\uebe1", b"\uf065"]


def network_status():
    with open("/proc/net/wireless") as f:
        status = f.readlines()
    if len(status) < 3:  # First 2 lines are header
        return WIFI[0]

    try:
        strength = (
            float(status[-1].split()[2]) / 70
        )  # 3rd field is quality and 70 is max
        return WIFI[round(2 * strength) + 1]
    except:
        return WIFI[0]


def main():
    # Reset and init
    # Partial reset doesn't wait for BUSY - helps initialize after possible power outage
    DISPLAY.init(DISPLAY.PART_UPDATE)  # type: ignore
    # Now properly reset and clean
    DISPLAY.init(DISPLAY.FULL_UPDATE)  # type: ignore
    DISPLAY.Clear(0xFF)  # type:ignore

    # Prepare to draw
    DISPLAY.displayPartBaseImage(DISPLAY.getbuffer(IMAGE))  # type: ignore
    DISPLAY.init(DISPLAY.PART_UPDATE)  # type: ignore

    LOGGER.info("Drawing template")
    DRAW.text((90, 30), "°C", font=BITTER_20)  # type: ignore
    DRAW.line((3, 64, DISPLAY.width - 3, 64))
    for i in range(37):
        DRAW.line((-10 + (i * 4), 74, 0 + (i * 4), 64))
    DRAW.line((0, 0, 0, 100), fill=1)
    DRAW.line((121, 0, 121, 110), fill=1)
    DRAW.rounded_rectangle((1, 14, 120, 124), radius=8)
    DRAW.text((90, 88), "°C", font=BITTER_20)  # type: ignore
    DRAW.text((90, 144), "%", font=BITTER_20)  # type: ignore
    DRAW.text((10, 180), "Topení", font=NOTO)  # type: ignore

    LOGGER.info("Serving content")
    ds_temp, dht_temp, dht_humidity, heat = (0, 0, 0, None)
    try:
        while True:
            now = datetime.now().strftime("%H:%M")
            DRAW.rectangle((0, 0, DISPLAY.width, 13), fill=1)
            DRAW.text((2, 0), now, font=NOTO)  # type: ignore
            quality = network_status().decode("unicode-escape")
            DRAW.text((105, 0), quality, font=MATERIAL_ICONS)  # type: ignore

            for s in SENSORS:
                update_sensor(s)

            heat_new = get_sensor_data("/tmp/relay/on", val=lambda m: m == "true\n")
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

            history = get_sensor_data("/tmp/dht/hist", lambda m: deque(m, maxlen=100))
            for idx, i in enumerate(history):
                DRAW.point((idx + 10, 250 - round((i - 10))))

            LOGGER.info(
                f"above={dht_temp:0.1f} °C, below={ds_temp:0.1f} °C, humidity={dht_humidity:0.0f} %, heat={heat}, history={len(history)}"
            )
            DISPLAY.displayPartial(DISPLAY.getbuffer(IMAGE))  # type: ignore

            # Do not loop on debug
            if isinstance(DISPLAY, Display):
                break
            sleep(DISPLAY_REFRESH)

    except KeyboardInterrupt:
        LOGGER.info("exiting")

    except Exception as e:
        LOGGER.error(e)


if __name__ == "__main__":
    assert_mode(LOGGER)
    main()
