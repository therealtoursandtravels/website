"""Visa section: country checklists, Request Price button, secure document upload (Supabase)."""
import json

SB_URL = "https://byvytpxqqgjschknqpms.supabase.co"
# Public (anon) key – safe to embed; database only allows insert, storage only allows upload.
SB_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ5dnl0cHhxcWdqc2Noa25xcG1zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTQ5MzM0NDMsImV4cCI6MjExMDUwOTQ0M30.AyJHMAk3jHQM7GahMLLxxWYT0-mr5SUnzrhAm0J2ZGA"

COMMON = ["Original passport valid for at least 6 months from the return date, with at least 2 blank pages",
          "Copies of old passports, if any"]
FIN = ["Bank statements for the last 6 months (signed and stamped by the bank)",
       "Income tax returns (ITR) for the last 2–3 years"]
JOB = ["Salaried: salary slips (last 3 months) and leave/NOC letter from employer",
       "Self-employed: business proof (GST certificate / Shop Act / company registration)",
       "Students: school or college ID and bonafide letter; retired: pension proof"]
TRIP = ["Confirmed return flight booking", "Hotel bookings for the whole stay", "Day-wise travel itinerary"]

COUNTRIES = [
 ("uae", "🇦🇪", "Dubai / UAE", "E-visa, usually processed online",
  ["Clear colour scan of passport front and back pages", "Recent passport-size photo with white background",
   "PAN card copy", "Return flight booking", "Hotel booking or address in the UAE"]),
 ("thailand", "🇹🇭", "Thailand", "Entry rules for Indians change often – we confirm the latest",
  COMMON[:1] + ["Recent passport-size photo with white background", "Return flight booking", "Hotel bookings",
   "Recent bank statement showing sufficient funds"]),
 ("singapore", "🇸🇬", "Singapore", "E-visa through an authorised agent",
  COMMON[:1] + ["Recent photo, 35 × 45 mm, white background, matte finish", "Visa application form (we fill it for you)",
   "Covering letter", "Return flight booking and hotel bookings", "Recent bank statements",
   "For business visits: invitation letter from the Singapore company"]),
 ("malaysia", "🇲🇾", "Malaysia", "eVisa / entry rules confirmed before booking",
  COMMON[:1] + ["Recent photo with white background", "Return flight booking", "Hotel bookings", "Recent bank statement"]),
 ("vietnam", "🇻🇳", "Vietnam", "E-visa, processed online",
  ["Clear colour scan of passport bio page", "Recent passport-size photo with white background",
   "Travel dates and entry/exit airport", "Hotel address in Vietnam"]),
 ("schengen", "🇪🇺", "Europe (Schengen)", "Appointment at the visa centre with biometrics",
  COMMON + ["2 recent photos, 35 × 45 mm, white background (80% face)", "Covering letter explaining the purpose of travel"] + FIN + JOB + TRIP +
  ["Travel insurance covering the whole Schengen stay, minimum €30,000 medical cover"]),
 ("uk", "🇬🇧", "United Kingdom", "Online application, then biometrics at the visa centre",
  COMMON + FIN + JOB + TRIP + ["For visiting family: invitation letter and host's ID / visa status"]),
 ("usa", "🇺🇸", "United States", "DS-160 form, then interview at the consulate",
  COMMON + ["Digital photo, 2 × 2 inch (51 × 51 mm), white background", "DS-160 confirmation page (we prepare it)",
   "Appointment and visa fee receipt"] + FIN + JOB + ["Proof of ties to India (property, family, job)", "Travel plan / itinerary"]),
 ("canada", "🇨🇦", "Canada", "Online application, then biometrics",
  COMMON + ["Digital photo as per Canada specifications"] + FIN + JOB + TRIP + ["For visiting family: invitation letter and host's status proof"]),
 ("australia", "🇦🇺", "Australia", "Online application",
  COMMON + ["Recent passport-size photo"] + FIN + JOB + TRIP),
 ("japan", "🇯🇵", "Japan", "Application through an authorised agency",
  COMMON + ["Recent photo, 45 × 35 mm, white background", "Visa application form (we fill it for you)"] + FIN + JOB + TRIP),
]


