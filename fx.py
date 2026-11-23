"""Site-wide visual effects: 3D scroll reveal, hero parallax, tilt on gallery tiles,
rotating Google reviews carousel and the Jain Yatra pop-up."""
import json, os

def load_reviews():
    p = os.path.join(os.path.dirname(__file__), "reviews.json")
    try:
        return json.load(open(p))
    except Exception:
        return {"rating": 4.8, "total": 0, "reviews": []}

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def reviews_carousel(maps_url, review_url, kicker=True):
    R = load_reviews()
    cards = "".join(
        f'<figure class="review rv"><div class="stars" aria-label="{r.get("stars",5)} stars">{"★"*int(r.get("stars",5))}</div>'
        f'<blockquote>“{esc(r["text"])}”</blockquote><figcaption><b>— {esc(r["name"])}</b><span>Google review</span></figcaption></figure>'
        for r in R["reviews"])
    total = f' from {R["total"]} reviews' if R.get("total") else ""
    return f"""<section class="revsec"><div class="wrap"><div class="head"><span class="kicker">Reviews</span><h2>What our travellers say</h2>
<p class="lead"><span class="gstar">★ {R["rating"]}</span> on Google{total}</p></div>
<div class="rcar" data-rcar><button type="button" class="rnav rprev" aria-label="Previous review">‹</button><div class="rtrack" tabindex="0">{cards}</div><button type="button" class="rnav rnext" aria-label="Next review">›</button></div>
<p style="margin-top:24px;text-align:center"><a class="btn outline" href="{maps_url}" target="_blank" rel="noopener">Read all reviews on Google</a> <a class="btn gold" href="{review_url}" target="_blank" rel="noopener">⭐ Write a review</a></p></div></section>"""

GALLERY = [
    ("g-maldives.jpg", "Maldives", "Overwater villas in the Maldives", 900, 600),
    ("g-swiss.jpg", "Switzerland", "Lake village in the Swiss Alps", 900, 600),
    ("g-taj.jpg", "Agra", "The Taj Mahal, Agra", 900, 433),
    ("g-dubai.jpg", "Dubai", "Dubai skyline with the Burj Khalifa", 900, 515),
    ("g-kerala.jpg", "Kerala", "Houseboat on the Kerala backwaters", 900, 599),
    ("g-bali.jpg", "Bali", "Rice terraces and palms in Bali", 900, 1200),
    ("g-jaipur.jpg", "Jaipur", "Hawa Mahal in Jaipur, Rajasthan", 900, 600),
    ("gulmarg.jpg", "Kashmir", "Snow-covered Gulmarg in Kashmir", 1200, 744),
]

def gallery(root=""):
    tiles = "".join(f'<a class="gtile rv" href="{root}customize-your-package/" aria-label="Plan a trip to {c}"><img src="{root}img/{f}" alt="{a}" loading="lazy" width="{w}" height="{h}"><span>{c}</span></a>' for f, c, a, w, h in GALLERY)
    return f"""<section class="gsec"><div class="wrap"><div class="head"><span class="kicker">Destinations</span><h2>Where will you go next?</h2><p class="lead">A few of the places we plan trips to – tap any destination to start your own itinerary.</p></div>
<div class="gallery">{tiles}</div></div></section>"""

def jain_popup(root):
    return f"""<div class="jpop" id="jpop" role="dialog" aria-modal="false" aria-labelledby="jpopT" hidden>
<button type="button" class="jpx" aria-label="Close">✕</button>
<img src="{root}img/jain.jpg" alt="Jain tirth yatra" width="320" height="180" loading="lazy">
<div class="jpb"><span class="kicker">🙏 Jain Yatra with Maharaj</span><b id="jpopT">Tirth yatras with pure Jain food cooked fresh every day</b>
<p>Palitana, Sammed Shikharji, Girnar and more – senior-friendly pacing, chovihar timings respected.</p>
<div class="btns"><a class="btn gold" href="{root}jain-yatra-tours-with-maharaj/">Explore Jain Yatras</a><a class="btn outline" href="{root}jain-yatra-tours-with-maharaj/#upcoming">Upcoming group yatras</a></div></div></div>"""

