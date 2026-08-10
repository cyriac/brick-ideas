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
    python extract_io_image.py --scan [root_dir]

--scan walks root_dir (default: script's directory) for .io files. For each:
  - if no <stem>_*.<img ext> thumbnail already sits next to it, extract one
  - if no .pdf sits next to it, report it as missing

If output_dir is omitted, the image is written next to the .io file.
"""

import sys
import zipfile
from pathlib import Path

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp"}
PDF_EXTS = {".pdf"}


def extract_image(io_path: str, output_dir: str | None = None) -> list[Path]:
    io_path = Path(io_path)
    if not io_path.exists():
        raise FileNotFoundError(f"No such file: {io_path}")

    out_dir = Path(output_dir) if output_dir else io_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    extracted = []

    with zipfile.ZipFile(io_path, "r") as zf:
        for name in zf.namelist():
            if Path(name).suffix.lower() in IMAGE_EXTS:
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


def has_thumbnail(io_path: Path) -> bool:
    return any(
        p.suffix.lower() in IMAGE_EXTS
        for p in io_path.parent.glob(f"{io_path.stem}_*")
    )


def has_instructions_pdf(io_path: Path) -> bool:
    return any(p.suffix.lower() in PDF_EXTS for p in io_path.parent.iterdir())


def scan(root_dir: str | None = None) -> None:
    root = Path(root_dir) if root_dir else Path(__file__).parent
    io_files = sorted(root.rglob("*.io"))

    if not io_files:
        print(f"No .io files found under {root}")
        return

    missing_pdfs = []

    for io_path in io_files:
        if has_thumbnail(io_path):
            print(f"[thumbnail ok] {io_path}")
        else:
            print(f"[thumbnail missing] {io_path} -> extracting")
            extract_image(str(io_path))

        if not has_instructions_pdf(io_path):
            missing_pdfs.append(io_path)

    if missing_pdfs:
        print("\nMissing instruction PDF:")
        for p in missing_pdfs:
            print(f"  {p}")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "--scan":
        scan(sys.argv[2] if len(sys.argv) > 2 else None)
    elif len(sys.argv) < 2:
        print("Usage: python extract_io_image.py <file.io> [output_dir]")
        print("       python extract_io_image.py --scan [root_dir]")
        sys.exit(1)
    else:
        io_file = sys.argv[1]
        out_dir = sys.argv[2] if len(sys.argv) > 2 else None
        extract_image(io_file, out_dir)
