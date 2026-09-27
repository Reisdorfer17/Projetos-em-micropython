from machine import Pin, PWM

class L298N:
    def __init__(self, in1, in2, ena, freq=1000):
        # Configura pinos de direção e PWM
        self.in1 = Pin(in1, Pin.OUT)
        self.in2 = Pin(in2, Pin.OUT)
        self.pwm = PWM(Pin(ena), freq=freq)
        self.pwm.duty_u16(0)
        self.velocidade = 0

    def speed(self, velocidade):
        """
        Define a velocidade do motor.
        velocidade: -100 a 100 (%)
        """
        velocidade = max(-100, min(100, velocidade))
        self.velocidade = velocidade

        if velocidade > 0:
            self.in1.value(1)
            self.in2.value(0)
            duty = int((velocidade / 100) * 65535)
        elif velocidade < 0:
            self.in1.value(0)
            self.in2.value(1)
            duty = int((abs(velocidade) / 100) * 65535)
        else:
            self.stop()
            return

        self.pwm.duty_u16(duty)

    def stop(self):
        """Para o motor completamente."""
        self.in1.value(0)
        self.in2.value(0)
        self.pwm.duty_u16(0)
