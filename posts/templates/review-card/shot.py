from playwright.sync_api import sync_playwright
import pathlib
P=pathlib.Path('card.html').resolve().as_uri()
cfg={'review-card-a5':dict(w='1080px',h='1528px',qr='360px',dpr=1.62),'review-share':dict(w='1080px',h='1528px',qr='360px',dpr=1)}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for k,v in cfg.items():
        pg=b.new_page(viewport={'width':1080,'height':1528},device_scale_factor=v['dpr'])
        pg.goto(P);pg.evaluate("v=>{for(const[k,x] of Object.entries(v))document.documentElement.style.setProperty('--'+k,x)}",{'w':v['w'],'h':v['h'],'qr':v['qr'],'z':'1'})
        pg.wait_for_timeout(800);pg.screenshot(path=k+'.png');pg.close()
    b.close()
