import eel
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from rss_parser import RssFeed, RssStatus


def main() -> None:
    SERVE_PATH = "serve"

    content = load_content()

    env = Environment(loader=FileSystemLoader("templates"),
                      autoescape=select_autoescape(enabled_extensions=()))

    for i in content.keys():
        generate(env, f"{SERVE_PATH}/cache/{content[i][0]}", i, content[i][1])

    eel.init(SERVE_PATH)

    eel.start(
        'cache/index.html',
        #   mode="chrome",
        #   cmdline_args=[
        #       "--start-fullscreen",
        #       "--autoplay-policy=no-user-gesture-required"
        #   ],
        mode='custom',
        cmdline_args=['node_modules/electron/dist/electron', '.'],
        block=False)

    while True:
        eel.sleep(1)


def load_content() -> dict:
    with open("content.json", "r") as file:
        return json.load(file)


def generate(env: Environment, fp: str, tp: str, contents: list) -> None:
    template = env.get_template(tp)
    with open(fp, "w") as file:
        file.write(template.render(contents=contents))


@eel.expose
def fetch_rss(url: str, tags: list[str], max_items: int) -> list:
    rss = RssFeed(url)
    if (status := rss.get_status()) == RssStatus.GOOD:
        feed = rss.get_items(tags, max_items)
        if feed != RssStatus.INVALID_TAG:
            return feed
        status = RssStatus.INVALID_TAG
    return [status.value]


if __name__ == "__main__":
    main()