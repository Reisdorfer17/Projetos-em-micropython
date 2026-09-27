import network
import espnow
from machine import Pin
from time import sleep
from l298n import L298N

motor_esq = L298N(in1=26, in2=25, ena=27)
motor_dir = L298N(in1=14, in2=12, ena=13)

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

e = espnow.ESPNow()
e.active(True)

led = Pin(2, Pin.OUT)

print("ESP32 escravo pronto")
print("MAC:", ':'.join('{:02X}'.format(b) for b in wifi.config('mac')))

vel_dir=0
vel_esq=0

while True:
    led.on()
    try:
        host, msg = e.recv()

        if msg:
            texto = msg.decode()
            print("Recebido:", texto)

            valores = texto.split(",")
        
            vel_dir=int(valores[0])
            vel_esq=int(valores[1])
        
            print(vel_dir, vel_esq)
        else:
        
            vel_dir=0
            vel_esq=0
        
            motor_esq.stop()
            motor_dir.stop()

        motor_esq.speed(vel_esq)
        motor_dir.speed(vel_dir)
        sleep(0.1)
    except:
        sleep(0.1)
        led.on()
        sleep(2)
        led.off()
    led.off()