PASSPORT = [
 ("fresh", "🆕", "Fresh Passport (Adult)", "Online application, then appointment at the Passport Seva Kendra and police verification",
  ["Proof of present address – Aadhaar card, electricity / water / telephone bill, bank passbook with photo, or registered rent agreement",
   "Proof of date of birth – birth certificate, PAN card, Aadhaar card or school leaving certificate",
   "Educational certificate (10th marksheet or higher), if available – for non-ECR status",
   "Marriage certificate, if you want your spouse's name on the passport"]),
 ("renewal", "🔁", "Passport Renewal / Re-issue", "When your passport has expired, is about to expire or the pages are full",
  ["Original old passport",
   "Self-attested copies of the first two and last two pages of the old passport (including ECR / non-ECR page)",
   "Proof of present address, if it has changed since your last passport",
   "Name change documents (marriage certificate / gazette notification), if applicable"]),
 ("minor", "👶", "Passport for Minors (below 18)", "Both parents' consent is required",
  ["Birth certificate of the child",
   "Copies of both parents' passports (or address proof of parents if they do not have passports)",
   "Declaration / consent of both parents in the prescribed format (we prepare it)",
   "Proof of present address in the parents' name"]),
 ("tatkaal", "⚡", "Tatkaal (Urgent) Passport", "Faster processing on payment of the Tatkaal fee",
  ["All documents required for a fresh passport or re-issue",
   "Additional identity proofs as required under the Tatkaal scheme – we confirm the exact list for your case",
   "Proof of present address"]),
 ("lost", "🧾", "Lost / Damaged Passport", "Re-issue of a lost, stolen or damaged passport",
  ["Police report / FIR for a lost or stolen passport (original)",
   "Damaged passport (original), if applicable",
   "Copy of the old passport, if available",
   "Proof of present address and date of birth",
   "Affidavit / declaration explaining how the passport was lost or damaged (we prepare it)"]),
]

def passport_page(PHONE, PHONE_RAW, EMAIL, seal, cta_band):
    return visa_page(PHONE, PHONE_RAW, EMAIL, seal, cta_band, mode="passport")

