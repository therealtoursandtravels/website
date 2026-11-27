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


SLIDES = [  # (tab, tag, title, line, cta, link, photo, tint)  – no prices
 ("rewards", "Rewards", "100 Welcome Points", "Create your free account today – 1 point = ₹1 off your next trip", "Sign up", "account/#signup", "h-planning", "74,30,36"),
 ("holidays", "Winter special", "December Family Holidays", "Snow, beaches and festive cities – book early for the best stays", "Explore", "blog/best-december-family-holidays/", "h-kashmir", "38,52,66"),
 ("holidays", "Couples", "Honeymoon Specials", "Bali, Maldives, Kashmir and more – planned just for the two of you", "Explore", "honeymoon-packages/", "h-honeymoon", "70,40,48"),
 ("flights", "Special fares", "Student, Senior & Forces Fares", "Special fares for students, senior citizens, armed forces, doctors and nurses", "Search flights", "flights-hotels/#flights", "h-airport", "34,58,72"),
 ("holidays", "Pure Jain food", "Jain Yatra with Maharaj", "Tirth yatras with Jain food cooked fresh every day by our Maharaj", "View yatras", "jain-yatra-tours-with-maharaj/", "h-jain", "84,52,36"),
 ("visa", "Visa", "Visa Documents Made Simple", "Check the checklist, upload documents securely and get updates on WhatsApp", "Check visa", "visa/", "h-passport", "40,48,60"),
 ("rewards", "Refer & earn", "Refer a Friend, Both Get 100", "Share your code – you both get 100 points on their first booking", "Get my code", "account/", "h-group", "56,44,62"),
 ("holidays", "International", "Dubai, Bali, Swiss & Paris", "Handpicked international holidays for families and couples", "Explore", "international-holiday-packages/", "h-swiss", "36,56,54"),
]
TABS = [("all", "All"), ("holidays", "Holidays"), ("flights", "Flights"), ("visa", "Visa"), ("rewards", "Rewards")]

EXPLORE = [  # (place, line, link, photo, tall)
 ("Kashmir", "Snow, shikaras and meadows", "domestic-holiday-packages/", "c-kashmir", 1),
 ("Dubai", "Desert safari and city lights", "international-holiday-packages/", "g-dubai", 0),
 ("Leh Ladakh", "High passes and blue lakes", "adventure-trekking-tours/", "c-ladakh", 0),
 ("Maldives", "Overwater villas, turquoise sea", "honeymoon-packages/", "g-maldives", 1),
 ("Wildlife safaris", "Tigers, jungles and lodges", "wildlife-safari-tours/", "c-safari", 1),
 ("Weekend getaways", "Short breaks near Mumbai", "weekend-getaways/", "c-weekend", 0),
 ("Jain tirth yatras", "Shikharji, Palitana and more", "jain-yatra-tours-with-maharaj/", "c-jain", 0),
 ("Swiss & Paris", "Alps, lakes and the Eiffel Tower", "international-holiday-packages/", "g-swiss", 1),
]

DISCOVER = [("🎁", "Refer & Earn", "account/"), ("⭐", "My Rewards", "offers/#points"), ("📖", "Travel Guides", "blog/"),
            ("💬", "24×7 Help", "contact/")]

SOCIAL = [("Instagram", "https://www.instagram.com/therealtoursandtravels/"), ("Facebook", "https://www.facebook.com/657186054138837"),
          ("YouTube", "https://www.youtube.com/@therealtoursandtravels")]


def _offers(root):
    tabs = "".join(f'<button type="button" class="ah-tab{" on" if k == "all" else ""}" data-t="{k}">{n}</button>' for k, n in TABS)
    sl = ""
    for (t, tag, title, line, cta, link, ph, tint) in SLIDES:
        sl += (f'<a class="ah-slide" data-t="{t}" href="{root}{link}" style="--tint:{tint}"><img src="{root}img/{ph}.jpg" alt="" loading="lazy">'
               f'<span class="ah-sl-in"><em>{tag}</em><b>{title}</b><small>{line}</small><i>{cta} ›</i></span></a>')
    return (f'<div class="ah-head"><h3>Offers for you</h3><a href="{root}offers/">View all ›</a></div>'
            f'<div class="ah-tabs" role="tablist">{tabs}</div>'
            f'<div class="ah-slider" id="ahSlider">{sl}</div><div class="ah-dots" id="ahDots"></div>')


