import gpiod

try:
    gpiochip = gpiod.chip('gpiochip2')
    config_input = gpiod.line_request()

    #Button declaration
    config_input.request_type = gpiod.line_request.DIRECTION_INPUT
    btn = gpiochip.get_line(1)
    btn.request(config_input)

    #Led declaration
    config_input.request_type = gpiod.line_request.DIRECTION_OUTPUT
    led = gpiochip.get_line(0)
    led.request(config_input)

    while True:
        if(btn.get_value() == 0) :
            led.set_value(1)
        else:
            led.set_value(0)

except:
    print("button except")
