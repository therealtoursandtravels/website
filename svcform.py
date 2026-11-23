"""Short enquiry form for service pages (honeymoon, group, yatra, FIT & MICE, Jain yatra…).
Saves to Supabase table service_enquiries, emails the team, opens WhatsApp with the details."""
from visa import SB_URL, SB_KEY

# slug -> (service name, destination label, destination placeholder, extra HTML)
JAIN_EXTRA = """<div class="sf-row">
<label>Senior citizens in the group<select name="x_seniors" data-lbl="Senior citizens"><option value="">None</option>""" + "".join(f"<option>{i}</option>" for i in range(1, 21)) + """<option>More than 20</option></select></label>
<label>Doli / palki for the climb?<select name="x_doli" data-lbl="Doli / palki"><option value="">Not needed</option><option>Yes – please arrange</option><option>Not sure yet</option></select></label>
<label>Stay preference<select name="x_stay" data-lbl="Stay"><option value="">Any – please suggest</option><option>Dharamshala</option><option>Hotel</option><option>Mix of both</option></select></label></div>
<div class="sf-chk"><span>Food &amp; observances:</span>
<label><input type="checkbox" name="x_food" value="Pure Jain food – no root vegetables" checked> Pure Jain food (no kandmool)</label>
<label><input type="checkbox" name="x_food" value="Chovihar – all meals before sunset"> Chovihar</label>
<label><input type="checkbox" name="x_food" value="No green vegetables on tithi days"> Tithi days – no green vegetables</label>
<label><input type="checkbox" name="x_food" value="Boiled (ukalelu) water"> Ukalelu (boiled) water</label>
<label><input type="checkbox" name="x_food" value="Ekasana / ayambil arrangements"> Ekasana / ayambil</label></div>
<label class="sf-chk1"><input type="checkbox" name="x_notify" value="Tell me about upcoming group yatras"> Tell me about upcoming <b>group yatras</b> with Maharaj</label>"""

GROUP_EXTRA = """<div class="sf-row"><label>Type of group<select name="x_gtype" data-lbl="Group type"><option value="">Choose…</option><option>Extended family / friends</option><option>Housing society / community</option><option>Women-only</option><option>Senior citizens</option><option>School / college</option><option>Corporate</option><option>Other</option></select></label>
<label>Departing from<input name="x_from" data-lbl="Departing from" maxlength="40" placeholder="e.g. your city" autocomplete="off"></label></div>"""

HONEY_EXTRA = """<div class="sf-row"><label>Wedding date (optional)<input name="x_wed" data-lbl="Wedding date" type="date"></label>
<label>Style<select name="x_style" data-lbl="Style"><option value="">Any – please suggest</option><option>Beach &amp; islands</option><option>Mountains &amp; snow</option><option>City &amp; culture</option><option>Adventure</option><option>Luxury / private villa</option></select></label></div>"""

MICE_EXTRA = """<div class="sf-row"><label>Type of travel<select name="x_mice" data-lbl="Type"><option value="">Choose…</option><option>FIT – individual / couple</option><option>Incentive trip</option><option>Conference / offsite</option><option>Event / exhibition</option><option>Dealer / employee meet</option></select></label>
<label>Company (optional)<input name="x_co" data-lbl="Company" maxlength="80" autocomplete="organization"></label></div>"""

YATRA_EXTRA = """<div class="sf-row"><label>Senior citizens in the group<select name="x_seniors" data-lbl="Senior citizens"><option value="">None</option>""" + "".join(f"<option>{i}</option>" for i in range(1, 21)) + """<option>More than 20</option></select></label>
<label>Helicopter / pony / palki help?<select name="x_help" data-lbl="Help needed"><option value="">Not needed</option><option>Yes – please arrange</option><option>Not sure yet</option></select></label></div>
<label class="sf-chk1"><input type="checkbox" name="x_jain" value="Jain / pure vegetarian food needed"> Jain / pure vegetarian food needed</label>"""

TRANSFER_EXTRA = """<div class="sf-row"><label>Type of trip<select name="x_type" data-lbl="Trip"><option>Airport pick-up</option><option>Airport drop</option><option>Outstation round trip</option><option>Outstation one way</option><option>Local car hire (full / half day)</option></select></label>
<label>Date &amp; time<input name="x_dt" data-lbl="Date &amp; time" type="datetime-local"></label></div>
<div class="sf-row"><label>Car<select name="x_car" data-lbl="Car"><option value="">Please suggest</option><option>Sedan (4 seats)</option><option>SUV (6–7 seats)</option><option>Innova Crysta</option><option>Tempo Traveller (12–17 seats)</option><option>Luxury car</option></select></label>
<label>Flight number (for airport trips)<input name="x_flt" data-lbl="Flight" maxlength="12" placeholder="e.g. 6E 2131" autocomplete="off"></label></div>"""

