import bluetooth
from ble_advertising import advertising_payload
from l298n import L298N
import time

motor_esq = L298N(in1=26, in2=25, ena=27)
motor_dir = L298N(in1=14, in2=12, ena=13)

vel_base = 60

def frente():
    print("Frente")
    motor_esq.speed(vel_base)
    motor_dir.speed(vel_base)

def tras():
    print("Ré")
    motor_esq.speed(-vel_base)
    motor_dir.speed(-vel_base)

def esquerda():
    print("Esquerda")
    motor_esq.speed(-vel_base)
    motor_dir.speed(vel_base)

def direita():
    print("Direita")
    motor_esq.speed(vel_base)
    motor_dir.speed(-vel_base)

def parar():
    print("Parar")
    motor_esq.stop()
    motor_dir.stop()

def turbo():
    global vel_base
    vel_base = 90
    print("Modo Turbo (90%)")

def normal():
    global vel_base
    vel_base = 60
    print("Velocidade Normal (60%)")

def lento():
    global vel_base
    vel_base = 30
    print("Modo Lento (40%)")

ble = bluetooth.BLE()
ble.active(True)

UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
UART_RX_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
UART_TX_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

UART_RX = (UART_RX_UUID, bluetooth.FLAG_WRITE)
UART_TX = (UART_TX_UUID, bluetooth.FLAG_NOTIFY)
UART_SERVICE = (UART_SERVICE_UUID, (UART_TX, UART_RX))

handles = bluetooth.BLE().gatts_register_services((UART_SERVICE,))
tx_handle, rx_handle = handles[0]

char_handle = rx_handle

def on_rx(event, data):
    if event == 3:  # _IRQ_GATTS_WRITE
        conn_handle, attr_handle = data
        if attr_handle == char_handle:
            msg = ble.gatts_read(char_handle).decode().strip()
            print("📨 Recebido:", msg)

            # Comandos do Bluefruit Control Pad
            if msg == "!B516":
                frente()
            elif msg == "!B615":
                tras()
            elif msg == "!B714":
                esquerda()
            elif msg == "!B813":
                direita()
            elif msg == "!B417":
                normal()
            elif msg == "!B219":
                turbo()
            elif msg == "!B318":  
                lento()
            else:
                parar()
                print("Comando desconhecido:", msg)

# -------------------------------
# Inicialização BLE
# -------------------------------
ble.irq(on_rx)
payload = advertising_payload(name="ESP32_BLUEFRUIT")
ble.gap_advertise(100, payload)

print("🔵 ESP32 pronto para conexão BLE!")
print("1 = Turbo (100%) | 2 = Normal (70%) | 3 = Lento (40%)")
