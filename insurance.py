"""Travel insurance section: what's covered + quote form -> Supabase + email alert + WhatsApp."""
from visa import SB_URL, SB_KEY

DESTS = ["Europe (Schengen)", "United Kingdom", "USA / Canada", "Dubai / UAE & Middle East", "Thailand / Singapore / Malaysia",
         "Bali / Vietnam / rest of Asia", "Maldives / Sri Lanka / Nepal", "Australia / New Zealand", "Japan / South Korea",
         "Africa", "Worldwide (multiple countries)", "Within India"]

def insurance_page(PHONE, PHONE_RAW, EMAIL, seal, cta_band):
    dopts = "".join(f"<option>{d}</option>" for d in DESTS)
    return f"""
<section class="hero"><div class="wrap"><div><div class="crumbs"><a href="../">Home</a> › Travel Insurance</div>
<span class="kicker">🛡️ Travel insurance</span>
<h1>Travel Insurance – Get a Quotation</h1>
<p>Medical emergencies, trip cancellation, lost baggage and flight delays – protect your family before you travel. Tell us about your trip and we'll send you the best plans from leading insurers.</p>
<div class="btns"><a class="btn gold" href="#ins-form">Get quotation</a><a class="btn ghost" href="tel:{PHONE_RAW}">📞 {PHONE}</a></div>
</div>{seal("../")}</div></section>

<section><div class="wrap">
<div class="head"><span class="kicker">What it covers</span><h2>Why travel insurance matters</h2><p class="lead">Cover depends on the plan and insurer – we explain every plan before you buy.</p></div>
<div class="grid">
<div class="card"><div class="ic">🏥</div><h3>Medical emergencies</h3><p>Hospitalisation and treatment abroad, emergency evacuation and repatriation.</p></div>
<div class="card"><div class="ic">✈️</div><h3>Trip cancellation &amp; delay</h3><p>Cancellation or cutting short for covered reasons, flight delays and missed connections.</p></div>
<div class="card"><div class="ic">🧳</div><h3>Baggage &amp; passport</h3><p>Lost or delayed checked baggage and loss of passport while travelling.</p></div>
<div class="card"><div class="ic">🇪🇺</div><h3>Visa-ready plans</h3><p>Schengen-compliant plans with minimum €30,000 medical cover for the whole stay, and plans for USA, UK and other visas.</p></div>
<div class="card"><div class="ic">👵</div><h3>Senior citizens</h3><p>Plans for travellers above 60 and 70 years – pre-existing conditions must be declared.</p></div>
<div class="card"><div class="ic">🎓</div><h3>Students &amp; frequent flyers</h3><p>Long-stay student plans and annual multi-trip plans for business travellers.</p></div>
</div></div></section>

<section class="alt" id="ins-form"><div class="wrap" style="max-width:860px">
<div class="head"><span class="kicker">Free quotation</span><h2>Get your travel insurance quotation</h2><p class="lead">Takes a minute. We compare plans and reply on WhatsApp or email.</p></div>
<form id="iform" class="vform" novalidate>
<fieldset><legend>Type of cover*</legend><div class="chips">
<label><input type="radio" name="trip_type" value="International" checked>🌍 International trip</label><label><input type="radio" name="trip_type" value="Domestic">🇮🇳 Domestic trip</label><label><input type="radio" name="trip_type" value="Annual multi-trip">🔁 Annual multi-trip</label><label><input type="radio" name="trip_type" value="Student">🎓 Student</label></div></fieldset>
<div class="row"><label>Destination*<select name="destination" required>{dopts}</select></label>
<label>Purpose of travel<select name="purpose"><option>Holiday / leisure</option><option>Business</option><option>Visiting family</option><option>Study</option><option>Pilgrimage / yatra</option></select></label></div>
<div class="row"><label>Travel start date*<input name="start" type="date" required></label>
<label id="endwrap">Travel end date*<input name="end" type="date"></label></div>
<div class="row"><label>Number of travellers*<input name="travellers" type="number" min="1" max="30" value="2" required></label>
<label>Ages of travellers* <small>(e.g. 45, 42, 12)</small><input name="ages" required maxlength="120" placeholder="45, 42, 12" inputmode="numeric"></label></div>
<div class="row"><label>Preferred medical cover<select name="cover"><option>Not sure – suggest</option><option>$50,000</option><option>$100,000</option><option>$250,000</option><option>$500,000</option><option>€30,000 (Schengen minimum)</option><option>₹5 lakh (domestic)</option><option>₹10 lakh (domestic)</option></select></label>
<label>Any pre-existing medical condition?<select name="pre_existing"><option>No</option><option>Yes</option><option>Not sure</option></select></label></div>
<label class="chk"><input type="checkbox" name="visa"><span>I need this policy for a <b>visa application</b> (we'll make sure it meets the embassy's requirements).</span></label>
<div class="row"><label>Your name<input name="full_name" maxlength="120" autocomplete="name"></label>
<label>Mobile or email* <small>(to send your quotation)</small><input name="contact" required maxlength="160" autocomplete="tel" placeholder="98xxxxxxxx, +971… or you@example.com"></label></div>
<label>Notes<textarea name="notes" rows="2" maxlength="1000" placeholder="e.g. adventure activities, cruise, cover for trip cancellation"></textarea></label>
<div class="hp" aria-hidden="true"><label>Leave this empty<input name="company_website" tabindex="-1" autocomplete="off"></label></div>
<button class="btn gold" type="submit" id="isubmit">🛡️ Get Quotation on WhatsApp</button>
<p id="imsg" class="vmsg" role="status" aria-live="polite"></p>
<p class="vpriv">🔒 We use your details only to prepare your quotation – never shared or sold. <a href="../privacy-policy/">Privacy Policy</a></p>
<p class="meta" style="margin:0">Premiums include GST as charged by the insurer. Policies are issued by the insurance company; terms, exclusions and claim decisions are as per the policy wording.</p>
</form></div></section>
{cta_band()}
<script>
(function(){{
const SB="{SB_URL}",KEY="{SB_KEY}";
const notify=(s,t,r)=>{{try{{fetch('https://formsubmit.co/ajax/enquiry@therealtoursandtravels.com',{{method:'POST',headers:{{'Content-Type':'application/json',Accept:'application/json'}},body:JSON.stringify((()=>{{const o={{_subject:s,message:t,_replyto:r||'',_template:'table',_captcha:'false',source:location.href}};const m=(s.match(/(\\S+) – /)||[])[1]||'';const ref=/^[A-Z0-9-]{{6,}}$/.test(m)?m:'';if(r&&/@/.test(r)&&ref){{o.email=r;o._autoresponse='Thank you for contacting The Real Tours and Travels. We have received your request (reference '+ref+') and our team will get back to you shortly. Please quote this reference in any message to us. For anything urgent, call or WhatsApp +91 98431 21212. – The Real Tours and Travels, Mulund West, Mumbai · www.therealtoursandtravels.com';}}return o;}})())}}).catch(()=>{{}});}}catch(_){{}}}};
const f=document.getElementById('iform'),msg=document.getElementById('imsg'),btn=document.getElementById('isubmit'),endw=document.getElementById('endwrap');
const today=new Date(Date.now()+330*6e4).toISOString().slice(0,10);f.start.min=f.end.min=today;
const tt=()=>f.querySelector('input[name=trip_type]:checked').value;
function sync(){{const t=tt();endw.style.display=t==='Annual multi-trip'?'none':'';if(t==='Domestic')f.destination.value='Within India';else if(f.destination.value==='Within India')f.destination.selectedIndex=0;}}
f.querySelectorAll('input[name=trip_type]').forEach(r=>r.addEventListener('change',sync));
f.start.addEventListener('change',()=>{{f.end.min=f.start.value||today;}});
function uuid(){{return crypto.randomUUID?crypto.randomUUID():'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,c=>{{const r=Math.random()*16|0;return (c=='x'?r:(r&3|8)).toString(16);}});}}
const fd=d=>new Date(d+'T00:00').toLocaleDateString('en-IN',{{day:'numeric',month:'short',year:'numeric'}});
f.addEventListener('submit',async e=>{{
 e.preventDefault();msg.className='vmsg';
 if(f.company_website.value){{msg.textContent='✅ Thank you – request received.';msg.classList.add('ok');return;}} // spam trap
 const t=tt(),c=f.contact.value.trim(),n=parseInt(f.travellers.value)||0,ages=f.ages.value.trim();
 const isEmail=/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(c),digits=c.replace(/[^0-9]/g,''),isPhone=!isEmail&&(c.startsWith('+')?digits.length>=8&&digits.length<=15:digits.length>=10&&digits.length<=13);
 const ageList=(ages.match(/\\d+/g)||[]).map(Number);
 let err='';
 if(!f.start.value)err='Please choose your travel start date.';
 else if(t!=='Annual multi-trip'&&!f.end.value)err='Please choose your travel end date.';
 else if(t!=='Annual multi-trip'&&f.end.value<f.start.value)err='End date must be after the start date.';
 else if(n<1||n>30)err='Please enter the number of travellers.';
 else if(!ageList.length||ageList.some(a=>a<0||a>100))err='Please enter the age of each traveller, e.g. 45, 42, 12.';
 else if(!isEmail&&!isPhone)err='Please enter a valid mobile number (outside India, start with your country code, e.g. +971…) or an email so we can send your quotation.';
 if(err){{msg.textContent=err;msg.classList.add('err');return;}}
 btn.disabled=true;msg.textContent='Sending your request…';
 let w=null;try{{w=window.open('','_blank');if(w)w.document.write('<p style="font:16px sans-serif;padding:20px">Opening WhatsApp…</p>');}}catch(_){{w=null;}}
 const id=uuid(),ref='IN-'+id.slice(0,6).toUpperCase(),name=f.full_name.value.trim()||null,notes=f.notes.value.trim()||null;
 const row={{id,trip_type:t,destination:f.destination.value,start_date:f.start.value,end_date:t==='Annual multi-trip'?null:f.end.value,travellers:n,ages:ages.slice(0,120),purpose:f.purpose.value,cover:f.cover.value,pre_existing:f.pre_existing.value,visa_required:f.visa.checked,full_name:name,phone:isPhone?digits:null,email:isEmail?c:null,notes}};
 try{{const r=await fetch(SB+'/rest/v1/insurance_enquiries',{{method:'POST',headers:{{apikey:KEY,Authorization:'Bearer '+(window.RTT_TOKEN||KEY),'Content-Type':'application/json',Prefer:'return=minimal'}},body:JSON.stringify(row)}});if(!r.ok)throw 0;}}
 catch(_){{if(w)w.close();btn.disabled=false;msg.textContent='Sorry, something went wrong. Please WhatsApp us on 98431 21212.';msg.classList.add('err');return;}}
 const lines=['🛡️ Travel insurance quote request ('+ref+')','Cover: '+t+' · '+row.purpose,'Destination: '+row.destination,'Dates: '+fd(row.start_date)+(row.end_date?' → '+fd(row.end_date):' (annual)'),'Travellers: '+n+' · Ages: '+ages,'Medical cover: '+row.cover,'Pre-existing condition: '+row.pre_existing,row.visa_required?'Needed for visa: Yes':'',notes?'Notes: '+notes:'',name?'Name: '+name:'','Contact: '+c].filter(Boolean);
 const wa='https://wa.me/919843121212?text='+encodeURIComponent(lines.join('\\n'));
 notify('New insurance enquiry '+ref+' – '+(name||c),lines.join('\\n'),isEmail?c:'');
 if(w){{try{{w.location.href=wa;}}catch(_){{}}}}
 msg.innerHTML='✅ Request received (Ref <b>'+ref+'</b>). Please press <b>Send</b> in WhatsApp so our team gets it instantly. If WhatsApp did not open: <a class="btn gold" style="margin-top:10px" href="'+wa+'" target="_blank" rel="noopener">💬 Send on WhatsApp</a>';
 msg.classList.add('ok');btn.disabled=false;
}});
}})();
</script>"""