WEEKEND_EXTRA = """<div class="sf-row"><label>Stay<select name="x_stay" data-lbl="Stay"><option value="">Please suggest</option><option>Resort</option><option>Private villa / bungalow</option><option>Hotel</option></select></label>
<label>Car from your city?<select name="x_car" data-lbl="Car"><option value="">Yes – please arrange</option><option>No – we will drive</option></select></label></div>"""

SENIOR_EXTRA = """<div class="sf-row"><label>Number of senior citizens<input name="x_sen" data-lbl="Senior citizens" type="number" min="1" max="200"></label>
<label>Wheelchair needed?<select name="x_wc" data-lbl="Wheelchair"><option value="">No</option><option>Yes – at airports</option><option>Yes – throughout the trip</option></select></label></div>
<div class="sf-row"><label>Walking comfort<select name="x_walk" data-lbl="Walking"><option value="">Comfortable walking</option><option>Short walks only</option><option>Needs assistance</option></select></label>
<label>Food<select name="x_food1" data-lbl="Food"><option value="">Any</option><option>Pure vegetarian</option><option>Jain</option></select></label></div>"""

WEDDING_EXTRA = """<div class="sf-row"><label>Occasion<select name="x_occ" data-lbl="Occasion"><option>Wedding</option><option>Engagement</option><option>Anniversary</option><option>Birthday</option><option>Other family function</option></select></label>
<label>Rooms needed (approx.)<input name="x_rooms" data-lbl="Rooms" type="number" min="1" max="500"></label></div>
<label class="sf-chk1"><input type="checkbox" name="x_guest" value="Guest flights / trains needed"> Arrange flights / trains for guests</label>"""

EDU_EXTRA = """<div class="sf-row"><label>School / college name<input name="x_inst" data-lbl="Institution" maxlength="100" autocomplete="organization"></label>
<label>Class / year<input name="x_cls" data-lbl="Class" maxlength="40" placeholder="e.g. Std 8, FY BCom"></label></div>
<div class="sf-row"><label>Teachers / staff travelling<input name="x_staff" data-lbl="Teachers" type="number" min="0" max="100"></label>
<label>Theme<select name="x_theme" data-lbl="Theme"><option value="">Please suggest</option><option>Heritage &amp; history</option><option>Science / space</option><option>Industrial visit</option><option>Nature &amp; adventure camp</option><option>International tour</option></select></label></div>"""

PCC_EXTRA = """<div class="sf-row"><label>Purpose<select name="x_pur" data-lbl="Purpose"><option>Visa – long stay / work</option><option>Study abroad</option><option>Emigration / PR</option><option>Job abroad</option><option>Other</option></select></label>
<label>Service needed<select name="x_svc" data-lbl="Service"><option>Police Clearance Certificate (PCC)</option><option>Attestation / apostille</option><option>Both</option></select></label></div>
<div class="sf-row"><label>Is your current address the same as in your passport?<select name="x_addr" data-lbl="Address same as passport"><option value="">Not sure</option><option>Yes</option><option>No</option></select></label><span></span></div>"""

SAFARI_EXTRA = """<div class="sf-row"><label>Preferred park<select name="x_park" data-lbl="Park"><option value="">Please suggest</option><option>Tadoba</option><option>Ranthambore</option><option>Jim Corbett</option><option>Kanha / Bandhavgarh</option><option>Gir</option><option>Kenya – Masai Mara</option><option>Tanzania – Serengeti</option></select></label>
<label>Number of safari drives<select name="x_drives" data-lbl="Safari drives"><option value="">Please suggest</option><option>2</option><option>3–4</option><option>5 or more</option></select></label></div>
<div class="sf-row"><label>Stay<select name="x_stay" data-lbl="Stay"><option value="">Please suggest</option><option>Comfortable resort</option><option>Luxury jungle lodge</option><option>Budget stay</option></select></label><span></span></div>"""

