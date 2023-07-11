# Code for controlling Lighting on Model A350

The Model I use is the [Revell Airbus A350-900](https://www.revell.de/produkte/modellbau/flugzeuge/zivile-flugzeuge/airbus-a350-900-lufthansa-new-livery.html?listtype=search&searchparam=A350). 

I modified the model to add small SMD-LEDs soldered on wires that I bought on ebay. 

Controlling the LEDs I use a Raspberry Pi Pico W with the Wires of the LEDs soldered to the Pico through resistors to not damage the LEDs. I store the Pico in the aircraft's fuselage and connect it to a battery pack that I want to store in a small container above the aircraft hanging from the ceiling. That is not built yet, hopefully it works as intended. 

Controlling the LEDs is done by opening the website the Pico hosts and clicking the buttons. The Pico then controls the LEDs accordingly. The Website also has a built in feedback so the user can see which LEDs are currently on.

Currently I have the following LEDs installed:
- Red/Green navigation lights in the wingtips
- White strobe lights in the wingtips
- Logo lights on the surface of the horizontal stabilizer
- Landing lights:
    - 2x in the wing roots
    - 2x in the back landing gear
    - in the front landing gear
- Cockpit lights
- Red Anti-collision beacons lights on the top and bottom of the fuselage

