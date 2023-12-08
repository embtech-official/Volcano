from pathlib import Path
import time


pwmchip0_dir = Path('/sys/class/pwm/pwmchip0')
pww0_dir = pwmchip0_dir / 'pwm0'



if not pww0_dir.exists():
    export = open((pwmchip0_dir / 'export'), 'w' ,buffering=1)
    export.write('0\n')
    export.flush()
    export.close()

    if not pwmchip0_dir.exists():
        print("Couldn\t export pwmchip0")
        exit()

duty_cycle = pww0_dir / 'duty_cycle'
period = pww0_dir / 'period'
enable = pww0_dir / 'enable'

with open(duty_cycle, 'w', buffering=1) as pwm_duty_cycle,\
    open(enable,'w',buffering=1) as pwm_enable,\
    open(period,'w',buffering=1) as pwm_period:

    pwm_period.write("2000000\n")
    pwm_duty_cycle.write("1000000\n")

    pwm_enable.write("1\n")

    time.sleep(1)

    pwm_period.write("1000000\n")
    pwm_duty_cycle.write("500000\n")

    time.sleep(1)

    pwm_period.write("3000000\n")
    pwm_duty_cycle.write("1500000\n")

    time.sleep(1)

    pwm_enable.write("0\n")


