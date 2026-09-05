from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageFilter, ImageDraw

ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "assets" / "images" / "earrings"
BACKDROP = SOURCE_DIR / "earring-landscape-backdrop-v1.webp"
SOURCES = [
    "S__8839174_0-retouched.png", "S__8593462_0-retouched.png", "S__8839172_0-retouched.png",
    "S__8839173_0-retouched.png", "S__8839175_0-retouched.png", "S__8839176-retouched.png",
    "S__8593442-retouched.png", "S__8593444_0.jpg", "S__8593445_0-retouched.png",
    "S__8593446_0-retouched.png", "S__8593447_0-retouched.png", "S__8593448_0-retouched.png",
    "S__8593449_0-retouched.png", "S__8593450_0-retouched.png", "S__8593451_0-retouched.png",
    "S__8593452_0-retouched.png", "S__8593453_0-retouched.png", "S__8593455_0-retouched.png",
    "S__8593456_0-retouched.png", "S__8593457_0-retouched.png", "S__8593458_0-retouched.png",
    "S__8593459_0-retouched.png", "S__8593460_0-retouched.png", "S__8593461_0-retouched.png",
]

def output_name(source_name: str) -> str:
    return f"{Path(source_name).stem.replace('-retouched', '')}-landscape.webp"

def feathered_mask(size: tuple[int, int], radius: int = 72) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rectangle((radius, radius, size[0] - radius, size[1] - radius), fill=255)
    return mask.filter(ImageFilter.GaussianBlur(radius / 2))

def compose(source_path: Path, backdrop: Image.Image) -> Image.Image:
    source = Image.open(source_path).convert("RGB")
    source.thumbnail((1260, 980), Image.Resampling.LANCZOS)
    x = (backdrop.width - source.width) // 2
    y = (backdrop.height - source.height) // 2
    mask = feathered_mask(source.size)
    result = backdrop.convert("RGBA")
    shadow_layer = Image.new("RGBA", source.size, (56, 42, 30, 0))
    shadow_layer.putalpha(mask.filter(ImageFilter.GaussianBlur(18)).point(lambda p: int(p * 0.13)))
    shadow = Image.new("RGBA", backdrop.size, (0, 0, 0, 0))
    shadow.alpha_composite(shadow_layer, (x + 4, y + 12))
    result.alpha_composite(shadow)
    product_layer = Image.new("RGBA", backdrop.size, (0, 0, 0, 0))
    product_layer.paste(source, (x, y), mask)
    result.alpha_composite(product_layer)
    return result.convert("RGB")

def main() -> None:
    backdrop = Image.open(BACKDROP).convert("RGB")
    for name in SOURCES:
        source_path = SOURCE_DIR / name
        target = SOURCE_DIR / output_name(name)
        compose(source_path, backdrop).save(target, format="WEBP", quality=90, method=6)
        print(target.name)

if __name__ == "__main__":
    main()
