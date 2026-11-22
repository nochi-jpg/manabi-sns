#!/usr/bin/env python3
"""紹介画像に、黄色い帯の見出しを入れる（先生の手作り紹介画像と同じ見た目）。

使い方:
  python3 tools/intro_caption.py <元のスクショ> <出力.png> <x> <y> <文字の大きさ> <1行目> [2行目 ...]
  例: python3 tools/intro_caption.py shop.png 6.png 520 4 44 "コインをためて、新しいデッキを手に入れよう！"
- 画像は 1920×1080 にそろえてから書く。帯は1行ずつ（黄 #FFEF5C・黒文字・Zen Maru Gothic Black）
- 帯が画像からはみ出すときは止まる。ボタンや大事な文字にかぶらない場所をえらぶ
- フォントは環境変数 FONT か、../fonts/ZenMaruGothic-Black.ttf
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

FONT = os.environ.get("FONT", os.path.join(os.path.dirname(__file__), "..", "..", "fonts", "ZenMaruGothic-Black.ttf"))


def caption(src, out, x, y, size, lines):
    im = Image.open(src).convert("RGB").resize((1920, 1080), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, size)
    pad, gap = 14, 10
    for t in lines:
        l, tp, r, b = d.textbbox((0, 0), t, font=f)
        w, h = r - l, b - tp
        if x + w + pad * 2 > 1920 or y + h + pad * 2 > 1080:
            sys.exit(f"帯が画像からはみ出す: {t}")
        d.rectangle([x, y, x + w + pad * 2, y + h + pad * 2], fill="#FFEF5C")
        d.text((x + pad - l, y + pad - tp), t, font=f, fill="#1A1A1A")
        y += h + pad * 2 + gap
    im.save(out)


if __name__ == "__main__":
    if len(sys.argv) < 7:
        sys.exit(__doc__)
    caption(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6:])
