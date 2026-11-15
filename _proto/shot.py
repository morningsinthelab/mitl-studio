import sys
from playwright.sync_api import sync_playwright
url=sys.argv[1]; outd=sys.argv[2]
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,vp,mob in [("desk",{"width":1440,"height":900},False),("mob",{"width":390,"height":844},True)]:
        pg=b.new_page(viewport=vp,device_scale_factor=2 if mob else 1,is_mobile=mob)
        pg.goto(url,wait_until="load")
        # scroll through to trigger reveals and lazy images
        h=pg.evaluate("document.body.scrollHeight")
        for y in range(0,h,400): pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(60)
        pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
        pg.add_style_tag(content="header.top{position:static!important}.og-media{position:relative!important;top:0!important}");pg.wait_for_timeout(1200)
        pg.locator("#products").screenshot(path=f"{outd}/proto-section-{name}.png")
        print(name, pg.locator("#products").bounding_box())
    b.close()
