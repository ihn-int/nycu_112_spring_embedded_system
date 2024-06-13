############################################################
# 8*8 Led  Matrix Drvier with Max7219 IC
# API mostly referenced from "LedControl.h" in Arduino
# function to control all matrix at once.
# Author: Kaic, Department of Computer Science, NYCU
# Modified and used as needed
############################################################

import spidev

# Max7219 register id
REG_NOOP   = 0x00
REG_DIGIT0 = 0x01
REG_DIGIT1 = 0x02
REG_DIGIT2 = 0x03
REG_DIGIT3 = 0x04
REG_DIGIT4 = 0x05
REG_DIGIT5 = 0x06
REG_DIGIT6 = 0x07
REG_DIGIT7 = 0x08
REG_DECODEMODE  = 0x09
REG_INTENSITY   = 0x0A
REG_SCANLIMIT   = 0x0B
REG_SHUTDOWN    = 0x0C
REG_DISPLAYTEST = 0x0F


class err():
    """
    Just a simple class for wrong message.
    """

    def DeviceErr(func):
        print("Invalid number of device. At {}.".format(func))
        exit()

    def AddrErr(func):
        print("Invalid address. At {}.".format(func))
        exit()
    
    def ValErr(func):
        print("Invalid value. At {}.".format(func))
        exit()

    def RowErr(func):
        print("Invalid row value. At {}.".format(func))
        exit()

    def ColErr(func):
        print("Invalid col value. At {}.".format(func))
        exit()


class LedControl():
    
    def __init__(self, bus=0, device=0, numDevice=1):
        """
        This is different from LedControl.h since spidev is more encapsulated.
        You should use bash command "ls /dev/*spi*" to check the
        spidev<bus>.<device> that you could use to control led matrix.
        """
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 1000000
        self.spi.lsbfirst = False

        #check numDevice
        if numDevice <= 0 or numDevice > 8 :
            err.DeviceErr("__init__")
        else:
            self.numDevice = numDevice
        
        # create frame buffer for each matrix, row major
        self.status = []
        for i in range(8 * self.numDevice):
            self.status.append(0x00)

        #create spi data for spidev to send
        self.spidata = []
        for i in range(2 * self.numDevice):
            self.spidata.append(0x00)
        
        for i in range(self.numDevice):
            self.spiTransfer(i, REG_DISPLAYTEST, 0x00)
            self.setScanLimit(i, 7)
            self.spiTransfer(i, REG_DECODEMODE, 0)
            self.clearDisplay(i)
            self.shutdown(i, 0x01)

    def getDeviceCount(self):
        return self.numDevice

    def shutdown(self, addr, value):
        if addr < 0 or addr >= self.numDevice:
            err.AddrErr("shutdown")
        if value != 0x00 and value != 0x01:
            err.ValErr("shutdown")
        self.spiTransfer(addr, REG_SHUTDOWN, value)

    def setScanLimit(self, addr, value):
        if addr < 0 or addr >= self.numDevice:
            err.AddrErr("setScanLimit")
        if value < 0 or value >= 8:
            err.ValErr("setScanLimit")
        self.spiTransfer(addr, REG_SCANLIMIT, value)

    def setIntensity(self, addr, value): 
        if addr < 0 or addr >= self.numDevice:
            err.AddrErr("setIntensity")
        if value < 0 or value >= 16:
            err.ValErr("setIntensity")
        self.spiTransfer(addr, REG_INTENSITY, value)

    def clearDisplay(self, addr):
        if addr < 0 or addr >= self.numDevice:
            err.AddrErr("clearDisplay")
        offset = addr * 8

        for i in range(8):
            self.status[offset+i] = 0x00
            self.spiTransfer(addr, REG_DIGIT0+i, self.status[offset+i])

    def setLed(self, addr, row, col, value):
        if addr < 0 or addr >= self.numDevice:
            err.AddrErr("setLed")

        offset = addr * 8
        val = 0x80 >> col
        if value == 0x00:
            self.status[offset + row] |= val
        elif value == 0x01:
            val ^= 0xFF
            self.status[offset + row] &= val
        else:
            err.ValErr("setLed")
        self.spiTransfer(addr, row, self.status[offset+row])
         
    def setRow(self, addr, row, value):
        if addr < 0 or addr >= self.numDevice:
            err.AddrErr("setRow")
        if row < 0 or row > 7:
            err.RowErr("setRow")

        # since no original byte type in Python
        if value < 0x00 or value > 0xFF:
            err.ValErr("setRow")

        offset = addr * 8
        self.status[offset+row] = value
        self.spiTransfer(addr, REG_DIGIT0 + row, self.status[offset+row])
    
    def setCol(self, addr, col, value):
        if addr < 0 or addr >= self.numDevice:
            err.AddrErr("setCol")
        if col < 0 or col > 7:
            err.ColErr("setCol")
        if value < 0x00 or value > 0xFF:
            err.ValErr("setCol")
        for i in range(8):
            val = value >> (7-i)
            val = (val & 0x01)
            self.setLed(addr, i, col, val)

    def spiTransfer(self, addr, reg, data):
        for i in range(self.numDevice * 2):
            self.spidata[i] = 0x00

        op = (self.numDevice-1-addr) * 2
        val = op + 1
        self.spidata[op] = reg
        self.spidata[val] = data
        
        self.spi.xfer3(self.spidata)

    





