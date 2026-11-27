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


SERVICES = [("Flights", "Flights"), ("Hotels", "Hotels"), ("Holiday Packages", "Holidays"), ("Visa", "Visa"),
            ("Passport", "Passport"), ("Cruise", "Cruise"), ("Cars", "Cars"), ("Travel Insurance", "Insurance"),
            ("Forex", "Forex"), ("Customized Packages", "Custom Trip"), ("Jain Yatra", "Jain Yatra"), ("Offers", "Offers")]

HERO_PHOTOS = [("h-kashmir", "Kashmir"), ("h-swiss", "Switzerland"), ("h-maldives", "Maldives"), ("h-ladakh", "Ladakh"),
               ("h-dubai", "Dubai"), ("h-honeymoon", "Bali")]

OCCASIONS = [("Family holidays", "Kids-friendly stays and easy days", "domestic-holiday-packages/", "c-kashmir"),
             ("Honeymoon", "Romantic escapes, planned for two", "honeymoon-packages/", "c-honeymoon"),
             ("Yatras & pilgrimages", "Char Dham, Shikharji, Palitana and more", "yatra-tours/", "c-yatra"),
             ("Group tours", "Fixed departures with like-minded travellers", "group-tours/", "c-group"),
             ("Senior citizen tours", "Comfortable pace, extra care", "senior-citizen-tours/", "c-senior"),
             ("Women-only tours", "Safe, fun trips with women leaders", "women-only-group-tours/", "c-women"),
             ("Weekend getaways", "Short breaks close to home", "weekend-getaways/", "c-weekend"),
             ("Wildlife safaris", "Tigers, jungles and lodges", "wildlife-safari-tours/", "c-safari")]


