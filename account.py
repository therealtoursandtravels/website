"""Customer accounts (Supabase Auth): login/sign-up page, profile, my enquiries, and site-wide form prefill."""
from visa import SB_URL, SB_KEY

SBJS = "/js/supabase.js"
STORE_KEY = "sb-byvytpxqqgjschknqpms-auth-token"

# Loaded on every page: only pulls in the login library when the visitor is (or may be) logged in.
SITE_JS = f"""<script>
(function(){{
 const SB="{SB_URL}",KEY="{SB_KEY}",LIB="{SBJS}";
 try{{const rf=new URLSearchParams(location.search).get('ref');if(rf&&/^[A-Za-z0-9]{{4,12}}$/.test(rf))localStorage.setItem('rtt_ref',rf.toUpperCase());}}catch(_){{}}
 let has=false;try{{has=!!localStorage.getItem('{STORE_KEY}');}}catch(_){{}}
 window.rttClient=function(){{return window.__rttc||(window.__rttc=new Promise((ok,no)=>{{const go=()=>ok(supabase.createClient(SB,KEY,{{auth:{{persistSession:true,autoRefreshToken:true,detectSessionInUrl:true}}}}));if(window.supabase)return go();const s=document.createElement('script');s.src=LIB;s.onload=go;s.onerror=no;document.head.appendChild(s);}}));}};
 if(!has&&!/[#&](access_token|type=recovery)/.test(location.hash))return;
 const run=()=>window.rttClient().then(async c=>{{const link=document.getElementById('acctLink');
  const {{data:{{session}}}}=await c.auth.getSession();if(!session)return;
  window.RTT_TOKEN=session.access_token;c.auth.onAuthStateChange((_e,s)=>{{window.RTT_TOKEN=s?s.access_token:null;}});
  if(link){{link.textContent='👤 My Account';}}
  const {{data:p}}=await c.from('profiles').select('full_name,phone,email').eq('id',session.user.id).maybeSingle();
  const pr=p||{{}},email=pr.email||session.user.email,phone=pr.phone||'',name=pr.full_name||'';
  window.RTT_PROFILE={{name,phone,email}};
  const fill=(sel,val)=>{{if(!val)return;document.querySelectorAll(sel).forEach(i=>{{if(!i.value&&!i.closest('#acct'))i.value=val;}});}};
  fill('input[name=full_name],input[name=name]',name);fill('input[name=phone]',phone);fill('input[name=email]',email);fill('input[name=contact]',phone||email);
  const {{data:TV}}=await c.from('travellers').select('*').order('is_self',{{ascending:false}}).order('created_at');const TRV=TV||[];
  const E=x=>String(x==null?'':x).replace(/[&<>"]/g,ch=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}})[ch]);
  const nm=t=>[t.title,t.first_name,t.last_name].filter(Boolean).join(' ');
  const fd=d=>d?new Date(d+'T00:00').toLocaleDateString('en-IN',{{day:'2-digit',month:'short',year:'numeric'}}):'';
  const age=d=>{{if(!d)return 30;const b=new Date(d+'T00:00'),n=new Date();let a=n.getFullYear()-b.getFullYear();if(n<new Date(n.getFullYear(),b.getMonth(),b.getDate()))a--;return a;}};
  const line=(t,i)=>(i+1)+'. '+nm(t)+[t.gender,t.date_of_birth?'DOB '+fd(t.date_of_birth):'',t.nationality,t.passport_no?'Passport '+t.passport_no+(t.passport_expiry?' (exp '+fd(t.passport_expiry)+')':'')+(t.passport_issue_place?' issued '+t.passport_issue_place:''):'',t.meal_pref?'Meal: '+t.meal_pref:'',t.mobile,t.email].filter(Boolean).map(x=>' · '+x).join('');
  let sheet=null,target=null;
  function openSheet(f){{target=f;if(!sheet){{sheet=document.createElement('div');sheet.className='trv-sheet';document.body.appendChild(sheet);sheet.addEventListener('click',e=>{{if(e.target===sheet)sheet.hidden=true;}});}}
   const pre=(f.dataset.trv||'').split(',');
   sheet.innerHTML='<div class="trv-pan"><div class="trv-h"><b>Choose travellers</b><button type="button" class="trv-x" aria-label="Close">✕</button></div>'+(TRV.length?'<div class="trv-opts">'+TRV.map(t=>'<label class="trv-op"><input type="checkbox" value="'+t.id+'"'+(pre.includes(t.id)?' checked':'')+'><span><b>'+E(nm(t))+(t.is_self?' (me)':'')+'</b><small>'+E([t.gender,t.date_of_birth?'DOB '+fd(t.date_of_birth):'',t.passport_no?'Passport ••'+t.passport_no.slice(-3):''].filter(Boolean).join(' · '))+'</small></span></label>').join('')+'</div><p class="trv-n">The first traveller ticked is the main contact – name, mobile and email are filled in for you.</p><button type="button" class="btn gold trv-ok">Fill details</button>':'<p class="trv-n">No travellers saved yet.</p>')+'<a class="trv-new" href="/account/#travellers">＋ Add or edit travellers</a></div>';
   sheet.hidden=false;sheet.querySelector('.trv-x').onclick=()=>{{sheet.hidden=true;}};
   const ok=sheet.querySelector('.trv-ok');if(ok)ok.onclick=()=>{{const ids=[...sheet.querySelectorAll('input:checked')].map(i=>i.value);apply(target,TRV.filter(t=>ids.includes(t.id)).sort((a,b)=>ids.indexOf(a.id)-ids.indexOf(b.id)));sheet.hidden=true;}};}}
  function setv(f,n,v){{const el=f.querySelector('[name="'+n+'"]');if(el&&v!=null&&v!==''){{el.value=v;el.dispatchEvent(new Event('input',{{bubbles:true}}));el.dispatchEvent(new Event('change',{{bubbles:true}}));}}}}
  function apply(f,sel){{f.dataset.trv=sel.map(t=>t.id).join(',');const chip=f.querySelector('.trv-chips');if(chip)chip.innerHTML=sel.map(t=>'<span>'+E(nm(t))+'</span>').join('');if(!sel.length)return;
   const lead=sel.find(t=>t.is_self)||sel[0];const ph=lead.mobile||phone,em=lead.email||email;
   setv(f,'full_name',nm(lead));setv(f,'name',nm(lead));setv(f,'phone',ph);setv(f,'email',em);setv(f,'contact',ph||em);
   const A=sel.map(t=>age(t.date_of_birth)),ad=A.filter(a=>a>=12).length,ch=A.filter(a=>a>=2&&a<12).length,inf=A.filter(a=>a<2).length;
   if(f.querySelector('[name=adults]')&&ad){{setv(f,'adults',ad);setv(f,'children',ch);setv(f,'infants',inf);}}
   setv(f,'travellers',sel.length);
   let n=f.querySelector('[name=notes]');if(!n)return;
   if(n.tagName==='INPUT'){{const ta=document.createElement('textarea');[...n.attributes].forEach(a=>{{if(a.name!=='type')ta.setAttribute(a.name,a.value);}});ta.rows=4;ta.maxLength=1500;n.replaceWith(ta);n=ta;}}
   else n.maxLength=Math.max(n.maxLength||0,1500);
   const own=n.value.split('\\n— Travellers —')[0].trim();n.value=(own?own+'\\n':'')+'— Travellers —\\n'+sel.map(line).join('\\n');}}
  document.querySelectorAll('form').forEach(f=>{{if(f.closest('#acct')||f.dataset.trvb)return;const inp=f.querySelector('input[name=full_name],input[name=name]');if(!inp)return;
   f.dataset.trvb='1';const box=document.createElement('div');box.className='trv-bar';box.innerHTML='<button type="button" class="trv-btn">👥 Fill from saved travellers</button><span class="trv-chips"></span>';
   const anchor=inp.closest('.row')||inp.closest('label')||inp;anchor.parentNode.insertBefore(box,anchor);box.querySelector('button').onclick=()=>openSheet(f);}});
 }}).catch(()=>{{}});
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
}})();
</script>"""

