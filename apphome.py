"""App-only home screen (shown when the site runs as the installed app) + opening animation (splash).
Own design for The Real Tours and Travels: red seal logo, light theme, muted colours, no prices.
Preview in a normal browser: add ?app=1 to the home page URL (and ?splash=1 to replay the opening animation)."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))


def _icons():
    """Reuse the line icons from the main navigation in build.py: label -> svg."""
    src = open(os.path.join(HERE, "build.py"), encoding="utf-8").read()
    out = {}
    for href, svg, label in re.findall(r'<a href="\{root\}([^"]*)">(<svg.*?</svg>)<span>(.*?)</span></a>', src):
        out[label] = (href, svg.replace('width="24" height="24"', 'width="28" height="28"'))
    return out


BIG = [("Flights", "Flights"), ("Hotels", "Hotels"), ("Holiday Packages", "Holidays"), ("Visa", "Visa")]
SMALL = [("Cruise", "Cruise"), ("Cars", "Cars"), ("Passport", "Passport"), ("Travel Insurance", "Insurance"),
         ("Forex", "Forex Card"), ("Customized Packages", "Customize Trip"), ("Jain Yatra", "Jain Yatra"), ("Offers", "Offers")]


def _search_index(icons):
    idx = []
    for label, (href, _) in icons.items():
        idx.append([label, href])
    extra = [("Honeymoon packages", "honeymoon-packages/"), ("Group tours", "group-tours/"), ("Domestic holidays", "domestic-holiday-packages/"),
             ("International holidays", "international-holiday-packages/"), ("Yatra tours", "yatra-tours/"), ("Weekend getaways", "weekend-getaways/"),
             ("Senior citizen tours", "senior-citizen-tours/"), ("Women-only tours", "women-only-group-tours/"), ("Wildlife safari", "wildlife-safari-tours/"),
             ("Trekking & adventure", "adventure-trekking-tours/"), ("School & college tours", "school-college-educational-tours/"),
             ("FIT & MICE tours", "fit-mice-tours/"), ("Destination weddings", "destination-weddings-family-functions/"),
             ("Airport transfers & cabs", "airport-transfers-outstation-cabs/"), ("Police clearance (PCC)", "police-clearance-certificate-pcc-document-services/"),
             ("Contact us", "contact/"), ("My account / Login", "account/")]
    idx += [list(x) for x in extra]
    vdir = os.path.join(HERE, "visa")
    if os.path.isdir(vdir):
        for slug in sorted(os.listdir(vdir)):
            if os.path.isdir(os.path.join(vdir, slug)):
                nm = slug.replace("-", " ").title().replace("Uae", "UAE").replace("Uk", "UK").replace("Usa", "USA")
                idx.append([f"{nm} visa", f"visa/{slug}/"])
    try:
        for p in json.load(open(os.path.join(HERE, "packages.json")))["packages"]:
            idx.append([f"{p['name']} – holiday package", "holiday-packages/"])
    except Exception:
        pass
    return idx


def html(root=""):
    icons = _icons()
    try:
        pk = json.load(open(os.path.join(HERE, "packages.json")))["packages"]
    except Exception:
        pk = []

    def tile(lbl, name, cls):
        href, svg = icons[lbl]
        return f'<a class="{cls}" href="{root}{href}"><i>{svg}</i><span>{name}</span></a>'

    big = "".join(tile(l, n, "ah-big") for l, n in BIG if l in icons)
    small = "".join(tile(l, n, "ah-sm") for l, n in SMALL if l in icons)
    cards = ""
    for p in pk[:10]:
        img = p.get("img") or ""
        if not os.path.exists(os.path.join(HERE, "img", img + ".jpg")):
            continue
        n = p.get("nights")
        sub = f'{n} nights · {"India" if p.get("type") == "india" else "International"}' if n else ""
        cards += (f'<a class="ah-card" href="{root}holiday-packages/"><img src="{root}img/{img}.jpg" alt="{p["name"]}" loading="lazy" width="320" height="220">'
                  f'<span><b>{p["name"]}</b><small>{sub}</small></span></a>')
    idx = json.dumps(_search_index(icons), ensure_ascii=False)
    return f"""<section class="app-home" aria-label="App home"><div class="ah-top">
