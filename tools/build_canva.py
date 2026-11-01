#!/usr/bin/env python3
"""ポータルの「Canva版」（1ファイル版）を作る。

index.html に、画像・音・文字（フォント）をぜんぶ入れて、1つの HTML にする。
- 画像（img/apps・img/face.webp）と音（audio/se_click.mp3）はそのまま入れる
- フォント（Zen Maru Gothic）は、ポータルで使っている字だけを取り出して入れる
- Canva版では「Canva版で ひらく」ボタンを上にする（CANVA = true）

使い方:  python3 tools/build_canva.py <Zen Maru Gothic の ttf があるフォルダ>
         → dist/portal_canva.html
フォントは Google Fonts の Zen Maru Gothic（Medium・Bold・Black）。
"""
import base64
import io
import re
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist" / "portal_canva.html"
LIMIT = 10 * 1024 * 1024
WEIGHTS = [("Medium", 500), ("Bold", 700), ("Black", 900)]


def b64(data):
    return base64.b64encode(data).decode("ascii")


def font_faces(font_dir, text):
    css = []
    for name, weight in WEIGHTS:
        f = TTFont(font_dir / f"ZenMaruGothic-{name}.ttf")
        opt = subset.Options()
        opt.flavor = "woff2"
        opt.layout_features = ["*"]
        sub = subset.Subsetter(options=opt)
        sub.populate(text=text)
        sub.subset(f)
        buf = io.BytesIO()
        f.flavor = "woff2"
        f.save(buf)
        css.append(f"@font-face{{font-family:'Zen Maru Gothic';font-style:normal;font-weight:{weight};font-display:swap;"
                   f"src:url(data:font/woff2;base64,{b64(buf.getvalue())}) format('woff2')}}")
    return "\n".join(css)


def must_replace(s, old, new):
    if s.count(old) != 1:
        sys.exit(f"index.html の中に、置きかえる場所が見つからない（{s.count(old)}か所）: {old[:60]}")
    return s.replace(old, new)


def main():
    font_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "fonts"
    html = (ROOT / "index.html").read_text(encoding="utf-8")

    # 使っている字（画面の文字＋英数字・記号）
    chars = set(html) | set("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/・〜（）「」、。！？ ")
    text = "".join(sorted(c for c in chars if c >= " "))

    # フォント：Google Fonts の読みこみを、中に入れたフォントに置きかえ
    html = re.sub(r'<link rel="preconnect"[^>]*>\n', "", html)
    html = must_replace(html,
                        '<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700;900&display=swap" rel="stylesheet">',
                        "<style>\n" + font_faces(font_dir, text) + "\n</style>")

    # 画像
    imgs = {}
    for p in sorted((ROOT / "img" / "apps").glob("*/*.webp")):
        imgs[f"{p.parent.name}/{p.stem}"] = "data:image/webp;base64," + b64(p.read_bytes())
    js_imgs = "const IMGS = {" + ",".join(f"'{k}':'{v}'" for k, v in imgs.items()) + "};\n"
    html = must_replace(html, "const img = (id, i) => `img/apps/${id}/${i}.webp`;",
                        js_imgs + "const img = (id, i) => IMGS[id + '/' + i];")
    face = "data:image/webp;base64," + b64((ROOT / "img" / "face.webp").read_bytes())
    html = html.replace('"img/face.webp"', f'"{face}"')

    # 音
    se = "data:audio/mpeg;base64," + b64((ROOT / "audio" / "se_click.mp3").read_bytes())
    html = must_replace(html, "new Audio('audio/se_click.mp3')", f"new Audio('{se}')")

    # Canva版の印
    html = must_replace(html, "const CANVA = false;", "const CANVA = true;")
    html = html.replace("<title>K.nomの教育アプリポータル</title>", "<title>K.nomの教育アプリポータル（Canva版）</title>")

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    size = OUT.stat().st_size
    print(f"{OUT.relative_to(ROOT)}  {size / 1024 / 1024:.2f} MB（上限 10 MB）  画像 {len(imgs)} 枚")
    if size > LIMIT:
        sys.exit("10 MB をこえています。画像を小さくしてください。")


if __name__ == "__main__":
    main()
