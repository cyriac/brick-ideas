# Brick Ideas

BrickLink Studio (`.io`) builds, tracked with their preview thumbnail and
instruction PDF.

## Builds

| Preview | Build | Model | Instructions |
|---|---|---|---|
| <a href="swinging-monkey"><img src="swinging-monkey/monkey-tree_thumbnail.png" width="200" alt="Swinging Monkey Tree"></a> | Swinging Monkey Tree | [`.io`](swinging-monkey/monkey-tree.io) | [`.pdf`](swinging-monkey/monkey-tree.pdf) |
| <a href="tasmanian-tiger"><img src="tasmanian-tiger/tasmanian-tiger_thumbnail.png" width="200" alt="Tasmanian Tiger"></a> | Tasmanian Tiger | [`.io`](tasmanian-tiger/tasmanian-tiger.io) | [`.pdf`](tasmanian-tiger/tasmanian-tiger.pdf) |
| <a href="black-cat"><img src="black-cat/black-cat_thumbnail.png" width="200" alt="Black Cat"></a> | Black Cat | [`.io`](black-cat/black-cat.io) | [`.pdf`](black-cat/black-cat.pdf) |
| <a href="whale"><img src="whale/whale_thumbnail.png" width="200" alt="Whale"></a> | Whale | [`.io`](whale/whale.io) | [`.pdf`](whale/whale.pdf) |

## extract_io_image.py

Extracts the embedded preview thumbnail from a `.io` file (it's just a zip).

```
python extract_io_image.py path/to/model.io [output_dir]
python extract_io_image.py --scan [root_dir]
```

`--scan` walks a directory for `.io` files, extracts a thumbnail only if one
isn't already sitting next to it, and reports any `.io` missing an
instruction PDF. PDFs are not auto-generated — export those manually from
BrickLink Studio.
