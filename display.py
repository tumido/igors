import sys
from time import sleep
from datetime import datetime
from typing import Any
from PIL import Image, ImageDraw, ImageFont
from utils.environment import DISPLAY_REFRESH, is_rpi
from waveshare_epd import epd2in13_V2
from utils.logging import assert_mode, get_logger
from utils.sensors import DHT_HST, DHT_HUM, DHT_TEMP, DS_TEMP, HEATER_POWER, Sensor
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
WIFI = [b"\ue1da", b"\uebe4", b"\uebe1", b"\uf065"]


SENSORS = [
    (0, DHT_TEMP),
    (57, DS_TEMP),
    (110, DHT_HUM),
]


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


def update_sensor(position: int, sensor: Sensor):
    new_value = sensor.read()
    if not sensor.value or new_value != sensor.value:
        DRAW.rectangle((4, 15 + position, 89, 58 + position), fill=1)
        sensor.set(new_value)
        length = DRAW.textlength(f"{sensor.value:0.1f}", font=BITTER_40)
        DRAW.text(  # type: ignore
            (89 - length, position),
            f"{sensor.value:0.1f}",
            font=BITTER_40,
        )


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
    DRAW.line((0, 60, DISPLAY.width, 60))
    for i in range(37):
        DRAW.line((-10 + (i * 4), 70, 0 + (i * 4), 60))
    DRAW.rounded_rectangle((1, 11, 121, 120), radius=8)
    DRAW.text((90, 84), "°C", font=BITTER_20)  # type: ignore
    DRAW.text((90, 135), "%", font=BITTER_20)  # type: ignore
    DRAW.text((10, 170), "Topení", font=NOTO)  # type: ignore

    LOGGER.info("Serving content")
    try:
        while True:
            now = datetime.now().strftime("%H:%M")
            DRAW.rectangle((0, 0, DISPLAY.width, 10), fill=1)
            DRAW.text((0, -3), now, font=NOTO)  # type: ignore
            quality = network_status().decode("unicode-escape")
            DRAW.text((110, -2), quality, font=MATERIAL_ICONS)  # type: ignore

            for s in SENSORS:
                update_sensor(*s)

            heat_new = HEATER_POWER.read()
            if HEATER_POWER.value != heat_new:
                HEATER_POWER.set(heat_new)
                DRAW.rounded_rectangle(
                    (27, 190, 57, 204), radius=7, outline=0, fill=not HEATER_POWER.value
                )
                DRAW.text((35, 190), "On", font=NOTO, fill=HEATER_POWER.value)  # type: ignore
                DRAW.rounded_rectangle(
                    (65, 190, 95, 204),
                    radius=7,
                    outline=0,
                    fill=bool(HEATER_POWER.value),
                )
                DRAW.text((72, 190), "Off", font=NOTO, fill=not HEATER_POWER.value)  # type: ignore

            history = DHT_HST.read()
            for idx, i in enumerate(history):
                DRAW.point((idx + 10, 250 - round((i - 10))))

            LOGGER.info(
                f"above={SENSORS[0][1].value:0.1f} °C, below={SENSORS[1][1].value:0.1f} °C, humidity={SENSORS[2][1].value:0.0f} %, heat={HEATER_POWER.value}, history={len(history)}"
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
