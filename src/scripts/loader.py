from typing import Union
import requests
import json
import os


def load_config(assets_path) -> dict:
    with open(os.path.join(assets_path, "appconfig.json"), "r") as file:
        return json.load(file)


def load_content(assets_path: str) -> tuple[dict, int]:
    config = load_config(assets_path)
    response = make_request(config["ip"], config["layout"])
    if response:
        with open(os.path.join(assets_path, "content2.json"), "w") as file:
            file.write(response)
        return json.loads(response), config["refreshTime"]
    else:
        print("Warning: No response from server, using last retrieved layout")
        with open(os.path.join(assets_path, "content2.json"), "r") as file:
            return json.load(file), config["refreshTime"]


def make_request(ip: str, layout: str) -> Union[str, None]:
    try:
        response = requests.get(f"{ip}/layout/{layout}")
        if response.status_code == 200:
            return json.loads(response.text)["response"][0]
        else:
            return None
    except (requests.ConnectionError, requests.Timeout,
            requests.TooManyRedirects, requests.RequestException):
        print("Warning: Request could not be completed")
        return None


if __name__ == "__main__":
    print(json.loads(make_request("http://localhost:8080", "sixth-form")))
    print(json.loads(make_request("http://localhost:8080", "test")))
    #print(load_content("src/assets"))