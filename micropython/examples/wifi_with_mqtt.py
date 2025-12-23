import esp32
import machine
import network
import ubinascii
import uos
import umqtt.simple
import time
from machine import Pin
from utime import sleep


def read_secrets(fname):
    result = dict()
    with open(fname, 'r') as f:
        for line in f.readlines():
            if len(line)==0 or line[0] == '#' or ':' not in line:
                continue
            line = line.rstrip('\n')
            (key, value) = line.split(':')
            result[key] = value
    return result


def time_as_str(seconds=None):
    if not seconds:
        seconds = time.time()
    tt = time.localtime(seconds)
    s = '{year:04d}-{month:02d}-{day:02d}T{hh:02}:{mm:02d}:{ss:02d}'.format(year=tt[0], month=tt[1], day=tt[2], hh=tt[3], mm=tt[4], ss=tt[5])
    return s
    
    
def host_info():
    result = dict()
    h = uos.uname()
    result['sysname'] = h.sysname
    result['nodename'] = h.nodename
    result['release'] = h.release
    result['version'] = h.version
    result['machine'] = h.machine
    result['unique_id'] = machine.unique_id().hex()
    return result
    

# See https://docs.micropython.org/en/latest/esp32/quickref.html#general-board-control
def connect_wifi(credentials):
    wlan = network.WLAN()
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WIFI...')
        wlan.connect(credentials.get("WIFI_SSID"), credentials.get("WIFI_KEY"))
        while not wlan.isconnected():
            machine.idle()
    print('WIFI connectivity:')
    print(f'\tWIFI IPv4 address(es): {", ".join(wlan.ipconfig("addr4"))}')
    print(f'\tWIFI MAC address: ' + ubinascii.hexlify(wlan.config('mac'),':').decode().upper())
    return wlan


# See https://mpython.readthedocs.io/en/v2.2.1/library/mPython/umqtt.simple.html
def connect_mqtt(credentials):
    client_id = 'esp32-'+machine.unique_id().hex()
    server = credentials.get('MQTT_HOST')
    port = credentials.get('MQTT_PORT')
    user = credentials.get('MQTT_USER', None)
    password = credentials.get('MQTT_PASS', None)
    keepalive = 60
    ssl = False
    ssl_params = {}
    mqtt = umqtt.simple.MQTTClient(client_id, server, port=port, user=user, password=password, keepalive=keepalive, ssl=ssl, ssl_params=ssl_params)
    mqtt.connect()
    return mqtt


# Main program
reason = machine.wake_reason()
print(f"Wake reason: {reason}")

hostinfo = host_info()
print('Host information:')
for k in hostinfo:
    print(f'\t{k}: {hostinfo.get(k)}')
    
secrets_filename='secrets.txt'
secrets = read_secrets(secrets_filename)
print('Secrets:')
for k in secrets:
    print(f'\t{k}: {secrets.get(k)}')
    
wifi = connect_wifi(secrets)
mqtt = connect_mqtt(secrets)

topic = secrets.get('MQTT_PUBLISH_TOPIC')
print(f'Using publish topic: {topic}')

mqtt.publish(topic,'Initiated connection from esp32',0)

light_on_time = 1         # seconds
light_off_time = 2        # seconds
deep_sleep_time = 60      # seconds
light_iterations = 5      # cycle count
led_pin_number = 5               # pin for LED
button_pin_number = 4            # pin for button


led = Pin(led_pin_number, Pin.OUT)
button = Pin(button_pin_number, Pin.IN)

esp32.wake_on_ext0(pin = button, level = esp32.WAKEUP_ANY_HIGH)

i = 0
while i < light_iterations:
    led.on()
    mqtt.publish(topic, 'Light ON',0)
    sleep(light_on_time)
    led.off()
    mqtt.publish(topic, 'Light OFF',0)
    sleep(light_off_time)
    i = i+1

print('Preparing for deepsleep...')
mqtt.publish(topic, 'Entering deepsleep...',0)
sleep(5)   # sleeping so MQTT message can be published to broker
print('Entering deepsleep')
machine.deepsleep(deep_sleep_time*1000)


