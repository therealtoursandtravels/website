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

GST_STATES = [("01","Jammu and Kashmir"),("02","Himachal Pradesh"),("03","Punjab"),("04","Chandigarh"),("05","Uttarakhand"),("06","Haryana"),
 ("07","Delhi"),("08","Rajasthan"),("09","Uttar Pradesh"),("10","Bihar"),("11","Sikkim"),("12","Arunachal Pradesh"),("13","Nagaland"),("14","Manipur"),
 ("15","Mizoram"),("16","Tripura"),("17","Meghalaya"),("18","Assam"),("19","West Bengal"),("20","Jharkhand"),("21","Odisha"),("22","Chhattisgarh"),
 ("23","Madhya Pradesh"),("24","Gujarat"),("26","Dadra and Nagar Haveli and Daman and Diu"),("27","Maharashtra"),("29","Karnataka"),("30","Goa"),
 ("31","Lakshadweep"),("32","Kerala"),("33","Tamil Nadu"),("34","Puducherry"),("35","Andaman and Nicobar Islands"),("36","Telangana"),
 ("37","Andhra Pradesh"),("38","Ladakh")]
GST_STATE_OPTS = ('<option value="27">Maharashtra</option>' + "".join(f'<option value="{c}">{n}</option>' for c, n in sorted(GST_STATES, key=lambda x: x[1]) if c != "27")
                  + '<option value="OUT">Outside India (NRI / foreign client)</option>')

VISA_CENTRE_CODES = {"schengen", "uk", "usa", "canada", "australia"}  # visa needs a visit to a visa centre / consulate

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
 ('fresh', '🆕', 'Fresh Passport (Adult)', 'Online application, then appointment at the Passport Seva Kendra and police verification. Carry originals plus one set of self-attested copies', ["Proof of present address (any one): Aadhaar / e-Aadhaar, Voter ID, electricity / water / telephone / gas bill, bank passbook or account statement with photo, income tax assessment order, registered rent agreement, or your spouse's passport (if your address is the same)", 'Proof of date of birth (any one): birth certificate from the Registrar of Births and Deaths / Municipal Corporation, school leaving / transfer / matriculation certificate, PAN card, driving licence, Voter ID, LIC or public-company policy bond, or service record / pay pension order (government employees and pensioners)', 'Aadhaar is accepted as address proof, but not as proof of date of birth under the 2025 passport rules', '10th marksheet or higher qualification certificate, if you have one – for non-ECR status', 'Name change documents (gazette notification or marriage certificate), if your name differs across documents', 'Government / PSU employees: Identity Certificate (Annexure A) or No Objection Certificate (Annexure B) from your office', 'Appointment confirmation (we book it and fill the application for you)', "Your name, date of birth and parents' names should match on every document – we check this before your appointment"]),
 ('renewal', '🔁', 'Passport Renewal / Re-issue', 'When your passport has expired, is about to expire or the pages are full', ['Original old passport', 'Self-attested copies of the first two and last two pages of the old passport (including ECR / non-ECR page)', 'Proof of present address, if it has changed since your last passport', 'Name change documents (marriage certificate / gazette notification), if applicable']),
 ('minor', '👶', 'Passport for Minors (below 18) – both parents', 'Both parents give consent by signing the declaration (Annexure D). Ideally both parents come to the appointment with the child', ['Birth certificate of the child – for children born on or after 1 October 2023 this is the only accepted proof of date of birth', 'Children born before 1 October 2023 may instead use another accepted proof, such as a school leaving certificate', 'Proof of present address in the name of either parent', "Self-attested copies of both parents' passports (first two and last two pages), if they hold passports", 'Annexure D – declaration signed by both parents (we prepare it)', "If the child's name is to be printed with a surname different from the parents', supporting documents – we advise"]),
 ('minorsingle', '👩\u200d👦', 'Minor – Single Parent / One Parent Unavailable', "A child's passport can still be issued when only one parent can apply – the documents depend on the situation. We prepare the right declaration for your case", ['Birth certificate of the child – for children born on or after 1 October 2023 this is the only accepted proof of date of birth', 'Proof of present address and passport copy (if any) of the parent who is applying', 'One parent has passed away: Annexure D signed by the surviving parent, plus the death certificate of the other parent', "Divorced or separated: Annexure C – declaration by the applying parent, plus a copy of the divorce decree or custody order, if one exists. If custody is being disputed in court, the court's permission may be needed", "Unmarried / single parent, or the other parent's whereabouts are unknown: Annexure C – declaration by the applying parent. Only one parent's name needs to be printed on the passport", 'Other parent gives consent but cannot come: declaration signed by both parents (Annexure D)', 'Legal guardian applying: guardianship order from the court plus Annexure D', 'Annexure formats are updated from time to time – we always use the current format from Passport Seva and confirm the exact documents for your case']),
 ('tatkaal', '⚡', 'Tatkaal (Urgent) Passport', 'Faster processing on payment of the Tatkaal fee', ['All documents required for a fresh passport or re-issue', 'Additional identity proofs as required under the Tatkaal scheme – we confirm the exact list for your case', 'Proof of present address']),
 ('lost', '🧾', 'Lost / Damaged Passport', 'Re-issue of a lost, stolen or damaged passport', ['Police report / FIR for a lost or stolen passport (original)', 'Damaged passport (original), if applicable', 'Copy of the old passport, if available', 'Proof of present address and date of birth', 'Affidavit / declaration explaining how the passport was lost or damaged (we prepare it)']),
]

# ---- Visa & entry requirements for Indian passport holders (researched Nov 2026; reviewed weekly) ----
from entry import UPDATES, NEW_COUNTRIES, ENTRY, GROUPS, SCHENGEN_EXTRA
COUNTRIES = [(c, f, n, UPDATES[c][0] if c in UPDATES else how,
              (UPDATES[c][1] if c in UPDATES and UPDATES[c][1] is not None else docs) + ([SCHENGEN_EXTRA] if c == "schengen" else []))
             for (c, f, n, how, docs) in COUNTRIES] + NEW_COUNTRIES

def passport_page(PHONE, PHONE_RAW, EMAIL, seal, cta_band):
    return visa_page(PHONE, PHONE_RAW, EMAIL, seal, cta_band, mode="passport")

def wa_free(n, card):
    import urllib.parse as U
    return "https://wa.me/919843121212?text=" + U.quote(f"Hi The Real Tours and Travels, I am travelling to {n}. Please help me with the entry requirements" + (f" and the {card}" if card else "") + ".\nTravellers: \nTravel date: ")

