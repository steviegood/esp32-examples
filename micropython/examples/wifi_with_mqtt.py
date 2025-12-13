import machine, network

def read_secrets(fname):
    result = dict()
    with open(fname, 'r') as f:
        for line in f.readlines():
            line = line.rstrip('\n')
            (key, value) = line.split(':')
            result[key] = value
    return result


# See https://docs.micropython.org/en/latest/esp32/quickref.html#general-board-control
def do_connect(credentials):
    wlan = network.WLAN()
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WIFI...')
        wlan.connect(credentials.get("SSID"), credentials.get("KEY"))
        while not wlan.isconnected():
            machine.idle()
    print('WIFI IPv4 address: ', wlan.ipconfig('addr4'))
    print('WIFI MAC address: ', wlan.config('mac'))


secrets_filename = "secrets.txt"


wifi_creds = read_secrets(secrets_filename)

do_connect(wifi_creds)
