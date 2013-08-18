#include <SevenSeg.h>

SevenSeg disp(11,7,3,5,6,10,2);

const int numOfDigits=4;
int digitPins[numOfDigits]={12,9,8,13};
int cost1=0;
int cost2=0;
int cost3=0;
int cost4=0;

char cost[4] ={'0','0','0','0'};

void setup () {
  Serial.begin(9600);

  disp.setDigitPins(numOfDigits, digitPins);
  disp.setCommonAnode();
  disp.setDPPin(4);
  disp.setSymbPins(1,7,7,11);
  disp.setTimer(2);
  disp.startTimer();
  Serial.print("Starting up!");
  disp.write(cost);
}

void loop() {
  while(Serial.available() == 0) {
  }

  cost[0] = Serial.read();

  while(Serial.available() == 0) {
  }

  cost[1] = Serial.read();

  while(Serial.available() == 0) {
  }

  cost[2] = Serial.read();
  while(Serial.available() == 0) {
  }

  cost[3] = Serial.read();

  disp.write(cost);
}

ISR(TIMER2_COMPA_vect){
  disp.interruptAction();
}