def _explore(root):
    cols = ["", ""]
    for i, (pl, line, link, ph, tall) in enumerate(EXPLORE):
        if not os.path.exists(os.path.join(HERE, "img", ph + ".jpg")):
            continue
        cols[i % 2] += (f'<a class="ah-ex{" tall" if tall else ""}" href="{root}{link}"><img src="{root}img/{ph}.jpg" alt="{pl}" loading="lazy">'
                        f'<span><b>📍 {pl}</b><small>{line}</small></span></a>')
    return f'<div class="ah-head"><h3>Where to next?</h3><a href="{root}holiday-packages/">All holidays ›</a></div><div class="ah-mason"><div>{cols[0]}</div><div>{cols[1]}</div></div>'


def _drawer(root):
    items = [("🎁", "Offers & coupons", "offers/"), ("👥", "Saved travellers", "account/#travellers"), ("🤝", "Refer & earn", "account/"),
             ("🧳", "Holiday packages", "holiday-packages/"), ("🛂", "Visa", "visa/"), ("📘", "Passport", "passport/"),
             ("🛡️", "Travel insurance", "insurance/"), ("💳", "Forex card", "forex/"), ("📖", "Travel guides", "blog/"),
             ("🎧", "Customer support", "contact/"), ("ℹ️", "About us", "about/")]
    li = "".join(f'<a href="{root}{h}"><span>{e}</span>{n}<i>›</i></a>' for e, n, h in items)
    soc = "".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SOCIAL)
    return f"""<div class="ah-dw" id="ahDw" hidden><div class="ah-dw-bg" data-x></div><aside class="ah-dw-p" role="dialog" aria-label="Menu">
<div class="ah-dw-me"><img src="{root}img/logo-512.png" alt="" width="64" height="64"><b>Welcome to The Real Tours and Travels</b><small>Log in to see your bookings and reward points. New here? Sign up and get 100 welcome points</small>
<div class="ah-dw-btns"><a class="btn gold" href="{root}account/">Log in</a><a class="btn outline" href="{root}account/#signup">Sign up</a></div></div>
<div class="ah-dw-q"><a href="{root}account/"><span>🧾</span>My Trips</a><a href="{root}offers/"><span>🎁</span>Offers</a><a href="{root}offers/#points"><span>⭐</span>Rewards</a></div>
<nav class="ah-dw-l">{li}</nav>
<div class="ah-dw-l"><a href="tel:+919843121212"><span>📞</span>Call 98431 21212<i>›</i></a><a href="https://search.google.com/local/writereview?placeid=ChIJn8v1TlS45zsRAQu5MAlfr1U" target="_blank" rel="noopener"><span>⭐</span>Rate us on Google<i>›</i></a></div>
<p class="ah-dw-s">Follow us</p><div class="ah-dw-so">{soc}</div>
<p class="ah-dw-v">The Real Tours and Travels · Estd. 1981<br>enquiry@therealtoursandtravels.com</p></aside></div>"""


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
    from visa import SB_URL as SBU, SB_KEY as SBK
    return f"""<section class="app-home" aria-label="App home"><div class="ah-top">
<p class="ah-hi"><span id="ahHi">Namaste</span> 🙏</p><h2>Where would you like to go?</h2></div>
<form class="ah-search" id="ahSearch" role="search" onsubmit="return false"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
<input id="ahQ" type="search" autocomplete="off" placeholder="Search destinations, visas, services…" aria-label="Search"><ul id="ahList" hidden></ul></form>
<div class="ah-grid ah-grid-big">{big}</div>
<div class="ah-grid ah-grid-sm">{small}</div>
{_offers(root)}
<div class="ah-head"><h3>Discover more</h3></div>
<div class="ah-disc">{"".join(f'<a href="{root}{h}"><span>{e}</span>{n}</a>' for e, n, h in DISCOVER)}</div>
<div class="ah-head"><h3>Trending holidays</h3><a href="{root}holiday-packages/">View all ›</a></div>
<div class="ah-row">{cards}</div>
{_explore(root)}
<div class="ah-head"><h3>Book a flight</h3></div>
{_drawer(root)}
</section>
<script>(function(){{const h=new Date().getHours();const g=document.getElementById('ahHi');if(g)g.textContent=h<12?'Good morning':h<17?'Good afternoon':'Good evening';
const I={idx},q=document.getElementById('ahQ'),L=document.getElementById('ahList'),R='{root}';
function show(){{const v=q.value.trim().toLowerCase();if(!v){{L.hidden=true;return;}}const m=I.filter(x=>x[0].toLowerCase().includes(v)).slice(0,7);
L.innerHTML=m.map(x=>'<li><a href="'+R+x[1]+'">'+x[0]+'</a></li>').join('')+'<li class="ah-ask"><a href="'+R+'customize-your-package/">✨ Plan a custom trip to “'+q.value.trim().replace(/[<>&"]/g,'')+'”</a></li>';L.hidden=false;}}
q.addEventListener('input',show);document.getElementById('ahSearch').addEventListener('submit',()=>{{const a=L.querySelector('a');if(a)location.href=a.href;}});
document.addEventListener('click',e=>{{if(!e.target.closest('#ahSearch'))L.hidden=true;}});
const hd=document.querySelector('header.site');function hh(){{if(hd)document.documentElement.style.setProperty('--hh',hd.offsetHeight+'px');}}hh();addEventListener('resize',hh);
const S=document.getElementById('ahSlider'),D=document.getElementById('ahDots');let vis=[],cur=0,tm=null,hold=false;
function slides(){{return [...S.children].filter(a=>!a.hidden);}}
function dots(){{vis=slides();D.innerHTML=vis.map((_,i)=>'<i'+(i===cur?' class="on"':'')+'></i>').join('');}}
function go(i){{vis=slides();if(!vis.length)return;cur=(i+vis.length)%vis.length;S.scrollTo({{left:vis[cur].offsetLeft-S.offsetLeft-16,behavior:'smooth'}});[...D.children].forEach((d,k)=>d.classList.toggle('on',k===cur));}}
function auto(){{clearInterval(tm);tm=setInterval(()=>{{if(!hold&&!document.hidden)go(cur+1);}},4500);}}
S.addEventListener('scroll',()=>{{vis=slides();const x=S.scrollLeft+S.clientWidth/2;let b=0,bd=1e9;vis.forEach((a,k)=>{{const c=a.offsetLeft-S.offsetLeft+a.offsetWidth/2,dd=Math.abs(c-x);if(dd<bd){{bd=dd;b=k;}}}});if(b!==cur){{cur=b;[...D.children].forEach((d,k)=>d.classList.toggle('on',k===cur));}}}},{{passive:true}});
S.addEventListener('touchstart',()=>{{hold=true;}},{{passive:true}});S.addEventListener('touchend',()=>{{setTimeout(()=>{{hold=false;}},2500);auto();}},{{passive:true}});
document.querySelectorAll('.ah-tab').forEach(b=>b.addEventListener('click',()=>{{document.querySelectorAll('.ah-tab').forEach(x=>x.classList.toggle('on',x===b));const t=b.dataset.t;[...S.children].forEach(a=>{{a.hidden=!(t==='all'||a.dataset.t===t||a.dataset.t==='coupon');}});cur=0;S.scrollLeft=0;dots();auto();}}));
fetch('{SBU}/rest/v1/coupons?select=code,title,description,valid_to&order=created_at.desc&limit=4',{{headers:{{apikey:'{SBK}',Authorization:'Bearer {SBK}'}}}}).then(r=>r.json()).then(d=>{{if(!Array.isArray(d))return;const esc=x=>String(x==null?'':x).replace(/[&<>"]/g,'');d.reverse().forEach(k=>{{if(k.valid_to&&new Date(k.valid_to+'T23:59')<new Date())return;const a=document.createElement('a');a.className='ah-slide ah-coupon';a.dataset.t='coupon';a.href=R+'offers/';a.innerHTML='<span class="ah-sl-in"><em>Coupon code</em><b>'+esc(k.title)+'</b><small>Use code <u>'+esc(k.code)+'</u> at checkout'+(k.valid_to?' · valid till '+new Date(k.valid_to+'T00:00').toLocaleDateString('en-IN',{{day:'numeric',month:'short'}}):'')+'</small><i>View offer ›</i></span>';S.prepend(a);}});dots();}}).catch(()=>{{}});
dots();auto();
const W=document.getElementById('ahDw');document.body.appendChild(W);const F=document.getElementById('ahSearch');addEventListener('scroll',()=>{{F.classList.toggle('stuck',F.getBoundingClientRect().top<=(hd?hd.offsetHeight:66)+8);}},{{passive:true}});function dw(o){{W.hidden=!o;document.documentElement.classList.toggle('dw-open',o);}}W.addEventListener('click',e=>{{if(e.target.hasAttribute('data-x'))dw(false);}});
const r=document.querySelector('header.site .hrow');if(r&&!document.querySelector('.ah-burger')){{const b=document.createElement('button');b.type='button';b.className='ah-burger';b.setAttribute('aria-label','Menu');b.innerHTML='<i></i><i></i><i></i>';b.onclick=()=>dw(true);r.prepend(b);}}
}})();</script>"""