def account_page(PHONE, PHONE_RAW, EMAIL, WA, seal, cta_band):
    return f"""
<section style="padding:44px 0 70px"><div class="wrap" style="max-width:980px" id="acct">
<div class="crumbs"><a href="../">Home</a> › My Account</div>

<div id="a_loading" class="meta" hidden>Loading…</div>

<!-- Logged out -->
<div id="a_out">
<div class="acct-grid">
<div class="acct-card">
<div class="atabs"><button type="button" class="atab on" data-t="login">Log in</button><button type="button" class="atab" data-t="signup">Create account</button></div>
<form id="f_login" class="vform anoborder" novalidate>
<button type="button" class="gbtn" data-google><svg width="18" height="18" viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg><span>Continue with Google</span></button><div class="aor"><span>or with email</span></div>
<label>Email<input name="email" type="email" required autocomplete="email"></label>
<label>Password<input name="password" type="password" required autocomplete="current-password" minlength="6"></label>
<button class="btn gold" type="submit">Log in</button>
<button class="linkbtn" type="button" id="forgot">Forgot password?</button>
<p class="vmsg" role="status"></p><div class="aswitch">New here? <button type="button" class="btn outline" data-go="signup">✨ Create a free account</button></div></form>
<form id="f_signup" class="vform anoborder" novalidate hidden>
<button type="button" class="gbtn" data-google><svg width="18" height="18" viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg><span>Sign up with Google</span></button><p class="meta gnote">One tap – no password needed. You get 100 welcome points. By continuing you agree to our <a href="../terms/">Terms</a> and <a href="../privacy-policy/">Privacy Policy</a>.</p><div class="aor"><span>or with email</span></div>
<label>Full name*<input name="full_name" required maxlength="120" autocomplete="name"></label>
<div class="row"><label>Mobile number*<input name="phone" required inputmode="tel" maxlength="15" autocomplete="tel" placeholder="10-digit mobile"></label>
<label>City<input name="city" maxlength="80" autocomplete="address-level2"></label></div>
<label>Email*<input name="email" type="email" required autocomplete="email"></label>
<label>Create password* <small>(min. 8 characters)</small><input name="password" type="password" required minlength="8" autocomplete="new-password"></label>
<label class="chk"><input type="checkbox" name="consent_whatsapp" checked><span>Send me travel offers and updates on <b>WhatsApp</b></span></label>
<label class="chk"><input type="checkbox" name="consent_email" checked><span>Send me travel offers and updates by <b>email</b></span></label>
<label class="chk"><input type="checkbox" name="agree" required><span>I agree to the <a href="../terms/">Terms</a> and <a href="../privacy-policy/">Privacy Policy</a>.</span></label>
<button class="btn gold" type="submit">Create my account</button>
<p class="vmsg" role="status"></p><div class="aswitch">Already registered? <button type="button" class="linkbtn" data-go="login">Log in here</button></div></form>
</div>
<div class="acct-why"><h2>Why create an account?</h2><ul class="ticks">
<li>Your details are filled in automatically when you book flights, hotels, cruises, visas, insurance or packages</li>
<li>See all your enquiries and their reference numbers in one place</li>
<li>Get members-first travel offers and festival deals (only if you choose)</li>
<li>🎁 <b>100 welcome reward points</b> + earn points on every booking</li><li>Refer friends – you both get bonus points</li><li>Free – no card needed</li></ul>
<p class="meta">Prefer to talk? Call or WhatsApp <a href="tel:{PHONE_RAW}">{PHONE}</a>.</p></div>
</div></div>

<!-- Password reset -->
<form id="f_reset" class="vform acct-card" hidden novalidate><h2 style="margin:0">Set a new password</h2>
<label>New password <small>(min. 8 characters)</small><input name="password" type="password" required minlength="8" autocomplete="new-password"></label>
<button class="btn gold" type="submit">Save new password</button><p class="vmsg" role="status"></p></form>

<!-- Logged in -->
<div id="a_in" hidden>
<div class="acct-top"><div><h1 style="margin:0;font-size:clamp(28px,4vw,38px);color:var(--wine)">Hello, <span id="a_name">traveller</span> 👋</h1><p class="meta" id="a_email"></p></div>
<button class="btn ghost" type="button" id="logout">Log out</button></div>
<div class="acct-quick"><a href="../flights-hotels/#flights">✈️ Flights</a><a href="../flights-hotels/#hotels">🏨 Hotels</a><a href="../flights-hotels/#cruise">🛳️ Cruise</a><a href="../visa/">🛂 Visa</a><a href="../passport/">📘 Passport</a><a href="../insurance/">🛡️ Insurance</a><a href="../customize-your-package/">✨ Packages</a></div>
<div class="acct-grid">
<form id="f_profile" class="vform acct-card" novalidate><h2 style="margin:0">My details</h2>
<p class="meta" style="margin:0">Saved details are filled in automatically when you book.</p>
<label>Full name<input name="full_name" maxlength="120" autocomplete="name"></label>
<div class="row"><label>Mobile number<input name="phone" inputmode="tel" maxlength="15" autocomplete="tel"></label>
<label>Email<input name="email" type="email" maxlength="160" autocomplete="email"></label></div>
<div class="row"><label>City<input name="city" maxlength="80"></label>
<label>Date of birth<input name="date_of_birth" type="date"></label></div>
<label>Food preference<select name="food_preference"><option value="">No preference</option><option>Vegetarian</option><option>Jain</option><option>Non-vegetarian</option><option>Vegan</option></select></label>
<label>Travel interests<input name="travel_interests" maxlength="300" placeholder="e.g. hill stations, Europe, yatras, cruises"></label>
<label class="chk"><input type="checkbox" name="consent_whatsapp"><span>Send me offers and updates on WhatsApp</span></label>
<label class="chk"><input type="checkbox" name="consent_email"><span>Send me offers and updates by email</span></label>
<button class="btn gold" type="submit">Save my details</button><p class="vmsg" role="status"></p></form>
<div style="display:grid;gap:24px"><div class="acct-card rwcard" id="a_rw"><div class="rwtop"><div><h2 style="margin:0">🎁 My Rewards</h2><p class="meta" style="margin:2px 0 0">1 point = ₹1 off your next booking</p></div><div class="rwbal"><b id="rw_bal">–</b><span>points</span></div></div>
<div class="rwref"><b>Refer &amp; earn</b><p class="meta" style="margin:2px 0 8px">Share your code. When your friend makes their first booking, you both get <b id="rw_refpts">100</b> points.</p>
<div class="rwcode"><span id="rw_code">……</span><button type="button" class="btn outline" id="rw_copy">Copy link</button><a class="btn gold" id="rw_wa" target="_blank" rel="noopener" href="#">Share on WhatsApp</a></div></div>
<details class="rwhow"><summary>How to earn points</summary><ul class="ticks" id="rw_earn"></ul><p class="meta">Points are valid for 12 months and can pay up to 10% of a booking. <a href="../offers/">See all offers</a></p></details>
<details class="rwhow"><summary>Points history</summary><ul class="enq" id="rw_hist"><li>Loading…</li></ul></details></div>
<div class="acct-card"><h2 style="margin:0 0 6px">My enquiries</h2><div id="a_enq" class="meta">Loading…</div></div></div>
<div class="acct-card trv" id="travellers"><div class="trv-top"><div><h2 style="margin:0">👥 Saved travellers</h2><p class="meta" style="margin:2px 0 0">Save family and friends once – then fill any booking form in one tap.</p></div><button type="button" class="btn gold" id="trv_add">＋ Add traveller</button></div>
<div id="trv_list" class="trv-list"><p class="meta">Loading…</p></div>
<form id="f_trv" class="vform trv-form" novalidate hidden><input type="hidden" name="id">
<div class="row"><label>Title<select name="title"><option>Mr</option><option>Mrs</option><option>Ms</option><option>Miss</option><option>Master</option></select></label><label>Gender<select name="gender"><option>Male</option><option>Female</option><option>Other</option></select></label></div>
<div class="row"><label>First &amp; middle name* <small>(as on passport)</small><input name="first_name" required maxlength="60" autocomplete="off"></label><label>Last name / surname<input name="last_name" maxlength="60" autocomplete="off"></label></div>
<div class="row"><label>Date of birth<input name="date_of_birth" type="date"></label><label>Nationality<input name="nationality" maxlength="40" value="Indian"></label></div>
<div class="row"><label>Passport number<input name="passport_no" maxlength="20" autocomplete="off" style="text-transform:uppercase"></label><label>Passport expiry date<input name="passport_expiry" type="date"></label></div>
<div class="row"><label>Passport place of issue<input name="passport_issue_place" maxlength="60"></label><label>Meal preference<select name="meal_pref"><option value="">No preference</option><option>Vegetarian</option><option>Jain</option><option>Non-vegetarian</option><option>Vegan</option></select></label></div>
<div class="row"><label>Mobile number<input name="mobile" inputmode="tel" maxlength="20"></label><label>Email<input name="email" type="email" maxlength="160"></label></div>
<label class="chk"><input type="checkbox" name="is_self"><span>This is me (main contact)</span></label>
<div class="btns"><button class="btn gold" type="submit">Save traveller</button><button class="btn outline" type="button" id="trv_cancel">Cancel</button></div>
<p class="vmsg" role="status"></p><p class="meta" style="font-size:12.5px">🔒 Only you (and our ticketing team, when you book) can see these details.</p></form>
</div>
</div></div>
</div></section>
<script src="{SBJS}"></script>
<script>
(function(){{
const $=s=>document.querySelector(s),show=(id,on)=>{{const e=$(id);if(e)e.hidden=!on;}};
const msg=(f,t,cls)=>{{const m=f.querySelector('.vmsg');m.className='vmsg'+(cls?' '+cls:'');m.textContent=t;}};
const notify=(s,t,r)=>{{try{{fetch('https://formsubmit.co/ajax/enquiry@therealtoursandtravels.com',{{method:'POST',headers:{{'Content-Type':'application/json',Accept:'application/json'}},body:JSON.stringify({{_subject:s,message:t,_replyto:r||'',_template:'table',_captcha:'false'}})}}).catch(()=>{{}});}}catch(_){{}}}};
window.rttClient().then(async c=>{{
 document.querySelectorAll('.atab').forEach(b=>b.addEventListener('click',()=>{{document.querySelectorAll('.atab').forEach(x=>x.classList.toggle('on',x===b));show('#f_login',b.dataset.t==='login');show('#f_signup',b.dataset.t==='signup');}}));
 document.querySelectorAll('[data-go]').forEach(b=>b.addEventListener('click',()=>{{document.querySelector('.atab[data-t='+b.dataset.go+']').click();scrollTo({{top:0,behavior:'smooth'}});}}));
 if(location.hash==='#signup')document.querySelector('.atab[data-t=signup]').click();
 let recovering=/type=recovery/.test(location.hash);
 c.auth.onAuthStateChange((ev)=>{{if(ev==='PASSWORD_RECOVERY'){{recovering=true;render();}}}});
 async function render(){{
  const {{data:{{session}}}}=await c.auth.getSession();show('#a_loading',false);
  if(recovering&&session){{show('#a_out',false);show('#a_in',false);show('#f_reset',true);return;}}
  show('#f_reset',false);
  if(!session){{show('#a_out',true);show('#a_in',false);return;}}
  show('#a_out',false);show('#a_in',true);
  const u=session.user;$('#a_email').textContent=u.email;
  let {{data:p}}=await c.from('profiles').select('*').eq('id',u.id).maybeSingle();
  if(!p){{const m=u.user_metadata||{{}};const row={{id:u.id,full_name:m.full_name||m.name||null,phone:m.phone||null,email:u.email,city:m.city||null,consent_email:!!m.consent_email,consent_whatsapp:!!m.consent_whatsapp}};
   const r=await c.from('profiles').insert(row);if(!r.error){{p=row;notify('New customer registered – '+(row.full_name||u.email),'Name: '+(row.full_name||'')+'\\nMobile: '+(row.phone||'')+'\\nEmail: '+u.email+'\\nCity: '+(row.city||'')+'\\nWhatsApp offers: '+(row.consent_whatsapp?'Yes':'No')+'\\nEmail offers: '+(row.consent_email?'Yes':'No'),u.email);}}}}
  p=p||{{}};if(!p.phone)setTimeout(()=>{{const f=$('#f_profile');if(f){{msg(f,'Please add your mobile number and tap Save – we need it to contact you about your bookings.','err');f.phone.focus();}}}},300);$('#a_name').textContent=(p.full_name||'traveller').split(' ')[0];
  const f=$('#f_profile');['full_name','phone','email','city','date_of_birth','food_preference','travel_interests'].forEach(k=>{{if(f[k])f[k].value=p[k]||'';}});
  f.consent_email.checked=!!p.consent_email;f.consent_whatsapp.checked=!!p.consent_whatsapp;
  loadEnq();loadRewards();loadTrv();if(location.hash==='#travellers')setTimeout(()=>$('#travellers').scrollIntoView({{behavior:'smooth'}}),300);
 }}
 const TF=()=>$('#f_trv');const esc2=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}})[c]);
 const fdt=d=>d?new Date(d+'T00:00').toLocaleDateString('en-IN',{{day:'2-digit',month:'short',year:'numeric'}}):'';
 async function loadTrv(){{const {{data,error}}=await c.from('travellers').select('*').order('is_self',{{ascending:false}}).order('created_at');const L=$('#trv_list');
  if(error){{L.innerHTML='<p class="meta">Could not load travellers.</p>';return;}}
  if(!data.length){{L.innerHTML='<p class="meta">No travellers saved yet. Tap <b>＋ Add traveller</b> to add yourself and your family.</p>';return;}}
  L.innerHTML=data.map(t=>{{const exp=t.passport_expiry&&new Date(t.passport_expiry)<new Date(Date.now()+182*864e5);return '<div class="trv-item"><div><b>'+esc2([t.title,t.first_name,t.last_name].filter(Boolean).join(' '))+(t.is_self?' <em>Me</em>':'')+'</b><small>'+[t.gender,t.date_of_birth?'DOB '+fdt(t.date_of_birth):'',t.nationality].filter(Boolean).map(esc2).join(' · ')+'</small>'+(t.passport_no?'<small>Passport '+esc2(t.passport_no.slice(0,2))+'••••'+esc2(t.passport_no.slice(-2))+(t.passport_expiry?' · exp '+fdt(t.passport_expiry):'')+(exp?' <span class="trv-warn">⚠️ expires within 6 months</span>':'')+'</small>':'')+'</div><div class="trv-act"><button type="button" class="linkbtn" data-e="'+t.id+'">Edit</button><button type="button" class="linkbtn" data-d="'+t.id+'">Remove</button></div></div>';}}).join('');
  L.querySelectorAll('[data-e]').forEach(b=>b.onclick=()=>openTrv(data.find(x=>x.id===b.dataset.e)));
  L.querySelectorAll('[data-d]').forEach(b=>b.onclick=async()=>{{if(!confirmRemove(b))return;await c.from('travellers').delete().eq('id',b.dataset.d);loadTrv();}});}}
 function confirmRemove(b){{if(b.dataset.sure)return true;b.dataset.sure='1';b.textContent='Tap again to remove';setTimeout(()=>{{delete b.dataset.sure;b.textContent='Remove';}},3000);return false;}}
 function openTrv(t){{const f=TF();f.reset();f.hidden=false;f.id.value='';msg(f,'');if(t){{['id','title','gender','first_name','last_name','date_of_birth','nationality','passport_no','passport_expiry','passport_issue_place','meal_pref','mobile','email'].forEach(k=>{{if(f[k])f[k].value=t[k]||'';}});f.is_self.checked=!!t.is_self;}}f.scrollIntoView({{behavior:'smooth',block:'start'}});}}
 $('#trv_add').onclick=()=>openTrv(null);$('#trv_cancel').onclick=()=>{{TF().hidden=true;}};
 $('#f_trv').addEventListener('submit',async e=>{{e.preventDefault();const f=e.target;if(f.first_name.value.trim().length<1)return msg(f,'Please enter the first name as on the passport.','err');
  const row={{title:f.title.value,gender:f.gender.value,first_name:f.first_name.value.trim(),last_name:f.last_name.value.trim()||null,date_of_birth:f.date_of_birth.value||null,nationality:f.nationality.value.trim()||null,passport_no:f.passport_no.value.trim().toUpperCase()||null,passport_expiry:f.passport_expiry.value||null,passport_issue_place:f.passport_issue_place.value.trim()||null,meal_pref:f.meal_pref.value||null,mobile:f.mobile.value.trim()||null,email:f.email.value.trim()||null,is_self:f.is_self.checked,updated_at:new Date().toISOString()}};
  msg(f,'Saving…');const r=f.id.value?await c.from('travellers').update(row).eq('id',f.id.value):await c.from('travellers').insert(row);
  if(r.error)return msg(f,'Could not save – please check the details and try again.','err');f.hidden=true;loadTrv();}});
 async function loadRewards(){{
  let ref=null;try{{ref=localStorage.getItem('rtt_ref');}}catch(_){{}}
  const r=await c.rpc('rewards_init',{{ref_code:ref}});if(r.error){{$('#a_rw').hidden=true;return;}}
  try{{localStorage.removeItem('rtt_ref');}}catch(_){{}}
  const code=r.data.code,link='https://www.therealtoursandtravels.com/?ref='+code;
  $('#rw_bal').textContent=r.data.balance;$('#rw_code').textContent=code;
  const {{data:set}}=await c.from('reward_settings').select('*').order('points');
  const S={{}};(set||[]).forEach(x=>S[x.key]=x);if(S.referral)$('#rw_refpts').textContent=S.referral.points;
  $('#rw_earn').innerHTML=(set||[]).filter(x=>!['welcome','referral'].includes(x.key)).map(x=>'<li>'+x.label+': <b>'+x.points+' points</b></li>').join('');
  $('#rw_wa').href='https://wa.me/?text='+encodeURIComponent('I book my trips with The Real Tours and Travels (since 1981). Use my code '+code+' – we both get '+((S.referral||{{}}).points||100)+' reward points on your first booking: '+link);
  $('#rw_copy').onclick=()=>{{navigator.clipboard&&navigator.clipboard.writeText(link).then(()=>{{$('#rw_copy').textContent='Copied ✓';}});}};
  const {{data:h}}=await c.from('reward_ledger').select('points,note,created_at,expires_at').order('created_at',{{ascending:false}}).limit(50);
  $('#rw_hist').innerHTML=(h||[]).map(x=>'<li><b style="color:'+(x.points>0?'#1b7a3a':'#b3121a')+'">'+(x.points>0?'+':'')+x.points+'</b> '+(x.note||'')+'<br><small>'+new Date(x.created_at).toLocaleDateString('en-IN',{{dateStyle:'medium'}})+(x.expires_at&&x.points>0?' · valid till '+new Date(x.expires_at).toLocaleDateString('en-IN',{{dateStyle:'medium'}}):'')+'</small></li>').join('')||'<li>No points yet.</li>';
 }}
 async function loadEnq(){{
  const T=[['flight_enquiries','FL','✈️ Flight',r=>r.from_city+' → '+r.to_city+' · '+r.depart_date],['booking_enquiries','',null,r=>r.destination+(r.start_date?' · '+r.start_date:(r.travel_month?' · '+r.travel_month:''))],['insurance_enquiries','IN','🛡️ Insurance',r=>r.destination+' · '+r.start_date],['trip_requests','','✨ Package',r=>r.destination+' · '+r.days+' days'],['visa_applications','','🛂 Visa / Passport',r=>r.country],['service_enquiries','SV','🧳 Enquiry',r=>r.service+' · '+(r.destination||r.travel_month||'')]];
  let rows=[];
  for(const [t,pre,label,desc] of T){{const {{data}}=await c.from(t).select('*').order('created_at',{{ascending:false}}).limit(20);(data||[]).forEach(r=>{{const lb=label||(r.kind==='hotel'?'🏨 Hotel':'🛳️ Cruise');const pf=pre||(t==='booking_enquiries'?(r.kind==='hotel'?'HT':'CR'):'');rows.push({{at:r.created_at,lb,ref:(pf?pf+'-'+r.id.slice(0,6):r.id.slice(0,8)).toUpperCase(),d:desc(r),st:r.status}});}});}}
  rows.sort((a,b)=>b.at.localeCompare(a.at));
  const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}})[c]);
  $('#a_enq').innerHTML=rows.length?'<ul class="enq">'+rows.map(r=>'<li><b>'+r.lb+'</b> <span class="eref">'+r.ref+'</span><br>'+esc(r.d)+'<br><small>'+new Date(r.at).toLocaleString('en-IN',{{dateStyle:'medium',timeStyle:'short'}})+' · '+(r.st==='new'?'Received':esc(r.st))+'</small></li>').join('')+'</ul>':'No enquiries yet. Use the links above to plan your next trip!';
 }}
 document.querySelectorAll('[data-google]').forEach(b=>b.addEventListener('click',async()=>{{const f=b.closest('form');msg(f,'Opening Google…');let on=true;try{{const st=await fetch('{SB_URL}/auth/v1/settings',{{headers:{{apikey:'{SB_KEY}'}}}}).then(r=>r.json());on=!!(st.external&&st.external.google);}}catch(_){{}}if(!on){{msg(f,'Google sign-in will be available shortly. Please use your email for now.','err');return;}}const {{error}}=await c.auth.signInWithOAuth({{provider:'google',options:{{redirectTo:location.origin+'/account/'}}}});if(error)msg(f,'Could not open Google sign-in. Please try again or use your email.','err');}}));
 $('#f_login').addEventListener('submit',async e=>{{e.preventDefault();const f=e.target;msg(f,'Logging in…');
  const {{error}}=await c.auth.signInWithPassword({{email:f.email.value.trim(),password:f.password.value}});
  if(error){{msg(f,/confirm/i.test(error.message)?'Please confirm your email first – check your inbox for our link.':'Wrong email or password. Please try again.','err');return;}}
  location.replace('./');}});
 $('#forgot').addEventListener('click',async()=>{{const f=$('#f_login'),em=f.email.value.trim();if(!em){{msg(f,'Enter your email above, then tap "Forgot password?".','err');return;}}
  await c.auth.resetPasswordForEmail(em,{{redirectTo:location.origin+'/account/'}});msg(f,'If an account exists for '+em+', we have emailed a link to reset your password.','ok');}});
 $('#f_signup').addEventListener('submit',async e=>{{e.preventDefault();const f=e.target;
  const ph=f.phone.value.replace(/[^0-9]/g,'');
  if(f.full_name.value.trim().length<2)return msg(f,'Please enter your full name.','err');
  if(ph.length<10||ph.length>13)return msg(f,'Please enter a valid 10-digit mobile number.','err');
  if(!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(f.email.value.trim()))return msg(f,'Please enter a valid email.','err');
  if(f.password.value.length<8)return msg(f,'Password must be at least 8 characters.','err');
  if(!f.agree.checked)return msg(f,'Please agree to the Terms and Privacy Policy.','err');
  msg(f,'Creating your account…');
  const meta={{full_name:f.full_name.value.trim(),phone:ph,city:f.city.value.trim(),consent_email:f.consent_email.checked,consent_whatsapp:f.consent_whatsapp.checked}};
  const {{data,error}}=await c.auth.signUp({{email:f.email.value.trim(),password:f.password.value,options:{{data:meta,emailRedirectTo:location.origin+'/account/'}}}});
  if(error){{msg(f,/registered|exists/i.test(error.message)?'This email already has an account – please log in.':'Sorry, could not create the account: '+error.message,'err');return;}}
  if(data.session){{location.replace('./');}}else{{msg(f,'✅ Almost done! We have emailed a confirmation link to '+f.email.value.trim()+'. Click it to activate your account.','ok');}}
 }});
 $('#f_profile').addEventListener('submit',async e=>{{e.preventDefault();const f=e.target;const {{data:{{session}}}}=await c.auth.getSession();if(!session)return render();
  const row={{full_name:f.full_name.value.trim()||null,phone:f.phone.value.replace(/[^0-9+]/g,'')||null,email:f.email.value.trim()||null,city:f.city.value.trim()||null,date_of_birth:f.date_of_birth.value||null,food_preference:f.food_preference.value||null,travel_interests:f.travel_interests.value.trim()||null,consent_email:f.consent_email.checked,consent_whatsapp:f.consent_whatsapp.checked,updated_at:new Date().toISOString()}};
  const {{error}}=await c.from('profiles').update(row).eq('id',session.user.id);
  if(error)msg(f,'Could not save. Please try again.','err');else{{msg(f,'✅ Saved.','ok');$('#a_name').textContent=(row.full_name||'traveller').split(' ')[0];}}}});
 $('#f_reset').addEventListener('submit',async e=>{{e.preventDefault();const f=e.target;if(f.password.value.length<8)return msg(f,'Password must be at least 8 characters.','err');
  const {{error}}=await c.auth.updateUser({{password:f.password.value}});if(error)return msg(f,'Could not update password. Please request a new link.','err');recovering=false;history.replaceState(null,'','./');render();}});
 $('#logout').addEventListener('click',async()=>{{await c.auth.signOut();location.replace('./');}});
 render();
}}).catch(()=>{{$('#a_loading').hidden=false;$('#a_loading').textContent='Could not load login. Please check your internet connection and refresh.';}});
}})();
</script>"""

