"""Installable app (PWA): manifest, service worker, install button and offline page."""
import json

VERSION = "rtt-v10"

def manifest(NAME):
    return json.dumps({
        "name": NAME,
        "short_name": "Real Tours",
        "description": "Holidays, flights, hotels, cruises, visas and passports – The Real Tours and Travels. Serving travellers across India since 1981.",
        "id": "/",
        "start_url": "/?source=app",
        "scope": "/",
        "display": "standalone",
        "orientation": "portrait",
        "background_color": "#ffffff",
        "theme_color": "#D7191F",
        "lang": "en-IN",
        "categories": ["travel", "lifestyle"],
        "icons": [
            {"src": "/img/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "/img/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "/img/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
        "shortcuts": [
            {"name": "Flights, Hotels & Cruise", "short_name": "Book travel", "url": "/flights-hotels/?source=app", "icons": [{"src": "/img/icon-192.png", "sizes": "192x192"}]},
            {"name": "Customized Packages", "short_name": "Plan a trip", "url": "/customize-your-package/?source=app", "icons": [{"src": "/img/icon-192.png", "sizes": "192x192"}]},
            {"name": "Visa services", "short_name": "Visa", "url": "/visa/?source=app", "icons": [{"src": "/img/icon-192.png", "sizes": "192x192"}]},
            {"name": "Travel insurance quote", "short_name": "Insurance", "url": "/insurance/?source=app", "icons": [{"src": "/img/icon-192.png", "sizes": "192x192"}]},
            {"name": "Passport services", "short_name": "Passport", "url": "/passport/?source=app", "icons": [{"src": "/img/icon-192.png", "sizes": "192x192"}]},
        ],
    }, ensure_ascii=False, indent=1)

def service_worker(urls, cssv):
    pre = ["/", "/offline/", "/style.css?v=" + cssv, "/img/logo.png", "/img/icon-192.png", "/favicon.png"] + [u for u in urls if u != "/"]
    return f"""// The Real Tours and Travels – app service worker
const CACHE='{VERSION}';
const PRECACHE={json.dumps(pre)};
self.addEventListener('install',e=>{{e.waitUntil(caches.open(CACHE).then(c=>Promise.allSettled(PRECACHE.map(u=>c.add(u)))).then(()=>self.skipWaiting()));}});
self.addEventListener('activate',e=>{{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==CACHE).map(x=>caches.delete(x)))).then(()=>self.clients.claim()));}});
self.addEventListener('fetch',e=>{{
  const r=e.request,u=new URL(r.url);
  if(r.method!=='GET'||u.origin!==location.origin)return; // never touch Supabase, Razorpay, WhatsApp or form submissions
  if(r.mode==='navigate'){{ // pages: network first, fall back to cache, then offline page
    e.respondWith(fetch(r).then(res=>{{const c=res.clone();caches.open(CACHE).then(x=>x.put(r,c));return res;}})
      .catch(()=>caches.match(r,{{ignoreSearch:true}}).then(m=>m||caches.match('/offline/'))));return;
  }}
  e.respondWith(caches.match(r).then(m=>{{const net=fetch(r).then(res=>{{if(res.ok){{const c=res.clone();caches.open(CACHE).then(x=>x.put(r,c));}}return res;}}).catch(()=>m);return m||net;}}));
}});
"""

def offline_body(PHONE, PHONE_RAW, WA):
    return f"""<section style="padding:70px 0"><div class="wrap" style="max-width:640px;text-align:center">
<img src="/img/logo.png" alt="" width="110" height="110" style="margin:0 auto 18px">
<h1 style="font-size:32px;color:var(--wine)">You're offline</h1>
<p class="lead">Please check your internet connection and try again. You can still call or WhatsApp us.</p>
<div class="btns" style="justify-content:center;margin-top:20px"><a class="btn gold" href="tel:{PHONE_RAW}">📞 Call {PHONE}</a><a class="btn ghost" href="{WA}">💬 WhatsApp</a><a class="btn outline" href="/">Try again</a></div>
</div></section>"""

HEAD = """<script>if(matchMedia('(display-mode: standalone)').matches||navigator.standalone)document.documentElement.classList.add('is-app');</script>
<link rel="manifest" href="/manifest.webmanifest">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default"><meta name="apple-mobile-web-app-title" content="Real Tours">"""

# Install button + iPhone instructions + service-worker registration
BODY = """<nav class="appbar" aria-label="App">
<a href="/"><span>🏠</span>Home</a><a href="/flights-hotels/#flights"><span>✈️</span>Book</a><a href="/customize-your-package/"><span>✨</span>Plan</a><a href="/visa/"><span>🛂</span>Visa</a><a href="/account/"><span>👤</span>Login</a><a href="https://wa.me/919843121212" target="_blank" rel="noopener"><span>💬</span>Chat</a></nav>
<button type="button" class="app-install" id="appInstall" hidden>📲 Install app</button>
<div class="ios-tip" id="iosTip" hidden role="dialog" aria-label="Install on iPhone"><button type="button" class="ios-x" aria-label="Close">✕</button>
<b>Install The Real Tours and Travels app</b><ol class="ios-steps" id="iosSteps"><li>Tap <b>•••</b> at the bottom-right of Safari, then tap <span class="ios-share">⬆︎</span> <b>Share</b>. (Older iPhones: tap the <span class="ios-share">⬆︎</span> Share button in the bottom bar.)</li><li>Scroll down and tap <b>Add to Home Screen</b>.</li><li>Keep <b>Open as Web App</b> switched on if you see it, then tap <b>Add</b>.</li></ol><p class="ios-inapp" id="iosInapp" hidden>You are inside the Instagram / Facebook / WhatsApp browser. Tap <b>•••</b> and choose <b>Open in Safari</b> (or Open in browser) first, then follow the steps.</p></div>
<div class="ios-arrow" id="iosArrow" hidden aria-hidden="true">⬇</div>
<script>
(function(){
 if('serviceWorker' in navigator)window.addEventListener('load',()=>navigator.serviceWorker.register('/sw.js').catch(()=>{}));
 const btn=document.getElementById('appInstall'),tip=document.getElementById('iosTip');
 const standalone=matchMedia('(display-mode: standalone)').matches||navigator.standalone;
 if(standalone){document.documentElement.classList.add('is-app');
  if(location.pathname!=='/'){const r=document.querySelector('header.site .hrow');if(r){const k=document.createElement('button');k.type='button';k.className='app-back';k.setAttribute('aria-label','Back');k.textContent='‹';k.onclick=()=>{if(history.length>1&&document.referrer.indexOf(location.host)>-1)history.back();else location.href='/';};r.prepend(k);}}
  const here=location.pathname;document.querySelectorAll('.appbar a').forEach(a=>{const h=new URL(a.href,location).pathname;if(h===here||(h!=='/'&&here.startsWith(h)))a.classList.add('on');});return;}
 let dismissed=false;try{dismissed=localStorage.getItem('rtt_app_x')==='1';}catch(_){}
 let ev=null;
 addEventListener('beforeinstallprompt',e=>{e.preventDefault();ev=e;btn.hidden=false;});
 btn.addEventListener('click',async e=>{e.stopPropagation();if(ev){ev.prompt();await ev.userChoice;ev=null;btn.hidden=true;}else{tip.hidden=!tip.hidden;btn.classList.toggle('open',!tip.hidden);const ar=document.getElementById('iosArrow');if(ar&&ios&&!inapp)ar.hidden=tip.hidden;}});
 document.addEventListener('click',e=>{if(!tip.hidden&&!tip.contains(e.target)&&e.target!==btn){tip.hidden=true;btn.classList.remove('open');const ar=document.getElementById('iosArrow');if(ar)ar.hidden=true;}});
 const ua=navigator.userAgent;
 const ios=/iphone|ipad|ipod/i.test(ua)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
 const inapp=/FBAN|FBAV|Instagram|Line\\/|WhatsApp|Snapchat/i.test(ua);
 const iv=+((ua.match(/Version\/(\d+)/)||[])[1]||0);if(ios&&iv&&iv<26)document.getElementById('iosArrow').classList.add('mid');
 if(ios){btn.hidden=false;document.getElementById('iosInapp').hidden=!inapp;
  if(/crios|edgios|fxios/i.test(ua))document.getElementById('iosSteps').firstElementChild.innerHTML='Tap the <span class="ios-share">⬆︎</span> <b>Share</b> button at the top-right, next to the address bar.';}
 tip.querySelector('.ios-x').addEventListener('click',()=>{tip.hidden=true;document.getElementById('iosArrow').hidden=true;btn.hidden=true;try{localStorage.setItem('rtt_app_x',String(Date.now()));}catch(_){}});
 // a dismissed button comes back after 7 days
 try{const t=+localStorage.getItem('rtt_app_x');dismissed=t>1&&Date.now()-t<7*864e5;}catch(_){}
 if(dismissed&&ios)btn.hidden=true;
 addEventListener('appinstalled',()=>{btn.hidden=true;});
})();
</script>"""

CSS = """
.app-install{position:fixed;left:16px;bottom:18px;z-index:60;border:0;background:#fff;color:var(--crimson);font:600 15px 'Jost',sans-serif;padding:12px 18px;border-radius:999px;box-shadow:0 8px 22px rgba(0,0,0,.18);border:1.5px solid var(--red);cursor:pointer}
.app-install[hidden],.ios-tip[hidden]{display:none!important}.app-install.open{background:var(--red);color:#fff}
.ios-tip{position:fixed;left:12px;right:12px;bottom:84px;z-index:70;background:#fff;border:1px solid var(--line);border-top:5px solid var(--red);border-radius:16px;padding:16px 18px;box-shadow:0 16px 40px rgba(0,0,0,.2)}
.ios-tip p{margin:6px 0 0;color:var(--muted)}.ios-steps{margin:8px 0 0;padding-left:20px;color:var(--ink);font-size:14.5px}.ios-steps li{margin:4px 0}.ios-inapp{background:#fdf0f0;border-radius:10px;padding:8px 10px;color:var(--crimson)!important;font-size:13.5px}.ios-share{display:inline-block;border:1px solid var(--line);border-radius:6px;padding:0 6px;color:#0a84ff}
.ios-x{position:absolute;right:10px;top:8px;border:0;background:none;font-size:18px;color:var(--muted);cursor:pointer}
html.is-app .topbar,html.is-app .float-wa,html.is-app .app-install,html.is-app .hcta{display:none!important}
.appbar{display:none}
html.is-app .appbar{display:grid;grid-template-columns:repeat(6,1fr);position:fixed;left:0;right:0;bottom:0;z-index:80;background:#fff;border-top:1px solid var(--line);box-shadow:0 -6px 18px rgba(0,0,0,.06);padding:6px 4px calc(6px + env(safe-area-inset-bottom))}
.appbar a{display:flex;flex-direction:column;align-items:center;gap:2px;text-decoration:none;color:var(--muted);font-size:11.5px;font-weight:600}.appbar a span{font-size:20px;line-height:1}.appbar a.on{color:var(--red)}
html.is-app body{padding-bottom:calc(64px + env(safe-area-inset-bottom))}
html.is-app .hero .seal{display:none}html.is-app .hero .wrap{padding-top:22px!important;padding-bottom:30px!important}html.is-app .fsec{margin-top:0}
@media(max-width:700px){.float-wa{bottom:16px;right:12px;width:50px;height:50px;font-size:22px}main .btns{padding-right:0}}

.ios-arrow{position:fixed;right:22px;bottom:6px;z-index:75;font-size:40px;color:var(--red);text-shadow:0 2px 8px rgba(0,0,0,.25);animation:iosb 1s ease-in-out infinite}.ios-arrow.mid{right:auto;left:50%;margin-left:-16px}.ios-arrow[hidden]{display:none!important}@keyframes iosb{0%,100%{transform:translateY(0)}50%{transform:translateY(10px)}}
/* iPhone fixes */
@supports(-webkit-touch-callout:none){input,select,textarea{font-size:16px!important}}
html.is-app header.site{padding-top:env(safe-area-inset-top)}
html.is-app header.site .wrap,html.is-app main,html.is-app footer{padding-left:max(18px,env(safe-area-inset-left));padding-right:max(18px,env(safe-area-inset-right))}
html.is-app{-webkit-tap-highlight-color:transparent}html.is-app body{overscroll-behavior-y:none;-webkit-text-size-adjust:100%}
html.is-app .appbar{padding-left:env(safe-area-inset-left);padding-right:env(safe-area-inset-right)}
.app-back{display:none}html.is-app .app-back{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;margin-right:6px;border:1px solid var(--line);border-radius:50%;background:#fff;color:var(--red);font-size:28px;line-height:1;padding:0 0 3px;cursor:pointer;flex:none}
@media print{.app-install,.ios-tip{display:none!important}}
"""
