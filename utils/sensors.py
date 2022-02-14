from collections import deque
from pathlib import Path
from typing import Callable, Any, Union, cast


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


class Sensor:
    def __init__(
        self,
        name: str,
        property: str,
        value: Union[float, int, str, deque[float], bool] = 0.0,
    ):
        self.path = Path(f"/tmp/{name}/{property}")
        self.value = value
        self.mapping: Callable[[str], Any] = lambda x: float(x)
        self.cast = next
        if isinstance(self.value, deque):
            self.cast = list
        elif isinstance(self.value, bool):
            self.mapping: Callable[[str], Any] = lambda x: x == "True\n"

        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)

    def set(self, value: Union[float, int, str, bool]):
        if isinstance(self.value, deque):
            self.value.append(cast(float, value))
        else:
            self.value = value

    def read(self) -> Any:
        with open(self.path) as f:
            try:
                return self.cast(map(self.mapping, f.readlines()))
            except StopIteration:
                return self.value

    def save(self):
        value = (
            [str(i) for i in self.value]
            if isinstance(self.value, deque)
            else [str(self.value)]
        )
        with open(self.path, "w") as f:
            f.write("\n".join(value) + "\n")


DHT_TEMP = Sensor("dht", "temp")
DHT_HUM = Sensor("dht", "humidity")
DHT_HST = Sensor("dht", "history", deque([], maxlen=100))
DS_TEMP = Sensor("ds", "temp")
HEATER_POWER = Sensor("heater", "power", False)
HEATER_TIMEOUT = Sensor("heater", "timeout", "")
