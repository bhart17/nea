import eel
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(loader=FileSystemLoader("templates"),
                  autoescape=select_autoescape())

template = env.get_template("template.html")

eel.init("serve")

with open("serve/index.html", "w") as file:
    file.write(template.render(contents=[{
        "type": "col",
        "size": 1/3,
        "content": [{
            "type": "row",
            "size": 0.5,
            "content": [{
                "type": "colour",
                "colour": "red"
            }]
        }]
    }, {
        "type": "col",
        "size": 1/3,
        "content": [{
            "type": "colour",
            "colour": "blue"
        }]
    },{
        "type": "col",
        "size": 1/3,
        "content": [{
            "type": "colour",
            "colour": "blue"
        }]
    }]))

eel.start('index.html', cmdline_args=['--start-fullscreen'], block=False)

while True:
    eel.sleep(1.0)