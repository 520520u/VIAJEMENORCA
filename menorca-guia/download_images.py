#!/usr/bin/env python3
"""Descarga extras de Wikimedia a menorca-guia/images/."""
import time
import urllib.request
from pathlib import Path

from images_data import REMOTE

OUT = Path(__file__).parent / "images"
UA = "MenorcaGuia/1.0 (https://github.com/520520u/VIAJEMENORCA)"


def main():
    OUT.mkdir(exist_ok=True)
    ok = 0
    for name, url in REMOTE.items():
        dest = OUT / name
        if dest.exists() and dest.stat().st_size > 500:
            ok += 1
            continue
        print(f"↓ {name}")
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                dest.write_bytes(r.read())
            ok += 1
        except Exception as e:
            print(f"  ERROR: {e}")
        time.sleep(0.6)
    # miniaturas
    try:
        from PIL import Image
        for f in OUT.glob("*.jpg"):
            thumb = f.with_name(f.stem + "_thumb.jpg")
            if thumb.exists():
                continue
            im = Image.open(f)
            if im.mode in ("RGBA", "P"):
                im = im.convert("RGB")
            im.thumbnail((960, 960), Image.Resampling.LANCZOS)
            im.save(thumb, optimize=True, quality=82)
        for f in OUT.glob("*.jpeg"):
            thumb = f.with_name(f.stem + "_thumb.jpeg")
            if thumb.exists():
                continue
            im = Image.open(f)
            im.thumbnail((960, 960), Image.Resampling.LANCZOS)
            im.save(thumb, optimize=True, quality=82)
    except ImportError:
        import subprocess
        for f in OUT.glob("*"):
            if "_thumb" in f.name or f.suffix.lower() not in (".jpg", ".jpeg"):
                continue
            thumb = f.with_name(f.stem + "_thumb" + f.suffix)
            if not thumb.exists():
                subprocess.run(["sips", "-Z", "960", str(f), "--out", str(thumb)], check=False)
    print(f"OK {ok}/{len(REMOTE)} → {OUT}")


if __name__ == "__main__":
    main()
