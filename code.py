import alarm
import board
import os
import time

from adafruit_seesaw.seesaw import Seesaw


from lib.lora_sender import LoraSender
from lib.battery_monitor import BatteryMonitor


def sleep(duration: int = 10800):
    time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + duration)
    alarm.exit_and_deep_sleep_until_alarms(time_alarm)


def celsius_to_fahrenheit(celsius: float) -> float:
    return (celsius * 9 / 5) + 32


battery = BatteryMonitor()
voltage: float = 0.0
try:
    voltage = battery.read_battery_voltage()
    battery.blink_status()
    print(f"Battery voltage: {voltage:.2f}V")

    if voltage < battery.voltage_threshold:
        print("Low battery detected!")
        sleep()
except Exception as e:
    print(f"Error: {e}")


i2c_bus = board.STEMMA_I2C()

soil = Seesaw(i2c_bus, addr=0x36)


message: dict = {
    "temp": celsius_to_fahrenheit(soil.get_temp()),
    "soil": soil.moisture_read(),
    "battery": voltage,
}

sender = LoraSender(device_num=int(os.getenv("DEVICE_ID", "123")))

success = sender.send_data(message)

sleep()