CSS = """
.app-home{display:none}
html.is-app .app-home{display:block;padding:14px 16px 4px;background:linear-gradient(180deg,#fbf4f4 0,#fbf4f4 170px,#fff 300px)}
html.is-app .home-hero{display:none!important}html.is-app .home-hero+.fsec{margin-top:0!important}
html.is-app body:has(.app-home) nav.main,html.is-app body:has(.app-home) #acctLink{display:none!important}
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
/* v2: sticky search, offers slider, discover, explore grid, drawer */
html.is-app .app-home .ah-search{position:sticky;top:calc(var(--hh,66px) + 6px);z-index:45}
.ah-search.stuck:before{content:"";position:absolute;inset:-8px -17px -9px;background:#fff;border-bottom:1px solid #eee;z-index:-1}
.ah-tabs{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;margin:0 -16px 10px;padding:0 16px}.ah-tabs::-webkit-scrollbar{display:none}
.ah-tab{flex:none;border:1px solid #e4d6d7;background:#fff;color:#5a4a4b;border-radius:999px;padding:7px 15px;font:600 13px 'Jost',sans-serif;cursor:pointer}
.ah-tab.on{background:#f8ecec;border-color:#c98f93;color:#8f1d24}
.ah-slider{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -16px;padding:0 16px 4px;scrollbar-width:none;scroll-padding:0 16px}.ah-slider::-webkit-scrollbar{display:none}
.ah-slide{flex:0 0 88%;scroll-snap-align:start;position:relative;height:178px;border-radius:18px;overflow:hidden;text-decoration:none;color:#fff;background:rgb(var(--tint,74,30,36));box-shadow:0 10px 22px rgba(40,20,20,.14)}
.ah-slide[hidden]{display:none}
.ah-slide img{position:absolute;right:0;top:0;width:70%;height:100%;object-fit:cover}
.ah-slide:before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(90deg,rgb(var(--tint)) 0,rgb(var(--tint)) 34%,rgba(var(--tint),.55) 62%,rgba(var(--tint),.05) 100%)}
.ah-sl-in{position:absolute;inset:0;z-index:2;display:flex;flex-direction:column;justify-content:center;gap:5px;padding:16px 18px;max-width:72%}
.ah-sl-in em{align-self:flex-start;font-style:normal;font-size:10.5px;font-weight:700;letter-spacing:1.4px;text-transform:uppercase;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.3);border-radius:999px;padding:3px 9px}
.ah-sl-in b{font-family:'Playfair Display',serif;font-size:21px;line-height:1.15}
.ah-sl-in small{font-size:12.5px;line-height:1.35;opacity:.9}
.ah-sl-in i{align-self:flex-start;font-style:normal;font-size:12.5px;font-weight:700;margin-top:4px;background:#fff;color:rgb(var(--tint));border-radius:999px;padding:6px 13px}
.ah-coupon{--tint:62,42,46;background:repeating-linear-gradient(135deg,#3e2a2e 0 14px,#45303a 14px 28px)}.ah-coupon:before{display:none}.ah-coupon .ah-sl-in{max-width:100%}.ah-coupon u{text-decoration:none;font-weight:700;letter-spacing:1px;border:1px dashed rgba(255,255,255,.6);border-radius:6px;padding:1px 6px}
.ah-dots{display:flex;justify-content:center;gap:6px;margin-top:10px}.ah-dots i{width:6px;height:6px;border-radius:99px;background:#dccbcc;transition:all .3s}.ah-dots i.on{width:18px;background:#b3121a}
.ah-disc{display:grid;grid-template-columns:repeat(4,1fr);background:#fff;border:1px solid #efe3e4;border-radius:16px;overflow:hidden}
.ah-disc a{display:flex;flex-direction:column;align-items:center;gap:5px;padding:13px 4px;text-decoration:none;color:#4a3b3c;font-size:11.5px;font-weight:600;text-align:center;border-right:1px solid #f1e8e8}.ah-disc a:last-child{border-right:0}.ah-disc span{font-size:22px}
.ah-mason{display:grid;grid-template-columns:1fr 1fr;gap:10px;align-items:start}.ah-mason>div{display:flex;flex-direction:column;gap:10px}
.ah-ex{position:relative;display:block;height:170px;border-radius:16px;overflow:hidden;text-decoration:none;color:#fff;box-shadow:0 6px 16px rgba(0,0,0,.1)}.ah-ex.tall{height:240px}
.ah-ex img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ah-ex span{position:absolute;left:0;right:0;bottom:0;padding:34px 11px 11px;background:linear-gradient(180deg,transparent,rgba(15,15,15,.75));display:flex;flex-direction:column;gap:2px}
.ah-ex b{font-size:14.5px}.ah-ex small{font-size:11.5px;opacity:.88;line-height:1.3}
.ah-burger{display:none}html.is-app .ah-burger{display:inline-flex;flex-direction:column;justify-content:center;gap:4px;width:40px;height:40px;margin-right:6px;padding:0 9px;border:1px solid var(--line);border-radius:12px;background:#fff;cursor:pointer}
.ah-burger i{display:block;height:2px;border-radius:2px;background:var(--wine)}.ah-burger i:nth-child(2){width:70%}
html.dw-open,html.dw-open body{overflow:hidden}
.ah-dw[hidden]{display:none}.ah-dw{position:fixed;inset:0;z-index:200}
.ah-dw-bg{position:absolute;inset:0;background:rgba(20,15,15,.42);animation:spFade .25s ease forwards;opacity:0}
.ah-dw-p{position:absolute;left:0;top:0;bottom:0;width:86%;max-width:360px;background:#f7f5f5;overflow-y:auto;padding:16px 14px calc(20px + env(safe-area-inset-bottom));box-shadow:10px 0 30px rgba(0,0,0,.15);animation:dwIn .3s cubic-bezier(.2,.8,.2,1)}
@keyframes dwIn{from{transform:translateX(-100%)}to{transform:none}}
.ah-dw-me{display:flex;flex-direction:column;align-items:center;text-align:center;gap:6px;background:#fff;border:1px solid #ece4e4;border-radius:18px;padding:18px 14px 14px}
.ah-dw-me img{width:64px;height:64px}.ah-dw-me b{font-family:'Playfair Display',serif;font-size:17px;color:var(--wine);line-height:1.25}.ah-dw-me small{font-size:12.5px;color:#7a6a6b}
.ah-dw-btns{display:grid;grid-template-columns:1fr 1fr;gap:8px;width:100%;margin-top:8px}.ah-dw-btns .btn{padding:9px 6px!important;min-height:0!important;line-height:1.2!important;font-size:14px!important;text-align:center;justify-content:center}
.ah-dw-q{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:12px 0}
.ah-dw-q a{display:flex;flex-direction:column;align-items:center;gap:4px;background:#fff;border:1px solid #ece4e4;border-radius:14px;padding:11px 4px;text-decoration:none;color:#3d3032;font-size:12px;font-weight:600}.ah-dw-q span{font-size:20px}
.ah-dw-l{display:flex;flex-direction:column;background:#fff;border:1px solid #ece4e4;border-radius:14px;margin-bottom:12px;overflow:hidden}
.ah-dw-l a{display:flex;align-items:center;gap:12px;padding:12px 14px;text-decoration:none;color:#2e2a2a;font-size:14.5px;border-bottom:1px solid #f3eeee}.ah-dw-l a:last-child{border-bottom:0}
.ah-dw-l span{width:22px;text-align:center}.ah-dw-l i{margin-left:auto;font-style:normal;color:#b9aeae;font-size:18px}
.ah-dw-s{margin:6px 4px 8px;font-size:12px;color:#7a6a6b;font-weight:600;letter-spacing:.5px;text-transform:uppercase}
.ah-dw-so{display:flex;gap:8px;flex-wrap:wrap}.ah-dw-so a{background:#fff;border:1px solid #ece4e4;border-radius:999px;padding:7px 14px;font-size:13px;color:#4a3b3c;text-decoration:none;font-weight:600}
.ah-dw-v{margin:16px 4px 0;font-size:11.5px;color:#9a8e8e;line-height:1.5;text-align:center}
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
