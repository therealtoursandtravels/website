// The Real Tours and Travels – app service worker
const CACHE='rtt-v4';
const PRECACHE=["/", "/offline/", "/style.css?v=0c4f5e1d", "/img/logo.png", "/img/icon-192.png", "/favicon.png", "/domestic-holiday-packages/", "/international-holiday-packages/", "/passport-visa-services/", "/travel-insurance/", "/yatra-tours/", "/group-tours/", "/honeymoon-packages/", "/customised-tours/", "/fit-mice-tours/", "/jain-yatra-tours-with-maharaj/", "/blog/", "/visa/", "/passport/", "/insurance/", "/about/", "/flights-hotels/", "/customize-your-package/", "/blog/best-december-holidays-from-mumbai/", "/blog/jain-yatra-guide-tirths-and-jain-food/", "/blog/passport-and-visa-checklist-for-indian-travellers/", "/blog/why-travel-insurance-matters/", "/contact/", "/terms/", "/privacy-policy/", "/cancellation-refund-policy/"];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>Promise.allSettled(PRECACHE.map(u=>c.add(u)))).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==CACHE).map(x=>caches.delete(x)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{
  const r=e.request,u=new URL(r.url);
  if(r.method!=='GET'||u.origin!==location.origin)return; // never touch Supabase, Razorpay, WhatsApp or form submissions
  if(r.mode==='navigate'){ // pages: network first, fall back to cache, then offline page
    e.respondWith(fetch(r).then(res=>{const c=res.clone();caches.open(CACHE).then(x=>x.put(r,c));return res;})
      .catch(()=>caches.match(r,{ignoreSearch:true}).then(m=>m||caches.match('/offline/'))));return;
  }
  e.respondWith(caches.match(r).then(m=>{const net=fetch(r).then(res=>{if(res.ok){const c=res.clone();caches.open(CACHE).then(x=>x.put(r,c));}return res;}).catch(()=>m);return m||net;}));
});
