from time import sleep
from typing import Callable, Literal
from utils.environment import SENSOR_POOLING, is_rpi
from utils.logging import assert_mode, get_logger
from utils.sensors import HEATER_POWER

LOGGER = get_logger("relay")


def main():
    if is_rpi():
        import RPi.GPIO as GPIO  # type: ignore

        RELAY_POWER = 14
        RELAY_INPUT = 15
        GPIO.setmode(GPIO.BCM)  # type: ignore
        GPIO.setup(RELAY_POWER, GPIO.OUT)  # type: ignore
        GPIO.setup(RELAY_INPUT, GPIO.OUT)  # type: ignore
        GPIO.output(RELAY_POWER, 1)  # type: ignore
        GPIO.output(RELAY_INPUT, 1)  # type: ignore

        set_data: Callable[[Literal[0, 1]], None] = lambda x: GPIO.output(RELAY_INPUT, x)  # type: ignore
    else:
        set_data = lambda x: print(x)

    try:
        while True:
            power = HEATER_POWER.read()
            LOGGER.info(f"{power=}")
            set_data(0 if power else 1)
            sleep(SENSOR_POOLING)
    except KeyboardInterrupt:
        LOGGER.info("exiting")
    except Exception as e:
        LOGGER.error(e)
    finally:
        if is_rpi():
            GPIO.cleanup([RELAY_POWER, RELAY_INPUT])  # type: ignore


if __name__ == "__main__":
    assert_mode(LOGGER)
    main()