def html(root=""):
    icons = _icons()
    try:
        pk = json.load(open(os.path.join(HERE, "packages.json")))["packages"]
    except Exception:
        pk = []
    try:
        import fx
        rating = fx.load_reviews().get("rating") or "4.8"
    except Exception:
        rating = "4.8"
    stamps = "".join(f'<a class="ah-st" href="{root}{icons[l][0]}"><i>{icons[l][1]}</i><span>{n}</span></a>' for l, n in SERVICES if l in icons)
    tickets = ""
    for p in pk[:10]:
        img = p.get("img") or ""
        if not os.path.exists(os.path.join(HERE, "img", img + ".jpg")):
            continue
        n = p.get("nights")
        sub = f'{n} nights · {"India" if p.get("type") == "india" else "Abroad"}' if n else ""
        tickets += (f'<a class="ah-tk" href="{root}holiday-packages/"><img src="{root}img/{img}.jpg" alt="{p["name"]}" loading="lazy" width="300" height="200">'
                    f'<span class="ah-tk-b"><b>{p["name"]}</b><small>{sub}</small><i>View plan ›</i></span></a>')
    slides = "".join(f'<a class="ah-pc" href="{root}{link}"><img src="{root}img/{ph}.jpg" alt="" loading="lazy"><em>{tag}</em>'
                     f'<span><b>{title}</b><small>{line}</small><i>{cta} ›</i></span></a>' for (_t, tag, title, line, cta, link, ph, _c) in SLIDES)
    occ = "".join(f'<a class="ah-oc" href="{root}{link}"><img src="{root}img/{ph}.jpg" alt="" loading="lazy" width="56" height="56"><span><b>{t}</b><small>{d}</small></span><i>›</i></a>'
                  for t, d, link, ph in OCCASIONS if os.path.exists(os.path.join(HERE, "img", ph + ".jpg")))
    heroes = json.dumps([[f"{root}img/{h}.jpg", n] for h, n in HERO_PHOTOS if os.path.exists(os.path.join(HERE, "img", h + ".jpg"))])
    idx = json.dumps(_search_index(icons), ensure_ascii=False)
    from visa import SB_URL as SBU, SB_KEY as SBK
    return f"""<section class="app-home" aria-label="App home">
<div class="ah-hero" id="ahHero"><div class="ah-ph"><img id="ahPh" src="{root}img/h-kashmir.jpg" alt=""></div>
<img class="ah-seal" src="{root}img/logo-512.png" alt="" width="64" height="64">
<div class="ah-hero-t"><p class="ah-hi"><span id="ahHi">Namaste</span>, <span id="ahNm">traveller</span></p><h2>Where shall we take you next?</h2><p class="ah-pl" id="ahPl">📍 Kashmir</p></div>
<form class="ah-search" id="ahSearch" role="search" onsubmit="return false"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
<input id="ahQ" type="search" autocomplete="off" placeholder="Try “Dubai”, “visa”, “Jain yatra”…" aria-label="Search"><ul id="ahList" hidden></ul></form></div>
<div class="ah-sec"><h3>How can we help?</h3></div>
<div class="ah-stamps">{stamps}</div>
<div class="ah-trust"><img src="{root}img/logo.png" alt="" width="40" height="40"><div><b>Your travel partner since 1981</b><small>★ {rating} on Google · 24×7 support · Jain food tours with Maharaj</small></div></div>
<div class="ah-sec"><h3>This season</h3><a href="{root}offers/">All offers ›</a></div>
<div class="ah-prog" id="ahProg"></div>
<div class="ah-pcs" id="ahSlider">{slides}</div>
<div class="ah-sec"><h3>Ready-made holidays</h3><a href="{root}holiday-packages/">See all ›</a></div>
<div class="ah-tks">{tickets}</div>
<div class="ah-sec"><h3>Plan by occasion</h3></div>
<div class="ah-occ">{occ}</div>
<div class="ah-sec"><h3>Book a flight</h3></div>
{_drawer(root)}
</section>
<script>(function(){{const h=new Date().getHours();const g=document.getElementById('ahHi');if(g)g.textContent=h<12?'Good morning':h<17?'Good afternoon':'Good evening';
const HP={heroes};try{{let k=+(sessionStorage.getItem('rtt_hp')||-1);k=(k+1)%HP.length;sessionStorage.setItem('rtt_hp',k);document.getElementById('ahPh').src=HP[k][0];document.getElementById('ahPl').textContent='📍 '+HP[k][1];}}catch(e){{}}
const nmT=setInterval(()=>{{const p=window.RTT_PROFILE;if(p&&p.name){{document.getElementById('ahNm').textContent=p.name.split(' ')[0];clearInterval(nmT);}}}},400);setTimeout(()=>clearInterval(nmT),8000);
const I={idx},q=document.getElementById('ahQ'),L=document.getElementById('ahList'),R='{root}';
function show(){{const v=q.value.trim().toLowerCase();if(!v){{L.hidden=true;return;}}const m=I.filter(x=>x[0].toLowerCase().includes(v)).slice(0,7);
L.innerHTML=m.map(x=>'<li><a href="'+R+x[1]+'">'+x[0]+'</a></li>').join('')+'<li class="ah-ask"><a href="'+R+'customize-your-package/">✨ Plan a custom trip to “'+q.value.trim().replace(/[<>&"]/g,'')+'”</a></li>';L.hidden=false;}}
q.addEventListener('input',show);document.getElementById('ahSearch').addEventListener('submit',()=>{{const a=L.querySelector('a');if(a)location.href=a.href;}});
document.addEventListener('click',e=>{{if(!e.target.closest('#ahSearch'))L.hidden=true;}});
const S=document.getElementById('ahSlider'),P=document.getElementById('ahProg');let cur=0,tm=null,hold=false;const DUR=5000;
function bars(){{P.innerHTML=[...S.children].map(()=>'<i><b></b></i>').join('');mark();}}
function mark(){{[...P.children].forEach((d,k)=>{{d.className=k<cur?'done':k===cur?'run':'';const b=d.firstChild;b.style.animation='none';void b.offsetWidth;b.style.animation='';}});}}
function go(i){{const n=S.children.length;if(!n)return;cur=(i+n)%n;S.scrollTo({{left:S.children[cur].offsetLeft-S.offsetLeft-16,behavior:'smooth'}});mark();}}
function auto(){{clearInterval(tm);tm=setInterval(()=>{{if(!hold&&!document.hidden)go(cur+1);}},DUR);}}
let st=null;S.addEventListener('scroll',()=>{{clearTimeout(st);st=setTimeout(()=>{{const x=S.scrollLeft+S.clientWidth/2;let b=0,bd=1e9;[...S.children].forEach((a,k)=>{{const c=a.offsetLeft-S.offsetLeft+a.offsetWidth/2,dd=Math.abs(c-x);if(dd<bd){{bd=dd;b=k;}}}});if(b!==cur){{cur=b;mark();auto();}}}},120);}},{{passive:true}});
S.addEventListener('touchstart',()=>{{hold=true;}},{{passive:true}});S.addEventListener('touchend',()=>{{setTimeout(()=>{{hold=false;}},1500);}},{{passive:true}});
fetch('{SBU}/rest/v1/coupons?select=code,title,valid_to&order=created_at.desc&limit=4',{{headers:{{apikey:'{SBK}',Authorization:'Bearer {SBK}'}}}}).then(r=>r.json()).then(d=>{{if(!Array.isArray(d))return;const esc=x=>String(x==null?'':x).replace(/[&<>"]/g,'');d.reverse().forEach(k=>{{if(k.valid_to&&new Date(k.valid_to+'T23:59')<new Date())return;const a=document.createElement('a');a.className='ah-pc ah-cp';a.href=R+'offers/';a.innerHTML='<em>Coupon</em><span><b>'+esc(k.title)+'</b><small>Use code <u>'+esc(k.code)+'</u> at checkout'+(k.valid_to?' · till '+new Date(k.valid_to+'T00:00').toLocaleDateString('en-IN',{{day:'numeric',month:'short'}}):'')+'</small><i>View offer ›</i></span>';S.prepend(a);}});bars();}}).catch(()=>{{}});
bars();auto();
const W=document.getElementById('ahDw');document.body.appendChild(W);function dw(o){{W.hidden=!o;document.documentElement.classList.toggle('dw-open',o);}}W.addEventListener('click',e=>{{if(e.target.hasAttribute('data-x'))dw(false);}});
const r=document.querySelector('header.site .hrow');if(r&&!document.querySelector('.ah-burger')){{const b=document.createElement('button');b.type='button';b.className='ah-burger';b.setAttribute('aria-label','Menu');b.innerHTML='<i></i><i></i><i></i>';b.onclick=()=>dw(true);r.prepend(b);}}
}})();</script>"""


