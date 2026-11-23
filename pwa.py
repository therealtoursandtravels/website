"""Installable app (PWA): manifest, service worker, install button and offline page."""
import json

VERSION = "rtt-v1"

def manifest(NAME):
    return json.dumps({
        "name": NAME,
        "short_name": "Real Tours",
        "description": "Holidays, flights, hotels, cruises, visas and passports – The Real Tours and Travels, Mulund West, Mumbai. Since 1981.",
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
            {"name": "Customize your package", "short_name": "Plan a trip", "url": "/customize-your-package/?source=app", "icons": [{"src": "/img/icon-192.png", "sizes": "192x192"}]},
            {"name": "Visa services", "short_name": "Visa", "url": "/visa/?source=app", "icons": [{"src": "/img/icon-192.png", "sizes": "192x192"}]},
            {"name": "Passport services", "short_name": "Passport", "url": "/passport/?source=app", "icons": [{"src": "/img/icon-192.png", "sizes": "192x192"}]},
        ],
    }, ensure_ascii=False, indent=1)

def service_worker(urls):
    pre = ["/", "/offline/", "/style.css", "/img/logo.png", "/img/icon-192.png", "/favicon.png"] + [u for u in urls if u != "/"]
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

HEAD = """<link rel="manifest" href="/manifest.webmanifest">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default"><meta name="apple-mobile-web-app-title" content="Real Tours">"""

# Install button + iPhone instructions + service-worker registration
BODY = """<button type="button" class="app-install" id="appInstall" hidden>📲 Install app</button>
<div class="ios-tip" id="iosTip" hidden role="dialog" aria-label="Install on iPhone"><button type="button" class="ios-x" aria-label="Close">✕</button>
<b>Install The Real Tours and Travels app</b><p>Tap <span class="ios-share">⬆︎</span> <b>Share</b> at the bottom of Safari, then <b>Add to Home Screen</b>.</p></div>
<script>
(function(){
 if('serviceWorker' in navigator)window.addEventListener('load',()=>navigator.serviceWorker.register('/sw.js').catch(()=>{}));
 const btn=document.getElementById('appInstall'),tip=document.getElementById('iosTip');
 const standalone=matchMedia('(display-mode: standalone)').matches||navigator.standalone;
 if(standalone){document.documentElement.classList.add('is-app');return;}
 let dismissed=false;try{dismissed=localStorage.getItem('rtt_app_x')==='1';}catch(_){}
 let ev=null;
 addEventListener('beforeinstallprompt',e=>{e.preventDefault();ev=e;btn.hidden=false;});
 btn.addEventListener('click',async()=>{if(ev){ev.prompt();await ev.userChoice;ev=null;btn.hidden=true;}else{tip.hidden=false;}});
 const ios=/iphone|ipad|ipod/i.test(navigator.userAgent)&&!/crios|fxios/i.test(navigator.userAgent);
 if(ios){btn.hidden=false;}
 tip.querySelector('.ios-x').addEventListener('click',()=>{tip.hidden=true;btn.hidden=true;try{localStorage.setItem('rtt_app_x','1');}catch(_){}});
 if(dismissed&&ios)btn.hidden=true;
 addEventListener('appinstalled',()=>{btn.hidden=true;});
})();
</script>"""

CSS = """
.app-install{position:fixed;left:16px;bottom:18px;z-index:60;border:0;background:#fff;color:var(--crimson);font:600 15px 'Jost',sans-serif;padding:12px 18px;border-radius:999px;box-shadow:0 8px 22px rgba(0,0,0,.18);border:1.5px solid var(--red);cursor:pointer}
.app-install[hidden],.ios-tip[hidden]{display:none!important}
.ios-tip{position:fixed;left:12px;right:12px;bottom:84px;z-index:70;background:#fff;border:1px solid var(--line);border-top:5px solid var(--red);border-radius:16px;padding:16px 18px;box-shadow:0 16px 40px rgba(0,0,0,.2)}
.ios-tip p{margin:6px 0 0;color:var(--muted)}.ios-share{display:inline-block;border:1px solid var(--line);border-radius:6px;padding:0 6px;color:#0a84ff}
.ios-x{position:absolute;right:10px;top:8px;border:0;background:none;font-size:18px;color:var(--muted);cursor:pointer}
html.is-app .topbar{display:none}
@media print{.app-install,.ios-tip{display:none!important}}
"""
