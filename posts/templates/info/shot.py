from playwright.sync_api import sync_playwright
import pathlib
P=pathlib.Path('post.html').resolve().as_uri()
cfg={'feed':dict(h='1350px',pt='56px',g1='34px',h1='60px',g2='26px',td='25px',tp='14px',g3='20px'),
     'story':dict(h='1920px',pt='130px',g1='80px',h1='80px',g2='50px',td='29px',tp='24px',g3='50px')}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for k,v in cfg.items():
        pg=b.new_page(viewport={'width':1080,'height':int(v['h'][:-2])})
        pg.goto(P);pg.evaluate("v=>{for(const[k,x] of Object.entries(v))document.documentElement.style.setProperty('--'+k,x)}",v)
        pg.wait_for_timeout(700);pg.screenshot(path=k+'.png');pg.close()
    b.close()
