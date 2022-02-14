from time import sleep
from typing import Tuple
from utils.environment import SENSOR_POOLING, is_rpi
from utils.logging import assert_mode, get_logger
from utils.sensors import DHT_HST, DHT_HUM, DHT_TEMP

LOGGER = get_logger("dht22")


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
            DHT_TEMP.set(temperature)
            DHT_TEMP.save()
            DHT_HUM.set(humidity)
            DHT_HUM.save()
            DHT_HST.set(temperature)
            DHT_HST.save()

            sleep(SENSOR_POOLING)
    except KeyboardInterrupt:
        LOGGER.info("exiting")

    except Exception as e:
        LOGGER.error(e)


if __name__ == "__main__":
    assert_mode(LOGGER)
    main()
