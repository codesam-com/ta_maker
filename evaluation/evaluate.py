import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim
from pathlib import Path

TARGET_PATH = Path("target_image.png")
GENERATED_PATH = Path("outputs/generated.png")


def load_image(path):
    img = Image.open(path).convert("RGB")
    return np.array(img)


def compute_ssim(img1, img2):
    # Convert to grayscale for SSIM simplicity
    from skimage.color import rgb2gray
    g1 = rgb2gray(img1)
    g2 = rgb2gray(img2)
    score, _ = ssim(g1, g2, full=True)
    return score


def pixel_diff(img1, img2):
    return np.mean(np.abs(img1.astype("float") - img2.astype("float")))


def evaluate():
    if not TARGET_PATH.exists():
        raise FileNotFoundError("target_image.png not found")
    if not GENERATED_PATH.exists():
        raise FileNotFoundError("generated image not found")

    img1 = load_image(TARGET_PATH)
    img2 = load_image(GENERATED_PATH)

    if img1.shape != img2.shape:
        raise ValueError(f"Shape mismatch: {img1.shape} vs {img2.shape}")

    ssim_score = compute_ssim(img1, img2)
    diff = pixel_diff(img1, img2)

    result = {
        "ssim": float(ssim_score),
        "pixel_diff": float(diff)
    }

    print(result)
    return result


if __name__ == "__main__":
    evaluate()