def visa_page(PHONE, PHONE_RAW, EMAIL, seal, cta_band, mode="visa"):
    P = mode == "passport"
    ITEMS = PASSPORT if P else COUNTRIES
    if P:
        tabs = "".join(f'<button type="button" class="vtab{" on" if i==0 else ""}" data-c="{c}">{f} {n}</button>' for i,(c,f,n,_,_) in enumerate(ITEMS))
    else:
        # group the destinations by what Indian travellers need: nothing in advance / online / a visa
        ITEMS = [it for g, _ in GROUPS for it in ITEMS if ENTRY.get(it[0], ("visa",))[0] == g]
        tabs = ""
        for g, gl in GROUPS:
            row = "".join(f'<button type="button" class="vtab" data-c="{c}">{f} {n}</button>' for (c, f, n, _, _) in ITEMS if ENTRY.get(c, ("visa",))[0] == g)
            tabs += f'<div class="vgrp vg-{g}"><span class="vgl">{gl}</span><div class="vgrow">{row}</div></div>'
        tabs = tabs.replace('class="vtab"', 'class="vtab on"', 1)
    panels = ""
    for i,(c,f,n,how,docs) in enumerate(ITEMS):
        lis = "".join(f"<li>{d}</li>" for d in docs)
        g, badge, card = ENTRY.get(c, ("visa", "Visa required", None)) if not P else ("visa", "", None)
        badges = "" if P else f'<div class="vbadges"><span class="vb vb-{g}">{badge}</span>' + (f'<span class="vb vb-card">📲 {card} needed</span>' if card else "") + '</div>'
        free = (not P) and g == "free"
        wa = "https://wa.me/919843121212?text=" + ("Hi%20The%20Real%20Tours%20and%20Travels%2C%20please%20share%20the%20price%20for%20" + n.replace(" ","%20").replace("/","%2F").replace("(","").replace(")","") + ("." if P else "%20visa.%20Travellers%3A%20%20Travel%20date%3A%20"))
        panels += f"""<div class="vpanel" data-c="{c}"{'' if i==0 else ' hidden'}>
<div class="vhead"><div><h3>{f} {n}</h3>{badges}<p class="meta">{how}</p></div>
<div class="vprice"><span>{"Need help?" if free else "Price"}</span><a class="btn gold" href="{wa_free(n, card) if free else wa}" target="_blank" rel="noopener">{"Ask us on WhatsApp" if free else "Request Price"}</a></div></div>
{"" if free else '<p class="meta" style="margin:8px 0 0">Price = government / embassy fee (no GST) + our service fee + 18% GST on the service fee.</p>'}<h4>{"What to carry" if free else "Documents required"}</h4><ul class="ticks">{lis}</ul>
<p class="meta">{"Requirements are set by Passport Seva (Ministry of External Affairs) and can change. We confirm the final checklist for your case before you apply." if P else "Rules for Indian passport holders – last checked November 2026 and reviewed every week. Requirements can change and may differ for business, student or family visits; we confirm the final checklist for your case before you travel."}</p>
{"" if free else f'<p><a class="btn outline" href="#upload" data-pick="{c}">Upload documents for {n}</a></p>'}</div>"""
    opts = "".join(f'<option value="{n}">{n}</option>' for (_,_,n,_,_) in ITEMS) + ('' if P else '<option value="Other">Other country – type below</option>')
    other_list = ""
    if not P:
        # Any destination not listed: customer types it, then requests the checklist/price or uploads documents.
        tabs += '<button type="button" class="vtab" data-c="other">🌐 Other country</button>'
        panels += f"""<div class="vpanel" data-c="other" hidden>
<div class="vhead"><div><h3>🌐 Other country</h3><p class="meta">Travelling somewhere not listed above? Type the country – our visa team will send you the exact documents, fee and processing time for it.</p></div></div>
<div class="vother"><label>Which country are you visiting?<input id="vo_country" maxlength="60" autocomplete="off" placeholder="e.g. Kenya, Bhutan, Brazil, South Korea"></label>
<a class="btn gold" id="vo_wa" href="https://wa.me/919843121212" target="_blank" rel="noopener">Request checklist &amp; price</a></div>
<p id="vo_msg" class="vmsg" role="status" aria-live="polite"></p>
<p class="meta" style="margin:8px 0 0">Price = government / embassy fee (no GST) + our service fee + 18% GST on the service fee. Requirements differ by country and visa type – we confirm the final checklist for your case before you apply.</p>
<p><a class="btn outline" href="#upload" id="vo_up">Upload documents for this country</a></p></div>"""
    T = dict(
      crumb="Passport Services" if P else "Visa Services",
      kicker="🛂 Passport services" if P else "🛂 Visa services",
      h1="Passport Services in Mulund, Mumbai" if P else "Visa Services in Mulund, Mumbai",
      intro=("New passport, renewal, minor, Tatkaal or lost passport – check the documents required, request the price, and upload your documents securely. We fill the forms and book your Passport Seva Kendra appointment." if P else
             "Check the documents required for your visa, request the price, and upload your documents securely – our visa team will review them and call you back."),
      k2="Choose your service" if P else "Visa & entry requirements",
      h2="Documents required by service" if P else "Visa & Entry Requirements for Indian Travellers",
      lead2=("Select a service to see the checklist. Tap <b>Request Price</b> to get the government fee and our service charge on WhatsApp." if P else
             "Many countries no longer need a visa – but most now ask for an online authorisation or a digital arrival card before you land. Pick a country to see exactly what Indian passport holders need and what to carry. We handle visas, e-visas and arrival cards for you."),
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
    if P:
        form_html = f"""<form id="vform" class="vform" novalidate>
<div class="row"><label>Full name*<input name="full_name" required maxlength="120" autocomplete="name"></label>
<label>Mobile number*<input name="phone" required inputmode="tel" maxlength="20" autocomplete="tel" placeholder="10-digit mobile, or +country code"></label></div>
<div class="row"><label>Email<input name="email" type="email" maxlength="160" autocomplete="email"></label>
<label>{T["sel_label"]}<select name="country" required>{opts}</select></label></div>
{'' if P else '<label id="ocwrap" hidden>Which country?*<input name="other_country" maxlength="60" autocomplete="off" placeholder="e.g. Kenya, Bhutan, South Korea"></label>'}
{other_list}
<div class="row">{T["type_row"]}
<label>{T["date_label"]}<input name="travel_date" type="date"></label></div>
<div class="row"><label>{T["trav_label"]}<input name="travellers" type="number" min="1" max="50" value="1"></label><span></span></div>
<label>Documents* <small>{T["files_hint"]}</small>
<input name="files" type="file" multiple required accept=".pdf,.jpg,.jpeg,.png,.heic,.heif,.webp,application/pdf,image/*"></label>
<div id="flist" class="flist"></div>
<label>Notes for our team<textarea name="notes" maxlength="2000" rows="3" placeholder="{T["notes_ph"]}"></textarea></label>
<label class="chk"><input type="checkbox" name="consent" required><span>I agree that The Real Tours and Travels may use these documents only {T["consent"]}, as per the <a href="../privacy-policy/">Privacy Policy</a>.</span></label>
<div class="hp" aria-hidden="true"><label>Leave this empty<input name="company_website" tabindex="-1" autocomplete="off"></label></div>
<button class="btn gold" type="submit" id="vsubmit">Upload documents securely</button>
<p id="vmsg" class="vmsg" role="status" aria-live="polite"></p>
</form>"""
        form_js = f"""const f=document.getElementById('vform'),msg=document.getElementById('vmsg'),btn=document.getElementById('vsubmit'),fl=document.getElementById('flist');
f.files.addEventListener('change',()=>{{fl.innerHTML=[...f.files.files].map(x=>'<span>📄 '+x.name.replace(/[<>&]/g,'')+' · '+(x.size/1048576).toFixed(1)+' MB</span>').join('');}});
function uuid(){{return (crypto.randomUUID?crypto.randomUUID():'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,c=>{{const r=Math.random()*16|0;return (c=='x'?r:(r&3|8)).toString(16);}}));}}
function safe(n){{return n.normalize('NFKD').replace(/[^A-Za-z0-9._-]+/g,'_').slice(-80)||'file';}}
f.addEventListener('submit',async e=>{{
 e.preventDefault();msg.className='vmsg';
 if(f.company_website.value){{msg.textContent='✅ Thank you – documents received.';msg.classList.add('ok');return;}} // spam trap
 const d=new FormData(f),files=[...f.files.files];
 const phone=(d.get('phone')||'').replace(/[^0-9+]/g,'');
 if(!d.get('full_name').trim()||phone.length<10){{msg.textContent='Please enter your name and a valid mobile number.';msg.classList.add('err');return;}}
 if(!files.length){{msg.textContent='Please choose at least one document to upload.';msg.classList.add('err');return;}}
 if(files.length>25){{msg.textContent='Please upload up to 25 files at a time.';msg.classList.add('err');return;}}
 const big=files.find(x=>x.size>10485760);if(big){{msg.textContent=big.name+' is larger than 10 MB. Please upload a smaller scan.';msg.classList.add('err');return;}}
 let country=d.get('country');
 if(country==='Other'){{country=(d.get('other_country')||'').trim();if(country.length<2){{msg.textContent='Please type the country you are visiting.';msg.classList.add('err');f.other_country.focus();return;}}}}
 if(!d.get('consent')){{msg.textContent='Please tick the consent box.';msg.classList.add('err');return;}}
 btn.disabled=true;const id=uuid(),paths=[];
 try{{
  for(let i=0;i<files.length;i++){{
   msg.textContent='Uploading '+(i+1)+' of '+files.length+'…';
   const p='applications/'+id+'/'+String(i+1).padStart(2,'0')+'-'+safe(files[i].name);
   const r=await fetch(SB+'/storage/v1/object/visa-documents/'+p,{{method:'POST',headers:{{apikey:KEY,Authorization:'Bearer '+(window.RTT_TOKEN||KEY),'Content-Type':files[i].type||'application/octet-stream','x-upsert':'false'}},body:files[i]}});
   if(!r.ok)throw new Error('upload '+r.status);
   paths.push(p);
  }}
  const row={{id,full_name:d.get('full_name').trim(),phone,email:(d.get('email')||'').trim()||null,country:country.slice(0,80),visa_type:d.get('visa_type'),travel_date:d.get('travel_date')||null,travellers:parseInt(d.get('travellers'))||null,notes:(d.get('notes')||'').trim()||null,files:paths}};
  const r2=await fetch(SB+'/rest/v1/visa_applications',{{method:'POST',headers:{{apikey:KEY,Authorization:'Bearer '+(window.RTT_TOKEN||KEY),'Content-Type':'application/json',Prefer:'return=minimal'}},body:JSON.stringify(row)}});
  if(!r2.ok)throw new Error('save '+r2.status);
  notify('New {"passport" if P else "visa"} documents '+id.slice(0,8).toUpperCase()+' – '+row.full_name,'Name: '+row.full_name+'\\nPhone: '+row.phone+(row.email?'\\nEmail: '+row.email:'')+'\\n{"Service" if P else "Country"}: '+row.country+'\\nType: '+row.visa_type+(row.travel_date?'\\nTravel date: '+row.travel_date:'')+'\\nApplicants: '+(row.travellers||1)+'\\nFiles uploaded: '+paths.length+' (see Supabase → Storage → visa-documents → applications/'+id+')'+(row.notes?'\\nNotes: '+row.notes:''),row.email||'');
  f.reset();fl.innerHTML='';syncOther();
  msg.innerHTML='✅ Thank you! Your documents were uploaded securely (reference: <b>'+id.slice(0,8).toUpperCase()+'</b>). Our team will call you shortly. For faster service, <a href="https://wa.me/919843121212?text='+encodeURIComponent('Hi, I uploaded my documents on your website. Reference: '+id.slice(0,8).toUpperCase())+'" target="_blank" rel="noopener">WhatsApp us your reference</a>.';
  msg.classList.add('ok');
 }}catch(err){{msg.textContent='Sorry, the upload did not complete. Please try again, or WhatsApp your documents to 98431 21212.';msg.classList.add('err');}}
 btn.disabled=false;
}});"""
    else:
        form_html = VISA_FORM_NEW.replace("__OPTS__", opts).replace("__OTHERLIST__", other_list)
        form_js = (VISA_JS_NEW.replace("__DOCS__", json.dumps({n: docs for (_, _, n, _, docs) in ITEMS}, ensure_ascii=False))
                   .replace("__CENTRE__", json.dumps([n for (c, _, n, _, _) in ITEMS if c in VISA_CENTRE_CODES])))
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
{form_html}
<div class="paybox" id="pay"><span class="kicker" style="justify-content:center">Secure payment</span><h3 style="font-size:26px;margin:4px 0 8px">Pay {T["payfor"]} online</h3>
<p class="lead" style="font-size:16px">Enter the fees confirmed by our team to see the GST and total, then pay securely. Add your name, phone and reference in the payment window so we can match your payment. UPI, cards, net banking and wallets accepted.</p>
<div class="gcalc" id="gcalc">
<div class="grow"><label>Government / embassy / VFS fee <small>(as confirmed by us – no GST)</small><span class="gin">₹<input type="number" min="0" step="1" inputmode="decimal" id="g_gov" placeholder="0"></span></label>
<label>Our service fee <small>(as confirmed by us)</small><span class="gin">₹<input type="number" min="0" step="1" inputmode="decimal" id="g_fee" placeholder="0"></span></label></div>
<label class="chk gb2b"><input type="checkbox" id="g_b2b"><span>I need a <b>GST invoice</b> for my business (enter your GSTIN)</span></label>
<div class="grow" id="g_bizrow" hidden><label>Client GSTIN<span class="gin"><input id="g_gstin" maxlength="15" placeholder="e.g. 27ABCDE1234F1Z5" style="text-transform:uppercase;letter-spacing:1px" autocomplete="off"></span><small id="g_gmsg"></small></label>
<label>Company / business name<span class="gin"><input id="g_co" maxlength="120" placeholder="As per GST registration"></span></label></div>
<label class="gst8">Your state / UT <select id="g_state">{GST_STATE_OPTS}</select></label>
<p class="gout" id="g_out" hidden>🌍 <b>Clients outside India:</b> GST on our service fee can be different when you live abroad. The total below is an estimate – our team will confirm the exact amount before you pay, so please message us first.</p>
<table class="gtab"><tr><td>Government / embassy fee (pure agent, no GST)</td><td id="o_gov">₹0.00</td></tr>
<tr><td>Service fee (SAC 9985)</td><td id="o_fee">₹0.00</td></tr>
<tr id="r_c"><td>CGST @ 9%</td><td id="o_c">₹0.00</td></tr><tr id="r_s"><td>SGST @ 9%</td><td id="o_s">₹0.00</td></tr><tr id="r_i" hidden><td>IGST @ 18%</td><td id="o_i">₹0.00</td></tr>
<tr class="gtot"><td>Total to pay</td><td id="o_t">₹0.00</td></tr></table>
<p class="gnote">Enter the <b>total</b> shown above as the Booking Amount in the payment window<span id="g_hint"></span>. A GST tax invoice (our GSTIN 27AMUPK4723E1ZU) will be issued for the service fee<span id="g_to"></span>.</p></div>
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
function calc(){{const g=Math.max(0,+$('g_gov').value||0),f=Math.max(0,+$('g_fee').value||0),inS=$('g_state').value==='27';$('g_out').hidden=$('g_state').value!=='OUT';const c=r2(f*.09),i=r2(f*.18);
$('o_gov').textContent=inr(g);$('o_fee').textContent=inr(f);$('o_c').textContent=$('o_s').textContent=inr(c);$('o_i').textContent=inr(i);
$('r_c').hidden=$('r_s').hidden=!inS;$('r_i').hidden=inS;$('o_t').textContent=inr(r2(g+f+(inS?2*c:i)));}}
const GST_RE=/^[0-3][0-9][A-Z]{{5}}[0-9]{{4}}[A-Z][1-9A-Z]Z[0-9A-Z]$/;
function biz(){{if(!$('g_b2b')){{calc();return;}}const on=$('g_b2b').checked;$('g_bizrow').hidden=!on;const g=$('g_gstin').value.toUpperCase().replace(/\\s/g,'');$('g_gstin').value=g;
 let ok=false;if(on&&g){{ok=GST_RE.test(g);$('g_gmsg').textContent=ok?'✓ Valid format · State code '+g.slice(0,2)+(g.slice(0,2)==='27'?' (Maharashtra – CGST + SGST)':' (outside Maharashtra – IGST)'):'Please check – GSTIN has 15 characters, e.g. 27ABCDE1234F1Z5';$('g_gmsg').style.color=ok?'#17703a':'var(--crimson)';if(ok){{const sc={{'25':'26','28':'37'}}[g.slice(0,2)]||g.slice(0,2);if($('g_state').querySelector('option[value="'+sc+'"]')){{$('g_state').value=sc;$('g_state').disabled=true;}}}}}}
 if(!ok){{$('g_state').disabled=false;if(!g)$('g_gmsg').textContent='';}}
 const stN=$('g_state').options[$('g_state').selectedIndex].text;$('g_hint').textContent=on&&ok?', and enter '+g+' in the “Client GSTIN” box (company name in “Tour or Booking Details”)':($('g_state').value==='OUT'?' – please mention the country you live in under “Tour or Booking Details”, and pay only after our team confirms the amount':' – please also mention your state (“'+stN+'”) in “Tour or Booking Details” so we can show it on your invoice');
 $('g_to').textContent=on&&ok?' in the name of '+($('g_co').value.trim()||'your business')+', GSTIN '+g:'';calc();}}
['g_gov','g_fee'].forEach(x=>$(x)&&$(x).addEventListener('input',calc));if($('g_state'))$('g_state').addEventListener('change',biz);['g_b2b','g_gstin','g_co'].forEach(x=>$(x)&&$(x).addEventListener('input',biz));if($('g_b2b'))$('g_b2b').addEventListener('change',biz);if($('g_gov'))biz();}})();
const tabs=document.querySelectorAll('.vtab'),panels=document.querySelectorAll('.vpanel');
function show(c){{tabs.forEach(t=>t.classList.toggle('on',t.dataset.c===c));panels.forEach(p=>p.hidden=p.dataset.c!==c);}}
tabs.forEach(t=>t.addEventListener('click',()=>show(t.dataset.c)));
const names={json.dumps({c:n for (c,_,n,_,_) in ITEMS})};
const csel=document.querySelector('select[name=country]'),ocw=document.getElementById('ocwrap');
const syncOther=()=>{{if(ocw)ocw.hidden=csel.value!=='Other';}};csel.addEventListener('change',syncOther);
document.querySelectorAll('[data-pick]').forEach(a=>a.addEventListener('click',()=>{{csel.value=names[a.dataset.pick];csel.dispatchEvent(new Event('change'));}}));
const vo=document.getElementById('vo_country');
if(vo){{
 const vmsg=document.getElementById('vo_msg');
 document.getElementById('vo_wa').addEventListener('click',e=>{{const c=vo.value.trim();vmsg.className='vmsg';vmsg.textContent='';
  if(c.length<2){{e.preventDefault();vmsg.textContent='Please type the country you are visiting.';vmsg.classList.add('err');vo.focus();return;}}
  e.currentTarget.href='https://wa.me/919843121212?text='+encodeURIComponent('Hi The Real Tours and Travels, please share the documents required and the price for a '+c+' visa. Travellers:  Travel date: ');}});
 document.getElementById('vo_up').addEventListener('click',()=>{{csel.value='Other';const c=vo.value.trim();if(c)f.other_country.value=c;csel.dispatchEvent(new Event('change'));}});
}}
{form_js}
}})();
</script>"""

# New visa upload form (visa page only). Plain/raw strings – tokens __X__ are filled in by visa_page().
VISA_FORM_NEW = r"""<form id="vform" class="vform" novalidate>
<div class="row"><label>Full name* <small>(main contact)</small><input name="full_name" required maxlength="120" autocomplete="name"></label>
<label>Mobile number*<input name="phone" required inputmode="tel" maxlength="20" autocomplete="tel" placeholder="10-digit mobile, or +country code"></label></div>
<div class="row"><label>Email<input name="email" type="email" maxlength="160" autocomplete="email"></label>
<label>Passport nationality*<select name="nationality"><option>Indian</option><option value="Other">Other – type below</option></select></label></div>
<label id="natwrap" hidden>Which nationality?*<input name="nationality_other" maxlength="40" autocomplete="off" placeholder="e.g. British, American, Canadian (OCI card holders too)"></label>
<div class="row"><label>Country*<select name="country" required>__OPTS__</select></label>
<label>Visa type<select name="visa_type"><option>Tourist</option><option>Business</option><option>Visiting family / friends</option><option>Student</option><option>Transit</option><option>Medical</option><option>Conference / Event</option><option>Work / Employment</option><option>Pilgrimage (e.g. Umrah)</option><option>Not sure – please advise</option></select></label></div>
<label id="ocwrap" hidden>Which country?*<input name="other_country" maxlength="60" autocomplete="off" placeholder="e.g. Kenya, Bhutan, South Korea"></label>
__OTHERLIST__
<div class="row"><label>Travel date<input name="travel_date" type="date"></label>
<label>Return date<input name="return_date" type="date"></label></div>
<div class="row"><label>Employment status<select name="employment"><option value="">Select…</option><option>Salaried</option><option>Self-employed / Business owner</option><option>Student</option><option>Retired</option><option>Homemaker</option><option>Other</option></select></label>
<label id="empow" hidden>Your occupation<input name="employment_other" maxlength="60" placeholder="e.g. freelancer, farmer, NRI, between jobs"></label></div>
<div id="apptwrap" class="appt" hidden><label>Your city or town <small>(for the visa-centre appointment)</small><input name="appt_city" maxlength="60" autocomplete="address-level2" placeholder="e.g. Mumbai, Thane, Nashik, Surat"></label>
<p class="vnote" id="apptnote"></p></div>
<div class="row"><fieldset class="yn"><legend>Ever been refused a visa for any country?</legend><div class="chips"><label><input type="radio" name="refused" value="No" checked>No</label><label><input type="radio" name="refused" value="Yes">Yes</label></div></fieldset>
<fieldset class="yn"><legend>Visited the US, UK, Schengen, Canada or Australia in the last 5 years?</legend><div class="chips"><label><input type="radio" name="history" value="No" checked>No</label><label><input type="radio" name="history" value="Yes">Yes</label></div></fieldset></div>
<p id="refnote" class="vnote" hidden>Please mention the country and year of the refusal in the notes below – it helps us prepare a stronger application.</p>
<div class="row"><label>Number of travellers<input name="travellers" type="number" min="1" max="10" value="1"></label><span class="vnote">Applying for 10 or more people? See <a href="#vgroup">group visa applications</a> below.</span></div>
<div id="vcheck" class="vcheck" hidden></div>
<label class="chk"><input type="checkbox" name="later"><span>I'll send my documents later – just save my details for now</span></label>
<p class="vnote famnote" id="famnote" hidden>👨‍👩‍👧‍👦 <b>Family or group trip?</b> Upload each person's passport and photo under their own name. Shared documents – bank statements, ITR, flight and hotel bookings – only need to be uploaded once, under the person paying for the trip. Scanned everyone into one file? Upload it under Traveller 1 and tick the box for the others.</p>
<div id="tlist" class="tlist"></div>
<label>Notes for our team<textarea name="notes" maxlength="1000" rows="3" placeholder="Anything we should know – e.g. details of a previous refusal, travelling with children, urgent travel"></textarea></label>
<label class="chk"><input type="checkbox" name="consent" required><span>I agree that The Real Tours and Travels may use my details and documents only to process my visa application, as per the <a href="../privacy-policy/">Privacy Policy</a>.</span></label>
<div class="hp" aria-hidden="true"><label>Leave this empty<input name="company_website" tabindex="-1" autocomplete="off"></label></div>
<button class="btn gold" type="submit" id="vsubmit">Upload documents securely</button>
<p id="vmsg" class="vmsg" role="status" aria-live="polite"></p>
</form>
<div class="grp" id="vgroup"><div><b>👥 Group visa applications – 10 or more applicants</b><p>For tour groups, corporate delegations, conferences and pilgrimage groups, our visa desk manages the complete process – a consolidated document checklist, verification of every file, form filling and coordinated visa-centre appointments – with a dedicated coordinator for your group.</p></div><div class="grpbtn"><a class="btn gold" href="https://wa.me/919843121212?text=Hello%20The%20Real%20Tours%20and%20Travels%2C%20we%20would%20like%20assistance%20with%20a%20group%20visa%20application.%0ADestination%20country%3A%20%0ANumber%20of%20applicants%3A%20%0ATravel%20dates%3A%20%0AGroup%20type%20%28corporate%20/%20tour%20/%20pilgrimage%20/%20other%29%3A%20" target="_blank" rel="noopener">💬 WhatsApp our visa desk</a><a class="btn outline" href="tel:+919843121212">📞 +91 98431 21212</a><a class="btn outline" href="mailto:enquiry@therealtoursandtravels.com?subject=Group%20visa%20application">✉️ Email us</a></div></div>"""

VISA_JS_NEW = r"""const f=document.getElementById('vform'),msg=document.getElementById('vmsg'),btn=document.getElementById('vsubmit');
const DOCS=__DOCS__;
const EMP={"Salaried":["Last 3 months' salary slips","Leave / NOC letter from your employer","Income tax returns (ITR) for the last 2–3 years","Bank statements for the last 6 months"],
"Self-employed / Business owner":["Business proof – GST certificate, Shop Act licence or company registration","Income tax returns (ITR) for the last 3 years","Personal and business bank statements for the last 6 months","Cover letter on your business letterhead"],
"Student":["College ID card and bonafide / enrolment letter","NOC / leave letter from your college","Parents' bank statements and ITR, with a sponsorship letter"],
"Retired":["Retirement letter or pension proof","Bank statements for the last 6 months","Income tax returns (ITR), if filed"],
"Homemaker":["Spouse's bank statements and ITR","Sponsorship letter from your spouse","Marriage certificate (if asked for)"],
"Other":["Proof of income – recent bank statements, and ITR if you file one","If someone else is paying for the trip: their bank statements, ITR and a sponsorship letter"]};
const CENTRE=__CENTRE__; // countries whose visa needs a visit to a visa centre / consulate
const REL=['Self (main contact)','Spouse','Child (under 18)','Child (18 or older)','Parent','Sibling','Other relative','Friend / colleague'];
const ACCEPT='.pdf,.jpg,.jpeg,.png,.heic,.heif,.webp,application/pdf,image/*';
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'})[c]);
const today=new Date(Date.now()+330*60000).toISOString().slice(0,10);
f.travel_date.min=today;f.return_date.min=today;
const addMonths=(ds,m)=>{const d=new Date(ds+'T00:00');d.setMonth(d.getMonth()+m);return d.toISOString().slice(0,10);};
const nice=ds=>new Date(ds+'T00:00').toLocaleDateString('en-IN',{day:'numeric',month:'short',year:'numeric'});
// ---- nationality / refusal note ----
const natw=document.getElementById('natwrap');f.nationality.addEventListener('change',()=>{natw.hidden=f.nationality.value!=='Other';});
f.querySelectorAll('input[name=refused]').forEach(r=>r.addEventListener('change',()=>{document.getElementById('refnote').hidden=f.querySelector('input[name=refused]:checked').value!=='Yes';}));
// ---- checklist for the chosen country (+ employment) ----
const vcheck=document.getElementById('vcheck');
function countryName(){return csel.value==='Other'?(f.other_country.value.trim()||'your destination'):csel.value;}
function drawCheck(){const c=csel.value,emp=f.employment.value;if(!c){vcheck.hidden=true;return;}
 let h='<h4>📋 Documents checklist – '+esc(countryName())+'</h4>';
 if(DOCS[c])h+='<ul>'+DOCS[c].map(x=>'<li>'+x+'</li>').join('')+'</ul>';
 else h+='<p>Our visa team will share the exact checklist for '+esc(countryName())+'. Usually needed: passport (front &amp; back), a recent photo with white background, bank statements, ITR and your flight / hotel bookings.</p>';
 if(EMP[emp])h+='<h4>Also needed – '+esc(emp==='Other'?(f.employment_other.value.trim()||'your occupation'):emp)+'</h4><ul>'+EMP[emp].map(x=>'<li>'+x+'</li>').join('')+'</ul>';
 h+='<p class="vnote">Upload what you have – our team will tell you if anything else is needed for your case.</p>';
 vcheck.innerHTML=h;vcheck.hidden=false;}