<p class="ah-hi"><span id="ahHi">Namaste</span> 🙏</p><h2>Where would you like to go?</h2>
<form class="ah-search" id="ahSearch" role="search" onsubmit="return false"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
<input id="ahQ" type="search" autocomplete="off" placeholder="Search destinations, visas, services…" aria-label="Search"><ul id="ahList" hidden></ul></form></div>
<div class="ah-grid ah-grid-big">{big}</div>
<div class="ah-grid ah-grid-sm">{small}</div>
<div class="ah-head"><h3>Trending holidays</h3><a href="{root}holiday-packages/">View all ›</a></div>
<div class="ah-row">{cards}</div>
<div class="ah-head"><h3>Book a flight</h3></div>
</section>
<script>(function(){{const h=new Date().getHours();const g=document.getElementById('ahHi');if(g)g.textContent=h<12?'Good morning':h<17?'Good afternoon':'Good evening';
const I={idx},q=document.getElementById('ahQ'),L=document.getElementById('ahList'),R='{root}';
function show(){{const v=q.value.trim().toLowerCase();if(!v){{L.hidden=true;return;}}const m=I.filter(x=>x[0].toLowerCase().includes(v)).slice(0,7);
L.innerHTML=m.map(x=>'<li><a href="'+R+x[1]+'">'+x[0]+'</a></li>').join('')+'<li class="ah-ask"><a href="'+R+'customize-your-package/">✨ Plan a custom trip to “'+q.value.trim().replace(/[<>&"]/g,'')+'”</a></li>';L.hidden=false;}}
q.addEventListener('input',show);document.getElementById('ahSearch').addEventListener('submit',()=>{{const a=L.querySelector('a');if(a)location.href=a.href;}});
document.addEventListener('click',e=>{{if(!e.target.closest('#ahSearch'))L.hidden=true;}});}})();</script>"""


CSS = """
.app-home{display:none}
html.is-app .app-home{display:block;padding:14px 16px 4px;background:linear-gradient(180deg,#fbf4f4 0,#fbf4f4 170px,#fff 300px)}
html.is-app .home-hero{display:none!important}html.is-app .home-hero+.fsec{margin-top:0!important}
html.is-app body:has(.app-home) nav.main{display:none!important}
.ah-hi{margin:2px 2px 0;font-size:13px;color:#7a6a6b;letter-spacing:.2px}
.app-home h2{margin:2px 2px 12px;font-family:'Playfair Display',serif;font-size:23px;color:var(--wine);line-height:1.2}
.ah-search{position:relative;display:flex;align-items:center;gap:10px;background:#fff;border:1px solid #ead9da;border-radius:14px;padding:0 14px;box-shadow:0 6px 18px rgba(120,40,40,.07);color:#9a8a8b}
.ah-search input{flex:1;border:0;outline:0;background:none;font:inherit;font-size:15px;padding:13px 0;color:var(--ink);min-width:0}
.ah-search ul{position:absolute;left:0;right:0;top:calc(100% + 6px);z-index:60;list-style:none;margin:0;padding:6px;background:#fff;border:1px solid var(--line);border-radius:14px;box-shadow:0 14px 30px rgba(0,0,0,.12)}
.ah-search li a{display:block;padding:11px 12px;border-radius:10px;color:var(--ink);text-decoration:none;font-size:14.5px}.ah-search li a:active{background:#f6eeee}
.ah-search li.ah-ask a{color:var(--crimson);font-weight:600;border-top:1px solid var(--line);border-radius:0 0 10px 10px}
.ah-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:14px}
.ah-grid a{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;text-decoration:none;color:var(--wine);text-align:center;line-height:1.15;-webkit-tap-highlight-color:transparent;transition:transform .15s}
.ah-grid a:active{transform:scale(.95)}
.ah-big{background:#fff;border:1px solid #efe3e4;border-radius:16px;padding:14px 4px 12px;font-weight:700;font-size:13px;box-shadow:0 4px 14px rgba(120,40,40,.06)}
.ah-big i{display:grid;place-items:center;width:48px;height:48px;border-radius:14px;background:#f8ecec;color:#b3121a}
.ah-grid-sm{background:#fafafa;border:1px solid #f0f0f0;border-radius:16px;padding:12px 4px;gap:14px 4px}
.ah-sm{font-size:11.5px;font-weight:500;color:#555!important}.ah-sm i{display:grid;place-items:center;width:40px;height:40px;border-radius:12px;background:#fff;border:1px solid #eee;color:#6b5a5b}
.ah-sm i svg{width:22px;height:22px}
.ah-head{display:flex;align-items:baseline;justify-content:space-between;margin:22px 2px 10px}
.ah-head h3{margin:0;font-size:17px;color:var(--wine)}.ah-head a{font-size:13px;color:var(--crimson);text-decoration:none;font-weight:600}
.ah-row{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -16px;padding:0 16px 6px;scrollbar-width:none}.ah-row::-webkit-scrollbar{display:none}
.ah-card{flex:0 0 62%;max-width:250px;scroll-snap-align:start;position:relative;border-radius:16px;overflow:hidden;text-decoration:none;color:#fff;aspect-ratio:4/5;box-shadow:0 8px 20px rgba(0,0,0,.12)}
.ah-card img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ah-card span{position:absolute;left:0;right:0;bottom:0;padding:40px 14px 14px;background:linear-gradient(180deg,transparent,rgba(20,20,20,.72));display:flex;flex-direction:column;gap:2px}
.ah-card b{font-size:16px;line-height:1.2}.ah-card small{font-size:12px;opacity:.85}
/* opening animation */
html.splash-on body{overflow:hidden}html.splash-on::after{content:"";position:fixed;inset:0;background:#fff;z-index:9998}
#splash{position:fixed;inset:0;z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;background:radial-gradient(circle at 50% 42%,#fff 0,#fff 35%,#f9efef 100%);transition:opacity .5s ease,transform .5s ease}
#splash.out{opacity:0;transform:scale(1.06);pointer-events:none}
.sp-stage{position:relative;width:220px;height:220px;display:grid;place-items:center}
.sp-logo{width:132px;height:132px;border-radius:50%;background:#fff;box-shadow:0 0 0 10px #fbf1f1,0 18px 40px rgba(179,18,26,.16);display:grid;place-items:center;opacity:0;transform:scale(.55) rotate(-25deg);animation:spIn .8s cubic-bezier(.2,.9,.3,1.25) .15s forwards}
.sp-logo img{width:118px;height:118px}
.sp-ring{position:absolute;inset:0}.sp-ring circle{fill:none;stroke:#d7191f;stroke-opacity:.28;stroke-width:1.5;stroke-dasharray:4 7;stroke-dashoffset:0;opacity:0;animation:spFade .4s ease .55s forwards}
.sp-orbit{position:absolute;inset:0;opacity:0;animation:spFade .3s ease .55s forwards,spSpin 1.6s cubic-bezier(.45,.05,.35,1) .55s forwards}
.sp-orbit svg{position:absolute;left:50%;top:-2px;width:26px;height:26px;margin-left:-13px;color:#b3121a;transform:rotate(90deg)}
.sp-name{margin:18px 0 0;font-family:'Playfair Display',serif;font-size:23px;color:#b3121a;opacity:0;transform:translateY(10px);animation:spUp .6s ease 1.15s forwards}
.sp-tag{margin:6px 0 0;font-size:11.5px;letter-spacing:2.4px;color:#7a6a6b;text-transform:uppercase;opacity:0;transform:translateY(10px);animation:spUp .6s ease 1.4s forwards}
.sp-dots{display:flex;gap:6px;margin-top:26px;opacity:0;animation:spFade .3s ease 1.6s forwards}.sp-dots i{width:6px;height:6px;border-radius:50%;background:#d7191f;opacity:.25;animation:spDot 1s ease-in-out infinite}.sp-dots i:nth-child(2){animation-delay:.15s}.sp-dots i:nth-child(3){animation-delay:.3s}
@keyframes spIn{to{opacity:1;transform:none}}@keyframes spFade{to{opacity:1}}@keyframes spUp{to{opacity:1;transform:none}}
@keyframes spSpin{from{transform:rotate(0)}to{transform:rotate(360deg)}}@keyframes spDot{50%{opacity:.9;transform:translateY(-3px)}}
@media(prefers-reduced-motion:reduce){#splash *{animation-duration:.01s!important;animation-delay:0s!important}}
"""

# Runs in <head>: decide early whether to show the opening animation (no flash of the page underneath)
HEAD_JS = """<script>(function(){try{var u=new URLSearchParams(location.search),d=document.documentElement;
if(u.get('app')==='1')d.classList.add('is-app');
var app=matchMedia('(display-mode: standalone)').matches||navigator.standalone;
if(u.get('splash')==='1'||(app&&!sessionStorage.getItem('rtt_splash')))d.classList.add('splash-on');}catch(e){}})();</script>"""

# Runs at the end of <body>
BODY_JS = """<script>(function(){var d=document.documentElement;if(!d.classList.contains('splash-on'))return;try{sessionStorage.setItem('rtt_splash','1')}catch(e){}
var s=document.createElement('div');s.id='splash';s.setAttribute('aria-hidden','true');
s.innerHTML='<div class="sp-stage"><svg class="sp-ring" viewBox="0 0 220 220"><circle cx="110" cy="110" r="100"/></svg><div class="sp-orbit"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z"/></svg></div><div class="sp-logo"><img src="/img/logo-512.png" alt=""></div></div><p class="sp-name">The Real Tours and Travels</p><p class="sp-tag">Estd. 1981 · All your travel needs</p><div class="sp-dots"><i></i><i></i><i></i></div>';
document.body.appendChild(s);d.classList.remove('splash-on');
var rm=matchMedia('(prefers-reduced-motion: reduce)').matches,t;function go(){clearTimeout(t);s.classList.add('out');setTimeout(function(){s.remove()},550);}
t=setTimeout(go,rm?900:2700);s.addEventListener('click',go);})();</script>"""
