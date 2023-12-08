import gpiod
import time

try:
    gpiochip = gpiod.chip('gpiochip2')
    config_output = gpiod.line_request()
    config_output.request_type = gpiod.line_request.DIRECTION_OUTPUT
    led = gpiochip.get_line(0)
    led.request(config_output)
    while True :
        print("LED ON")
        led.set_value(1)
        time.sleep(1)
        print("LED OFF")
        led.set_value(0)
        time.sleep(1)
except:
    print("Led except")
