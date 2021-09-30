import eel
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(loader=FileSystemLoader("src/templates"),
                  autoescape=select_autoescape())

template = env.get_template("template.tmpl")

eel.init("serve")

with open("serve/cache/index.html", "w") as file:
    file.write(
        template.render(
            contents=[{
                "type": "col",
                "size": 1 / 3,
                "content": [{
                    "type": "row",
                    "size": 0.5,
                    "content": [{
                        "type": "colour",
                        "content": "red"
                    }]
                }, {
                    "type": "row",
                    "size": 0.5,
                    "content": [{
                        "type": "text",
                        "content": "hello"
                    }]
                }]
            }, {
                "type": "col",
                "size": 1 / 3,
                "content": [{
                    "type": "colour",
                    "content": "blue"
                }]
            }, {
                "type": "col",
                "size": 1 / 3,
                "content": [{
                    "type": "colour",
                    "content": "blue"
                }]
            }]))

eel.start('cache/index.html', cmdline_args=['--start-fullscreen'], block=False)

while True:
    eel.sleep(1.0)