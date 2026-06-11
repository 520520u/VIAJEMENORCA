#!/usr/bin/env python3
"""Copia la guía generada a menorca-pwa/ (incluye imágenes locales)."""
import shutil
from pathlib import Path

BASE = Path(__file__).parent.resolve()
ROOT = BASE.parent
TARGET = ROOT / "menorca-pwa"


def main():
    html = (BASE / "index.html").read_text(encoding="utf-8")
    TARGET.mkdir(exist_ok=True)
    (TARGET / "index.html").write_text(html, encoding="utf-8")
    src_img = BASE / "images"
    if src_img.is_dir():
        dst = TARGET / "images"
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src_img, dst)
    sw = TARGET / "sw.js"
    if sw.exists():
        sw.write_text(sw.read_text(encoding="utf-8").replace("menorca-guia-v8", "menorca-guia-v9"), encoding="utf-8")
    print("PWA:", TARGET)


if __name__ == "__main__":
    main()