CSS = """
.app-home{display:none}
html.is-app .app-home{display:block;padding:12px 16px 4px;background:#fff}
html.is-app .home-hero{display:none!important}html.is-app .home-hero+.fsec{margin-top:0!important}
html.is-app body:has(.app-home) nav.main,html.is-app body:has(.app-home) #acctLink{display:none!important}
.ah-hero{position:relative;border-radius:22px;min-height:300px;padding:18px 16px 16px;display:flex;flex-direction:column;justify-content:flex-end;color:#fff}
.ah-ph{position:absolute;inset:0;border-radius:22px;overflow:hidden;background:#3a2b2d}
.ah-ph img{width:100%;height:100%;object-fit:cover;animation:ahKen 14s ease-out both}
.ah-ph:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,15,15,.05) 20%,rgba(30,18,20,.72) 100%)}
@keyframes ahKen{from{transform:scale(1.08)}to{transform:scale(1)}}
.ah-seal{position:absolute;right:14px;top:14px;width:64px;height:64px;border-radius:50%;background:rgba(255,255,255,.92);padding:3px;transform:rotate(-12deg);box-shadow:0 4px 14px rgba(0,0,0,.18)}
.ah-hero-t{position:relative;margin-bottom:14px}
.ah-hi{margin:0;font-size:13.5px;opacity:.92}
.app-home .ah-hero h2{margin:4px 0 6px;font-family:'Playfair Display',serif;font-size:26px;line-height:1.15;color:#fff;max-width:290px}
.ah-pl{margin:0;font-size:12px;opacity:.85;letter-spacing:.3px}
.ah-search{position:relative;display:flex;align-items:center;gap:10px;background:#fff;border-radius:999px;padding:0 16px;color:#8a7a7b;box-shadow:0 8px 24px rgba(0,0,0,.18)}
.ah-search input{flex:1;border:0;outline:0;background:none;font:inherit;font-size:15px;padding:13px 0;color:var(--ink);min-width:0}
.ah-search ul{position:absolute;left:0;right:0;top:calc(100% + 6px);z-index:60;list-style:none;margin:0;padding:6px;background:#fff;border:1px solid var(--line);border-radius:16px;box-shadow:0 14px 30px rgba(0,0,0,.14)}
.ah-search li a{display:block;padding:11px 12px;border-radius:10px;color:var(--ink);text-decoration:none;font-size:14.5px}.ah-search li a:active{background:#f6eeee}
.ah-search li.ah-ask a{color:var(--crimson);font-weight:600;border-top:1px solid var(--line);border-radius:0 0 10px 10px}
.ah-sec{display:flex;align-items:baseline;justify-content:space-between;margin:24px 2px 12px}
.ah-sec h3{margin:0;font-family:'Playfair Display',serif;font-size:19px;color:var(--wine)}.ah-sec a{font-size:13px;color:var(--crimson);text-decoration:none;font-weight:600}
.ah-stamps{display:grid;grid-template-columns:repeat(4,1fr);gap:16px 6px}
.ah-st{display:flex;flex-direction:column;align-items:center;gap:7px;text-decoration:none;color:#4a3b3c;font-size:12px;font-weight:600;text-align:center;line-height:1.15;-webkit-tap-highlight-color:transparent}
.ah-st i{display:grid;place-items:center;width:60px;height:60px;border-radius:50%;border:1.5px dashed #cfa9ac;color:#8f1d24;background:radial-gradient(circle,#fff 58%,#fbf4f4 59%);transition:transform .15s}
.ah-st i svg{width:26px;height:26px}.ah-st:active i{transform:scale(.92) rotate(-6deg)}
.ah-trust{display:flex;align-items:center;gap:12px;margin-top:22px;background:#faf6f6;border:1px solid #efe5e5;border-radius:16px;padding:12px 14px}
.ah-trust b{display:block;font-size:14px;color:var(--wine)}.ah-trust small{font-size:12px;color:#7a6a6b}
.ah-prog{display:flex;gap:4px;margin:0 2px 10px}.ah-prog i{flex:1;height:3px;border-radius:3px;background:#eadfe0;overflow:hidden}.ah-prog i b{display:block;height:100%;width:0;background:#8f1d24}
.ah-prog i.done b{width:100%}.ah-prog i.run b{animation:ahBar 5s linear forwards}@keyframes ahBar{to{width:100%}}
.ah-pcs{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -16px;padding:0 16px 4px;scrollbar-width:none;scroll-padding:0 16px}.ah-pcs::-webkit-scrollbar{display:none}
.ah-pc{flex:0 0 100%;scroll-snap-align:start;position:relative;height:230px;border-radius:20px;overflow:hidden;text-decoration:none;color:#fff;background:#4a2e32}
.ah-pc img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ah-pc:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 30%,rgba(25,15,17,.8) 100%)}
.ah-pc em{position:absolute;top:14px;right:14px;z-index:2;font-style:normal;font-size:10.5px;font-weight:700;letter-spacing:1.3px;text-transform:uppercase;padding:6px 10px;border:1.5px dashed rgba(255,255,255,.85);border-radius:8px;transform:rotate(4deg);background:rgba(0,0,0,.18)}
.ah-pc span{position:absolute;left:0;right:0;bottom:0;z-index:2;padding:16px;display:flex;flex-direction:column;gap:4px}
.ah-pc b{font-family:'Playfair Display',serif;font-size:22px;line-height:1.15}.ah-pc small{font-size:13px;opacity:.9;line-height:1.35}
.ah-pc i{font-style:normal;font-size:13px;font-weight:700;margin-top:4px;text-decoration:underline;text-underline-offset:3px}
.ah-cp{background:repeating-linear-gradient(135deg,#3e2a2e 0 14px,#46313a 14px 28px)}.ah-cp:after{display:none}.ah-cp u{text-decoration:none;font-weight:700;letter-spacing:1px;border:1px dashed rgba(255,255,255,.6);border-radius:6px;padding:1px 6px}
.ah-tks{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -16px;padding:0 16px 8px;scrollbar-width:none}.ah-tks::-webkit-scrollbar{display:none}
.ah-tk{flex:0 0 58%;max-width:230px;scroll-snap-align:start;display:flex;flex-direction:column;background:#fff;border:1px solid #ece3e3;border-radius:16px;overflow:hidden;text-decoration:none;color:var(--ink);box-shadow:0 6px 16px rgba(60,30,30,.06)}
.ah-tk img{width:100%;height:120px;object-fit:cover}
.ah-tk-b{position:relative;display:flex;flex-direction:column;gap:2px;padding:14px 13px 12px;border-top:2px dashed #e6d7d8}
.ah-tk-b:before,.ah-tk-b:after{content:"";position:absolute;top:-9px;width:16px;height:16px;border-radius:50%;background:#fff;border:1px solid #ece3e3}.ah-tk-b:before{left:-9px}.ah-tk-b:after{right:-9px}
.ah-tk b{font-size:14.5px;color:var(--wine);line-height:1.2}.ah-tk small{font-size:12px;color:#7a6a6b}.ah-tk i{font-style:normal;font-size:12.5px;font-weight:700;color:var(--crimson);margin-top:6px}
.ah-occ{display:flex;flex-direction:column;border:1px solid #efe5e5;border-radius:18px;overflow:hidden}
.ah-oc{display:flex;align-items:center;gap:12px;padding:10px 14px;text-decoration:none;color:var(--ink);border-bottom:1px solid #f4eded;background:#fff}.ah-oc:last-child{border-bottom:0}
.ah-oc img{width:52px;height:52px;border-radius:50%;object-fit:cover;flex:none;border:2px solid #fff;box-shadow:0 0 0 1.5px #e3cfd1}
.ah-oc span{flex:1;display:flex;flex-direction:column}.ah-oc b{font-size:14.5px;color:var(--wine)}.ah-oc small{font-size:12px;color:#7a6a6b}.ah-oc i{font-style:normal;color:#b9aeae;font-size:20px}
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
#splash{position:fixed;inset:0;z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#fff;transition:opacity .5s ease,transform .5s ease}
#splash.out{opacity:0;transform:scale(1.06);pointer-events:none}
.sp-stage{position:relative;width:220px;height:220px;display:grid;place-items:center}
.sp-logo{width:132px;height:132px;border-radius:50%;background:#fff;display:grid;place-items:center;animation:spGlow .9s ease .05s both}
.sp-logo img{width:118px;height:118px}
.sp-ring{position:absolute;inset:0}.sp-ring circle{fill:none;stroke:#d7191f;stroke-opacity:.28;stroke-width:1.5;stroke-dasharray:4 7;stroke-dashoffset:0;opacity:0;animation:spFade .35s ease .1s forwards}
.sp-orbit{position:absolute;inset:0;opacity:0;animation:spFade .25s ease .1s forwards,spSpin 1.5s cubic-bezier(.45,.05,.35,1) .1s forwards}
.sp-orbit svg{position:absolute;left:50%;top:-2px;width:26px;height:26px;margin-left:-13px;color:#b3121a;transform:rotate(90deg)}
.sp-txt{position:absolute;left:0;right:0;top:calc(50% + 120px);display:flex;flex-direction:column;align-items:center;text-align:center}.sp-name{margin:0;font-family:'Playfair Display',serif;font-size:23px;color:#b3121a;opacity:0;transform:translateY(10px);animation:spUp .5s ease .55s forwards}
.sp-tag{margin:6px 0 0;font-size:11.5px;letter-spacing:2.4px;color:#7a6a6b;text-transform:uppercase;opacity:0;transform:translateY(10px);animation:spUp .5s ease .75s forwards}
.sp-dots{display:flex;gap:6px;margin-top:26px;opacity:0;animation:spFade .3s ease 1s forwards}.sp-dots i{width:6px;height:6px;border-radius:50%;background:#d7191f;opacity:.25;animation:spDot 1s ease-in-out infinite}.sp-dots i:nth-child(2){animation-delay:.15s}.sp-dots i:nth-child(3){animation-delay:.3s}
@keyframes spGlow{from{box-shadow:0 0 0 0 #fbf1f1,0 0 0 rgba(179,18,26,0)}to{box-shadow:0 0 0 10px #fbf1f1,0 18px 40px rgba(179,18,26,.16)}}@keyframes spFade{to{opacity:1}}@keyframes spUp{to{opacity:1;transform:none}}
@keyframes spSpin{from{transform:rotate(0)}to{transform:rotate(360deg)}}@keyframes spDot{50%{opacity:.9;transform:translateY(-3px)}}
@media(prefers-reduced-motion:reduce){#splash *{animation-duration:.01s!important;animation-delay:0s!important}}
"""