csel.addEventListener('change',drawCheck);f.employment.addEventListener('change',drawCheck);f.other_country.addEventListener('input',drawCheck);
// ---- employment "Other": ask what they do ----
const empow=document.getElementById('empow');f.employment.addEventListener('change',()=>{empow.hidden=f.employment.value!=='Other';});f.employment_other.addEventListener('input',drawCheck);
// ---- visa-centre city: only asked when the visa needs a visit (or the country is not listed) ----
const apptw=document.getElementById('apptwrap'),apptn=document.getElementById('apptnote');
function syncAppt(){const c=csel.value,need=CENTRE.includes(c),oth=c==='Other';apptw.hidden=!(need||oth);
 apptn.textContent=need&&c==='Australia'?'Australia may ask applicants in India to give fingerprints and a photo at a visa centre. Tell us where you live – if it is needed, we\'ll book the nearest centre for you.':need?c+' visas need a visit to a visa centre'+(c==='United States'?' and an interview at the US consulate':' for fingerprints and a photo')+'. Tell us where you live – we\'ll book your appointment at the nearest centre and tell you exactly where to go and what to carry.'
  :'If '+countryName()+' needs a visa-centre visit, we\'ll book it at the centre nearest to you. Many countries are online-only – we\'ll let you know.';}
csel.addEventListener('change',syncAppt);f.other_country.addEventListener('input',syncAppt);
// ---- one block per traveller: name, passport expiry, documents ----
const tlist=document.getElementById('tlist');
function block(i){const b=document.createElement('div');b.className='tblock';
 b.innerHTML='<h4>Traveller '+(i+1)+'</h4><div class="row"><label>Name as on passport'+(i?'*':' <small>(if different from main contact)</small>')+'<input data-tn maxlength="80" autocomplete="off"></label>'+
 '<label>Relationship to main contact<select data-tr>'+(i?'<option value="">Select…</option>':'')+REL.map(r=>'<option>'+r+'</option>').join('')+'</select></label></div>'+
 '<div class="row"><label>Passport expiry date<input data-tx type="date"></label><span></span></div><p class="pwarn" hidden></p>'+
 '<p class="tminor" hidden></p>'+
 (i?'<label class="chk tsame"><input type="checkbox" data-ts><span>This traveller\'s documents are in the same file(s) as Traveller 1</span></label>':'')+
 '<label class="tfiles">Documents for this traveller* <small>(select several files – passport, photo, bank statements, ITR…)</small><input data-tf type="file" multiple accept="'+ACCEPT+'"></label><div class="flist"></div>';
 const fi=b.querySelector('[data-tf]'),fl=b.querySelector('.flist'),tr=b.querySelector('[data-tr]'),tm=b.querySelector('.tminor'),ts=b.querySelector('[data-ts]');
 fi.addEventListener('change',()=>{fl.innerHTML=[...fi.files].map(x=>{const big=x.size>10485760,shr=/^image\/(jpeg|png|webp)$/.test(x.type)&&x.size>3145728;
  return '<span>📄 '+esc(x.name)+' · '+(x.size/1048576).toFixed(1)+' MB'+(shr?' – will be resized':big?' – too large (max 10 MB)':'')+'</span>';}).join('');});
 tr.addEventListener('change',()=>{tm.hidden=tr.value!=='Child (under 18)';tm.innerHTML='<b>For children under 18, usually also needed:</b> birth certificate · copies of both parents\' passports · if travelling with only one parent, a consent (NOC) letter from the other parent. We confirm the exact list for '+esc(countryName())+'.';});
 if(ts)ts.addEventListener('change',()=>syncFiles(b));
 b.querySelector('[data-tx]').addEventListener('change',checkPassports);return b;}