JS = """<script>
(function(){
 const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
 // 3D scroll reveal
 const sel='.card,.review,.gtile,.yexp>div,.head,.ticks li,.iday,.vpanel:not([hidden]),.sform,.fbar,.trust>div,.yd,.ynone';
 const els=[...document.querySelectorAll(sel)].filter(e=>!e.closest('.jpop'));
 if(!reduce&&'IntersectionObserver' in window){
  els.forEach((e,i)=>{e.classList.add('rv3');e.style.setProperty('--d',(i%4)*70+'ms');});
  const io=new IntersectionObserver(es=>es.forEach(x=>{if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}}),{rootMargin:'0px 0px -8% 0px',threshold:.08});
  els.forEach(e=>io.observe(e));
  // gentle hero parallax
  const hero=document.querySelector('.hero');
  if(hero){let t=0;addEventListener('scroll',()=>{if(t)return;t=requestAnimationFrame(()=>{t=0;const y=Math.min(scrollY,700);hero.style.setProperty('--py',(y*0.25)+'px');hero.style.setProperty('--ps',(1+y/4000));});},{passive:true});}
  // 3D tilt on gallery tiles and cards (pointer devices only)
  if(matchMedia('(hover:hover)').matches){document.querySelectorAll('.gtile,.card').forEach(t=>{
   t.addEventListener('pointermove',e=>{const r=t.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;t.style.setProperty('--rx',(-y*7)+'deg');t.style.setProperty('--ry',(x*9)+'deg');t.classList.add('tilt');});
   t.addEventListener('pointerleave',()=>{t.classList.remove('tilt');t.style.removeProperty('--rx');t.style.removeProperty('--ry');});});}
 }
 // reviews carousel: auto-rotates, pauses on hover/touch
 document.querySelectorAll('[data-rcar]').forEach(c=>{const tr=c.querySelector('.rtrack');if(!tr)return;
  const step=d=>{const card=tr.querySelector('.review');const w=card?card.getBoundingClientRect().width+18:300;const end=tr.scrollLeft+tr.clientWidth>=tr.scrollWidth-8;
   if(d>0&&end)tr.scrollTo({left:0,behavior:reduce?'auto':'smooth'});else if(d<0&&tr.scrollLeft<8)tr.scrollTo({left:tr.scrollWidth,behavior:reduce?'auto':'smooth'});else tr.scrollBy({left:d*w,behavior:reduce?'auto':'smooth'});};
  c.querySelector('.rnext').onclick=()=>step(1);c.querySelector('.rprev').onclick=()=>step(-1);
  let pause=false;['pointerenter','touchstart','focusin'].forEach(ev=>c.addEventListener(ev,()=>pause=true,{passive:true}));['pointerleave','focusout'].forEach(ev=>c.addEventListener(ev,()=>pause=false));
  if(!reduce)setInterval(()=>{if(!pause&&!document.hidden)step(1);},5500);});
 // Jain Yatra pop-up: once per visit, after 8 s or half-way down the page
 const jp=document.getElementById('jpop');
 if(jp&&!/jain-yatra/.test(location.pathname)&&!document.documentElement.classList.contains('is-app')){
  let seen=false;try{seen=sessionStorage.getItem('rtt_jpop')==='1';}catch(_){}
  if(!seen){let shown=false;const show=()=>{if(shown)return;shown=true;jp.hidden=false;requestAnimationFrame(()=>jp.classList.add('on'));try{sessionStorage.setItem('rtt_jpop','1');}catch(_){}};
   const close=()=>{jp.classList.remove('on');setTimeout(()=>jp.hidden=true,300);};
   setTimeout(show,8000);addEventListener('scroll',()=>{if(scrollY>document.body.scrollHeight*0.45)show();},{passive:true});
   jp.querySelector('.jpx').onclick=close;addEventListener('keydown',e=>{if(e.key==='Escape'&&!jp.hidden)close();});}
 }
})();
</script>"""

