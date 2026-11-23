"""Customer accounts (Supabase Auth): login/sign-up page, profile, my enquiries, and site-wide form prefill."""
from visa import SB_URL, SB_KEY

SBJS = "/js/supabase.js"
STORE_KEY = "sb-byvytpxqqgjschknqpms-auth-token"

# Loaded on every page: only pulls in the login library when the visitor is (or may be) logged in.
SITE_JS = f"""<script>
(function(){{
 const SB="{SB_URL}",KEY="{SB_KEY}",LIB="{SBJS}";
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
<label>Email<input name="email" type="email" required autocomplete="email"></label>
<label>Password<input name="password" type="password" required autocomplete="current-password" minlength="6"></label>
<button class="btn gold" type="submit">Log in</button>
<button class="linkbtn" type="button" id="forgot">Forgot password?</button>
<p class="vmsg" role="status"></p><div class="aswitch">New here? <button type="button" class="btn outline" data-go="signup">✨ Create a free account</button></div></form>
<form id="f_signup" class="vform anoborder" novalidate hidden>
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
<li>Free – no card needed</li></ul>
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
<div class="acct-card"><h2 style="margin:0 0 6px">My enquiries</h2><div id="a_enq" class="meta">Loading…</div></div>
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
  if(!p){{const m=u.user_metadata||{{}};const row={{id:u.id,full_name:m.full_name||null,phone:m.phone||null,email:u.email,city:m.city||null,consent_email:!!m.consent_email,consent_whatsapp:!!m.consent_whatsapp}};
   const r=await c.from('profiles').insert(row);if(!r.error){{p=row;notify('New customer registered – '+(row.full_name||u.email),'Name: '+(row.full_name||'')+'\\nMobile: '+(row.phone||'')+'\\nEmail: '+u.email+'\\nCity: '+(row.city||'')+'\\nWhatsApp offers: '+(row.consent_whatsapp?'Yes':'No')+'\\nEmail offers: '+(row.consent_email?'Yes':'No'),u.email);}}}}
  p=p||{{}};$('#a_name').textContent=(p.full_name||'traveller').split(' ')[0];
  const f=$('#f_profile');['full_name','phone','email','city','date_of_birth','food_preference','travel_interests'].forEach(k=>{{if(f[k])f[k].value=p[k]||'';}});
  f.consent_email.checked=!!p.consent_email;f.consent_whatsapp.checked=!!p.consent_whatsapp;
  loadEnq();
 }}
 async function loadEnq(){{
  const T=[['flight_enquiries','FL','✈️ Flight',r=>r.from_city+' → '+r.to_city+' · '+r.depart_date],['booking_enquiries','',null,r=>r.destination+(r.start_date?' · '+r.start_date:(r.travel_month?' · '+r.travel_month:''))],['insurance_enquiries','IN','🛡️ Insurance',r=>r.destination+' · '+r.start_date],['trip_requests','','✨ Package',r=>r.destination+' · '+r.days+' days'],['visa_applications','','🛂 Visa / Passport',r=>r.country],['service_enquiries','SV','🧳 Enquiry',r=>r.service+' · '+(r.destination||r.travel_month||'')]];
  let rows=[];
  for(const [t,pre,label,desc] of T){{const {{data}}=await c.from(t).select('*').order('created_at',{{ascending:false}}).limit(20);(data||[]).forEach(r=>{{const lb=label||(r.kind==='hotel'?'🏨 Hotel':'🛳️ Cruise');const pf=pre||(t==='booking_enquiries'?(r.kind==='hotel'?'HT':'CR'):'');rows.push({{at:r.created_at,lb,ref:(pf?pf+'-'+r.id.slice(0,6):r.id.slice(0,8)).toUpperCase(),d:desc(r),st:r.status}});}});}}
  rows.sort((a,b)=>b.at.localeCompare(a.at));
  const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}})[c]);
  $('#a_enq').innerHTML=rows.length?'<ul class="enq">'+rows.map(r=>'<li><b>'+r.lb+'</b> <span class="eref">'+r.ref+'</span><br>'+esc(r.d)+'<br><small>'+new Date(r.at).toLocaleString('en-IN',{{dateStyle:'medium',timeStyle:'short'}})+' · '+(r.st==='new'?'Received':esc(r.st))+'</small></li>').join('')+'</ul>':'No enquiries yet. Use the links above to plan your next trip!';
 }}
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