function drawTravellers(){const n=Math.min(10,Math.max(1,parseInt(f.travellers.value)||1));
 while(tlist.children.length<n)tlist.appendChild(block(tlist.children.length));
 while(tlist.children.length>n)tlist.lastElementChild.remove();
 syncLater();checkPassports();}
f.travellers.addEventListener('input',drawTravellers);
// ---- send documents later ----
function syncFiles(b){const later=f.later.checked,ts=b.querySelector('[data-ts]'),same=!!(ts&&ts.checked);b.querySelectorAll('.tfiles,.flist').forEach(x=>x.hidden=later||same);if(ts)ts.closest('label').hidden=later;}
function syncLater(){const later=f.later.checked;tlist.querySelectorAll('.tblock').forEach(syncFiles);document.getElementById('famnote').hidden=later||tlist.children.length<2;btn.textContent=later?'Save my details':'Upload documents securely';}
f.later.addEventListener('change',syncLater);
// ---- passport validity: most countries need 6 months beyond the return date ----
function checkPassports(){const trav=f.travel_date.value,ret=f.return_date.value||trav;
 tlist.querySelectorAll('.tblock').forEach(b=>{const x=b.querySelector('[data-tx]').value,w=b.querySelector('.pwarn');b.dataset.warn='';
  if(!x){w.hidden=true;return;}
  let t='';
  if(x<=today)t='⚠️ This passport has already expired – it must be renewed before you apply.';
  else if(trav&&x<=trav)t='⚠️ This passport expires before your trip – it must be renewed before you apply.';
  else if(ret&&x<addMonths(ret,6))t='⚠️ This passport expires on '+nice(x)+', less than 6 months after your return date. Most countries need 6 months\' validity – please renew it first.';
  else if(!ret&&x<addMonths(today,6))t='⚠️ This passport expires within 6 months. Most countries need 6 months\' validity after your return – please check before you apply.';
  if(t){w.innerHTML=t+' <a href="../passport/">We can help you renew it →</a>';w.hidden=false;b.dataset.warn='1';}else w.hidden=true;});}
