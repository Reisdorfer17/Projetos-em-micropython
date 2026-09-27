import network
import espnow
from machine import Pin, ADC
from time import sleep

eixo_x = ADC(Pin(35))
eixo_y = ADC(Pin(34))


eixo_x.atten(ADC.ATTN_11DB)
eixo_y.atten(ADC.ATTN_11DB)


eixo_x.width(ADC.WIDTH_12BIT)
eixo_y.width(ADC.WIDTH_12BIT)

# Botão do joystick
botao = Pin(4, Pin.IN, Pin.PULL_UP)

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

e = espnow.ESPNow()
e.active(True)

# MAC do ESP32 escravo/receptor MAC: 08:D1:F9:E0:2D:E0
peer = b'\x08\xD1\xF9\xE0\x2D\xE0'

e.add_peer(peer)

mensagem = 1
print("FOI")
while True:
    x = eixo_x.read()
    y = eixo_y.read()
    sw = botao.value()
    x = int((x/40.95 - 50)*2)
    y = int((y/40.95 - 50)*2)
    print(x, y, sw)
    vel_dir = min(100, max(x - y, -100))
    vel_esq = min(100, max(x + y, -100))
    print(f'Velocidade direita: {vel_dir}, velocidade esquerda: {vel_esq}')
    
    mensagem = f"{vel_dir},{vel_esq}"
    
    e.send(peer, mensagem)

    print("Enviado:", mensagem)

    sleep(0.2)