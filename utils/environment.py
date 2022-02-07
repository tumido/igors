import os


def is_rpi():
    return os.path.exists("/sys/bus/platform/drivers/gpiomem-bcm2835")


SENSOR_POOLING = 10
DISPLAY_REFRESH = 600
