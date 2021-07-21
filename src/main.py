import eel
import jinja2

eel.init('web')

eel.start('html/index.html', cmdline_args=['--start-fullscreen'], block=False)

while True:
    eel.sleep(1.0)