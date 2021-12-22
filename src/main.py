import eel
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json


def main() -> None:
    SERVE_PATH = "serve"

    content = load_content()

    env = Environment(loader=FileSystemLoader("src/templates"),
                      autoescape=select_autoescape(enabled_extensions=()))

    for i in content.keys():
        generate(env, f"{SERVE_PATH}/cache/{content[i][0]}", i, content[i][1])

    eel.init(SERVE_PATH)

    eel.start('cache/index.html',
              cmdline_args=["--start-fullscreen"],
              block=False)

    while True:
        eel.sleep(1)


def load_content() -> dict:
    with open("src/content.json", "r") as file:
        return json.load(file)


def generate(env, fp, tp, contents) -> None:
    template = env.get_template(tp)
    with open(fp, "w") as file:
        file.write(template.render(contents=contents))


if __name__ == "__main__":
    main()