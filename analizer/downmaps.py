import os

import requests

MAP_URLS: dict[str, str] = {
    "ascent": "https://media.valorant-api.com/maps/7eaecc1b-4337-bbf6-6ab9-04b8f06b3319/displayicon.png",
    "bind": "https://media.valorant-api.com/maps/2c9d57ec-4431-9c5e-2939-8f9ef6dd5cba/displayicon.png",
    "haven": "https://media.valorant-api.com/maps/2bee0dc9-4ffe-519b-1cbd-7fbe763a6047/displayicon.png",
    "split": "https://media.valorant-api.com/maps/d960549e-485c-e861-8d71-aa9d1aed12a2/displayicon.png",
    "icebox": "https://media.valorant-api.com/maps/e2ad5c54-4114-a870-9641-8ea21279579a/displayicon.png",
    "breeze": "https://media.valorant-api.com/maps/2fb9a4fd-47b8-4e7d-a969-74b4046ebd53/displayicon.png",
    "fracture": "https://media.valorant-api.com/maps/b529448b-4d60-346e-e89e-00a4c527a405/displayicon.png",
    "pearl": "https://media.valorant-api.com/maps/fd267378-4d1d-484f-ff52-77821ed10dc2/displayicon.png",
    "lotus": "https://media.valorant-api.com/maps/2fe4ed3a-450a-948b-6d6b-e89a78e680a9/displayicon.png",
    "sunset": "https://media.valorant-api.com/maps/92584fbe-486a-b1b2-9faa-39b0f486b498/displayicon.png",
    "abyss": "https://media.valorant-api.com/maps/224b0a95-48b9-f703-1bd8-67aca101a61f/displayicon.png"
}


class ImageDownloader:
    def __init__(self, urls: dict[str, str], folder: str = "analizer/src/assets/maps"
) -> None:
        self.urls = urls
        self.folder = folder

    def download_images(self) -> None:
        for key, url in self.urls.items():
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    with open(os.path.join(self.folder, f"{key}.png"), "wb") as f:
                        f.write(response.content)
                    print(f"✅\033[32mDownloaded {key}.png\033[0m")
                else:
                    print(f"\033[31mFailed to download {key}.png. Status code: {response.status_code}\033[0m")
            except requests.exceptions.RequestException as e:
                print(f"⚠\033[31mFailed to download {key}.png. Error: {e}\033[0m")


downloader = ImageDownloader(MAP_URLS)
downloader.download_images()
print("\033[36m- Base maps updated! -\033[0m")