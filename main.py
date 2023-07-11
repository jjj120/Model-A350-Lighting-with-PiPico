import network, time, uasyncio as asyncio
from aircraft import Aircraft
from lib.microdot_asyncio import Microdot, Request



Request.socket_read_timeout = 10 # increase socket timeout to 5 seconds

WIFI_SSID: str = "WLAN Netzwerk"
WIFI_PASSWORD: str = "ISLAND2006"

PIN_LOGO: int = 2           # Color: white; Voltage: 3,20V; Current: 20mA; Resistor:  5 Ohm
PIN_NAVIGATION: int = 4     # Color: red;   Voltage: 2,00V; Current: 20mA; Resistor: 65 Ohm
                            # Color: green; Voltage: 2,27V; Current: 20mA; Resistor: 50 Ohm
PIN_LANDING_FRONT: int = 5  # Color: white; Voltage: 3,20V; Current: 20mA; Resistor:  5 Ohm
PIN_LANDING_WINGS: int = 12 # Color: white; Voltage: 3,20V; Current: 20mA; Resistor:  5 Ohm
PIN_LANDING_BACK: int = 11  # Color: white; Voltage: 3,20V; Current: 20mA; Resistor:  5 Ohm
PIN_STROBE: int = 17        # Color: white; Voltage: 3,20V; Current: 20mA; Resistor:  5 Ohm
PIN_BEACON: int = 18        # Color: red;   Voltage: 2,00V; Current: 20mA; Resistor: 65 Ohm
PIN_COCKPIT: int = 19       # Color: white; Voltage: 3,20V; Current: 20mA; Resistor:  5 Ohm


def debugPrint(*args, **kwargs) -> None:
    # pass
    print(*args, **kwargs)


aircraft: Aircraft = Aircraft(PIN_LOGO, PIN_NAVIGATION, PIN_LANDING_FRONT, PIN_LANDING_WINGS, PIN_LANDING_BACK, PIN_STROBE, PIN_BEACON, PIN_COCKPIT)

# Connect to WLAN
wlan: network.WLAN = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)


# Wait for connect or fail
wait: int = 20
while wait > 0:
    debugPrint('status: ', wlan.status())
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print('waiting for connection...')
    time.sleep(1)
 
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('wifi connection failed')
else:
    print('connected')
    ip=wlan.ifconfig()[0]
    print('IP: ', ip)

# Start webserver
with open('index.html', 'r') as f:
    HTML_STRING: str = f.read()



app: Microdot = Microdot()

@app.route('/')
async def index(request):
    debugPrint("serve index")
    return HTML_STRING, 200, {'Content-Type': 'text/html'}

@app.route('/api/status')
async def status(request):
    debugPrint("serve status")
    return str(aircraft.status), 200, {'Content-Type': 'application/json'}

@app.route('/api/logo/enable')
async def logo_on(request):
    debugPrint("enable logo_on")
    aircraft.logo_on()
    return str(aircraft.status), 200, {'Content-Type': 'application/json'}

@app.route('/api/logo/disable')
async def logo_off(request):
    debugPrint("disable logo_off")
    aircraft.logo_off()
    return str(aircraft.status), 200, {'Content-Type': 'application/json'}

@app.route('/api/navigation/enable')
async def navigation_on(request):
    debugPrint("enable navigation_on")
    aircraft.navigation_on()
    return str(aircraft.status), 200, {'Content-Type': 'application/json'}

@app.route('/api/navigation/disable')
async def navigation_off(request):
    debugPrint("disable navigation_off")
    aircraft.navigation_off()
    return str(aircraft.status), 200, {'Content-Type': 'application/json'}

@app.route('/api/landing-front/enable')
async def landing_front_on(request):
    debugPrint("enable landing_front_on")
    aircraft.landing_front_on()
    return str(aircraft.status), 200, {'Content-Type': 'application/json'}

@app.route('/api/landing-front/disable')
async def landing_front_off(request):
    debugPrint("disable landing_front_off")
    aircraft.landing_front_off()
    return str(aircraft.status), 200, {'Content-Type': 'application/json'}

@app.route('/api/landing-wings/enable')
async def landing_wings_on(request):
    debugPrint("enable landing_wings_on")
    aircraft.landing_wings_on()
    return str(aircraft.status), 200, {'Content-Type': 'application/json'}

@app.route('/api/landing-wings/disable')
async def landing_wings_off(request):
    debugPrint("disable landing_wings_off")
    aircraft.landing_wings_off()
    return str(aircraft.status), 200, {'Content-Type': 'application/json'}

@app.route('/api/landing/enable')
async def landing_on(request):
    debugPrint("enable landing_on")
    aircraft.landing_front_on()
    aircraft.landing_wings_on()
    return str(aircraft.status), 200, {'Content-Type': 'application/json'}

@app.route('/api/landing/disable')
async def landing_off(request):
    debugPrint("disable landing_off")
    aircraft.landing_front_off()
    aircraft.landing_wings_off()
    return str(aircraft.status), 200, {'Content-Type': 'application/json'}

@app.route('/api/strobe/enable')
async def strobe_on(request):
    debugPrint("enable strobe_on")
    aircraft.strobe_on()
    return str(aircraft.status), 200, {'Content-Type': 'application/json'}

@app.route('/api/strobe/disable')
async def strobe_off(request):
    debugPrint("disable strobe_off")
    aircraft.strobe_off()
    return str(aircraft.status), 200, {'Content-Type': 'application/json'}

@app.route('/api/beacon/enable')
async def beacon_on(request):
    debugPrint("enable beacon_on")
    aircraft.beacon_on()
    return str(aircraft.status), 200, {'Content-Type': 'application/json'}

@app.route('/api/beacon/disable')
async def beacon_off(request):
    debugPrint("disable beacon_off")
    aircraft.beacon_off()
    return str(aircraft.status), 200, {'Content-Type': 'application/json'}

@app.route('/api/anti-collision/enable')
async def anti_collision_on(request):
    debugPrint("enable anti-collision_on")
    aircraft.strobe_on()
    aircraft.beacon_on()
    return str(aircraft.status), 200, {'Content-Type': 'application/json'}

@app.route('/api/anti-collision/disable')
async def anti_collision_off(request):
    debugPrint("disable anti-collision_off")
    aircraft.strobe_off()
    aircraft.beacon_off()
    return str(aircraft.status), 200, {'Content-Type': 'application/json'}

@app.route('/api/all/enable')
async def all_on(request):
    debugPrint("enable all_on")
    aircraft.all_on()
    return str(aircraft.status), 200, {'Content-Type': 'application/json'}

@app.route('/api/all/disable')
async def all_off(request):
    debugPrint("disable all_off")
    aircraft.all_off()
    return str(aircraft.status), 200, {'Content-Type': 'application/json'}


async def main():
    try:
        await app.start_server(ip, 80)
    except KeyboardInterrupt:
        print('Closing server')
        app.shutdown()
        wlan.disconnect()
        wlan.active(False)
        print('Server closed')


if __name__ == '__main__':
    asyncio.run(main())