ACCOUNT_CSS = """
.trv-bar{grid-column:1/-1;display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:0 0 4px}.trv-btn{border:1px dashed #c98f93;background:#fbf4f4;color:#8f1d24;border-radius:12px;padding:9px 14px;font:600 14px 'Jost',sans-serif;cursor:pointer}
.trv-chips{display:flex;flex-wrap:wrap;gap:6px}.trv-chips span{background:#fff;border:1px solid #e4d6d7;border-radius:99px;padding:4px 10px;font-size:12.5px;color:#4a3b3c}
.trv-sheet{position:fixed;inset:0;z-index:300;background:rgba(20,15,15,.45);display:flex;align-items:flex-end;justify-content:center}.trv-sheet[hidden]{display:none}
.trv-pan{width:100%;max-width:520px;max-height:82vh;overflow:auto;background:#fff;border-radius:20px 20px 0 0;padding:16px 16px calc(18px + env(safe-area-inset-bottom));animation:trvUp .25s ease}@keyframes trvUp{from{transform:translateY(40px);opacity:0}}
@media(min-width:700px){.trv-sheet{align-items:center}.trv-pan{border-radius:20px}}
.trv-h{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}.trv-h b{font-size:17px;color:var(--wine)}.trv-x{border:0;background:#f3eeee;border-radius:50%;width:32px;height:32px;cursor:pointer}
.trv-opts{display:flex;flex-direction:column;gap:8px}.trv-op{display:flex;gap:12px;align-items:center;border:1px solid var(--line);border-radius:14px;padding:11px 12px;cursor:pointer}.trv-op:has(input:checked){border-color:#c98f93;background:#fbf4f4}.trv-op input{width:20px;height:20px;accent-color:#b3121a}.trv-op small{display:block;color:var(--muted);font-size:12.5px}
.trv-n{font-size:12.5px;color:var(--muted);margin:10px 2px}.trv-ok{width:100%;justify-content:center}.trv-new{display:block;text-align:center;margin-top:12px;color:var(--crimson);font-weight:600;text-decoration:none;font-size:14px}
.trv{margin-top:24px}.trv-top{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap}.trv-top .btn{padding:9px 16px;font-size:14px}
.trv-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px;margin-top:14px}
.trv-item{display:flex;justify-content:space-between;gap:10px;background:var(--bg);border:1px solid var(--line);border-radius:14px;padding:12px 14px}.trv-item b{display:block}.trv-item em{font-style:normal;font-size:11px;background:#f8ecec;color:#8f1d24;border-radius:99px;padding:2px 8px;margin-left:4px}.trv-item small{display:block;color:var(--muted);font-size:12.5px;margin-top:2px}.trv-warn{color:#9a3b12}.trv-act{display:flex;flex-direction:column;gap:6px;align-items:flex-end}
.trv-form{margin-top:16px;border-top:1px solid var(--line);padding-top:16px}
.gbtn{display:flex;align-items:center;justify-content:center;gap:10px;width:100%;background:#fff;border:1px solid #dadce0;border-radius:12px;padding:12px 14px;font:600 15px 'Jost',sans-serif;color:#3c4043;cursor:pointer;box-shadow:0 1px 3px rgba(0,0,0,.06)}.gbtn:active{background:#f6f6f6}
.aor{display:flex;align-items:center;gap:10px;margin:2px 0;color:#9a8e8e;font-size:12.5px}.aor:before,.aor:after{content:"";flex:1;height:1px;background:var(--line)}
.gnote{margin:-6px 0 0;font-size:12.5px;text-align:center}
.rwcard{display:grid;gap:14px;border-top:4px solid var(--red)}.rwtop{display:flex;justify-content:space-between;align-items:center;gap:12px}.rwbal{display:grid;text-align:center;background:var(--bg);border:1px solid var(--line);border-radius:16px;padding:8px 16px}.rwbal b{font-size:30px;color:var(--crimson);line-height:1.1}.rwbal span{font-size:12px;color:var(--muted)}.rwref{background:#fdf6f6;border-radius:14px;padding:12px 14px}.rwcode{display:flex;flex-wrap:wrap;gap:8px;align-items:center}.rwcode span{font:700 18px monospace;letter-spacing:2px;background:#fff;border:1px dashed var(--crimson);border-radius:10px;padding:6px 12px}.rwcode .btn{padding:7px 14px;font-size:14px}.rwhow summary{cursor:pointer;font-weight:600}
.acct-link{position:absolute;right:22px;top:50%;transform:translateY(-50%);text-decoration:none;color:var(--crimson);font-weight:600;border:1.5px solid var(--red);border-radius:999px;padding:8px 16px;white-space:nowrap;background:#fff}
.acct-link:hover{background:#fdf0f0}
header.site .hrow{position:relative}
.acct-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:24px;align-items:start;margin-top:18px}
.acct-card{background:#fff;border:1px solid var(--line);border-radius:20px;padding:26px;box-shadow:0 16px 36px rgba(0,0,0,.05)}
.vform.anoborder{border:0;padding:0;background:none;box-shadow:none}
.atabs{display:flex;gap:6px;border-bottom:1px solid var(--line);margin-bottom:18px}.atab{border:0;background:none;padding:10px 14px;font:600 16px 'Jost',sans-serif;color:var(--muted);border-bottom:3px solid transparent;margin-bottom:-1px;cursor:pointer}.atab.on{color:var(--red);border-bottom-color:var(--red)}
.linkbtn{border:0;background:none;color:var(--red);text-decoration:underline;font:500 14px 'Jost',sans-serif;cursor:pointer;justify-self:start;padding:0}
.acct-why{padding:10px 6px}.acct-why h2{margin-top:0}
.acct-top{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}.acct-top .btn{border:1.5px solid var(--ink);background:#fff;cursor:pointer;font-family:inherit}
.acct-quick{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}.acct-quick a{border:1px solid var(--line);border-radius:999px;padding:8px 14px;text-decoration:none;color:var(--ink);font-weight:500;background:#fff}.acct-quick a:hover{border-color:var(--red);color:var(--red)}
ul.enq{list-style:none;padding:0;margin:0}ul.enq li{padding:12px 0;border-bottom:1px solid var(--line);color:var(--ink);font-size:15px}.eref{font-size:12px;background:var(--bg);border:1px solid var(--line);border-radius:999px;padding:1px 8px;color:var(--muted)}
@media(max-width:1100px){.acct-link{position:static;transform:none;margin-left:auto;margin-right:6px;flex:none;padding:7px 12px;font-size:14px}header.site .brand{min-width:0;flex:1 1 auto}header.site .brand span{min-width:0}}
@media(max-width:560px){header.site .brand b{white-space:normal;font-size:15.5px}header.site .brand{gap:8px}}
@media(max-width:800px){.acct-grid{grid-template-columns:1fr}.acct-card{padding:18px}}
@media(max-width:420px){.acct-link{font-size:0;padding:7px 10px}.acct-link:before{content:'👤';font-size:18px}}
html.is-app .acct-link{font-size:0;padding:7px 10px}html.is-app .acct-link:before{content:'👤';font-size:18px}.aswitch{margin-top:18px;padding-top:14px;border-top:1px dashed var(--line);color:var(--muted);display:flex;flex-wrap:wrap;align-items:center;gap:10px}.atab{font-size:17px}
"""