f.travel_date.addEventListener('change',()=>{f.return_date.min=f.travel_date.value||today;if(f.return_date.value&&f.return_date.value<f.travel_date.value)f.return_date.value='';checkPassports();});
f.return_date.addEventListener('change',checkPassports);
drawTravellers();drawCheck();
// ---- shrink large phone photos before upload (keeps PDFs and HEIC as they are) ----
async function shrink(file){if(!/^image\/(jpeg|png|webp)$/.test(file.type)||file.size<=3145728)return file;
 try{const img=await createImageBitmap(file),k=Math.min(1,2400/Math.max(img.width,img.height)),c=document.createElement('canvas');
  c.width=Math.round(img.width*k);c.height=Math.round(img.height*k);c.getContext('2d').drawImage(img,0,0,c.width,c.height);
  const blob=await new Promise(r=>c.toBlob(r,'image/jpeg',.85));if(!blob||blob.size>=file.size)return file;
  return new File([blob],file.name.replace(/\.[^.]+$/,'')+'.jpg',{type:'image/jpeg'});}catch(_){return file;}}
function uuid(){return (crypto.randomUUID?crypto.randomUUID():'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,c=>{const r=Math.random()*16|0;return (c=='x'?r:(r&3|8)).toString(16);}));}
function safe(n){return n.normalize('NFKD').replace(/[^A-Za-z0-9._-]+/g,'_').slice(-80)||'file';}
f.addEventListener('submit',async e=>{
 e.preventDefault();msg.className='vmsg';
 const fail=(t,el)=>{msg.textContent=t;msg.classList.add('err');if(el)el.focus();};
 if(f.company_website.value){msg.textContent='✅ Thank you – details received.';msg.classList.add('ok');return;} // spam trap
 const d=new FormData(f),later=f.later.checked;
 const phone=(d.get('phone')||'').replace(/[^0-9+]/g,'');
 if(!d.get('full_name').trim()||phone.length<10)return fail('Please enter your name and a valid mobile number.',f.full_name);
 let country=d.get('country');
 if(country==='Other'){country=(d.get('other_country')||'').trim();if(country.length<2)return fail('Please type the country you are visiting.',f.other_country);}
 let nat=d.get('nationality');if(nat==='Other'){nat=(d.get('nationality_other')||'').trim();if(nat.length<2)return fail('Please type your passport nationality.',f.nationality_other);}
 const trav=d.get('travel_date')||'',ret=d.get('return_date')||'';
 if(trav&&trav<today)return fail('The travel date cannot be in the past.',f.travel_date);
 if(ret&&trav&&ret<trav)return fail('The return date must be after the travel date.',f.return_date);
 const blocks=[...tlist.querySelectorAll('.tblock')],T=[];
 for(let i=0;i<blocks.length;i++){const b=blocks[i],nm=b.querySelector('[data-tn]').value.trim();
  if(i&&nm.length<2)return fail('Please enter the name of traveller '+(i+1)+' as on their passport.',b.querySelector('[data-tn]'));
  const ts=b.querySelector('[data-ts]'),same=!!(ts&&ts.checked),files=same?[]:[...b.querySelector('[data-tf]').files];
  if(!later&&!same&&!files.length)return fail('Please choose the documents for traveller '+(i+1)+' – or tick "I\'ll send my documents later".',b.querySelector('[data-tf]'));
  T.push({name:nm||d.get('full_name').trim(),rel:b.querySelector('[data-tr]').value,same,expiry:b.querySelector('[data-tx]').value,warn:!!b.dataset.warn,files:later?[]:files});}
 if(!later&&T.some(t=>t.same)&&!T[0].files.length)return fail('Please upload the combined file under Traveller 1.',blocks[0].querySelector('[data-tf]'));
 let emp=d.get('employment')||'';if(emp==='Other')emp='Other – '+((d.get('employment_other')||'').trim()||'not specified');
 const appt=apptw.hidden?'':((d.get('appt_city')||'').trim()||'not given');
 const total=T.reduce((a,t)=>a+t.files.length,0);
 if(total>30)return fail('Please upload up to 30 files in total – WhatsApp us any extra documents.');
 const tooBig=T.flatMap(t=>t.files).find(x=>x.size>10485760&&!/^image\/(jpeg|png|webp)$/.test(x.type));
 if(tooBig)return fail(tooBig.name+' is larger than 10 MB. Please upload a smaller scan (or WhatsApp it to us).');
 if(!d.get('consent'))return fail('Please tick the consent box.');
 btn.disabled=true;const id=uuid(),ref=id.slice(0,8).toUpperCase(),paths=[];
 try{
  let k=0;
  for(let i=0;i<T.length;i++)for(let j=0;j<T[i].files.length;j++){
   k++;msg.textContent=(T[i].files[j].size>3145728?'Preparing':'Uploading')+' file '+k+' of '+total+'…';
   const file=await shrink(T[i].files[j]);
   if(file.size>10485760)throw {user:file.name+' is larger than 10 MB. Please upload a smaller scan (or WhatsApp it to us).'};
   const p='applications/'+id+'/T'+(i+1)+'-'+String(j+1).padStart(2,'0')+'-'+safe(file.name);
   msg.textContent='Uploading file '+k+' of '+total+'…';
   const r=await fetch(SB+'/storage/v1/object/visa-documents/'+p,{method:'POST',headers:{apikey:KEY,Authorization:'Bearer '+(window.RTT_TOKEN||KEY),'Content-Type':file.type||'application/octet-stream','x-upsert':'false'},body:file});
   if(!r.ok)throw new Error('upload '+r.status);
   paths.push(p);
  }
  const det=['Passport nationality: '+nat,'Return date: '+(ret||'not given'),'Employment: '+(emp||'not given'),
   'Ever refused a visa: '+d.get('refused'),'Visited US/UK/Schengen/Canada/Australia in last 5 years: '+d.get('history')].concat(appt?['City for visa-centre appointment: '+appt]:[])
   .concat(T.map((t,i)=>'Traveller '+(i+1)+': '+t.name+(t.rel?' ('+t.rel+')':'')+(t.expiry?' – passport expires '+t.expiry+(t.warn?' (⚠ under 6 months validity)':''):'')+(later?'':t.same?' – documents in Traveller 1\'s file':' – '+t.files.length+' file'+(t.files.length==1?'':'s'))));
  if(later)det.push('Documents: client will send them later');
  const un=(d.get('notes')||'').trim();
  const notes=(det.join('\n')+(un?'\n---\n'+un:'')).slice(0,2000);
  const row={id,full_name:d.get('full_name').trim(),phone,email:(d.get('email')||'').trim()||null,country:country.slice(0,60),visa_type:d.get('visa_type'),travel_date:trav||null,travellers:T.length,notes,files:paths};
  const r2=await fetch(SB+'/rest/v1/visa_applications',{method:'POST',headers:{apikey:KEY,Authorization:'Bearer '+(window.RTT_TOKEN||KEY),'Content-Type':'application/json',Prefer:'return=minimal'},body:JSON.stringify(row)});
  if(!r2.ok)throw new Error('save '+r2.status);
  notify('New visa '+(later?'enquiry (documents to follow) ':'documents ')+ref+' – '+row.full_name,'Name: '+row.full_name+'\nPhone: '+row.phone+(row.email?'\nEmail: '+row.email:'')+'\nCountry: '+row.country+'\nVisa type: '+row.visa_type+(trav?'\nTravel date: '+trav:'')+'\nTravellers: '+T.length+'\n'+det.join('\n')+(un?'\nNotes: '+un:'')+'\nFiles uploaded: '+paths.length+(paths.length?' (stored privately in Supabase › Storage › visa-documents/applications/'+id+')':''),row.email||'');
  f.reset();tlist.innerHTML='';drawTravellers();syncOther();drawCheck();syncAppt();empow.hidden=true;natw.hidden=true;document.getElementById('refnote').hidden=true;
  const wa='https://wa.me/919843121212?text='+encodeURIComponent((later?'Hi, I saved my visa details on your website and will send my documents. Reference: ':'Hi, I uploaded my visa documents on your website. Reference: ')+ref);
  msg.innerHTML=later?'✅ Thank you! Your details are saved (reference: <b>'+ref+'</b>). Send your documents any time – <a href="'+wa+'" target="_blank" rel="noopener">WhatsApp them to us with this reference</a>, or upload them here.':'✅ Thank you! Your documents were uploaded securely (reference: <b>'+ref+'</b>). Our team will call you shortly. For faster service, <a href="'+wa+'" target="_blank" rel="noopener">WhatsApp us your reference</a>.';
  msg.classList.add('ok');
 }catch(err){msg.textContent=err&&err.user?err.user:'Sorry, the upload did not complete. Please try again, or WhatsApp your documents to 98431 21212.';msg.classList.add('err');}
 btn.disabled=false;
});"""


VISA_CSS = """
.yn{border:0;padding:0;margin:0;display:grid;gap:8px}.yn legend{font-weight:500;font-size:15px;margin-bottom:8px}
.vnote{margin:0;font-size:13.5px;color:var(--muted);align-self:center}
.vcheck{background:var(--bg);border:1px solid var(--line);border-left:4px solid var(--red);border-radius:14px;padding:14px 18px}
.vcheck h4{margin:4px 0 6px;font-family:'Playfair Display',serif;font-size:18px;color:var(--wine)}.vcheck ul{margin:0 0 8px;padding-left:20px}.vcheck li{margin:3px 0}.vcheck p{margin:4px 0}
.tlist{display:grid;gap:14px}.tblock{border:1px solid var(--line);border-radius:16px;padding:14px 16px;background:#fff;display:grid;gap:10px}
.tblock h4{margin:0;font-family:'Playfair Display',serif;font-size:18px;color:var(--wine)}
.tminor{margin:0;background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:10px 14px;font-size:14px}.famnote{background:#fdf0f0;border-radius:12px;padding:10px 14px}.appt{display:grid;gap:6px}
.pwarn{margin:0;background:#fff4e5;border:1px solid #f2c48b;color:#7a4300;border-radius:12px;padding:10px 14px;font-size:14px}.pwarn a{color:var(--crimson);font-weight:500}

.gcalc{text-align:left;margin:16px 0 6px;display:grid;gap:12px}.grow{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.gcalc label{display:grid;gap:6px;font-weight:500;font-size:14.5px;color:var(--wine)}.gcalc small{font-weight:400;color:var(--muted);font-size:12.5px}
.gin{display:flex;align-items:center;gap:6px;border:1px solid var(--line);border-radius:12px;padding:0 12px;background:#fff}.gin input{border:0;outline:0;font:500 17px 'Jost',sans-serif;padding:11px 0;width:100%;background:none}
.gin:focus-within{border-color:var(--red);box-shadow:0 0 0 2px rgba(215,25,31,.15)}.gst8 select{font:400 15px 'Jost',sans-serif;padding:10px 12px;border:1px solid var(--line);border-radius:12px;max-width:260px}
.gtab{width:100%;border-collapse:collapse;font-size:15px}.gtab td{padding:8px 4px;border-bottom:1px solid var(--line)}.gtab td:last-child{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.gtot td{font-weight:700;font-size:17px;color:var(--crimson);border-bottom:0;border-top:2px solid var(--wine)}.gnote{font-size:13px;color:var(--muted);margin:0}.gout{margin:0;background:#fff4e5;border:1px solid #f2c48b;color:#7a4300;border-radius:12px;padding:10px 14px;font-size:14px}
@media(max-width:600px){.grow{grid-template-columns:1fr}}
#upload .paybox{margin:28px auto 0}
.gb2b{font-weight:400!important;color:var(--ink)!important}.gcalc .chk{display:flex!important;gap:8px;align-items:flex-start}.gcalc .chk input{width:auto;margin-top:3px}#g_gmsg{font-size:12.5px}
.vtabs{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-bottom:26px}
.vother{display:flex;flex-wrap:wrap;gap:10px;align-items:end;margin-top:6px}.vother label{flex:1;min-width:220px;display:grid;gap:6px;font-weight:500}.vother input{font:inherit;padding:12px 14px;border:1px solid var(--line);border-radius:12px}.vother input:focus{outline:2px solid var(--red);border-color:var(--red)}
.vgrp{display:grid;gap:8px;margin-bottom:14px;justify-items:center}.vgl{font-size:13px;font-weight:600;letter-spacing:.6px;text-transform:uppercase;color:var(--muted)}.vgrow{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.vbadges{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 4px}.vb{font-size:13px;font-weight:600;border-radius:999px;padding:4px 12px;border:1px solid}
.vb-free{color:#17703a;border-color:#cdebd6;background:#eef9f1}.vb-online{color:var(--wine);border-color:var(--line);background:var(--bg)}.vb-visa{color:var(--crimson);border-color:#f1c9cb;background:#fdf0f0}.vb-card{color:var(--ink);border-color:var(--line);background:#fff}
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
