import eel
from jinja2 import Environment, FileSystemLoader, select_autoescape


def main() -> None:
    content = {
        "template-html.j2": [
            "index.html",
            [{
                "type":
                "col",
                "size":
                1 / 3,
                "content": [{
                    "type":
                    "row",
                    "size":
                    0.5,
                    "content": [{
                        "type":
                        "scrolling",
                        "content":
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Mattis rhoncus urna neque viverra justo nec ultrices dui. Nunc mattis enim ut tellus elementum sagittis vitae et. Libero enim sed faucibus turpis in. In mollis nunc sed id semper. Fringilla ut morbi tincidunt augue. Nisl nisi scelerisque eu ultrices vitae auctor. Curabitur vitae nunc sed velit dignissim sodales. Dui vivamus arcu felis bibendum ut tristique et egestas quis. At erat pellentesque adipiscing commodo. Facilisi nullam vehicula ipsum a arcu cursus vitae. Euismod lacinia at quis risus sed vulputate odio ut. Pellentesque nec nam aliquam sem. Tortor at auctor urna nunc id cursus metus. Diam in arcu cursus euismod quis viverra nibh cras pulvinar. In aliquam sem fringilla ut morbi tincidunt. Consequat mauris nunc congue nisi. Cursus turpis massa tincidunt dui ut. Augue eget arcu dictum varius duis at consectetur lorem. Sapien eget mi proin sed libero enim sed faucibus turpis. Urna duis convallis convallis tellus id interdum velit laoreet. Commodo odio aenean sed adipiscing. At imperdiet dui accumsan sit amet nulla. Commodo ullamcorper a lacus vestibulum sed arcu. Varius quam quisque id diam. Ac turpis egestas integer eget. Elementum curabitur vitae nunc sed velit dignissim sodales. Sem et tortor consequat id porta nibh venenatis. Tincidunt dui ut ornare lectus sit amet. Pretium fusce id velit ut tortor pretium viverra suspendisse. Ornare massa eget egestas purus viverra. Volutpat ac tincidunt vitae semper quis. Pharetra sit amet aliquam id diam maecenas. Elementum integer enim neque volutpat ac tincidunt. Imperdiet massa tincidunt nunc pulvinar sapien et ligula ullamcorper malesuada. Duis at consectetur lorem donec massa sapien faucibus et molestie. Potenti nullam ac tortor vitae purus faucibus ornare suspendisse sed. Sagittis purus sit amet volutpat consequat mauris nunc congue. Mus mauris vitae ultricies leo integer malesuada nunc vel risus. Euismod quis viverra nibh cras pulvinar mattis nunc sed blandit. Duis tristique sollicitudin nibh sit amet. Amet massa vitae tortor condimentum lacinia quis. Sociis natoque penatibus et magnis. Pellentesque pulvinar pellentesque habitant morbi tristique. Facilisis leo vel fringilla est ullamcorper eget. Ac felis donec et odio pellentesque diam volutpat. Purus sit amet volutpat consequat. Facilisis magna etiam tempor orci eu lobortis elementum. Facilisi morbi tempus iaculis urna id volutpat lacus laoreet. Diam volutpat commodo sed egestas egestas. Tellus orci ac auctor augue mauris augue neque gravida. Auctor neque vitae tempus quam pellentesque nec nam aliquam. Lectus quam id leo in vitae turpis massa sed elementum. Commodo quis imperdiet massa tincidunt nunc pulvinar sapien. Tempor commodo ullamcorper a lacus vestibulum sed arcu. In nisl nisi scelerisque eu ultrices vitae. Laoreet suspendisse interdum consectetur libero id faucibus nisl tincidunt. Nibh sit amet commodo nulla facilisi nullam vehicula. Nisi quis eleifend quam adipiscing vitae proin sagittis. Faucibus vitae aliquet nec ullamcorper. Enim nulla aliquet porttitor lacus luctus accumsan tortor. Gravida cum sociis natoque penatibus. Commodo ullamcorper a lacus vestibulum sed arcu non odio. Ut tortor pretium viverra suspendisse potenti nullam ac. Convallis convallis tellus id interdum velit laoreet id donec ultrices. Tincidunt praesent semper feugiat nibh sed pulvinar proin. Aliquam vestibulum morbi blandit cursus risus at. Libero justo laoreet sit amet. Duis at tellus at urna condimentum. Eget arcu dictum varius duis at. Diam sollicitudin tempor id eu nisl. Diam quis enim lobortis scelerisque fermentum dui faucibus in ornare. Posuere lorem ipsum dolor sit amet. Augue ut lectus arcu bibendum. Faucibus scelerisque eleifend donec pretium vulputate sapien. Morbi tempus iaculis urna id volutpat lacus laoreet non. Elementum sagittis vitae et leo. Turpis egestas pretium aenean pharetra magna. Tristique magna sit amet purus gravida quis blandit. Turpis massa sed elementum tempus egestas sed. Tincidunt ornare massa eget egestas. Faucibus interdum posuere lorem ipsum dolor sit. Ultrices mi tempus imperdiet nulla malesuada pellentesque. Nunc eget lorem dolor sed viverra. Fringilla urna porttitor rhoncus dolor. Faucibus a pellentesque sit amet porttitor eget dolor. Id eu nisl nunc mi ipsum faucibus vitae aliquet. Vitae purus faucibus ornare suspendisse sed nisi lacus sed viverra. Urna molestie at elementum eu facilisis sed."
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
                "type":
                "col",
                "size":
                1 / 3,
                "content": [{
                    "type": "slideshow",
                    "content": ["tom.jpg", "tom.jpg", "tom.jpg"]
                }]
            }, {
                "type":
                "col",
                "size":
                1 / 3,
                "content": [{
                    "type": "slideshow",
                    "content": ["tom.jpg", "tom.jpg", "tom.jpg"]
                }]
            }]
        ],
        "template.css": ["styles.css", []]
    }

    env = Environment(loader=FileSystemLoader("src/templates"),
                      autoescape=select_autoescape(enabled_extensions=()))

    for i in content.keys():
        generate(env, "serve/cache/" + content[i][0], i, content[i][1])

    eel.init("serve")

    eel.start('cache/index.html',
              cmdline_args=["--start-fullscreen"],
              block=False)

    while True:
        eel.sleep(1.0)


def generate(env, file_p, template_p, contents) -> None:
    template = env.get_template(template_p)
    with open(file_p, "w") as file:
        file.write(template.render(contents=contents))


if __name__ == "__main__":
    main()