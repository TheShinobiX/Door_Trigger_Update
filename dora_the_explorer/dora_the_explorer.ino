int ldr=A1;//Set A0(Analog Input) for LDR.
int led_pin=3;
int value=0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(led_pin,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  value=analogRead(ldr);//Reads the Value of LDR(light).

  // If light level is dim
  if(value<100)
  {
    digitalWrite(led_pin,LOW);//Makes the LED off when door is CLOSED.
    Serial.println(0);//Print to serial that door is CLOSED with code 0.
  }
  
  // If light level is higher
  else
  {
    digitalWrite(led_pin,HIGH);//Turns the LED glow when door is OPEN.
    Serial.println(1);//Print to serial that door is OPEN with code 1.
  }
}
