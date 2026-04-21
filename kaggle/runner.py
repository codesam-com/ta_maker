import os
import subprocess
import time
import json
import base64
import io
from pathlib import Path
from PIL import Image

# Paths
REPO_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = REPO_ROOT / "models"
A1111_DIR = REPO_ROOT / "stable-diffusion-webui"
OUTPUT_DIR = REPO_ROOT / "outputs"


def run(cmd, cwd=None):
    print(f"[RUN] {cmd}")
    subprocess.run(cmd, shell=True, check=True, cwd=cwd)


def setup_environment():
    run("pip install --upgrade pip setuptools wheel")
    run("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
    run("pip install pillow pyyaml gdown requests")


def clone_a1111():
    if not A1111_DIR.exists():
        run("git clone --branch dev https://github.com/AUTOMATIC1111/stable-diffusion-webui.git")


def prepare_models():
    run("python scripts/download_models.py")

    (A1111_DIR / "models/Stable-diffusion").mkdir(parents=True, exist_ok=True)
    (A1111_DIR / "models/Lora").mkdir(parents=True, exist_ok=True)
    (A1111_DIR / "models/ESRGAN").mkdir(parents=True, exist_ok=True)

    run(f"cp models/lustify.safetensors {A1111_DIR}/models/Stable-diffusion/")
    run(f"cp models/more_details.safetensors {A1111_DIR}/models/Lora/")
    run(f"cp models/age_slider.safetensors {A1111_DIR}/models/Lora/")
    run(f"cp models/4x-UltraSharp.pth {A1111_DIR}/models/ESRGAN/")


def start_a1111():
    cmd = (
        "python launch.py --api --skip-torch-cuda-test --xformers "
        "--no-half-vae"
    )
    subprocess.Popen(cmd, shell=True, cwd=A1111_DIR)

    print("[WAIT] Waiting for A1111 API...")
    import requests
    while True:
        try:
            requests.get("http://127.0.0.1:7860/sdapi/v1/samplers")
            break
        except Exception:
            time.sleep(5)
    print("[OK] A1111 ready")


def generate():
    from generation.build_payload import parse_control_panel

    payload = parse_control_panel()

    import requests

    response = requests.post(
        "http://127.0.0.1:7860/sdapi/v1/txt2img",
        json=payload
    )

    data = response.json()

    img = base64.b64decode(data["images"][0])
    image = Image.open(io.BytesIO(img))

    OUTPUT_DIR.mkdir(exist_ok=True)
    image.save(OUTPUT_DIR / "generated.png")

    print("[DONE] Image generated")


def main():
    setup_environment()
    clone_a1111()
    prepare_models()
    start_a1111()
    generate()


if __name__ == "__main__":
    main()
