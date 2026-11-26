"""Ready / fixed-price holiday packages page (/holiday-packages/). Data: packages.json."""
import json, os, html

def _load():
    return json.load(open(os.path.join(os.path.dirname(__file__), "packages.json")))["packages"]

def _inr(n):
    s = str(int(n)); last = s[-3:]; rest = s[:-3]
    parts = []
    while len(rest) > 2:
        parts.insert(0, rest[-2:]); rest = rest[:-2]
    if rest: parts.insert(0, rest)
    return "₹" + ",".join(parts + [last]) if parts else "₹" + last

def holiday_packages_page(root, wa_number, cta_band):
    pk = _load()
    cards = []
    for p in pk:
        e = html.escape
        days = p["nights"] + 1
        price = (f'<div class="hpprice"><small>Starting from</small><b>{_inr(p["price"])}</b><small>per person, twin sharing</small></div>'
                 if p.get("price") else '<div class="hpprice"><b class="hpreq">Price on request</b><small>per person</small></div>')
        msg = f'Hi The Real Tours and Travels, I am interested in the {p["name"]} package ({p["nights"]}N/{days}D). Travel date:  Travellers: '
        wa = f'https://wa.me/{wa_number}?text=' + __import__("urllib.parse").parse.quote(msg)
        cards.append(f'''<article class="hpcard" data-type="{p["type"]}" data-tags="{" ".join(p["tags"])}">
<div class="hpimg"><img src="{root}img/{p["img"]}.jpg" alt="{e(p["name"])}" loading="lazy" width="600" height="400"><span class="hpdur">{p["nights"]}N / {days}D</span></div>
<div class="hpbody"><h3>{e(p["name"])}</h3><p class="hproute">📍 {e(p["route"])}</p>
<ul class="hpinc">{"".join(f"<li>{e(x)}</li>" for x in p["inc"])}</ul>
<details class="hpdet"><summary>Highlights</summary><ul class="ticks">{"".join(f"<li>{e(x)}</li>" for x in p["highlights"])}</ul></details>
<div class="hpfoot">{price}<div class="hpbtn"><a class="btn gold" href="{wa}" target="_blank" rel="noopener">Book now</a><a class="btn outline" href="{root}customize-your-package/">Customise</a></div></div></div></article>''')
    filters = [("all", "All packages"), ("india", "India"), ("international", "International"), ("honeymoon", "Honeymoon"), ("family", "Family"), ("yatra", "Yatra")]
    fb = "".join(f'<button type="button" class="hpf{" on" if k == "all" else ""}" data-f="{k}">{t}</button>' for k, t in filters)
    return f"""<section class="hero"><div class="wrap"><div><div class="crumbs"><a href="{root}">Home</a> › Holiday Packages</div><h1>Holiday Packages</h1><p>Ready-made holiday packages with fixed itineraries – pick one, choose your date and book. Want something different? Use Customized Packages.</p></div></div></section>
<section class="hpsec"><div class="wrap">
<div class="hpfilters" role="tablist">{fb}</div>
<div class="hpgrid">{"".join(cards)}</div>
<p class="meta hpnote">Prices are per person on twin sharing and depend on travel dates, hotel availability and flights (flights not included unless mentioned). Our team confirms the final price before you pay. GST and TCS as applicable.</p>
</div></section>
<section><div class="wrap"><h2>Destination guides</h2><div class="tlinks">{"".join(f'<a class="tlink" href="{root}tours/{d["slug"]}/">{d["name"]}</a>' for d in __import__("tours").DEST)}</div></div></section>
<section class="alt"><div class="wrap" style="text-align:center"><h2>Want a different plan?</h2><p class="lead">Choose your own places, days, hotels and car – get an instant itinerary.</p><a class="btn gold" href="{root}customize-your-package/">Create a Customized Package</a></div></section>
{cta_band()}
<script>(function(){{const g=document.querySelector('.hpgrid');document.querySelectorAll('.hpf').forEach(b=>b.addEventListener('click',()=>{{document.querySelectorAll('.hpf').forEach(x=>x.classList.toggle('on',x===b));const f=b.dataset.f;g.querySelectorAll('.hpcard').forEach(c=>{{c.hidden=!(f==='all'||c.dataset.type===f||c.dataset.tags.split(' ').includes(f));}});}}));}})();</script>"""

CSS = """
.hpsec{padding-top:0!important}
.hpfilters{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:0 0 22px;background:#fff;border:1px solid var(--line);border-radius:16px;padding:12px;box-shadow:0 10px 30px rgba(60,20,25,.08)}
.hpf{border:1px solid var(--line);background:#fff;border-radius:999px;padding:8px 18px;font:600 14.5px 'Jost',sans-serif;color:#555;cursor:pointer}
.hpf.on{background:var(--wine);border-color:var(--wine);color:#fff}.hpf:hover:not(.on){border-color:var(--wine);color:var(--wine)}
.hpgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}
.hpcard{background:#fff;border:1px solid var(--line);border-radius:18px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 6px 18px rgba(60,20,25,.05)}
.hpcard[hidden]{display:none}
.hpimg{position:relative;aspect-ratio:3/2;overflow:hidden}.hpimg img{width:100%;height:100%;object-fit:cover;display:block}
.hpdur{position:absolute;left:12px;top:12px;background:rgba(255,255,255,.94);color:var(--wine);font-weight:700;font-size:13px;padding:4px 10px;border-radius:999px}
.hpbody{padding:16px;display:flex;flex-direction:column;gap:10px;flex:1}
.hpbody h3{margin:0;font-family:'Playfair Display',serif;font-size:21px;color:var(--ink)}
.hproute{margin:0;font-size:14px;color:var(--muted)}
.hpinc{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px}.hpinc li{font-size:12.5px;background:var(--bg);border:1px solid var(--line);border-radius:999px;padding:3px 10px}
.hpdet summary{cursor:pointer;font-weight:600;color:var(--wine);font-size:14.5px}.hpdet ul{margin:8px 0 0;font-size:14px}
.hpfoot{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;gap:10px;flex-wrap:wrap;border-top:1px dashed var(--line);padding-top:12px}
.hpprice{display:grid}.hpprice small{font-size:12px;color:var(--muted)}.hpprice b{font-size:22px;color:var(--ink)}.hpprice b.hpreq{font-size:17px;color:var(--wine)}
.hpbtn{display:flex;gap:8px}.hpbtn .btn{padding:9px 16px;font-size:14px}
.hpnote{margin-top:18px;text-align:center}
"""
