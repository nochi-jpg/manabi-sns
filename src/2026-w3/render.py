import sys,pathlib
from playwright.sync_api import sync_playwright
h=pathlib.Path(sys.argv[1]).resolve(); out=pathlib.Path(sys.argv[2]); out.mkdir(exist_ok=True)
ids=sys.argv[3].split(',')
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1700,'height':1000}); pg.goto(h.as_uri()); pg.wait_for_timeout(1500)
    for i in ids:
        pg.locator('#'+i).screenshot(path=str(out/(i+'.png')))
    b.close()
