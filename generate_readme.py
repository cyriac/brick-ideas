#!/usr/bin/env python3
"""
Regenerate the build table in README.md between the
<!-- BUILDS:START --> / <!-- BUILDS:END --> markers.

A directory counts as a "complete" build if it has at least one
.io, one .png (thumbnail), and one .pdf file. Incomplete builds
(missing pdf, e.g. work-in-progress) are skipped and reported.

Usage: python generate_readme.py [root_dir]
"""
import sys
from pathlib import Path

SKIP_DIRS = {".git", ".github", "__pycache__"}
START = "<!-- BUILDS:START -->"
END = "<!-- BUILDS:END -->"


def find_builds(root: Path):
    complete = []
    incomplete = []
    for d in sorted(p for p in root.iterdir() if p.is_dir() and p.name not in SKIP_DIRS):
        ios = sorted(d.glob("*.io"))
        pngs = sorted(d.glob("*.png"))
        pdfs = sorted(d.glob("*.pdf"))
        if not ios:
            continue
        if ios and pngs and pdfs:
            thumb = next((p for p in pngs if "thumbnail" in p.name), pngs[0])
            complete.append((d, ios[0], thumb, pdfs[0]))
        else:
            missing = [n for n, v in (("png", pngs), ("pdf", pdfs)) if not v]
            incomplete.append((d.name, missing))
    return complete, incomplete


def render_table(builds):
    lines = [START, "| Preview | Build | Model | Instructions |", "|---|---|---|---|"]
    for d, io, thumb, pdf in builds:
        title = d.name.replace("-", " ").title()
        lines.append(
            f'| <a href="{d.name}"><img src="{d.name}/{thumb.name}" width="200" alt="{title}"></a> '
            f"| {title} | [`.io`]({d.name}/{io.name}) | [`.pdf`]({d.name}/{pdf.name}) |"
        )
    lines.append(END)
    return "\n".join(lines)


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
    readme = root / "README.md"
    text = readme.read_text()

    if START not in text or END not in text:
        print(f"Markers {START}/{END} not found in README.md")
        sys.exit(1)

    complete, incomplete = find_builds(root)
    before, rest = text.split(START, 1)
    _, after = rest.split(END, 1)
    new_text = before + render_table(complete) + after

    if new_text != text:
        readme.write_text(new_text)
        print("README.md updated")
    else:
        print("README.md already up to date")

    for name, missing in incomplete:
        print(f"Skipped {name}: missing {', '.join(missing)}")


if __name__ == "__main__":
    main()