WOMEN_EXTRA = """<div class="sf-row"><label>How would you like to travel?<select name="x_how" data-lbl="Trip type"><option>Join a women-only group departure</option><option>Private trip for our own group</option></select></label>
<label>Age group (approx.)<select name="x_age" data-lbl="Age group"><option value="">Mixed</option><option>18–30</option><option>30–45</option><option>45–60</option><option>60+</option></select></label></div>
<div class="sf-row"><label>Room preference<select name="x_room" data-lbl="Rooms"><option value="">Twin sharing</option><option>Single rooms</option><option>Triple sharing</option></select></label>
<label>Food<select name="x_food1" data-lbl="Food"><option value="">Any</option><option>Pure vegetarian</option><option>Jain</option></select></label></div>
<label class="sf-chk1"><input type="checkbox" name="x_tm" value="Woman tour manager requested"> Woman tour manager requested</label>"""

TREK_EXTRA = """<div class="sf-row"><label>Experience level<select name="x_lvl" data-lbl="Experience"><option>First trek / beginner</option><option>Done 1–2 treks</option><option>Experienced trekker</option></select></label>
<label>Type of adventure<select name="x_adv" data-lbl="Adventure"><option value="">Please suggest</option><option>Himalayan trek</option><option>Ladakh / Spiti road trip</option><option>Rafting / paragliding / camping</option><option>Bhutan / Nepal</option><option>Sahyadri / weekend trek</option></select></label></div>
<label class="sf-chk1"><input type="checkbox" name="x_gear" value="Needs rental trekking gear"> We'll need rental gear (jackets, poles, sleeping bags)</label>"""

CFG = {
 "domestic-holiday-packages": ("Domestic holiday", "Where in India?", "e.g. Kashmir, Kerala, Goa – or suggest", ""),
 "international-holiday-packages": ("International holiday", "Which country or countries?", "e.g. Dubai, Bali, Europe – or suggest", ""),
 "yatra-tours": ("Yatra", "Which yatra?", "e.g. Char Dham, Vaishno Devi, Kashi–Ayodhya", YATRA_EXTRA),
 "group-tours": ("Group tour", "Where would the group like to go?", "e.g. Rajasthan, Thailand – or suggest", GROUP_EXTRA),
 "honeymoon-packages": ("Honeymoon", "Where would you like to go?", "e.g. Maldives, Bali, Kashmir – or suggest", HONEY_EXTRA),
 "fit-mice-tours": ("FIT / MICE", "Destination or city", "e.g. Goa offsite, Dubai incentive trip", MICE_EXTRA),
 "airport-transfers-outstation-cabs": ("Airport transfer / cab", "Pick-up and drop (from → to)", "e.g. Home → Airport (Terminal 2)", TRANSFER_EXTRA),
 "weekend-getaways": ("Weekend getaway", "Where would you like to go?", "e.g. a hill station or beach – or suggest", WEEKEND_EXTRA),
 "senior-citizen-tours": ("Senior citizen tour", "Where would you like to go?", "e.g. Kerala, Char Dham, Singapore – or suggest", SENIOR_EXTRA),
 "destination-weddings-family-functions": ("Wedding / family function", "Preferred destination", "e.g. Udaipur, Goa, Dubai – or suggest", WEDDING_EXTRA),
 "school-college-educational-tours": ("Educational tour", "Where would you like to go?", "e.g. Delhi–Agra, ISRO Bengaluru, Singapore", EDU_EXTRA),
 "police-clearance-certificate-pcc-document-services": ("PCC / document", "Country the document is for", "e.g. Canada, UAE, Germany", PCC_EXTRA),
 "wildlife-safari-tours": ("Wildlife safari", "Where would you like to go?", "e.g. Tadoba, Ranthambore, Kenya – or suggest", SAFARI_EXTRA),
 "women-only-group-tours": ("Women-only tour", "Where would you like to go?", "e.g. Kerala, Bhutan, Vietnam – or suggest", WOMEN_EXTRA),
 "adventure-trekking-tours": ("Adventure / trek", "Where would you like to go?", "e.g. Kedarkantha, Ladakh, Rishikesh – or suggest", TREK_EXTRA),
 "jain-yatra-tours-with-maharaj": ("Jain yatra", "Which tirth(s)?", "e.g. Palitana, Sammed Shikharji, Girnar", JAIN_EXTRA),
}


