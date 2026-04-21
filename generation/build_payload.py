import re
from pathlib import Path

CONTROL_PANEL_PATH = "target_image-control_panel.txt"


def extract_between(text, start, end):
    pattern = re.escape(start) + r"(.*?)" + re.escape(end)
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""


def extract_value(text, label):
    pattern = re.escape(label) + r"\s*:\s*(.*)"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None


def parse_loras(text):
    loras = []
    blocks = re.findall(r"\* LoRA \d+:\n\t\*\* (.*?)\n\t\*\* Peso: (.*?)\n", text)
    for name, weight in blocks:
        loras.append((name.strip(), float(weight.strip())))
    return loras


def build_lora_prompt(loras):
    parts = []
    for name, weight in loras:
        filename = name.split('|')[0].strip().replace(' ', '_').lower()
        parts.append(f"<lora:{filename}:{weight}>")
    return " ".join(parts)


def parse_control_panel(path=CONTROL_PANEL_PATH):
    txt = Path(path).read_text(encoding="utf-8")

    prompt = extract_between(txt, "### Prompt", "---")
    negative_prompt = extract_between(txt, "### Prompt negativo", "---")

    steps = int(extract_value(txt, "Pasos de Sampleo"))
    cfg = float(extract_value(txt, "Escala CFG"))
    seed = int(extract_value(txt, "Semilla"))

    sampler = extract_value(txt, "Sampler")
    scheduler = extract_value(txt, "Planificador")

    sampler_name = f"{sampler} {scheduler}".replace("dpmpp_sde_gpu", "DPM++ SDE").replace("karras", "Karras")

    width = int(re.search(r"(\d+)x(\d+)", txt).group(1))
    height = int(re.search(r"(\d+)x(\d+)", txt).group(2))

    hr_width = int(extract_value(txt, "Redimensionar Anchura"))
    hr_height = int(extract_value(txt, "Redimensionar Altura"))

    clip_skip = int(extract_value(txt, "Clip Skip"))
    ensd = int(extract_value(txt, "ENSD"))

    hr_steps = int(extract_value(txt, "Etapas de Upscaling"))
    denoise = float(extract_value(txt, "Fuerza de Denoising"))

    loras = parse_loras(txt)
    lora_prompt = build_lora_prompt(loras)

    full_prompt = f"{lora_prompt} {prompt}".strip()

    return {
        "prompt": full_prompt,
        "negative_prompt": negative_prompt,
        "steps": steps,
        "cfg_scale": cfg,
        "width": width,
        "height": height,
        "sampler_name": sampler_name,
        "seed": seed,
        "override_settings": {
            "CLIP_stop_at_last_layers": clip_skip,
            "eta_noise_seed_delta": ensd
        },
        "enable_hr": True,
        "hr_resize_x": hr_width,
        "hr_resize_y": hr_height,
        "hr_upscaler": "4x-UltraSharp",
        "hr_second_pass_steps": hr_steps,
        "denoising_strength": denoise
    }


if __name__ == "__main__":
    payload = parse_control_panel()
    import json
    print(json.dumps(payload, indent=2, ensure_ascii=False))