def visa_page(PHONE, PHONE_RAW, EMAIL, seal, cta_band, mode="visa"):
    P = mode == "passport"
    ITEMS = PASSPORT if P else COUNTRIES
    tabs = "".join(f'<button type="button" class="vtab{" on" if i==0 else ""}" data-c="{c}">{f} {n}</button>' for i,(c,f,n,_,_) in enumerate(ITEMS))
    panels = ""
    for i,(c,f,n,how,docs) in enumerate(ITEMS):
        lis = "".join(f"<li>{d}</li>" for d in docs)
        wa = "https://wa.me/919843121212?text=" + ("Hi%20The%20Real%20Tours%20and%20Travels%2C%20please%20share%20the%20price%20for%20" + n.replace(" ","%20").replace("/","%2F").replace("(","").replace(")","") + ("." if P else "%20visa.%20Travellers%3A%20%20Travel%20date%3A%20"))
        panels += f"""<div class="vpanel" data-c="{c}"{'' if i==0 else ' hidden'}>
<div class="vhead"><div><h3>{f} {n}</h3><p class="meta">{how}</p></div>
<div class="vprice"><span>Price</span><a class="btn gold" href="{wa}" target="_blank" rel="noopener">Request Price</a></div></div>
<p class="meta" style="margin:8px 0 0">Price = government / embassy fee (no GST) + our service fee + 18% GST on the service fee.</p><h4>Documents required</h4><ul class="ticks">{lis}</ul>
<p class="meta">{"Requirements are set by Passport Seva (Ministry of External Affairs) and can change. We confirm the final checklist for your case before you apply." if P else "Requirements can change and may differ for business, student or family visits. We confirm the final checklist for your case before you apply."}</p>
<p><a class="btn outline" href="#upload" data-pick="{c}">Upload documents for {n}</a></p></div>"""
    opts = "".join(f'<option value="{n}">{n}</option>' for (_,_,n,_,_) in ITEMS) + ('' if P else '<option value="Other">Other country</option>')
    T = dict(
      crumb="Passport Services" if P else "Visa Services",
      kicker="🛂 Passport services" if P else "🛂 Visa services",
      h1="Passport Services in Mulund, Mumbai" if P else "Visa Services in Mulund, Mumbai",
      intro=("New passport, renewal, minor, Tatkaal or lost passport – check the documents required, request the price, and upload your documents securely. We fill the forms and book your Passport Seva Kendra appointment." if P else
             "Check the documents required for your visa, request the price, and upload your documents securely – our visa team will review them and call you back."),
      k2="Choose your service" if P else "Choose your destination",
      h2="Documents required by service" if P else "Documents required by country",
      lead2=("Select a service to see the checklist. Tap <b>Request Price</b> to get the government fee and our service charge on WhatsApp." if P else
             "Select a country to see the checklist. Tap <b>Request Price</b> to get the current visa fee and our service charge on WhatsApp."),
      h3="Upload your passport documents" if P else "Upload your visa documents",
      team="passport team" if P else "visa team",
      sel_label="Service*" if P else "Country*",
      type_row=('<input type="hidden" name="visa_type" value="Passport">' if P else
                '<label>Visa type<select name="visa_type"><option>Tourist</option><option>Business</option><option>Visiting family / friends</option><option>Student</option><option>Transit</option></select></label>'),
      date_label="Needed by (travel date, if any)" if P else "Travel date",
      trav_label="Number of applicants" if P else "Number of travellers",
      files_hint="(select multiple files – address proof, birth proof, old passport…)" if P else "(select multiple files – passport, photo, bank statements, ITR, bookings…)",
      notes_ph="e.g. change of name or address, urgent travel" if P else "Anything we should know – e.g. previous visa refusals, travelling with children",
      consent="to process my passport application" if P else "to process my visa application",
      payfor="passport service fees" if P else "visa fees",
    )
    return f"""
<section class="hero"><div class="wrap"><div><div class="crumbs"><a href="../">Home</a> › {T["crumb"]}</div>
<span class="kicker">{T["kicker"]}</span>
<h1>{T["h1"]}</h1>
<p>{T["intro"]}</p>
<div class="btns"><a class="btn gold" href="#countries">See documents required</a><a class="btn ghost" href="#upload">Upload documents</a><a class="btn outline" href="#pay">💳 Pay online</a></div>
</div>{seal("../")}</div></section>

<section id="countries"><div class="wrap">
<div class="head"><span class="kicker">{T["k2"]}</span><h2>{T["h2"]}</h2><p class="lead">{T["lead2"]}</p></div>
<div class="vtabs" role="tablist">{tabs}</div>
<div class="vbox">{panels}</div>
</div></section>

<section class="alt" id="upload"><div class="wrap" style="max-width:820px">
<div class="head"><span class="kicker">Secure upload</span><h2>{T["h3"]}</h2><p class="lead">Upload clear scans or photos (PDF, JPG or PNG, up to 10 MB each). Your documents are stored privately and seen only by our {T["team"]}.</p></div>
<form id="vform" class="vform" novalidate>
<div class="row"><label>Full name*<input name="full_name" required maxlength="120" autocomplete="name"></label>
<label>Mobile number*<input name="phone" required inputmode="tel" maxlength="20" autocomplete="tel" placeholder="10-digit mobile"></label></div>
<div class="row"><label>Email<input name="email" type="email" maxlength="160" autocomplete="email"></label>
<label>{T["sel_label"]}<select name="country" required>{opts}</select></label></div>
<div class="row">{T["type_row"]}
<label>{T["date_label"]}<input name="travel_date" type="date"></label></div>
<div class="row"><label>{T["trav_label"]}<input name="travellers" type="number" min="1" max="50" value="1"></label><span></span></div>
<label>Documents* <small>{T["files_hint"]}</small>
<input name="files" type="file" multiple required accept=".pdf,.jpg,.jpeg,.png,.heic,.heif,.webp,application/pdf,image/*"></label>
<div id="flist" class="flist"></div>
<label>Notes for our team<textarea name="notes" maxlength="2000" rows="3" placeholder="{T["notes_ph"]}"></textarea></label>
<label class="chk"><input type="checkbox" name="consent" required><span>I agree that The Real Tours and Travels may use these documents only {T["consent"]}, as per the <a href="../privacy-policy/">Privacy Policy</a>.</span></label>
<button class="btn gold" type="submit" id="vsubmit">Upload documents securely</button>
<p id="vmsg" class="vmsg" role="status" aria-live="polite"></p>
</form>
<div class="paybox" id="pay"><span class="kicker" style="justify-content:center">Secure payment</span><h3 style="font-size:26px;margin:4px 0 8px">Pay {T["payfor"]} online</h3>
<p class="lead" style="font-size:16px">Enter the fees confirmed by our team to see the GST and total, then pay securely. Add your name, phone and reference in the payment window so we can match your payment. UPI, cards, net banking and wallets accepted.</p>
<div class="gcalc" id="gcalc">
<div class="grow"><label>Government / embassy / VFS fee <small>(as confirmed by us – no GST)</small><span class="gin">₹<input type="number" min="0" step="1" inputmode="decimal" id="g_gov" placeholder="0"></span></label>
<label>Our service fee <small>(as confirmed by us)</small><span class="gin">₹<input type="number" min="0" step="1" inputmode="decimal" id="g_fee" placeholder="0"></span></label></div>
<label class="gst8">Your state <select id="g_state"><option value="in">Maharashtra</option><option value="out">Other state / UT</option></select></label>
<table class="gtab"><tr><td>Government / embassy fee (pure agent, no GST)</td><td id="o_gov">₹0.00</td></tr>
<tr><td>Service fee (SAC 9985)</td><td id="o_fee">₹0.00</td></tr>
<tr id="r_c"><td>CGST @ 9%</td><td id="o_c">₹0.00</td></tr><tr id="r_s"><td>SGST @ 9%</td><td id="o_s">₹0.00</td></tr><tr id="r_i" hidden><td>IGST @ 18%</td><td id="o_i">₹0.00</td></tr>
<tr class="gtot"><td>Total to pay</td><td id="o_t">₹0.00</td></tr></table>
<p class="gnote">Enter the <b>total</b> shown above as the Booking Amount in the payment window. A GST tax invoice (GSTIN 27AMUPK4723E1ZU) will be issued for the service fee.</p></div>
<form><script src="https://checkout.razorpay.com/v1/payment-button.js" data-payment_button_id="pl_U3RKkNsxkSYwez" async></script></form>
<p style="font-size:13px;color:var(--muted);margin:6px 0 0">🔒 Secured by Razorpay · By paying you agree to our <a href="../terms/">Terms</a> and <a href="../cancellation-refund-policy/">Cancellation &amp; Refund Policy</a>.</p></div>
<p class="meta" style="text-align:center;margin-top:16px">Prefer WhatsApp or visiting us? Call/WhatsApp <a href="tel:{PHONE_RAW}">{PHONE}</a> or visit our Mulund West office, open daily 9 am – 10 pm.</p>
</div></section>
{cta_band()}
<script>
(function(){{
const SB="{SB_URL}",KEY="{SB_KEY}";
const notify=(s,t,r)=>{{try{{fetch('https://formsubmit.co/ajax/enquiry@therealtoursandtravels.com',{{method:'POST',headers:{{'Content-Type':'application/json',Accept:'application/json'}},body:JSON.stringify({{_subject:s,message:t,_replyto:r||'',_template:'table',_captcha:'false',source:location.href}})}}).catch(()=>{{}});}}catch(_){{}}}};
(function(){{const $=i=>document.getElementById(i),inr=n=>'₹'+n.toLocaleString('en-IN',{{minimumFractionDigits:2,maximumFractionDigits:2}}),r2=n=>Math.round(n*100)/100;
function calc(){{const g=Math.max(0,+$('g_gov').value||0),f=Math.max(0,+$('g_fee').value||0),inS=$('g_state').value==='in';const c=r2(f*.09),i=r2(f*.18);
$('o_gov').textContent=inr(g);$('o_fee').textContent=inr(f);$('o_c').textContent=$('o_s').textContent=inr(c);$('o_i').textContent=inr(i);
$('r_c').hidden=$('r_s').hidden=!inS;$('r_i').hidden=inS;$('o_t').textContent=inr(r2(g+f+(inS?2*c:i)));}}
['g_gov','g_fee','g_state'].forEach(x=>$(x)&&$(x).addEventListener('input',calc));if($('g_gov'))calc();}})();
const tabs=document.querySelectorAll('.vtab'),panels=document.querySelectorAll('.vpanel');
function show(c){{tabs.forEach(t=>t.classList.toggle('on',t.dataset.c===c));panels.forEach(p=>p.hidden=p.dataset.c!==c);}}
tabs.forEach(t=>t.addEventListener('click',()=>show(t.dataset.c)));
const names={json.dumps({c:n for (c,_,n,_,_) in ITEMS})};
document.querySelectorAll('[data-pick]').forEach(a=>a.addEventListener('click',()=>{{const s=document.querySelector('select[name=country]');s.value=names[a.dataset.pick];}}));
const f=document.getElementById('vform'),msg=document.getElementById('vmsg'),btn=document.getElementById('vsubmit'),fl=document.getElementById('flist');
f.files.addEventListener('change',()=>{{fl.innerHTML=[...f.files.files].map(x=>'<span>📄 '+x.name.replace(/[<>&]/g,'')+' · '+(x.size/1048576).toFixed(1)+' MB</span>').join('');}});
function uuid(){{return (crypto.randomUUID?crypto.randomUUID():'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,c=>{{const r=Math.random()*16|0;return (c=='x'?r:(r&3|8)).toString(16);}}));}}
function safe(n){{return n.normalize('NFKD').replace(/[^A-Za-z0-9._-]+/g,'_').slice(-80)||'file';}}
f.addEventListener('submit',async e=>{{
 e.preventDefault();msg.className='vmsg';
 const d=new FormData(f),files=[...f.files.files];
 const phone=(d.get('phone')||'').replace(/[^0-9+]/g,'');
 if(!d.get('full_name').trim()||phone.length<10){{msg.textContent='Please enter your name and a valid mobile number.';msg.classList.add('err');return;}}
 if(!files.length){{msg.textContent='Please choose at least one document to upload.';msg.classList.add('err');return;}}
 if(files.length>25){{msg.textContent='Please upload up to 25 files at a time.';msg.classList.add('err');return;}}
 const big=files.find(x=>x.size>10485760);if(big){{msg.textContent=big.name+' is larger than 10 MB. Please upload a smaller scan.';msg.classList.add('err');return;}}
 if(!d.get('consent')){{msg.textContent='Please tick the consent box.';msg.classList.add('err');return;}}
 btn.disabled=true;const id=uuid(),paths=[];
 try{{
  for(let i=0;i<files.length;i++){{
   msg.textContent='Uploading '+(i+1)+' of '+files.length+'…';
   const p='applications/'+id+'/'+String(i+1).padStart(2,'0')+'-'+safe(files[i].name);
   const r=await fetch(SB+'/storage/v1/object/visa-documents/'+p,{{method:'POST',headers:{{apikey:KEY,Authorization:'Bearer '+KEY,'Content-Type':files[i].type||'application/octet-stream','x-upsert':'false'}},body:files[i]}});
   if(!r.ok)throw new Error('upload '+r.status);
   paths.push(p);
  }}
  const row={{id,full_name:d.get('full_name').trim(),phone,email:(d.get('email')||'').trim()||null,country:d.get('country'),visa_type:d.get('visa_type'),travel_date:d.get('travel_date')||null,travellers:parseInt(d.get('travellers'))||null,notes:(d.get('notes')||'').trim()||null,files:paths}};
  const r2=await fetch(SB+'/rest/v1/visa_applications',{{method:'POST',headers:{{apikey:KEY,Authorization:'Bearer '+KEY,'Content-Type':'application/json',Prefer:'return=minimal'}},body:JSON.stringify(row)}});
  if(!r2.ok)throw new Error('save '+r2.status);
  notify('New {"passport" if P else "visa"} documents '+id.slice(0,8).toUpperCase()+' – '+row.full_name,'Name: '+row.full_name+'\\nPhone: '+row.phone+(row.email?'\\nEmail: '+row.email:'')+'\\n{"Service" if P else "Country"}: '+row.country+'\\nType: '+row.visa_type+(row.travel_date?'\\nTravel date: '+row.travel_date:'')+'\\nApplicants: '+(row.travellers||1)+'\\nFiles uploaded: '+paths.length+' (see Supabase → Storage → visa-documents → applications/'+id+')'+(row.notes?'\\nNotes: '+row.notes:''),row.email||'');
  f.reset();fl.innerHTML='';
  msg.innerHTML='✅ Thank you! Your documents were uploaded securely (reference: <b>'+id.slice(0,8).toUpperCase()+'</b>). Our team will call you shortly. For faster service, <a href="https://wa.me/919843121212?text='+encodeURIComponent('Hi, I uploaded my documents on your website. Reference: '+id.slice(0,8).toUpperCase())+'" target="_blank" rel="noopener">WhatsApp us your reference</a>.';
  msg.classList.add('ok');
 }}catch(err){{msg.textContent='Sorry, the upload did not complete. Please try again, or WhatsApp your documents to 98431 21212.';msg.classList.add('err');}}
 btn.disabled=false;
}});
}})();
</script>"""