def svc_form(slug, root="../"):
    if slug not in CFG:
        return ""
    name, dlabel, dph, extra = CFG[slug]
    return f"""<section class="alt" id="enquire"><div class="wrap" style="max-width:860px">
<div class="head"><span class="kicker">Quick enquiry</span><h2>Tell us about your {name if name.split()[0] in ('Jain','FIT','PCC') else name.lower()} plans</h2><p class="lead">Takes a minute – we reply with options on WhatsApp or email.</p></div>
<form class="sform" data-svc="{name}" novalidate>
<div class="sf-row"><label>{dlabel}*<input name="dest" required maxlength="120" placeholder="{dph}" autocomplete="off"></label>
<label>Month of travel<input name="month" type="month"></label></div>
<div class="sf-row"><label>Number of travellers*<input name="trav" type="number" min="1" max="500" value="2" required></label>
<label>Children (under 12)<input name="kids" type="number" min="0" max="100" value="0"></label></div>
{extra}
<div class="sf-row"><label>Your name<input name="name" maxlength="120" autocomplete="name"></label>
<label>Mobile or email*<input name="contact" required maxlength="160" placeholder="98xxxxxxxx, +971… or you@example.com" autocomplete="tel"></label></div>
<label>Anything else?<textarea name="notes" maxlength="600" rows="2" placeholder="Budget, hotel preference, special requests…"></textarea></label>
<div class="hp" aria-hidden="true"><label>Leave this empty<input name="company_website" tabindex="-1" autocomplete="off"></label></div>
<button class="btn gold" type="submit">Send enquiry on WhatsApp</button>
<p class="vmsg sf-msg" role="status" aria-live="polite"></p>
<p class="vpriv">🔒 We use your details only to reply to this enquiry – never shared or sold. <a href="{root}privacy-policy/">Privacy Policy</a></p>
</form></div></section>
<script>
(function(){{
const SB="{SB_URL}",KEY="{SB_KEY}";
const notify=(s,t,r)=>{{try{{const o={{_subject:s,message:t,_replyto:r||'',_template:'table',_captcha:'false',source:location.href}};const m=(s.match(/(\\S+) – /)||[])[1]||'';if(r&&/@/.test(r)&&/^[A-Z0-9-]{{6,}}$/.test(m)){{o.email=r;o._autoresponse='Thank you for contacting The Real Tours and Travels. We have received your request (reference '+m+') and our team will get back to you shortly. Please quote this reference in any message to us. For anything urgent, call or WhatsApp +91 98431 21212. – The Real Tours and Travels · www.therealtoursandtravels.com';}}fetch('https://formsubmit.co/ajax/enquiry@therealtoursandtravels.com',{{method:'POST',headers:{{'Content-Type':'application/json',Accept:'application/json'}},body:JSON.stringify(o)}}).catch(()=>{{}});}}catch(_){{}}}};
document.querySelectorAll('[data-yatra]').forEach(a=>a.addEventListener('click',()=>{{const f=document.querySelector('form.sform');if(!f)return;const cb=f.querySelector('input[name=x_notify]');if(cb)cb.checked=true;if(a.dataset.yatra)f.dest.value=a.dataset.yatra;}}));
document.querySelectorAll('form.sform').forEach(f=>{{
 const m=f.querySelector('.sf-msg');const now=new Date(Date.now()+330*60000).toISOString();f.month.min=now.slice(0,7);
 f.addEventListener('submit',async e=>{{
  e.preventDefault();m.className='vmsg sf-msg';
  if(f.company_website.value){{m.textContent='✅ Thank you – enquiry received.';m.classList.add('ok');return;}}
  const c=f.contact.value.trim(),isEmail=/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(c),dg=c.replace(/[^0-9]/g,''),isPhone=!isEmail&&(c.startsWith('+')?dg.length>=8&&dg.length<=15:dg.length>=10&&dg.length<=13);
  const dest=f.dest.value.trim(),trav=parseInt(f.trav.value)||0,kids=parseInt(f.kids.value)||0;
  let err='';if(dest.length<2)err='Please tell us where you would like to go.';else if(trav<1)err='Please enter the number of travellers.';else if(!isEmail&&!isPhone)err='Please enter a valid mobile number (outside India, start with your country code) or an email.';
  if(err){{m.textContent=err;m.classList.add('err');return;}}
  const ex=[];f.querySelectorAll('[data-lbl]').forEach(x=>{{const v=(x.value||'').trim();if(v)ex.push(x.dataset.lbl+': '+v);}});
  const food=[...f.querySelectorAll('input[name=x_food]:checked')].map(x=>x.value);if(food.length)ex.push('Food: '+food.join(', '));
  f.querySelectorAll('.sf-chk1 input:checked').forEach(x=>ex.push(x.value));
  const mon=f.month.value?new Date(f.month.value+'-01T00:00').toLocaleDateString('en-IN',{{month:'long',year:'numeric'}}):'';
  const svc=f.dataset.svc,name=f.name.value.trim(),notes=f.notes.value.trim();
  const id=crypto.randomUUID?crypto.randomUUID():'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,ch=>{{const r=Math.random()*16|0;return (ch=='x'?r:(r&3|8)).toString(16);}});
  const ref='SV-'+id.slice(0,6).toUpperCase();
  const row={{id,service:svc,destination:dest.slice(0,120),travel_month:mon||null,travellers:trav,full_name:name||null,phone:isPhone?dg.slice(0,20):null,email:isEmail?c:null,notes:[kids?'Children: '+kids:'',...ex,notes].filter(Boolean).join(' | ').slice(0,2000)||null}};
  const lines=['🧳 '+svc+' enquiry ('+ref+')',(svc==='Jain yatra'||svc==='Yatra'?'Yatra: ':'Where: ')+dest,mon?'When: '+mon:'','Travellers: '+trav+(kids?' (incl. '+kids+' children)':''),...ex,notes?'Notes: '+notes:'',name?'Name: '+name:'','Contact: '+c].filter(Boolean);
  const btn=f.querySelector('button[type=submit]');btn.disabled=true;m.textContent='Sending your enquiry…';
  let w=null;try{{w=window.open('','_blank');if(w)w.document.write('<p style="font:16px sans-serif;padding:20px">Opening WhatsApp…</p>');}}catch(_){{w=null;}}
  try{{const r=await fetch(SB+'/rest/v1/service_enquiries',{{method:'POST',headers:{{apikey:KEY,Authorization:'Bearer '+(window.RTT_TOKEN||KEY),'Content-Type':'application/json',Prefer:'return=minimal'}},body:JSON.stringify(row)}});if(!r.ok)throw 0;}}
  catch(_){{if(w)w.close();btn.disabled=false;m.textContent='Sorry, something went wrong. Please WhatsApp us on 98431 21212.';m.classList.add('err');return;}}
  const wa='https://wa.me/919843121212?text='+encodeURIComponent(lines.join('\\n'));
  notify('New '+svc+' enquiry '+ref+' – '+(name||c),lines.join('\\n'),isEmail?c:'');
  if(w){{try{{w.location.href=wa;}}catch(_){{}}}}
  m.innerHTML='✅ Enquiry received (Ref <b>'+ref+'</b>). Please press <b>Send</b> in WhatsApp so our team gets it instantly. If WhatsApp did not open: <a class="btn gold" style="margin-top:10px" href="'+wa+'" target="_blank" rel="noopener">💬 Send on WhatsApp</a>';
  m.classList.add('ok');btn.disabled=false;
 }});
}});
}})();
</script>"""


