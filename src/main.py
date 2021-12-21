import eel
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json


def main() -> None:
    SERVE_PATH = "serve"

    with open("src/content.json", "r") as file:
        content = json.load(file)

    env = Environment(loader=FileSystemLoader("src/templates"),
                      autoescape=select_autoescape(enabled_extensions=()))

    for i in content.keys():
        generate(env, f"{SERVE_PATH}/cache/" + content[i][0], i, content[i][1])

    eel.init(SERVE_PATH)

    eel.start('cache/index.html',
              cmdline_args=["--start-fullscreen"],
              block=False)

    while True:
        eel.sleep(1)


def generate(env, file_p, template_p, contents) -> None:
    template = env.get_template(template_p)
    with open(file_p, "w") as file:
        file.write(template.render(contents=contents))


def make_contents() -> dict:
    return {}


if __name__ == "__main__":
    main()