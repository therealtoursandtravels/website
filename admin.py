"""Private office admin panel: all enquiries & bookings, status, notes, admins. Data access is enforced by Supabase RLS (is_admin())."""
from visa import SB_URL, SB_KEY

ADMIN_HTML = r"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow"><title>Office Admin | The Real Tours and Travels</title>
<link rel="icon" href="/favicon.png"><link rel="manifest" href="/manifest.webmanifest">
<style>
:root{--red:#c8102e;--crimson:#9d0b22;--ink:#1d1d1f;--muted:#6b6b70;--line:#e6e2dd;--bg:#f7f6f4;--ok:#1b7f3b;--warn:#b25e00}
*{box-sizing:border-box}body{margin:0;font:15px/1.45 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:var(--bg)}
header{position:sticky;top:0;z-index:20;background:#fff;border-bottom:1px solid var(--line);padding:calc(8px + env(safe-area-inset-top)) 16px 8px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
header img{width:40px;height:40px}header b{font-size:17px}header small{display:block;color:var(--muted)}header .sp{flex:1}
button,select,input,textarea{font:inherit;font-size:16px}
.btn{border:1.5px solid var(--red);background:var(--red);color:#fff;border-radius:999px;padding:8px 16px;cursor:pointer;font-weight:600}.btn.o{background:#fff;color:var(--crimson)}.btn.s{padding:5px 12px;font-size:14px}
main{max-width:1280px;margin:0 auto;padding:16px}
.card{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px}
.login{max-width:380px;margin:60px auto}.login label{display:block;margin:10px 0;font-weight:600}.login input{width:100%;padding:11px;border:1px solid var(--line);border-radius:10px;margin-top:4px}
.msg{min-height:20px;color:var(--muted);margin-top:8px}.msg.err{color:var(--red)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:14px}.stat{background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px 14px}.stat b{display:block;font-size:26px;color:var(--crimson)}.stat span{color:var(--muted);font-size:13px}
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px}.tab{border:1px solid var(--line);background:#fff;border-radius:999px;padding:7px 14px;cursor:pointer;font-weight:600;color:var(--muted)}.tab.on{background:var(--red);border-color:var(--red);color:#fff}.tab i{font-style:normal;opacity:.8;margin-left:4px}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px}.filters input,.filters select{padding:8px 10px;border:1px solid var(--line);border-radius:10px;background:#fff}.filters input[type=search]{flex:1;min-width:200px}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden}
th,td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top;font-size:14px}th{background:#faf8f6;color:var(--muted);font-weight:600;white-space:nowrap}
tr.r{cursor:pointer}tr.r:hover{background:#fdf6f6}.ref{font-family:ui-monospace,Consolas,monospace;font-size:13px;color:var(--crimson)}
.st{display:inline-block;border-radius:999px;padding:2px 10px;font-size:12.5px;font-weight:700;white-space:nowrap}
.st.new{background:#fdecee;color:var(--red)}.st.quoted{background:#fff4e5;color:var(--warn)}.st.confirmed{background:#e8f5ec;color:var(--ok)}.st.completed{background:#eef0f3;color:#44474d}.st.cancelled{background:#f2f2f2;color:#888;text-decoration:line-through}
.empty{padding:30px;text-align:center;color:var(--muted)}
.drawer{position:fixed;inset:0;background:rgba(0,0,0,.35);z-index:40;display:flex;justify-content:flex-end}.drawer[hidden]{display:none}
.panel{background:#fff;width:min(560px,100%);height:100%;overflow:auto;padding:18px 18px calc(18px + env(safe-area-inset-bottom))}
.panel h2{margin:0 0 4px;font-size:20px}.kv{display:grid;grid-template-columns:140px 1fr;gap:4px 10px;margin:12px 0;font-size:14px}.kv dt{color:var(--muted)}.kv dd{margin:0;word-break:break-word;white-space:pre-wrap}
.quick{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}.quick a{text-decoration:none}
.panel label{display:block;font-weight:600;margin-top:12px}.panel select,.panel textarea{width:100%;padding:9px;border:1px solid var(--line);border-radius:10px;margin-top:4px}.panel textarea{min-height:90px}
.files a{display:block;margin:3px 0}
.admins li{display:flex;justify-content:space-between;gap:8px;padding:6px 0;border-bottom:1px solid var(--line)}
.hide-sm{}@media(max-width:760px){.hide-sm{display:none}th,td{padding:8px 6px;font-size:13.5px}.kv{grid-template-columns:110px 1fr}}
.rwf{display:flex;flex-wrap:wrap;gap:8px}.rwf input,.rwf select{padding:9px;border:1px solid var(--line);border-radius:10px;flex:1 1 160px}#rwDrawer h3{margin:22px 0 6px}#rwDrawer table{width:100%}
</style></head><body>
<header><img src="/img/logo.png" alt=""><div><b>The Real Tours and Travels</b><small>Office admin – staff only</small></div><span class="sp"></span>
<span id="who" class="msg"></span><button class="btn o s" id="btnRewards" hidden>🎁 Rewards</button><button class="btn o s" id="btnCars" hidden>🚗 Car quote</button><button class="btn o s" id="btnAdmins" hidden>👥 Admins</button><button class="btn o s" id="btnRefresh" hidden>⟳ Refresh</button><button class="btn s" id="btnOut" hidden>Log out</button></header>
<main>
<div id="vLoading" class="empty">Loading…</div>

<div id="vLogin" class="card login" hidden><h2 style="margin-top:0">Admin login</h2><p class="msg">Only office staff with admin access can open this page.</p>
<form id="fLogin"><label>Email<input name="email" type="email" required autocomplete="username"></label><label>Password<input name="password" type="password" required autocomplete="current-password"></label>
<button class="btn" type="submit" style="width:100%;margin-top:8px">Log in</button><p class="msg" id="lMsg"></p></form></div>

<div id="vDenied" class="card login" hidden><h2 style="margin-top:0">No admin access</h2><p>You are logged in as <b id="dEmail"></b>, but this account is not an office admin. Ask an existing admin to add you.</p><button class="btn o" id="btnOut2">Log out</button></div>

<div id="vApp" hidden>
<div class="stats" id="stats"></div>
<div class="tabs" id="tabs"></div>
<div class="filters"><input type="search" id="q" placeholder="Search name, phone, email, destination, reference…">
<select id="fType"><option value="">All services</option></select>
<select id="fSort"><option value="created">Newest first</option><option value="travel">By travel date</option></select>
<button class="btn o s" id="btnCsv">⬇ Export CSV</button></div>
<div style="overflow:auto"><table><thead><tr><th>Ref</th><th>Service</th><th>Customer</th><th class="hide-sm">Trip</th><th>Travel date</th><th class="hide-sm">Received</th><th>Status</th></tr></thead><tbody id="rows"></tbody></table></div>
<p class="msg" id="count"></p>
</div>
</main>

<div class="drawer" id="drawer" hidden><div class="panel" id="panel"></div></div>
<div class="drawer" id="admDrawer" hidden><div class="panel"><div style="display:flex;justify-content:space-between;align-items:center"><h2>Office admins</h2><button class="btn o s" data-close>✕ Close</button></div>
<p class="msg">Admins can see every enquiry and booking. The person must first create an account on the website (Login → Create account) and confirm their email.</p>
<ul class="admins" id="admList" style="list-style:none;padding:0"></ul>
<form id="fAdd" style="display:flex;gap:8px;margin-top:10px"><input name="email" type="email" required placeholder="staff@email.com" style="flex:1;padding:9px;border:1px solid var(--line);border-radius:10px"><button class="btn s">Add admin</button></form><p class="msg" id="admMsg"></p></div></div>
<div class="drawer" id="rwDrawer" hidden><div class="panel"><div style="display:flex;justify-content:space-between;align-items:center"><h2>Rewards &amp; coupons</h2><button class="btn o s" data-close>✕ Close</button></div>
<h3>Give points for a booking</h3><p class="msg">Use the customer's account email. If a friend referred them, both get referral points on their first booking.</p>
<form id="fAward" class="rwf"><input name="email" type="email" required placeholder="customer@email.com"><select name="service" id="rwSvc"></select><input name="ref" placeholder="Booking ref (optional)"><button class="btn s">Give points</button></form><p class="msg" id="awMsg"></p>
<h3>Correct points</h3><p class="msg">Positive number adds points (e.g. refund an unused redemption), negative removes.</p>
<form id="fAdj" class="rwf"><input name="email" type="email" required placeholder="customer@email.com"><input name="pts" type="number" required placeholder="e.g. 150 or -150"><input name="note" required placeholder="Reason"><button class="btn s">Save</button></form><p class="msg" id="adjMsg"></p>
<h3>Coupon codes</h3>
<form id="fCoup" class="rwf"><input name="code" required placeholder="CODE e.g. FIRSTTRIP" style="text-transform:uppercase"><input name="title" required placeholder="Title e.g. ₹250 off your first trip"><select name="kind"><option value="flat">₹ off</option><option value="percent">% off</option></select><input name="amount" type="number" min="1" required placeholder="Amount"><input name="max_discount" type="number" min="1" placeholder="Max ₹ (for %)"><input name="min_amount" type="number" min="0" placeholder="Min booking ₹"><input name="valid_to" type="date" title="Valid till (optional)"><button class="btn s">Add coupon</button></form><p class="msg" id="cpMsg"></p>
<ul class="admins" id="cpList" style="list-style:none;padding:0"></ul>
<h3>Points per service</h3><div id="rwSet" class="msg">Loading…</div>
<h3>Customers' points</h3><div id="rwList" class="msg">Loading…</div>
</div></div>

<div class="drawer" id="carDrawer" hidden><div class="panel"><div style="display:flex;justify-content:space-between;align-items:center"><h2>Car / transfer quote</h2><button class="btn o s" data-close>✕ Close</button></div>
<p class="msg">Enter the price from Kiwitaxi / Mozio / Savaari (in ₹). The customer price adds your margin (default 6%). The customer gets a payment link that shows only the final price.</p>
<form id="fCar" class="rwf"><select name="supplier"><option>Kiwitaxi</option><option>Mozio</option><option>Savaari</option><option>CabBazar</option><option>Other</option></select>
<input name="cost" type="number" min="1" step="0.01" required placeholder="Supplier price ₹"><input name="margin" type="number" min="0" max="100" step="0.5" value="6" title="Margin %" style="width:90px">
<input name="trip" required maxlength="200" placeholder="Trip e.g. Dubai Airport T3 → Hotel, Deira"><input name="when" maxlength="60" placeholder="Pick-up date &amp; time"><input name="car" maxlength="60" placeholder="Car e.g. Sedan"><input name="pax" type="number" min="1" max="60" placeholder="Passengers">
<input name="name" maxlength="120" placeholder="Customer name"><input name="contact" maxlength="160" placeholder="Customer mobile / email"><button class="btn s">Create payment link</button></form>
<p class="msg" id="carCalc"></p><div class="msg" id="carMsg"></div>
<h3>Recent car quotes</h3><div id="carList" class="msg">Loading…</div>
</div></div>
<script src="/js/supabase.js"></script>
<script>
(function(){
const c=supabase.createClient("__SB_URL__","__SB_KEY__",{auth:{persistSession:true,autoRefreshToken:true}});
const $=s=>document.querySelector(s),esc=s=>String(s==null?'':s).replace(/[&<>"]/g,x=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'})[x]);
const views=['vLoading','vLogin','vDenied','vApp'];const view=v=>views.forEach(x=>$('#'+x).hidden=x!==v);
const STAT=['new','quoted','confirmed','completed','cancelled'];
const STL={new:'New',quoted:'Quoted',confirmed:'Confirmed',completed:'Completed',cancelled:'Cancelled'};
const fd=d=>d?new Date(d+(String(d).length===10?'T00:00:00':'')).toLocaleDateString('en-IN',{day:'2-digit',month:'short',year:'numeric'}):'';
const fdt=d=>d?new Date(d).toLocaleString('en-IN',{day:'2-digit',month:'short',hour:'2-digit',minute:'2-digit'}):'';
const T=[
 {t:'flight_enquiries',label:()=>'✈️ Flight',pre:()=> 'FL',date:r=>r.depart_date,trip:r=>[r.from_city,r.to_city].filter(Boolean).join(' → ')+(r.trip_type?' · '+r.trip_type:'')+(r.cabin?' · '+r.cabin:''),pax:r=>[r.adults&&r.adults+' adult',r.children&&r.children+' child',r.infants&&r.infants+' infant'].filter(Boolean).join(', ')},
 {t:'booking_enquiries',label:r=>r.kind==='hotel'?'🏨 Hotel':'🛳️ Cruise',pre:r=>r.kind==='hotel'?'HT':'CR',date:r=>r.start_date,trip:r=>[r.destination,r.provider,r.category,r.nights&&r.nights+' nights',!r.start_date&&r.travel_month].filter(Boolean).join(' · '),pax:r=>[r.rooms&&r.rooms+' room',r.adults&&r.adults+' adult',r.children&&r.children+' child'].filter(Boolean).join(', ')},
 {t:'hotel_enquiries',label:()=>'🏨 Hotel',pre:()=>'HT',date:r=>r.check_in,trip:r=>[r.destination,r.category].filter(Boolean).join(' · '),pax:r=>[r.rooms&&r.rooms+' room',r.adults&&r.adults+' adult',r.children&&r.children+' child'].filter(Boolean).join(', ')},
 {t:'trip_requests',label:()=>'✨ Package',pre:()=>'PK',date:r=>r.start_date,trip:r=>[r.destination,r.days&&r.days+' days',r.trip_scope,r.hotel_category,r.car_type,r.travel_mode].filter(Boolean).join(' · '),pax:r=>[r.adults&&r.adults+' adult',r.children&&r.children+' child',r.infants&&r.infants+' infant'].filter(Boolean).join(', ')},
 {t:'visa_applications',label:r=>/passport/i.test(r.visa_type||'')||/passport/i.test(r.country||'')?'📘 Passport':'🛂 Visa',pre:()=>'VS',date:r=>r.travel_date,trip:r=>[r.country,r.visa_type].filter(Boolean).join(' · '),pax:r=>r.travellers?r.travellers+' traveller(s)':''},
 {t:'insurance_enquiries',label:()=>'🛡️ Insurance',pre:()=>'IN',date:r=>r.start_date,trip:r=>[r.destination,r.trip_type,r.cover].filter(Boolean).join(' · '),pax:r=>r.travellers?r.travellers+' traveller(s)':''},
 {t:'service_enquiries',label:r=>'🧳 '+(r.service||'Enquiry'),pre:()=>'SV',date:r=>null,trip:r=>[r.destination,r.travel_month].filter(Boolean).join(' · '),pax:r=>r.travellers?r.travellers+' traveller(s)':''}
];
let ALL=[],tab='open',me=null;
const today=new Date().toISOString().slice(0,10);
function bucket(x){
 if(x.status==='cancelled')return 'cancelled';
 if(x.status==='completed')return 'history';
 if(x.status==='confirmed')return (x.date&&x.date<today)?'history':'upcoming';
 return 'open';
}
const TABS=[['open','🆕 New & quoted'],['upcoming','📅 Upcoming (confirmed)'],['history','🗂️ History'],['cancelled','❌ Cancelled'],['all','All']];

async function load(){
 $('#rows').innerHTML='<tr><td colspan="7" class="empty">Loading all enquiries…</td></tr>';
 const res=await Promise.all(T.map(d=>c.from(d.t).select('*').order('created_at',{ascending:false}).limit(2000).then(r=>({d,r}))));
 ALL=[];
 res.forEach(({d,r})=>{ if(r.error){console.warn(d.t,r.error.message);return;}
  (r.data||[]).forEach(row=>{const pre=d.pre(row);ALL.push({d,row,table:d.t,id:row.id,ref:(pre+'-'+row.id.slice(0,6)).toUpperCase(),type:d.label(row),date:d.date(row)||null,
   name:row.full_name||'',phone:row.phone||'',email:row.email||'',trip:d.trip(row),pax:d.pax(row),status:STAT.includes(row.status)?row.status:'new',created:row.created_at});});});
 const types=[...new Set(ALL.map(x=>x.type))].sort();const fs=$('#fType'),cur=fs.value;
 fs.innerHTML='<option value="">All services</option>'+types.map(t=>'<option'+(t===cur?' selected':'')+'>'+esc(t)+'</option>').join('');
 render();
}
function filtered(){
 const q=$('#q').value.trim().toLowerCase(),ty=$('#fType').value;
 let L=ALL.filter(x=>(tab==='all'||bucket(x)===tab)&&(!ty||x.type===ty)&&(!q||[x.ref,x.name,x.phone,x.email,x.trip,x.type,x.row.notes,x.row.admin_notes].join(' ').toLowerCase().includes(q)));
 if($('#fSort').value==='travel'||tab==='upcoming')L.sort((a,b)=>(a.date||'9999').localeCompare(b.date||'9999'));else L.sort((a,b)=>b.created.localeCompare(a.created));
 return L;
}
function render(){
 const cnt=k=>ALL.filter(x=>k==='all'||bucket(x)===k).length;
 $('#tabs').innerHTML=TABS.map(([k,l])=>'<button class="tab'+(k===tab?' on':'')+'" data-k="'+k+'">'+l+'<i>'+cnt(k)+'</i></button>').join('');
 const d30=new Date(Date.now()+30*864e5).toISOString().slice(0,10),t0=today;
 const sToday=ALL.filter(x=>x.created.slice(0,10)===t0).length,sOpen=cnt('open'),sUp=ALL.filter(x=>bucket(x)==='upcoming'&&x.date&&x.date<=d30).length,sNew=ALL.filter(x=>x.status==='new').length;
 $('#stats').innerHTML=[[sToday,'Received today'],[sNew,'Not yet replied (New)'],[sOpen,'Open enquiries'],[sUp,'Trips in next 30 days'],[ALL.length,'Total on record']].map(([n,l])=>'<div class="stat"><b>'+n+'</b><span>'+l+'</span></div>').join('');
 const L=filtered();
 $('#rows').innerHTML=L.length?L.map((x,i)=>'<tr class="r" data-i="'+ALL.indexOf(x)+'"><td class="ref">'+x.ref+'</td><td>'+esc(x.type)+'</td><td><b>'+esc(x.name)+'</b><br><small>'+esc(x.phone)+'</small></td><td class="hide-sm">'+esc(x.trip)+(x.pax?'<br><small>'+esc(x.pax)+'</small>':'')+'</td><td>'+(fd(x.date)||'<small>—</small>')+'</td><td class="hide-sm"><small>'+fdt(x.created)+'</small></td><td><span class="st '+x.status+'">'+STL[x.status]+'</span></td></tr>').join(''):'<tr><td colspan="7" class="empty">Nothing here.</td></tr>';
 $('#count').textContent=L.length+' shown';
}
const NICE={full_name:'Name',phone:'Mobile',email:'Email',created_at:'Received',updated_at:'Last updated',user_id:'Registered customer',status:'Status'};
const SKIP=['id','admin_notes','files'];
async function open(i){
 const x=ALL[i],r=x.row,ph=(x.phone||'').replace(/[^0-9]/g,''),wa=ph.length===10?'91'+ph:ph;
 const kv=Object.keys(r).filter(k=>!SKIP.includes(k)&&r[k]!==null&&r[k]!=='').map(k=>'<dt>'+esc(NICE[k]||k.replace(/_/g,' '))+'</dt><dd>'+esc(k==='created_at'||k==='updated_at'?fdt(r[k]):k==='user_id'?'Yes (has an account)':typeof r[k]==='boolean'?(r[k]?'Yes':'No'):r[k])+'</dd>').join('');
 const msg=encodeURIComponent('Hello '+(x.name||'')+', this is The Real Tours and Travels regarding your '+x.type.replace(/^\S+\s/,'')+' enquiry (Ref '+x.ref+').');
 $('#panel').innerHTML='<div style="display:flex;justify-content:space-between;gap:8px"><div><h2>'+esc(x.type)+' <span class="ref">'+x.ref+'</span></h2><span class="st '+x.status+'">'+STL[x.status]+'</span></div><button class="btn o s" data-close>✕ Close</button></div>'
 +'<div class="quick">'+(ph?'<a class="btn s" href="https://wa.me/'+wa+'?text='+msg+'" target="_blank" rel="noopener">💬 WhatsApp</a><a class="btn o s" href="tel:+'+(ph.length===10?'91'+ph:ph)+'">📞 Call</a>':'')+(x.email?'<a class="btn o s" href="mailto:'+esc(x.email)+'?subject='+encodeURIComponent('Your enquiry '+x.ref+' – The Real Tours and Travels')+'">✉️ Email</a>':'')+'</div>'
 +'<dl class="kv">'+kv+'</dl><div class="files" id="files"></div>'
 +'<label>Status<select id="eSt">'+STAT.map(s=>'<option value="'+s+'"'+(s===x.status?' selected':'')+'>'+STL[s]+'</option>').join('')+'</select></label>'
 +'<label>Office notes <small style="font-weight:400;color:var(--muted)">(only admins see this)</small><textarea id="eNotes" placeholder="e.g. Quote sent on WhatsApp, PNR, hotel confirmation no., payment received…">'+esc(r.admin_notes||'')+'</textarea></label>'
 +'<button class="btn" id="eSave" style="margin-top:12px">Save</button> <span class="msg" id="eMsg"></span>';
 $('#drawer').hidden=false;
 if(Array.isArray(r.files)&&r.files.length){$('#files').innerHTML='<b>Uploaded documents</b>';
  for(const p of r.files){const {data}=await c.storage.from('visa-documents').createSignedUrl(p,3600);$('#files').insertAdjacentHTML('beforeend',data?'<a href="'+data.signedUrl+'" target="_blank" rel="noopener">📎 '+esc(p.split('/').pop())+'</a>':'<div>📎 '+esc(p.split('/').pop())+' (cannot open)</div>');}}
 $('#eSave').onclick=async()=>{$('#eMsg').textContent='Saving…';
  const upd={status:$('#eSt').value,admin_notes:$('#eNotes').value.trim()||null};
  const {data,error}=await c.from(x.table).update(upd).eq('id',x.id).select().maybeSingle();
  if(error||!data){$('#eMsg').textContent='Could not save: '+(error?error.message:'no permission');$('#eMsg').className='msg err';return;}
  x.row=data;x.status=data.status;$('#eMsg').textContent='✅ Saved';$('#eMsg').className='msg';render();};
}
function csv(){
 const L=filtered(),H=['Ref','Service','Status','Name','Mobile','Email','Trip','Travellers','Travel date','Received','Customer notes','Office notes'];
 const q=v=>'"'+String(v==null?'':v).replace(/"/g,'""')+'"';
 const s=[H.map(q).join(',')].concat(L.map(x=>[x.ref,x.type,STL[x.status],x.name,x.phone,x.email,x.trip,x.pax,x.date||'',fdt(x.created),x.row.notes||'',x.row.admin_notes||''].map(q).join(','))).join('\r\n');
 const a=document.createElement('a');a.href=URL.createObjectURL(new Blob(['﻿'+s],{type:'text/csv'}));a.download='enquiries-'+tab+'-'+today+'.csv';a.click();
}
async function admins(){
 $('#admDrawer').hidden=false;$('#admList').innerHTML='<li>Loading…</li>';
 const {data}=await c.from('admins').select('email,added_at').order('added_at');
 $('#admList').innerHTML=(data||[]).map(a=>'<li><span>'+esc(a.email)+'</span>'+(a.email===me?'<small>(you)</small>':'<button class="btn o s" data-rm="'+esc(a.email)+'">Remove</button>')+'</li>').join('');
}
async function start(){
 const {data:{session}}=await c.auth.getSession();
 if(!session){view('vLogin');['btnOut','btnRefresh','btnAdmins','btnRewards','btnCars'].forEach(b=>$('#'+b).hidden=true);$('#who').textContent='';return;}
 me=(session.user.email||'').toLowerCase();$('#who').textContent=me;$('#btnOut').hidden=false;
 const {data:ok}=await c.rpc('is_admin');
 if(!ok){$('#dEmail').textContent=me;view('vDenied');return;}
 $('#btnRefresh').hidden=false;$('#btnAdmins').hidden=false;$('#btnRewards').hidden=false;$('#btnCars').hidden=false;view('vApp');load();
}
$('#fLogin').addEventListener('submit',async e=>{e.preventDefault();const f=e.target;$('#lMsg').textContent='Logging in…';$('#lMsg').className='msg';
 const {error}=await c.auth.signInWithPassword({email:f.email.value.trim(),password:f.password.value});
 if(error){$('#lMsg').textContent='Wrong email or password.';$('#lMsg').className='msg err';return;}start();});
const out=async()=>{await c.auth.signOut();start();};$('#btnOut').onclick=out;$('#btnOut2').onclick=out;

async function rewards(){
 $('#rwDrawer').hidden=false;
 const {data:set}=await c.from('reward_settings').select('*').order('points');
 $('#rwSvc').innerHTML=(set||[]).filter(x=>!['welcome','referral'].includes(x.key)).map(x=>'<option value="'+x.key+'">'+esc(x.label)+' – '+x.points+' pts</option>').join('');
 $('#rwSet').innerHTML='<table><tbody>'+(set||[]).map(x=>'<tr><td>'+esc(x.label)+'</td><td><input type="number" min="0" value="'+x.points+'" data-set="'+x.key+'" style="width:90px"> pts</td></tr>').join('')+'</tbody></table>';
 coupons();
 const {data:l}=await c.rpc('rewards_admin_list');
 $('#rwList').innerHTML=(l&&l.length)?'<table><thead><tr><th>Customer</th><th>Points</th><th>Referral code</th><th>Referred by</th></tr></thead><tbody>'+l.map(r=>'<tr><td>'+esc(r.email)+'</td><td>'+r.balance+'</td><td>'+esc(r.code||'')+'</td><td>'+esc(r.referred_by_email||'')+'</td></tr>').join('')+'</tbody></table>':'No customers yet.';
}
async function coupons(){
 const {data}=await c.from('coupons').select('*').order('created_at',{ascending:false});
 $('#cpList').innerHTML=(data||[]).map(k=>'<li><span><b>'+esc(k.code)+'</b> – '+esc(k.title)+' · '+(k.kind==='percent'?k.amount+'%':'₹'+k.amount)+(k.min_amount?' · min ₹'+k.min_amount:'')+(k.valid_to?' · till '+fd(k.valid_to):'')+(k.active?'':' · <i>off</i>')+'</span><button class="btn o s" data-cp="'+esc(k.code)+'" data-on="'+(k.active?1:0)+'">'+(k.active?'Turn off':'Turn on')+'</button></li>').join('')||'<li>No coupons yet.</li>';
}
$('#btnRewards').onclick=rewards;
const CSITE='https://www.therealtoursandtravels.com/car-rental/?pay=';
const cinr=n=>'₹'+Number(n).toLocaleString('en-IN',{minimumFractionDigits:0,maximumFractionDigits:2});
function carTot(){const f=$('#fCar');const c=+f.cost.value||0,m=+f.margin.value||0;const t=Math.ceil(c*(1+m/100));$('#carCalc').innerHTML=c?('Customer pays <b>'+cinr(t)+'</b> (your margin '+cinr(t-c)+')'):'';return t;}
async function cars(){$('#carDrawer').hidden=false;carTot();
 const {data}=await c.from('car_quotes').select('*').order('created_at',{ascending:false}).limit(30);
 $('#carList').innerHTML=(data&&data.length)?'<table><thead><tr><th>Ref</th><th>Trip</th><th>Supplier ₹</th><th>Customer ₹</th><th>Status</th><th></th></tr></thead><tbody>'+data.map(q=>'<tr><td>'+esc(q.ref)+'</td><td>'+esc(q.trip)+(q.pickup_at?'<br><small>'+esc(q.pickup_at)+'</small>':'')+'</td><td>'+esc(q.supplier)+' '+cinr(q.supplier_cost)+'</td><td><b>'+cinr(q.total)+'</b></td><td><select data-cq="'+esc(q.ref)+'">'+['sent','paid','booked','cancelled'].map(s=>'<option'+(s===q.status?' selected':'')+'>'+s+'</option>').join('')+'</select></td><td><button class="btn o s" data-cl="'+esc(q.ref)+'">Copy link</button></td></tr>').join('')+'</tbody></table>':'No car quotes yet.';}
$('#btnCars').onclick=cars;
$('#fCar').addEventListener('input',carTot);
$('#fCar').addEventListener('submit',async e=>{e.preventDefault();const f=e.target;const total=carTot();
 const ref='CR-'+Math.random().toString(36).slice(2,8).toUpperCase();
 const row={ref,supplier:f.supplier.value,supplier_cost:+f.cost.value,margin_pct:+f.margin.value||0,total,trip:f.trip.value.trim(),pickup_at:f.when.value.trim()||null,car:f.car.value.trim()||null,pax:f.pax.value?+f.pax.value:null,customer_name:f.name.value.trim()||null,customer_contact:f.contact.value.trim()||null};
 const {error}=await c.from('car_quotes').insert(row);
 if(error){$('#carMsg').textContent=error.message;return;}
 const link=CSITE+ref;const txt='Hello'+(row.customer_name?' '+row.customer_name:'')+', your car booking quote from The Real Tours and Travels:\n'+row.trip+(row.pickup_at?'\n'+row.pickup_at:'')+(row.car?'\nCar: '+row.car:'')+'\nTotal: '+cinr(total)+'\nPay securely here: '+link;
 const ph=(row.customer_contact||'').replace(/[^0-9]/g,'');const wa='https://wa.me/'+(ph.length===10?'91'+ph:ph)+'?text='+encodeURIComponent(txt);
 $('#carMsg').innerHTML='✅ Quote <b>'+ref+'</b> created – customer pays <b>'+cinr(total)+'</b>.<br>Link: <a href="'+link+'" target="_blank">'+link+'</a><br><a class="btn s" href="'+wa+'" target="_blank" rel="noopener">💬 Send on WhatsApp</a> <button type="button" class="btn o s" data-cl="'+ref+'">Copy link</button>';
 f.reset();f.margin.value=6;carTot();cars();});
document.addEventListener('click',e=>{const b=e.target.closest('[data-cl]');if(b){navigator.clipboard&&navigator.clipboard.writeText(CSITE+b.dataset.cl);b.textContent='Copied ✓';}});
document.addEventListener('change',async e=>{const s=e.target.closest('[data-cq]');if(s){const {error}=await c.from('car_quotes').update({status:s.value}).eq('ref',s.dataset.cq);if(error)alert(error.message);}});

$('#fAward').addEventListener('submit',async e=>{e.preventDefault();const f=e.target;$('#awMsg').textContent='Saving…';
 const {data,error}=await c.rpc('rewards_award',{customer_email:f.email.value.trim(),service:f.service.value,ref:f.ref.value.trim()||null});
 $('#awMsg').textContent=error?error.message:('✅ Gave '+data.points+' points. New balance: '+data.balance);if(!error){f.reset();rewards();}});
$('#fAdj').addEventListener('submit',async e=>{e.preventDefault();const f=e.target;
 const {data,error}=await c.rpc('rewards_adjust',{customer_email:f.email.value.trim(),pts:+f.pts.value,note:f.note.value.trim()});
 $('#adjMsg').textContent=error?error.message:'✅ Saved. New balance: '+data;if(!error){f.reset();rewards();}});
$('#fCoup').addEventListener('submit',async e=>{e.preventDefault();const f=e.target;
 const row={code:f.code.value.trim().toUpperCase(),title:f.title.value.trim(),kind:f.kind.value,amount:+f.amount.value,max_discount:f.max_discount.value?+f.max_discount.value:null,min_amount:f.min_amount.value?+f.min_amount.value:0,valid_to:f.valid_to.value||null};
 const {error}=await c.from('coupons').insert(row);$('#cpMsg').textContent=error?error.message:'✅ Coupon '+row.code+' added.';if(!error){f.reset();coupons();}});
document.addEventListener('click',async e=>{const b=e.target.closest('[data-cp]');if(!b)return;await c.from('coupons').update({active:b.dataset.on!=='1'}).eq('code',b.dataset.cp);coupons();});
document.addEventListener('change',async e=>{const i=e.target.closest('[data-set]');if(!i)return;const {error}=await c.from('reward_settings').update({points:+i.value}).eq('key',i.dataset.set);i.style.borderColor=error?'red':'green';});
$('#btnRefresh').onclick=load;$('#btnCsv').onclick=csv;$('#btnAdmins').onclick=admins;
$('#tabs').addEventListener('click',e=>{const b=e.target.closest('.tab');if(b){tab=b.dataset.k;render();}});
['#q','#fType','#fSort'].forEach(s=>$(s).addEventListener('input',render));
$('#rows').addEventListener('click',e=>{const tr=e.target.closest('tr.r');if(tr)open(+tr.dataset.i);});
document.addEventListener('click',e=>{if(e.target.matches('[data-close]')||e.target.classList.contains('drawer')){e.target.closest('.drawer').hidden=true;}
 const rm=e.target.closest('[data-rm]');if(rm&&confirm('Remove admin access for '+rm.dataset.rm+'?')){c.rpc('remove_admin',{p_email:rm.dataset.rm}).then(({data,error})=>{$('#admMsg').textContent=error?error.message:data;admins();});}});
$('#fAdd').addEventListener('submit',async e=>{e.preventDefault();const em=e.target.email.value.trim();$('#admMsg').textContent='Adding…';
 const {data,error}=await c.rpc('add_admin',{p_email:em});$('#admMsg').textContent=error?error.message:data;if(!error){e.target.reset();admins();}});
document.addEventListener('keydown',e=>{if(e.key==='Escape')document.querySelectorAll('.drawer').forEach(d=>d.hidden=true);});
start();
})();
</script></body></html>"""

def admin_page():
    return ADMIN_HTML.replace("__SB_URL__", SB_URL).replace("__SB_KEY__", SB_KEY)
