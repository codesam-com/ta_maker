import re
from pathlib import Path

CONTROL_PANEL_PATH = "target_image-control_panel.txt"


def extract_between(text, start, end):
    pattern = re.escape(start) + r"(.*?)" + re.escape(end)
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""


def parse_control_panel(path=CONTROL_PANEL_PATH):
    txt = Path(path).read_text(encoding="utf-8")

    prompt = extract_between(txt, "### Prompt", "---")
    negative_prompt = extract_between(txt, "### Prompt negativo", "---")

    width, height = 768, 1152
    hr_width, hr_height = 1024, 1536

    return {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "steps": 25,
        "cfg_scale": 4.5,
        "width": width,
        "height": height,
        "sampler_name": "DPM++ SDE Karras",
        "seed": 2356449947,
        "override_settings": {
            "CLIP_stop_at_last_layers": 1,
            "eta_noise_seed_delta": 31337
        },
        "enable_hr": True,
        "hr_resize_x": hr_width,
        "hr_resize_y": hr_height,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": 25,
        "denoising_strength": 0.35
    }


if __name__ == "__main__":
    payload = parse_control_panel()
    import json
    print(json.dumps(payload, indent=2, ensure_ascii=False))