SVC_CSS = """
.sform{display:grid;gap:12px;background:#fff;border:1px solid var(--line);border-radius:18px;padding:22px;border-top:5px solid var(--red)}
.sform label{display:grid;gap:5px;font-size:13px;font-weight:600;color:var(--muted)}
.sform input:not([type=checkbox]),.sform select,.sform textarea{font:500 15.5px 'Jost',sans-serif;color:var(--ink);padding:11px 12px;border:1px solid var(--line);border-radius:12px;background:#fff;width:100%;min-width:0}
.sf-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}
.sf-chk{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;font-size:14.5px}.sf-chk>span{font-size:13px;font-weight:600;color:var(--muted)}
.sform .sf-chk label,.sform label.sf-chk1{display:flex;gap:6px;align-items:center;font-weight:500;color:var(--ink);font-size:14.5px}
.sform input[type=checkbox]{accent-color:var(--red)}.sform button{justify-self:start;border:0;cursor:pointer;font-family:inherit}.sform button[disabled]{opacity:.6}
.sf-msg:empty{display:none}
.yexp{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px}.yexp>div{background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px}.yexp h3{font-size:19px;margin:0 0 8px}.yexp ul{margin:0;padding-left:18px}.yexp li{margin:4px 0}
.yup{display:grid;gap:10px}.yup .yd{display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px;align-items:center;background:#fff;border:1px solid var(--line);border-left:4px solid var(--red);border-radius:14px;padding:14px 16px}
.ynone{background:#fff;border:1px dashed var(--line);border-radius:14px;padding:18px;text-align:center}
.iages{display:grid;gap:6px}.iages>span{font-size:14px;font-weight:600;color:var(--ink)}.iages small{font-weight:400;color:var(--muted)}.iagesel{display:flex;flex-wrap:wrap;gap:8px}.iagesel input{width:120px;font:500 15px 'Jost',sans-serif;padding:10px;border:1px solid var(--line);border-radius:12px}
.revstrip .grid{grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
"""