CSS = """
.rv3{opacity:0;transform:perspective(1000px) rotateX(14deg) translateY(34px) scale(.98);transform-origin:50% 100%;transition:opacity .7s ease var(--d,0ms),transform .8s cubic-bezier(.2,.7,.2,1) var(--d,0ms)}
.rv3.in{opacity:1;transform:none}
.card,.gtile{transform-style:preserve-3d}
.card.tilt,.gtile.tilt{transform:perspective(900px) rotateX(var(--rx,0)) rotateY(var(--ry,0)) translateZ(0);transition:transform .12s ease}
.hero:before{transform:translateY(var(--py,0)) scale(var(--ps,1));will-change:transform}
@media (prefers-reduced-motion: reduce){.rv3{opacity:1!important;transform:none!important;transition:none!important}}
/* home hero with a visible travel photo */
.hero.home-hero:before{opacity:1;background-position:center 40%}
.hero.home-hero:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(255,255,255,.96) 0%,rgba(255,255,255,.88) 42%,rgba(255,255,255,.25) 75%,rgba(255,255,255,0) 100%);pointer-events:none}
.hero.home-hero>.wrap{position:relative;z-index:1}
.hero.home-hero .seal{box-shadow:0 20px 60px rgba(0,0,0,.25)}
@media(max-width:900px){.hero.home-hero:before{background-position:72% top;background-size:auto 62%}.hero.home-hero:after{background:linear-gradient(180deg,rgba(255,255,255,0) 0%,rgba(255,255,255,.15) 30%,rgba(255,255,255,.94) 46%,#fff 56%)}}
/* inner pages: let the photo show instead of the big seal */
.hero.photo-hero .seal{display:none}
.hero.photo-hero:after{background:linear-gradient(90deg,rgba(255,255,255,.97) 0%,rgba(255,255,255,.9) 40%,rgba(255,255,255,.2) 72%,rgba(255,255,255,0) 100%)}
@media(max-width:900px){.hero.home-hero.photo-hero:before{inset:0 0 auto 0;height:230px;background-size:cover;background-position:center}
.hero.home-hero.photo-hero:after{background:linear-gradient(180deg,rgba(255,255,255,0) 0,rgba(255,255,255,0) 170px,#fff 232px)}
.hero.photo-hero>.wrap{padding-top:230px!important}}
/* photo service cards */
.card.pcard{padding:0;overflow:hidden;display:flex;flex-direction:column}
.card.pcard .cimg{width:100%;height:170px;object-fit:cover;display:block;transition:transform .6s ease}
.card.pcard:hover .cimg{transform:scale(1.05)}
.card.pcard .ic{margin:-26px 0 0 18px;position:relative;z-index:1;background:#fff;box-shadow:0 6px 16px rgba(0,0,0,.12)}
.card.pcard h3,.card.pcard p,.card.pcard .more{margin-left:20px;margin-right:20px}.card.pcard .more{margin-bottom:20px}
/* gallery */
.gallery{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:200px;gap:14px;grid-auto-flow:dense}
.gtile{position:relative;overflow:hidden;border-radius:18px;display:block;box-shadow:0 10px 26px rgba(0,0,0,.10)}
.gtile img{width:100%;height:100%;object-fit:cover;transition:transform .6s ease}
.gtile:hover img{transform:scale(1.06)}
.gtile span{position:absolute;left:12px;bottom:12px;background:rgba(255,255,255,.94);color:var(--crimson);font-weight:600;padding:6px 14px;border-radius:999px;font-size:14.5px;transform:translateZ(30px)}
.gtile:nth-child(1){grid-column:span 2;grid-row:span 2}.gtile:nth-child(6){grid-column:4;grid-row:2 / span 2}
@media(max-width:900px){.gallery{grid-template-columns:1fr 1fr;grid-auto-rows:150px}.gtile:nth-child(6){grid-column:auto;grid-row:span 2}}
/* reviews carousel */
.rcar{position:relative}
.rtrack{display:grid;grid-auto-flow:column;grid-auto-columns:calc((100% - 36px)/3);gap:18px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;padding:6px 2px 10px}
.rtrack::-webkit-scrollbar{display:none}
.rtrack .review{scroll-snap-align:start;margin:0;display:flex;flex-direction:column}
.rtrack blockquote{margin:10px 0 14px;font-family:'Playfair Display',serif;font-style:italic;font-size:17px;color:#3b2f2f;display:-webkit-box;-webkit-line-clamp:7;-webkit-box-orient:vertical;overflow:hidden}
.rtrack figcaption{margin-top:auto;display:flex;flex-direction:column}.rtrack figcaption span{font-size:12.5px;color:var(--muted)}
.rnav{position:absolute;top:50%;transform:translateY(-50%);z-index:2;width:42px;height:42px;border-radius:50%;border:1px solid var(--line);background:#fff;color:var(--crimson);font-size:24px;line-height:1;cursor:pointer;box-shadow:0 6px 16px rgba(0,0,0,.1)}
.rprev{left:-14px}.rnext{right:-14px}
.gstar{color:var(--red);font-weight:700}
@media(max-width:900px){.rtrack{grid-auto-columns:85%}.rprev{left:-6px}.rnext{right:-6px}}
/* Jain yatra pop-up */
.jpop{position:fixed;right:18px;bottom:88px;z-index:90;width:340px;max-width:calc(100vw - 24px);background:#fff;border-radius:20px;overflow:hidden;box-shadow:0 24px 60px rgba(0,0,0,.25);border-top:5px solid var(--red);opacity:0;transform:translateY(24px) scale(.96);transition:opacity .3s ease,transform .3s ease}
.jpop.on{opacity:1;transform:none}.jpop[hidden]{display:none}
.jpop img{width:100%;height:150px;object-fit:cover;display:block}
.jpb{padding:14px 18px 18px}.jpb b{display:block;font-family:'Playfair Display',serif;font-size:19px;line-height:1.3;color:var(--ink);margin:6px 0}
.jpb p{margin:0 0 12px;font-size:14px;color:var(--muted)}.jpb .btns{gap:8px}.jpb .btn{padding:9px 14px;font-size:14px}
.jpx{position:absolute;top:8px;right:8px;width:32px;height:32px;border-radius:50%;border:0;background:rgba(255,255,255,.92);font-size:16px;cursor:pointer;color:var(--ink)}
@media(max-width:600px){.jpop{left:12px;right:12px;bottom:78px;width:auto}.jpop img{display:none}.jpb{padding:12px 44px 14px 16px}.jpb b{font-size:16.5px;margin:4px 0}.jpb p{display:none}.jpb .btns{flex-direction:row;flex-wrap:wrap}.jpb .btn{width:auto!important;flex:1 1 auto;padding:8px 10px;font-size:13.5px}}
@media print{.jpop{display:none!important}}
"""
