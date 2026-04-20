import os
import yaml
import urllib.request

CONFIG_PATH = "config/project.yaml"
OUTPUT_DIR = "models"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def download_file(url, output_path):
    if os.path.exists(output_path):
        print(f"[SKIP] {output_path}")
        return

    print(f"[DOWNLOAD] {url}")

    if "drive.google.com" in url:
        if "/d/" in url:
            file_id = url.split("/d/")[1].split("/")[0]
        elif "id=" in url:
            file_id = url.split("id=")[1].split("&")[0]
        else:
            raise ValueError("Invalid Google Drive URL")

        url = f"https://drive.google.com/uc?export=download&id={file_id}"

    urllib.request.urlretrieve(url, output_path)


def main():
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    for res in config["resources"]:
        path = os.path.join(OUTPUT_DIR, res["filename"])
        download_file(res["url"], path)

    print("DONE")


if __name__ == "__main__":
    main()
