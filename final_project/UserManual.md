# About LedControl.py
> I haven't search someone else do it, so I did.

The bulk of code and usage is referenced from "LedControl.cpp" in Arduino. But no seven-segment part is implemented.

You'll need to install spidev to use this module on Raspberry pi.

## For Raspberry Pi
Download "LedControl.py" to use led matrix drived by MAX7219.

## For Arduino type
Download "LedControl.h" library with Arduino IDE.

frame.py is NOT a necessary file but a function library for myself to complete the project.

## API list

class LedControl
- LedControl(bus=0, device=0,numDevice=1) -> None
  - bus: which spi bus to use
  - device: while slave to use
- getDeviceCount() -> int
- shutdown(addr, value) -> None
  - addr: which matrix to shutdown
  - value: decide whether turn on or off
- setIntensity(addr, value) -> None
  - addr: which matrix to set intensity
  - value: the intensity value
- 