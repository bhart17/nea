import eel
from jinja2 import Environment, FileSystemLoader, select_autoescape
import sys
import os

import loader
from rss_parser import RssFeed, RssStatus


def main() -> None:
    content, refresh_time, env = start()

    while True:
        eel.sleep(refresh_time)
        new_content, refresh_time = loader.load_content(ASSETS_PATH)
        if content != new_content:
            content = new_content
            iter_content(content, env)
            eel.refresh()


def start() -> tuple[dict, int, Environment]:
    content, refresh_time = loader.load_content(ASSETS_PATH)

    env = Environment(loader=FileSystemLoader(
        os.path.join(ASSETS_PATH, "templates")),
                      autoescape=select_autoescape(enabled_extensions=()))

    iter_content(content, env)

    eel.init(SERVE_PATH)

    eel.start('cache/index.html',
              mode='custom',
              cmdline_args=[ELECTRON_PATH, '.'],
              block=False)

    return content, refresh_time, env


def iter_content(content, env):
    for i in content.keys():
        generate(env, f"{SERVE_PATH}/cache/{content[i][0]}", i, content[i][1])


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
    try:
        wd = sys._MEIPASS
        ELECTRON_PATH = os.path.join(wd, "electron/electron.AppImage")
        SERVE_PATH = os.path.join(wd, "serve")
        ASSETS_PATH = os.path.join(wd, "assets")
    except AttributeError:
        wd = os.getcwd()
        ASSETS_PATH = os.path.join(wd, "src/assets")
        SERVE_PATH = os.path.join(wd, "src/serve")
        ELECTRON_PATH = os.path.join(wd, "node_modules/electron/dist/electron")
    main()