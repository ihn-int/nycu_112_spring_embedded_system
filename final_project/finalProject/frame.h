#include "font.h"
#include "LedControl.h"

// VSPI_MOSI GPIO23 23
// VSPI_CLK GPIO18  18
// VSPI_CS GPIO5    5
// VSPI_CS2 GPIO17  17

#define MOSI 11
#define SCLK 13
#define SS1 10
#define SS2 9


#define mask0 0b00000000000000000000000011111111
#define mask1 0b00000000000000001111111100000000
#define mask2 0b00000000111111110000000000000000
#define mask3 0b11111111000000000000000000000000

#define DELAY 70
#define FRAME_SIZE 24


LedControl lc12 = LedControl(MOSI, SCLK, SS1, 8);
LedControl lc3 = LedControl(MOSI, SCLK, SS2, 4);



void shutdownAll(){
  for(int i = 0; i < 4; i++){
    lc12.shutdown(i, false);
    lc12.clearDisplay(0);
    lc12.shutdown(i+4, false);
    lc12.clearDisplay(0);
    lc3.shutdown(i, false);
    lc3.clearDisplay(0);
  }
  return;
}

void setIntensityAll(){
  for(int i = 0; i < 4; i++){
    lc12.setIntensity(i, 7);
    lc12.setIntensity(i+4, 7);
    lc3.setIntensity(i, 7);
  }
  return;
}

unsigned char reverse(unsigned char b){
  /** /
  b = (b & 0xF0) >> 4 | (b & 0x0F) << 4;
  b = (b & 0xCC) >> 2 | (b & 0x33) << 2;
  b = (b & 0xAA) >> 1 | (b & 0x55) << 1;
  /**/
  return b;
}

void updateFrame(unsigned long* pframe){
  unsigned char n1, n2, n3;

  for(int i = 0; i < 8; i++){
    
    n1 = (pframe[i] & mask0);
    n2 = (pframe[i+8] & mask0);
    n3 = (pframe[i+16] & mask0);
    lc12.setRow(0, i, reverse(n1));
    lc12.setRow(4, i, reverse(n2));
    lc3.setRow(0, i, reverse(n3));

    n1 = (pframe[i] & mask1) >> 8;
    n2 = (pframe[i+8] & mask1) >> 8;
    n3 = (pframe[i+16] & mask1) >> 8;
    lc12.setRow(1, i, reverse(n1));
    lc12.setRow(5, i, reverse(n2));
    lc3.setRow(1, i, reverse(n3));

    n1 = (pframe[i] & mask2) >> 16;
    n2 = (pframe[i+8] & mask2) >> 16;
    n3 = (pframe[i+16] & mask2) >> 16;
    lc12.setRow(2, i, reverse(n1));
    lc12.setRow(6, i, reverse(n2));
    lc3.setRow(2, i, reverse(n3));
    
    n1 = (pframe[i] & mask3) >> 24;
    n2 = (pframe[i+8] & mask3) >> 24;
    n3 = (pframe[i+16] & mask3) >> 24;
    lc12.setRow(3, i, reverse(n1));
    lc12.setRow(7, i, reverse(n2));
    lc3.setRow(3, i, reverse(n3));
  }
  return;
}


unsigned char* mapChar(char ch){
  switch(ch){
    case 'A': return FONT_A;
    case 'B': return FONT_B;
    case 'C': return FONT_C;
    case 'D': return FONT_D;
    case 'E': return FONT_E;
    case 'F': return FONT_F;
    case 'G': return FONT_G;
    case 'H': return FONT_H;
    case 'I': return FONT_I;
    case 'J': return FONT_J;
    case 'K': return FONT_K;
    case 'L': return FONT_L;
    case 'M': return FONT_M;
    case 'N': return FONT_N;
    case 'O': return FONT_O;
    case 'P': return FONT_P;
    case 'Q': return FONT_Q;
    case 'R': return FONT_R;
    case 'S': return FONT_S;
    case 'T': return FONT_T;
    case 'U': return FONT_U;
    case 'V': return FONT_V;
    case 'W': return FONT_W;
    case 'X': return FONT_X;
    case 'Y': return FONT_Y;
    case 'Z': return FONT_Z;
    case ' ': return FONT_SPACE;
    case ',': return FONT_COMMA;
    case '.': return FONT_DOT;
    case ':': return FONT_COLON;
    case ';': return FONT_SCOL;
    case '\'':return FONT_APO;
    default: return NULL;
  }
}

void writeChar(int x, int y, char ch, unsigned long* pframe){
  unsigned char *data = mapChar(ch);
  if(data == NULL) {
    Serial.println("NULL");
    return;
  }
  int xoff, yoff;
  xoff = 27 - x;
  bool lsf = true;
  if (xoff < 0) {
    lsf = false;
    xoff = xoff < -4 ? 4 : -1 * xoff;
  }
  else if (xoff > 27) xoff = 27;
  yoff = y;
  if (yoff < 0) yoff = 0;
  else if (yoff > 23) yoff = 23;
  for(int i = 0; i < 5; i++){ // for each row
    if(i + yoff > 23) break;

    unsigned long mask = 31; // 0b0...011111
    /**/
    if(lsf) mask = ~(mask << xoff);
    else mask = ~(mask >> xoff);
    pframe[yoff+i] &= mask; // clear
    /**/
    if(lsf) mask = ((unsigned long)data[i]) << xoff;
    else mask = ((unsigned long)data[i]) >> xoff;
    pframe[yoff+i] |= mask;
  }
}
void scrollLine(unsigned long* pframe, int upperLine, char* start, int scrollTime){
  char ch;
  for(int c = 0; (ch = start[c]) != '\0'; c++){ // for all char in start
    for(int i = 0; i < 5; i++){
      delay(scrollTime);
      for(int k = 0; k < 5; k++){
        pframe[upperLine + k] = pframe[upperLine + k] << 1;
      }
      writeChar(31-i, upperLine, ch, pframe);
      updateFrame(pframe);
    }
    delay(scrollTime);
    for(int k = 0; k < 5; k++){
        pframe[upperLine + k] = pframe[upperLine + k] << 1;
    }
    updateFrame(pframe);
  }
  for(int c = 0; c < 31; c++){
    delay(scrollTime);
    for(int k = 0; k < 5; k++){
        pframe[upperLine + k] = pframe[upperLine + k] << 1;
    }
    updateFrame(pframe);
  }
}
