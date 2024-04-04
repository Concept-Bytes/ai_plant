from gpiozero import LightSensor, Buzzer

ldr = LightSensor(4)  # alter if using a different pin
while True:
    print(ldr.value)