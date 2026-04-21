import os
import yaml
import gdown

CONFIG_PATH = "config/project.yaml"
OUTPUT_DIR = "models"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def download_file(url, output_path):
    if os.path.exists(output_path):
        print(f"[SKIP] {output_path}")
        return

    print(f"[DOWNLOAD] {url}")

    if "drive.google.com" in url:
        # gdown handles /file/d/.../view links, confirmation pages,
        # and large-file downloads more reliably than urllib.
        gdown.download(url=url, output=output_path, quiet=False, fuzzy=True)
    else:
        gdown.download(url=url, output=output_path, quiet=False, fuzzy=False)


def main():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    for res in config["resources"]:
        path = os.path.join(OUTPUT_DIR, res["filename"])
        download_file(res["url"], path)

    print("DONE")


if __name__ == "__main__":
    main()
