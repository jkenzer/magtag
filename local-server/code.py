# MagTag Shower Thoughts
# Be sure to put WiFi access point info in secrets.py file to connect

import time
import alarm
import board
from adafruit_magtag.magtag import MagTag


# Set up where we'll be fetching data from
DATA_SOURCE = "http://192.168.86.38:5000/"
MSG_LOCATION = ["message"]

# in seconds, we can refresh about 100 times on a battery
# TIME_BETWEEN_REFRESHES = (1 * 60 * 60) / 2  # one hour delay
pin_alarm = alarm.pin.PinAlarm(
    pin=board.D15, value=False, pull=True)
time_alarm = alarm.time.TimeAlarm(
    monotonic_time=time.monotonic() + (1 * 60 * 60) / 2)

magtag = MagTag(
    url=DATA_SOURCE,
    json_path=(MSG_LOCATION),
)


magtag.graphics.set_background("/bmps/magtag_shower_bg.bmp")

# joke in bold text, with text wrapping
magtag.add_text(
    text_font="/fonts/Arial-Bold-12.pcf",
    text_wrap=28,
    text_maxlen=140,
    text_position=(
        (magtag.graphics.display.width // 2),
        (magtag.graphics.display.height // 2) - 10,
    ),
    line_spacing=0.75,
    text_anchor_point=(0.5, 0.5),  # center the text on x & y
)

try:
    magtag.network.connect()
    value = magtag.fetch()
    print("Response is", value)
except (ValueError, RuntimeError) as e:
    magtag.set_text(e)
    print("Some error occured, retrying! -", e)

# wait 2 seconds for display to complete
time.sleep(2)
# magtag.exit_and_deep_sleep(TIME_BETWEEN_REFRESHES)
# alarm.exit_and_deep_sleep_until_alarms([pin_alarm, TIME_BETWEEN_REFRESHES])
alarm.exit_and_deep_sleep_until_alarms(time_alarm, pin_alarm)
