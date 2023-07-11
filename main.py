import network, time, uasyncio as asyncio
from aircraft import Aircraft
from lib.microdot_asyncio import Microdot, Request



Request.socket_read_timeout = 5 # increase socket timeout to 5 seconds

WIFI_SSID: str = "WLAN Netzwerk"
WIFI_PASSWORD: str = "ISLAND2006"

PIN_LOGO: int = 2
PIN_NAVIGATION: int = 4
PIN_LANDING_FRONT: int = 5
PIN_LANDING_WINGS: int = 12
PIN_STROBE: int = 17
PIN_BEACON: int = 18



def debugPrint(*args, **kwargs) -> None:
    print(*args, **kwargs)


aircraft: Aircraft = Aircraft(PIN_LOGO, PIN_NAVIGATION, PIN_LANDING_FRONT, PIN_LANDING_WINGS, PIN_STROBE, PIN_BEACON)

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
    return {"done": True}, 200, {'Content-Type': 'application/json'}

@app.route('/api/logo/disable')
async def logo_off(request):
    debugPrint("disable logo_off")
    aircraft.logo_off()
    return {"done": True}, 200, {'Content-Type': 'application/json'}

@app.route('/api/navigation/enable')
async def navigation_on(request):
    debugPrint("enable navigation_on")
    aircraft.navigation_on()
    return {"done": True}, 200, {'Content-Type': 'application/json'}

@app.route('/api/navigation/disable')
async def navigation_off(request):
    debugPrint("disable navigation_off")
    aircraft.navigation_off()
    return {"done": True}, 200, {'Content-Type': 'application/json'}

@app.route('/api/landing-front/enable')
async def landing_front_on(request):
    debugPrint("enable landing_front_on")
    aircraft.landing_front_on()
    return {"done": True}, 200, {'Content-Type': 'application/json'}

@app.route('/api/landing-front/disable')
async def landing_front_off(request):
    debugPrint("disable landing_front_off")
    aircraft.landing_front_off()
    return {"done": True}, 200, {'Content-Type': 'application/json'}

@app.route('/api/landing-wings/enable')
async def landing_wings_on(request):
    debugPrint("enable landing_wings_on")
    aircraft.landing_wings_on()
    return {"done": True}, 200, {'Content-Type': 'application/json'}

@app.route('/api/landing-wings/disable')
async def landing_wings_off(request):
    debugPrint("disable landing_wings_off")
    aircraft.landing_wings_off()
    return {"done": True}, 200, {'Content-Type': 'application/json'}

@app.route('/api/strobe/enable')
async def strobe_on(request):
    debugPrint("enable strobe_on")
    aircraft.strobe_on()
    return {"done": True}, 200, {'Content-Type': 'application/json'}

@app.route('/api/strobe/disable')
async def strobe_off(request):
    debugPrint("disable strobe_off")
    aircraft.strobe_off()
    return {"done": True}, 200, {'Content-Type': 'application/json'}

@app.route('/api/beacon/enable')
async def beacon_on(request):
    debugPrint("enable beacon_on")
    aircraft.beacon_on()
    return {"done": True}, 200, {'Content-Type': 'application/json'}

@app.route('/api/beacon/disable')
async def beacon_off(request):
    debugPrint("disable beacon_off")
    aircraft.beacon_off()
    return {"done": True}, 200, {'Content-Type': 'application/json'}


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
