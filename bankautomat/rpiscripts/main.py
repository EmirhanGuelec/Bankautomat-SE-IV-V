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
