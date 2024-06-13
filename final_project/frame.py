import LedControl
import time

MASK0 = 0b00000000000000000000000011111111
MASK1 = 0b00000000000000001111111100000000
MASK2 = 0b00000000111111110000000000000000
MASK3 = 0b11111111000000000000000000000000

FRAME_DELAY = 70
FRAME_SIZE  = 24

lc12 = LedControl.LedControl(bus=0, device=0, numDevice=8)
lc3  = LedControl.LedControl(bus=0, device=1, numDevice=4)

def shutdownAll(b):
    if b == True:
        value = 0x01
    elif b == False:
        value = 0x00
    for i in range(8):
        lc12.shutdown(i, value)
        lc12.clearDisplay(i)
    for i in range(4):
        lc3.shutdown(i, value)
        lc3.clearDisplay(i)

def setIntensityAll(value):
    for i in range(8):
        lc12.setIntensity(i, value)
    for i in range(4):
        lc3.setIntensity(i, value)
    
def reverse(ch):
    """
    ch = (ch & 0xF0) >> 4 | (ch & 0x0F) << 4;
    ch = (ch & 0xCC) >> 2 | (ch & 0x33) << 2;
    ch = (ch & 0xAA) >> 1 | (ch & 0x55) << 1;
    """
    return ch

def update_frame(lframe : list):
    n1, n2, n3 = 0x00, 0x00, 0x00
    
    for i in range(7, -1, -1):
        n1 = (lframe[i]    & MASK0)
        n2 = (lframe[i+8]  & MASK0)
        n3 = (lframe[i+16] & MASK0)
        lc12.setRow(0, i, n1)
        lc12.setRow(4, i, n2)
        lc3.setRow(0, i, n3)
        
        n1 = (lframe[i]    & MASK1) >> 8
        n2 = (lframe[i+8]  & MASK1) >> 8
        n3 = (lframe[i+16] & MASK1) >> 8
        lc12.setRow(1, i, reverse(n1))
        lc12.setRow(5, i, reverse(n2))
        lc3.setRow(1, i, reverse(n3))

        n1 = (lframe[i]    & MASK2) >> 16
        n2 = (lframe[i+8]  & MASK2) >> 16
        n3 = (lframe[i+16] & MASK2) >> 16
        lc12.setRow(2, i, reverse(n1))
        lc12.setRow(6, i, reverse(n2))
        lc3.setRow(2, i, reverse(n3))

        n1 = (lframe[i]    & MASK3) >> 24
        n2 = (lframe[i+8]  & MASK3) >> 24
        n3 = (lframe[i+16] & MASK3) >> 24
        lc12.setRow(3, i, reverse(n1))
        lc12.setRow(7, i, reverse(n2))
        lc3.setRow(3, i, reverse(n3))


############################################################
# write function
############################################################

def write_char(x, y, ch, lframe):
    data = FONT(ch)
    if not len(data) == 5:
        print("Undefined Character!!!")
        return

    xoff = 27 - x
    yoff = 0
    lsf = True
    if xoff < 0:
        lsf = False
        if xoff < -4:
            xoff = 4
        else:
            xoff *= -1
    elif xoff > 27:
        xoff = 27
    yoff = y
    if yoff < 0:
        yoff = 0
    elif yoff > 23:
        yoff = 23
    
    for i in range(5):
        if i + yoff > 23:
            break

        mask = 31   # mask = 0b00...011111
        if lsf:
            mask = ~(mask << xoff)
        else:
            mask = ~(mask >> xoff)
        lframe[yoff + i] &= mask    # clear block
        
        if lsf:
            mask = data[i] << xoff
        else:
            mask = data[i] >> xoff

        lframe[yoff + i] |= mask

    update_frame(lframe)

def scroll_line(upperline, text, delay, lframe):
    for ch in text:
        for i in range(5):
            time.sleep(delay * 0.001)
            for k in range(5):
                lframe[upperline + k] = lframe[upperline + k] << 1

            write_char(31 - i, upperline, ch, lframe)
            update_frame(lframe)
        #time.sleep(delay * 0.001)
    
    for i in range(31):
        time.sleep(delay * 0.001)
        for k in range(5):
            lframe[upperline + k] = lframe[upperline + k] << 1

        update_frame(lframe)










