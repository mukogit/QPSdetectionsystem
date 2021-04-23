int v1; //voltage at S@$_1$@
int v2; //voltage at S@$_2$@
char data[18];
int trigger = 0;
int trigger_in = 7;
int trigger_out = 8;
unsigned long time;                                                // microsecond timer
unsigned long Notch;

void setup() {
    Serial.begin(2000000); 	  //baud rate
    analogReadResolution(12); //12-bit res.

    pinMode(A1, INPUT);
    pinMode(A2, INPUT);
    pinMode(trigger_in, INPUT);
    pinMode(trigger_out, OUTPUT);
}

bool Delay(unsigned long dtime) {
    unsigned long rt = micros();
    if (abs(rt - Notch) > dtime ) {
        Notch = rt;
        return true;
    }
    else return false;
}  
  
void loop() {
    trigger = digitalRead(trigger_in);
    
    if (trigger == HIGH) {
        digitalWrite(trigger_out, HIGH);
    }
    
    time = (int) micros(); //get time in µs
    
    if (Delay(200)) {
        v1 = analogRead(A1);
        v2 = analogRead(A2);
        sprintf(data, "%09i%04i%04i", time, v1, v2);
    }
    
    if (trigger == HIGH) {    
        Serial.println(data); //send data
        for(int i = 0; i < 18;  ++i ) {
    	    data[i] = (char)0;
        }
        Serial.flush();
    }
}
