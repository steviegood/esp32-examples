import machine
import network
import uos
import umqtt.simple
import time


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
    print('WIFI IPv4 address: ', wlan.ipconfig('addr4'))
    print('WIFI MAC address: ', wlan.config('mac'))


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
hostinfo = host_info()
for k in hostinfo:
    print(k+': '+hostinfo.get(k))
    
credentials = read_secrets(secrets_filename)
for k in credentials:
    print('Found credendtial: '+k)
    
connect_wifi(credentials)

mqtt = connect_mqtt(credentials)



connect_wifi(wifi_creds)
