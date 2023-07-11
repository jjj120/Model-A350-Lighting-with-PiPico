import machine
import uasyncio as asyncio


# class Aircraft:
#     def __init__(self, pin_logo, pin_navigation, pin_landing_front, pin_landing_wings, pin_strobe, pin_beacon) -> None:
#         pass

class Aircraft:
    _logo: bool = False
    _navigation: bool = False
    _landing_front: bool = False
    _landing_wings: bool = False
    _strobe: bool = False
    _beacon: bool = False

    pin_logo: machine.Pin
    pin_navigation: machine.Pin
    pin_landing_front: machine.Pin
    pin_landing_wings: machine.Pin
    pin_strobe: machine.Pin
    pin_beacon: machine.Pin
    

    def __init__(self, pin_logo, pin_navigation, pin_landing_front, pin_landing_wings, pin_strobe, pin_beacon):
        self.pin_logo = machine.Pin(pin_logo, machine.Pin.OUT)
        self.pin_navigation = machine.Pin(pin_navigation, machine.Pin.OUT)
        self.pin_landing_front = machine.Pin(pin_landing_front, machine.Pin.OUT)
        self.pin_landing_wings = machine.Pin(pin_landing_wings, machine.Pin.OUT)
        self.pin_strobe = machine.Pin(pin_strobe, machine.Pin.OUT)
        self.pin_beacon = machine.Pin(pin_beacon, machine.Pin.OUT)



    def debugPrint(self, message) -> None:
        print(message)

    @property
    def logo(self) -> bool:
        return self._logo

    def logo_on(self) -> None:
        self.debugPrint("enable logo_on")
        self.pin_logo.on()
        self._logo = True
    def logo_off(self) -> None:
        self.debugPrint("disable logo_off")
        self.pin_logo.off()
        self._logo = False

    
    @property
    def navigation(self) -> bool:
        return self._navigation

    def navigation_on(self) -> None:
        self.debugPrint("enable navigation_on")
        self.pin_navigation.on()
        self._navigation = True
    def navigation_off(self) -> None:
        self.debugPrint("disable navigation_off")
        self.pin_navigation.off()
        self._navigation = False


    @property
    def landing_front(self) -> bool:
        return self._landing_front

    def landing_front_on(self) -> None:
        self.debugPrint("enable landing_front_on")
        self.pin_landing_front.on()
        self._landing_front = True
    def landing_front_off(self) -> None:
        self.debugPrint("disable landing_front_off")
        self.pin_landing_front.off()
        self._landing_front = False


    @property
    def landing_wings(self) -> bool:
        return self._landing_wings

    def landing_wings_on(self) -> None:
        self.debugPrint("enable landing_wings_on")
        self.pin_landing_wings.on()
        self._landing_wings = True
    def landing_wings_off(self) -> None:
        self.debugPrint("disable landing_wings_off")
        self.pin_landing_wings.off()
        self._landing_wings = False



    strobe_task: asyncio.Task
    @property
    def strobe(self) -> bool:
        return self._strobe

    def strobe_on(self) -> None:
        if (self._strobe == True): return
        self.debugPrint("enable strobe_on")
        self.strobe_task = asyncio.create_task(self.blink(self.pin_strobe, 0.04, 0.05, 0.04, 0.87))
        self._strobe = True
    def strobe_off(self) -> None:
        if (self._strobe == False): return
        self.debugPrint("disable strobe_off")
        try:
            self.strobe_task.cancel()
        except Exception as e:
            self.debugPrint("Exception: " + str(e))
        self._strobe = False


    beacon_task: asyncio.Task
    @property
    def beacon(self) -> bool:
        return self._beacon

    def beacon_on(self) -> None:
        if (self._beacon == True): return
        self.debugPrint("enable beacon_on")
        self.beacon_task = asyncio.create_task(self.blink(self.pin_beacon, 0.08, 0.92))
        self._beacon = True
    def beacon_off(self) -> None:
        if (self._beacon == False): return
        self.debugPrint("disable beacon_off")
        try:
            self.beacon_task.cancel()
        except Exception as e:
            self.debugPrint("Exception: " + str(e))
        self._beacon = False


    @property
    def status(self) -> dict:
        return {
            'logo': self.logo,
            'navigation': self.navigation,
            'landingFront': self.landing_front,
            'landingWings': self.landing_wings,
            'strobe': self.strobe,
            'beacon': self.beacon
        }
    
    async def blink(self, pin: machine.Pin, delay_on1: float, delay_off1: float, delay_on2: float = 0, delay_off2: float = 0) -> None:
        while True:
            pin.on()
            await asyncio.sleep(delay_on1)
            pin.off()
            await asyncio.sleep(delay_off1)
            if delay_on2 > 0:
                pin.on()
                await asyncio.sleep(delay_on2)
                pin.off()
                await asyncio.sleep(delay_off2)


