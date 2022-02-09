import os
from time import sleep
from typing import Tuple
from collections import deque
from utils.environment import SENSOR_POOLING, is_rpi
from utils.logging import assert_mode, get_logger

LOGGER = get_logger("dht22")
PATH = "/tmp/dht"

HISTORY = deque([], maxlen=100)


def main():
    if is_rpi():
        import Adafruit_DHT  # type: ignore

        DHT_SENSOR = Adafruit_DHT.DHT22  # type: ignore
        DHT_PIN = 3  # type: ignore

        def get_data() -> Tuple[float, float]:
            return Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)  # type: ignore

    else:
        from random import randint

        def get_data():
            return randint(0, 1000) / 10, randint(100, 320) / 10

    try:
        while True:
            humidity, temperature = get_data()
            LOGGER.info(f"temp={temperature:0.1f} humidity={humidity:0.1f}")
            with open(f"{PATH}/temp", "w") as f:
                f.write(f"{temperature}\n")
            with open(f"{PATH}/humidity", "w") as f:
                f.write(f"{humidity}\n")

            HISTORY.append(temperature)
            with open(f"{PATH}/history", "w") as f:
                f.write("\n".join(str(i) for i in HISTORY) + "\n")

            sleep(SENSOR_POOLING)
    except KeyboardInterrupt:
        LOGGER.info("exiting")

    except Exception as e:
        LOGGER.error(e)


if __name__ == "__main__":
    assert_mode(LOGGER)
    os.makedirs(PATH, exist_ok=True)
    main()