# Runs in <head>: decide early whether to show the opening animation (no flash of the page underneath)
HEAD_JS = """<script>(function(){try{var u=new URLSearchParams(location.search),d=document.documentElement;
if(u.get('app')==='1')d.classList.add('is-app');
var app=matchMedia('(display-mode: standalone)').matches||navigator.standalone;
if(u.get('splash')==='1'||(app&&!sessionStorage.getItem('rtt_splash')))d.classList.add('splash-on');}catch(e){}})();</script>"""

# Runs right after <body>: shows the animation on the very first paint (no waiting for the page)
SPLASH_EARLY = """<script>(function(){var d=document.documentElement;if(!d.classList.contains('splash-on'))return;try{sessionStorage.setItem('rtt_splash','1')}catch(e){}
var s=document.createElement('div');s.id='splash';s.setAttribute('aria-hidden','true');
s.innerHTML='<div class="sp-stage"><svg class="sp-ring" viewBox="0 0 220 220"><circle cx="110" cy="110" r="100"/></svg><div class="sp-orbit"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z"/></svg></div><div class="sp-logo"><img src="/img/logo-512.png" alt="" width="118" height="118"></div></div><div class="sp-txt"><p class="sp-name">The Real Tours and Travels</p><p class="sp-tag">Estd. 1981 · All your travel needs</p><div class="sp-dots"><i></i><i></i><i></i></div></div>';
document.body.appendChild(s);d.classList.remove('splash-on');
var t0=Date.now(),rm=matchMedia('(prefers-reduced-motion: reduce)').matches,done=false;
function go(){if(done)return;done=true;s.classList.add('out');setTimeout(function(){s.remove()},550);}
function later(){setTimeout(go,Math.max(0,(rm?700:2100)-(Date.now()-t0)));}
if(document.readyState==='complete')later();else{addEventListener('load',later);setTimeout(go,5000);}
s.addEventListener('click',go);})();</script>"""

BODY_JS = ""
