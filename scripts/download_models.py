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

    # gdown supports shared Google Drive links directly and also works
    # as a general HTTP/HTTPS downloader. Avoid unsupported kwargs like
    # fuzzy in the Python API to keep compatibility with the installed version.
    result = gdown.download(url=url, output=output_path, quiet=False)
    if result is None or not os.path.exists(output_path):
        raise RuntimeError(f"Download failed for {url}")


def main():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    for res in config["resources"]:
        path = os.path.join(OUTPUT_DIR, res["filename"])
        download_file(res["url"], path)

    print("DONE")


if __name__ == "__main__":
    main()