VISA_CSS = """
.gcalc{text-align:left;margin:16px 0 6px;display:grid;gap:12px}.grow{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.gcalc label{display:grid;gap:6px;font-weight:500;font-size:14.5px;color:var(--wine)}.gcalc small{font-weight:400;color:var(--muted);font-size:12.5px}
.gin{display:flex;align-items:center;gap:6px;border:1px solid var(--line);border-radius:12px;padding:0 12px;background:#fff}.gin input{border:0;outline:0;font:500 17px 'Jost',sans-serif;padding:11px 0;width:100%;background:none}
.gin:focus-within{border-color:var(--red);box-shadow:0 0 0 2px rgba(215,25,31,.15)}.gst8 select{font:400 15px 'Jost',sans-serif;padding:10px 12px;border:1px solid var(--line);border-radius:12px;max-width:260px}
.gtab{width:100%;border-collapse:collapse;font-size:15px}.gtab td{padding:8px 4px;border-bottom:1px solid var(--line)}.gtab td:last-child{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.gtot td{font-weight:700;font-size:17px;color:var(--crimson);border-bottom:0;border-top:2px solid var(--wine)}.gnote{font-size:13px;color:var(--muted);margin:0}
@media(max-width:600px){.grow{grid-template-columns:1fr}}
#upload .paybox{margin:28px auto 0}
.vtabs{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-bottom:26px}
.vtab{border:1px solid var(--line);background:#fff;border-radius:999px;padding:10px 16px;font:500 15px 'Jost',sans-serif;color:var(--ink);cursor:pointer}
.vtab.on,.vtab:hover{border-color:var(--red);color:var(--red);background:#fdf0f0}
.vbox{background:#fff;border:1px solid var(--line);border-radius:20px;padding:30px;box-shadow:0 16px 36px rgba(0,0,0,.05)}
.vhead{display:flex;justify-content:space-between;align-items:flex-start;gap:20px;flex-wrap:wrap;border-bottom:1px solid var(--line);padding-bottom:16px;margin-bottom:10px}
.vhead h3{margin:0;font-size:26px;color:var(--wine)}.vhead .meta{margin:4px 0 0}
.vprice{display:flex;align-items:center;gap:14px;background:var(--bg);border:1px solid var(--line);border-radius:16px;padding:10px 12px 10px 18px}
.vprice span{font-weight:600;color:var(--muted);letter-spacing:1px;text-transform:uppercase;font-size:13px}
.vbox h4{font-family:'Playfair Display',serif;font-size:20px;color:var(--crimson);margin:18px 0 6px}
.vform{background:#fff;border:1px solid var(--line);border-radius:20px;padding:30px;display:grid;gap:16px}
.vform .row{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.vform label{display:grid;gap:6px;font-weight:500;font-size:15px;color:var(--wine)}
.vform small{font-weight:400;color:var(--muted)}
.vform input,.vform select,.vform textarea{font:400 16px 'Jost',sans-serif;padding:12px 14px;border:1px solid var(--line);border-radius:12px;background:#fff;color:var(--ink);width:100%}
.vform input:focus,.vform select:focus,.vform textarea:focus{outline:2px solid var(--red);border-color:var(--red)}
.vform .chk{display:flex;gap:10px;align-items:flex-start;font-weight:400;color:var(--muted);font-size:14px}.vform .chk input{width:auto;margin-top:3px}
.flist{display:flex;flex-wrap:wrap;gap:8px}.flist span{background:var(--bg);border:1px solid var(--line);border-radius:999px;padding:4px 12px;font-size:13px}
.vmsg{margin:0;font-size:15px}.vmsg.ok{color:#17703a;background:#eef9f1;border:1px solid #cdebd6;padding:12px 14px;border-radius:12px}.vmsg.err{color:var(--crimson)}
.vform button{border:0;justify-self:start;cursor:pointer;font-family:inherit}
.vform button[disabled]{opacity:.6;cursor:wait}
@media(max-width:700px){.vform .row{grid-template-columns:1fr}.vbox,.vform{padding:20px}.vhead h3{font-size:22px}.vprice{width:100%;justify-content:space-between}.vtab{font-size:14px;padding:8px 13px}}
"""
