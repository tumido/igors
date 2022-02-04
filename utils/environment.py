import os


def is_rpi():
    return os.path.exists("/sys/bus/platform/drivers/gpiomem-bcm2835")
