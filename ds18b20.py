import os
from time import sleep
from typing import Callable
from utils.environment import SENSOR_POOLING, is_rpi
from utils.logging import assert_mode, get_logger

LOGGER = get_logger("ds18b20")

PATH = "/tmp/ds"


def main():
    if is_rpi():
        from w1thermsensor import W1ThermSensor  # type: ignore
        import RPi.GPIO as GPIO  # type: ignore

        DS_PIN = 2
        GPIO.setmode(GPIO.BCM)  # type: ignore
        GPIO.setup(DS_PIN, GPIO.OUT)  # type: ignore
        GPIO.output(DS_PIN, 1)  # type: ignore

        DS_SENSOR = W1ThermSensor()  # type: ignore

        get_data: Callable[[], float] = DS_SENSOR.get_temperature  # type: ignore
    else:
        from random import randint

        get_data = lambda: randint(100, 320) / 10

    try:
        while True:
            temperature = get_data()
            LOGGER.info(f"temp={temperature:0.1f}")
            with open(f"{PATH}/temp", "w") as f:
                f.write(f"{temperature}\n")
            sleep(SENSOR_POOLING)
    except KeyboardInterrupt:
        LOGGER.info("exiting")
    except Exception as e:
        LOGGER.error(e)
    finally:
        if is_rpi():
            GPIO.cleanup()  # type: ignore


if __name__ == "__main__":
    assert_mode(LOGGER)
    os.makedirs(PATH, exist_ok=True)
    main()
