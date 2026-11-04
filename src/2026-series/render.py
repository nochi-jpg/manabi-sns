# 作品紹介シリーズの Instagram 画像（1080×1350）を作る。
# 使い方: python3 render.py <manabi-sns のパス> <Zen Maru Gothic の ttf フォルダ> <出力フォルダ>
import sys, os, html
sys.path.insert(0, os.path.dirname(__file__))
from data import APPS
from playwright.sync_api import sync_playwright

ROOT, FONTS, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(OUT, exist_ok=True)
e = html.escape

CSS = f"""
@font-face{{font-family:Z;src:url(file://{FONTS}/ZenMaruGothic-Medium.ttf);font-weight:500}}
@font-face{{font-family:Z;src:url(file://{FONTS}/ZenMaruGothic-Bold.ttf);font-weight:700}}
@font-face{{font-family:Z;src:url(file://{FONTS}/ZenMaruGothic-Black.ttf);font-weight:900}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1350px;font-family:Z;font-weight:500;color:#222;background:var(--c);overflow:hidden}}
.s{{position:absolute;inset:40px;background:#fffdf8;border:6px solid #222;border-radius:36px;display:flex;flex-direction:column;padding:48px 54px 0;overflow:hidden}}
.top{{height:56px;display:flex;align-items:center;justify-content:space-between}}
.tag{{height:56px;line-height:50px;padding:0 26px;border:4px solid #222;border-radius:28px;background:var(--c);font-weight:900;font-size:30px}}
.who{{font-size:30px;font-weight:700;color:#555}}
h1{{font-weight:900;font-size:var(--h1);line-height:1.25;margin-top:30px;height:150px;display:flex;align-items:center}}
h2{{font-weight:900;font-size:46px;line-height:1.3;margin-top:30px;height:120px;display:flex;align-items:center}}
.img{{width:100%;aspect-ratio:16/9;margin:24px 0 0 0;border:5px solid #222;border-radius:18px;overflow:hidden;background:#fff;flex:none}}
.img img{{width:100%;height:100%;object-fit:contain;display:block}}
.txt{{font-size:36px;line-height:1.6;margin-top:34px;font-weight:700}}
ul{{list-style:none;margin-top:30px}}
li{{font-size:34px;line-height:1.45;font-weight:700;padding-left:48px;position:relative;margin-bottom:16px}}
li::before{{content:"";position:absolute;left:4px;top:13px;width:24px;height:24px;border-radius:50%;background:var(--c);border:4px solid #222}}
.foot{{position:absolute;left:0;right:0;bottom:0;height:84px;border-top:4px solid #222;display:flex;align-items:center;justify-content:space-between;padding:0 54px;font-size:28px;font-weight:700;background:#fff}}
.bub{{border:4px solid #222;border-radius:28px;background:#fff;padding:26px 34px;font-size:34px;line-height:1.55;font-weight:700;margin-top:26px;position:relative}}
.bub b{{display:block;font-size:26px;color:#666;font-weight:700;margin-bottom:6px}}
.me{{margin-left:80px;background:var(--c)}}
.note{{font-size:26px;color:#555;margin-top:24px;line-height:1.5}}
.big{{font-size:44px;font-weight:900;line-height:1.5;margin-top:40px}}
.url{{margin-top:30px;font-size:34px;font-weight:700;border:4px dashed #222;border-radius:20px;padding:22px 28px;line-height:1.5}}
"""

def page(a, body):
    h1 = "64px" if len(a["name"]) <= 9 else ("54px" if len(a["name"]) <= 14 else "46px")
    return f"""<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head>
<body style="--c:{a['color']};--h1:{h1}"><div class=s>
<div class=top><span class=tag>作品紹介 #{a['no']}</span><span class=who>{e(a['who'])}</span></div>
{body}
<div class=foot><span>Claudeで作った学習アプリ</span><span>K.nom</span></div></div></body></html>"""

def im(a, n):
    return f'<div class=img><img src="file://{ROOT}/img/apps/{a["id"]}/{n}.webp"></div>'

def slides(a):
    i2, i3 = a["imgs"]
    yield page(a, f'<h1>{e(a["name"])}</h1>{im(a,1)}<p class=txt>{e(a["lead"])}</p>')
    yield page(a, f'<h2>どんなアプリ？</h2>{im(a,i2)}<ul>' + "".join(f"<li>{e(t)}</li>" for t in a["feat"]) + "</ul>")
    yield page(a, f'<h2>どう使う？</h2>{im(a,i3)}<p class=txt>{e(a["use"])}</p>')
    memo = a["instr_title"].startswith("引き")
    lab = "理念メモより" if memo else "K.nom → Claude"
    nt = "※ 整数版で決めた理念メモから、そのまま抜き出しています。" if memo else "※ Claudeとのやりとりの記録を、短くまとめたものです。"
    yield page(a, f'<h2>{e(a["instr_title"])}</h2>' + "".join(f'<div class="bub me"><b>{lab}</b>{e(t)}</div>' for t in a["instr"])
               + f'<p class=note>{nt}</p>')
    yield page(a, f'<h2>遊んでみてください</h2>{im(a,1)}<p class=big>プロフィールのリンク<br>「K.nomの教育アプリポータル」から</p>'
               f'<p class=url>nochi-jpg.github.io/manabi-sns/#{a["id"]}</p>')

CHECK = """() => { const bad=[]; const s=document.querySelector('.s').getBoundingClientRect();
const foot=document.querySelector('.foot').getBoundingClientRect();
document.querySelectorAll('.s > *:not(.foot)').forEach(el=>{const r=el.getBoundingClientRect();
 if(r.bottom>foot.top-10) bad.push('下にはみだし:'+el.className+el.tagName);
 if(r.right>s.right-50||r.left<s.left+40) bad.push('横に切れ:'+el.className+el.tagName);
 if(el.scrollWidth>el.clientWidth+1) bad.push('横にはみだし:'+el.tagName);});
document.querySelectorAll('h1,h2').forEach(el=>{if(el.scrollHeight>el.clientHeight+1) bad.push('見出しがあふれ:'+el.textContent)});
return bad; }"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    problems = []
    for a in APPS:
        for k, h in enumerate(slides(a), 1):
            f = f"/tmp/s_{a['id']}_{k}.html"
            open(f, "w").write(h)
            pg.goto("file://" + f); pg.wait_for_timeout(150)
            bad = pg.evaluate(CHECK)
            if bad: problems.append((a["id"], k, bad))
            pg.screenshot(path=f"{OUT}/{a['no']:02d}_{a['id']}_ig{k}.jpg", type="jpeg", quality=90)
    b.close()
print("problems:", problems or "なし")
