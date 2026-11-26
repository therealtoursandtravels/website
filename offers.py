"""Offers & rewards page (/offers/): welcome bonus, refer & earn, points per service, live coupon codes (from Supabase)."""
from visa import SB_URL, SB_KEY

POINTS = [("Holiday / customised package", 500), ("Cruise booking", 250), ("Flight booking", 100), ("Hotel booking", 100),
          ("Visa", 50), ("Passport", 50), ("Travel insurance", 25)]

def offers_page(root, cta_band):
    rows = "".join(f'<tr><td>{n}</td><td><b>{p} points</b></td><td>₹{p} off next trip</td></tr>' for n, p in POINTS)
    return f"""<section class="hero"><div class="wrap"><div><div class="crumbs"><a href="{root}">Home</a> › Offers &amp; Rewards</div><h1>Offers &amp; Rewards</h1><p>Earn reward points on every booking, get a welcome bonus, refer friends and use coupon codes – 1 point = ₹1 off your next trip.</p></div></div></section>
<section class="ofsec"><div class="wrap">
<div class="ofgrid">
<div class="ofcard of1"><span class="ofic">🎁</span><h3>100 welcome points</h3><p>Create your free account and get 100 reward points straight away.</p><a class="btn gold" href="{root}account/#signup">Create free account</a></div>
<div class="ofcard of2"><span class="ofic">🤝</span><h3>Refer &amp; earn</h3><p>Share your code from My Account. When your friend makes their first booking, you <b>both</b> get 100 points.</p><a class="btn outline" href="{root}account/">Get my referral code</a></div>
<div class="ofcard of3"><span class="ofic">⭐</span><h3>Points on every booking</h3><p>Flights, hotels, cruises, holidays, visas, passports and insurance – every paid booking earns points.</p><a class="btn outline" href="#points">See points table</a></div>
</div>
<div class="ofcoup"><div class="ofhead" style="margin:0 0 12px"><h2 style="margin:0">Coupon codes</h2><p class="lead" style="margin:4px 0 0">Enter the code in the payment box at checkout.</p></div>
<div id="ofList" class="ofcodes"><p class="meta">Loading current offers…</p></div></div>
<div id="points" class="oftable"><h2>Reward points per booking</h2><table><thead><tr><th>Service</th><th>You earn</th><th>Worth</th></tr></thead><tbody>{rows}</tbody></table>
<ul class="ticks ofrules"><li>1 point = ₹1. Points can pay up to 10% of a booking.</li><li>Points are added after your booking is confirmed and paid, and are valid for 12 months.</li><li>Log in when you pay to use your points; coupon codes work for everyone.</li><li>Points and coupons have no cash value and cannot be transferred. The Real Tours and Travels may change or end offers at any time; bookings already made are not affected.</li></ul></div>
</div></section>
{cta_band()}
<script>(function(){{
 fetch("{SB_URL}/rest/v1/coupons?select=code,title,description,kind,amount,max_discount,min_amount,valid_to&order=created_at.desc",{{headers:{{apikey:"{SB_KEY}",Authorization:"Bearer {SB_KEY}"}}}})
 .then(r=>r.json()).then(d=>{{const el=document.getElementById('ofList');const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,x=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}})[x]);
  if(!Array.isArray(d)||!d.length){{el.innerHTML='<p class="meta">New coupon codes are coming soon – meanwhile, create your free account for 100 welcome points.</p>';return;}}
  el.innerHTML=d.map(k=>'<div class="ofcode"><div><b>'+esc(k.title)+'</b><small>'+(k.min_amount>0?'Min booking ₹'+Number(k.min_amount).toLocaleString('en-IN')+' · ':'')+(k.valid_to?'Valid till '+new Date(k.valid_to+'T00:00').toLocaleDateString('en-IN',{{dateStyle:'medium'}}):'Limited period')+'</small>'+(k.description?'<small>'+esc(k.description)+'</small>':'')+'</div><button type="button" class="ofcp" data-c="'+esc(k.code)+'">'+esc(k.code)+' <span>Copy</span></button></div>').join('');
  el.querySelectorAll('.ofcp').forEach(b=>b.addEventListener('click',()=>{{navigator.clipboard&&navigator.clipboard.writeText(b.dataset.c);b.querySelector('span').textContent='Copied ✓';}}));
 }}).catch(()=>{{document.getElementById('ofList').innerHTML='<p class="meta">Could not load offers right now.</p>';}});
}})();</script>"""

CSS = """
.ofsec{padding-top:0!important}
.ofgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.ofcard{background:#fff;border:1px solid var(--line);border-radius:18px;padding:20px;display:flex;flex-direction:column;gap:8px;box-shadow:0 10px 26px rgba(60,20,25,.06)}
.ofcard h3{margin:0;font-size:20px}.ofcard p{margin:0;color:var(--muted);flex:1}.ofcard .btn{align-self:flex-start;padding:9px 18px;font-size:14.5px}
.ofic{font-size:30px}.of1{background:linear-gradient(180deg,#fdf3f3,#fff)}
.ofcoup{margin-top:28px;background:var(--bg);border:1px solid var(--line);border-radius:18px;padding:20px}
.ofcodes{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}
.ofcode{display:flex;justify-content:space-between;align-items:center;gap:10px;background:#fff;border:1px dashed var(--crimson);border-radius:14px;padding:12px 14px}
.ofcode b{display:block}.ofcode small{display:block;color:var(--muted);font-size:12.5px}
.ofcp{border:0;background:var(--crimson);color:#fff;border-radius:10px;padding:8px 12px;font:700 14px monospace;letter-spacing:1px;cursor:pointer;white-space:nowrap}.ofcp span{font:500 11px 'Jost',sans-serif;opacity:.85;margin-left:4px}
.oftable{margin-top:28px}.oftable table{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden}.oftable th,.oftable td{padding:11px 14px;border-bottom:1px solid var(--line);text-align:left}.oftable th{background:var(--bg);font-size:13.5px}
.ofrules{margin-top:14px;font-size:14.5px}
@media(max-width:800px){.ofgrid{grid-template-columns:1fr}}
"""
