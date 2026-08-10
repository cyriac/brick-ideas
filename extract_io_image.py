#!/usr/bin/env python3
"""
Extract the embedded preview image from a BrickLink Studio (.io) file.

A .io file is just a ZIP archive. It typically contains:
  - model.ldr / modelv2.ldr / model2.ldr  (LDraw geometry)
  - model.lxfml                            (legacy LXF metadata)
  - thumbnail.png                          (the preview image)
  - errorPartList.err, .info               (misc metadata)

Usage:
    python extract_io_image.py path/to/model.io [output_dir]

If output_dir is omitted, the image is written next to the .io file.
"""

import sys
import zipfile
from pathlib import Path


def extract_image(io_path: str, output_dir: str | None = None) -> list[Path]:
    io_path = Path(io_path)
    if not io_path.exists():
        raise FileNotFoundError(f"No such file: {io_path}")

    out_dir = Path(output_dir) if output_dir else io_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    image_exts = {".png", ".jpg", ".jpeg", ".bmp"}
    extracted = []

    with zipfile.ZipFile(io_path, "r") as zf:
        for name in zf.namelist():
            if Path(name).suffix.lower() in image_exts:
                data = zf.read(name)
                out_path = out_dir / f"{io_path.stem}_{Path(name).name}"
                out_path.write_bytes(data)
                extracted.append(out_path)

    if not extracted:
        print(f"No image found inside {io_path.name}. "
              f"Contents were: {zf.namelist()}")
    else:
        for p in extracted:
            print(f"Extracted: {p}")

    return extracted


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_io_image.py <file.io> [output_dir]")
        sys.exit(1)

    io_file = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else None
    extract_image(io_file, out_dir)
