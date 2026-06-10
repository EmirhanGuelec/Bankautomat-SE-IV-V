from fastapi import FastAPI
from GPIO import RPIO.GPIO
GPIO.setmode(BCM)
GPIO.setup(13,OUT)
GPIO.setup(12,OUT)
GPIO.setup(14,OUT)

app = FastAPI()

@app.post("/coin")
async def pusha(coin: int):
    if coin==2:
        GPIO.output(13,HIGH)
        
    return "success "+ str(coin)

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)



def berechne_muenzen(betrag):
	ein_euro = 1
	
	rest = betrag - ein_euro
	zwei_euro = rest // 2
	
	fuenfzig_cent = (rest % 2) * 2

	return ein_euro, zwei_euro, fuenfzig_cent

    motor(17, ein_euro)
    motor(27, zwei_euro)
    motor(7, fuenfzig_cent)

def motor(pin, anzahl):
    x = 0
    while x < anzahl and anzahl != 0:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.5)
        x += 1

def auzahlen(betrag):
    muenzen = berechne_muenzen(betrag)
    for i in range(muenzen1):

