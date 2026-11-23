from playwright.sync_api import sync_playwright
import pathlib
P=pathlib.Path('post.html').resolve().as_uri()
cfg={'feed':dict(h=1350,py='62%',bx='0%',bs='122%',tt='56px',ls='118px',ht='240px',h1='190px',h2s='40px'),
     'story':dict(h=1920,py='40%',bx='10%',bs='auto 118%',tt='120px',ls='130px',ht='330px',h1='220px',h2s='46px')}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for k,v in cfg.items():
        pg=b.new_page(viewport={'width':1080,'height':v['h']})
        pg.goto(P); pg.evaluate("v=>{for(const[k,x] of Object.entries(v))document.documentElement.style.setProperty('--'+k,typeof x==='number'?x+'px':x)}",v)
        pg.wait_for_timeout(800); pg.screenshot(path=f'{k}.png'); pg.close()
    b.close()
