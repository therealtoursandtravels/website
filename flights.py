"""Offline flight enquiry bar: client searches -> enquiry saved -> sent to agent on WhatsApp -> agent quotes & tickets offline."""
from visa import SB_URL, SB_KEY

AIRPORTS = [
 ("Mumbai","BOM","Chhatrapati Shivaji Maharaj Intl"),("Navi Mumbai","NMI","Navi Mumbai Intl"),("Delhi","DEL","Indira Gandhi Intl"),
 ("Bengaluru","BLR","Kempegowda Intl"),("Chennai","MAA","Chennai Intl"),("Kolkata","CCU","Netaji Subhas Chandra Bose Intl"),
 ("Hyderabad","HYD","Rajiv Gandhi Intl"),("Ahmedabad","AMD","Sardar Vallabhbhai Patel Intl"),("Pune","PNQ","Pune"),
 ("Goa (Dabolim)","GOI","Dabolim"),("Goa (Mopa)","GOX","Manohar Intl"),("Jaipur","JAI","Jaipur Intl"),("Udaipur","UDR","Maharana Pratap"),
 ("Jodhpur","JDH","Jodhpur"),("Srinagar","SXR","Srinagar"),("Jammu","IXJ","Jammu"),("Leh","IXL","Kushok Bakula Rimpochee"),
 ("Chandigarh","IXC","Chandigarh Intl"),("Amritsar","ATQ","Sri Guru Ram Dass Jee Intl"),("Dehradun","DED","Jolly Grant"),
 ("Varanasi","VNS","Lal Bahadur Shastri Intl"),("Lucknow","LKO","Chaudhary Charan Singh Intl"),("Ayodhya","AYJ","Maharishi Valmiki Intl"),
 ("Patna","PAT","Jay Prakash Narayan"),("Bagdogra","IXB","Bagdogra"),("Guwahati","GAU","Lokpriya Gopinath Bordoloi Intl"),
 ("Bhubaneswar","BBI","Biju Patnaik Intl"),("Port Blair","IXZ","Veer Savarkar Intl"),("Kochi","COK","Cochin Intl"),
 ("Thiruvananthapuram","TRV","Trivandrum Intl"),("Kozhikode","CCJ","Calicut Intl"),("Mangaluru","IXE","Mangaluru Intl"),
 ("Coimbatore","CJB","Coimbatore Intl"),("Madurai","IXM","Madurai"),("Indore","IDR","Devi Ahilyabai Holkar"),("Bhopal","BHO","Raja Bhoj"),
 ("Nagpur","NAG","Dr. Babasaheb Ambedkar Intl"),("Aurangabad","IXU","Aurangabad"),("Nashik","ISK","Nashik"),("Surat","STV","Surat"),
 ("Vadodara","BDQ","Vadodara"),("Rajkot","HSR","Rajkot Intl"),("Bhavnagar","BHU","Bhavnagar"),("Raipur","RPR","Swami Vivekananda"),
 ("Ranchi","IXR","Birsa Munda"),("Visakhapatnam","VTZ","Visakhapatnam"),
 ("Dubai","DXB","Dubai Intl"),("Abu Dhabi","AUH","Zayed Intl"),("Sharjah","SHJ","Sharjah Intl"),("Doha","DOH","Hamad Intl"),
 ("Muscat","MCT","Muscat Intl"),("Bahrain","BAH","Bahrain Intl"),("Kuwait","KWI","Kuwait Intl"),("Riyadh","RUH","King Khalid Intl"),
 ("Jeddah","JED","King Abdulaziz Intl"),("Singapore","SIN","Changi"),("Bangkok","BKK","Suvarnabhumi"),("Phuket","HKT","Phuket Intl"),
 ("Kuala Lumpur","KUL","Kuala Lumpur Intl"),("Bali (Denpasar)","DPS","Ngurah Rai Intl"),("Hanoi","HAN","Noi Bai Intl"),
 ("Ho Chi Minh City","SGN","Tan Son Nhat Intl"),("Da Nang","DAD","Da Nang Intl"),("Malé","MLE","Velana Intl"),("Colombo","CMB","Bandaranaike Intl"),
 ("Kathmandu","KTM","Tribhuvan Intl"),("Hong Kong","HKG","Hong Kong Intl"),("Tokyo","NRT","Narita Intl"),("Tokyo (Haneda)","HND","Haneda"),
 ("Seoul","ICN","Incheon Intl"),("Sydney","SYD","Kingsford Smith"),("Melbourne","MEL","Melbourne"),("Auckland","AKL","Auckland"),
 ("London","LHR","Heathrow"),("Paris","CDG","Charles de Gaulle"),("Frankfurt","FRA","Frankfurt"),("Zurich","ZRH","Zurich"),
 ("Amsterdam","AMS","Schiphol"),("Rome","FCO","Fiumicino"),("Istanbul","IST","Istanbul"),("Vienna","VIE","Vienna Intl"),
 ("New York","JFK","John F. Kennedy Intl"),("Newark","EWR","Newark Liberty Intl"),("Chicago","ORD","O'Hare Intl"),
 ("San Francisco","SFO","San Francisco Intl"),("Toronto","YYZ","Pearson Intl"),("Vancouver","YVR","Vancouver Intl"),
 ("Nairobi","NBO","Jomo Kenyatta Intl"),("Johannesburg","JNB","O. R. Tambo Intl"),("Mauritius","MRU","Sir Seewoosagur Ramgoolam Intl"),
]

HOTEL_CITIES = ["Mumbai","Delhi","Goa","Jaipur","Udaipur","Jodhpur","Jaisalmer","Srinagar","Gulmarg","Pahalgam","Manali","Shimla","Dharamshala","Rishikesh","Mussoorie","Nainital","Leh","Munnar","Alleppey","Kochi","Thekkady","Kovalam","Ooty","Coorg","Mysuru","Port Blair","Havelock Island","Darjeeling","Gangtok","Varanasi","Ayodhya","Palitana","Shirdi","Mahabaleshwar","Lonavala","Dubai","Abu Dhabi","Singapore","Bangkok","Pattaya","Phuket","Krabi","Bali","Kuala Lumpur","Maldives","Hanoi","Da Nang","Paris","London","Zurich","Interlaken","Lucerne","Istanbul","Baku","Tokyo","Sydney","New York"]

def _sel(name, label, rng, unit):
    return f'<select name="{name}" aria-label="{label}">' + "".join(f'<option value="{i}">{i} {unit(i)}</option>' for i in rng) + '</select>'

def _contact(btn):
    return f"""<div class="fgrid2">
<label class="fcell">Your name<input name="name" maxlength="120" autocomplete="name"></label>
<label class="fcell">Mobile or email*<input name="contact" required maxlength="160" placeholder="98xxxxxxxx or you@example.com" autocomplete="tel"></label>
<label class="fcell">Notes<input name="notes" maxlength="200" placeholder=""></label>
<button class="btn gold fgo" type="submit">{btn} on WhatsApp</button></div>
<p class="fmsg vmsg" role="status" aria-live="polite"></p>"""

AD = lambda i: "Adult" + ("s" if i > 1 else "")
CH = lambda i: "Child" + ("ren" if i != 1 else "")
INF = lambda i: "Infant" + ("s" if i != 1 else "")
RM = lambda i: "Room" + ("s" if i > 1 else "")

CRUISE_LINES = ["Any cruise line", "Cordelia Cruises", "Royal Caribbean", "Costa Cruises", "MSC Cruises", "Norwegian Cruise Line", "Celebrity Cruises", "Princess Cruises", "Disney Cruise Line", "Resorts World Cruises", "Dream / Genting", "Viking (river cruises)"]
PORTS = ["Mumbai", "Goa", "Kochi", "Chennai", "Singapore", "Dubai", "Abu Dhabi", "Miami / Florida", "Barcelona", "Rome (Civitavecchia)", "Southampton", "Sydney", "Other"]

def flight_widget(root):
    opts = "".join(f'<option value="{c} ({k})">{n}</option>' for c,k,n in AIRPORTS)
    flight = f"""<form class="fform" data-kind="flight" novalidate>
<div class="ftrip" role="radiogroup"><label><input type="radio" name="ftrip" value="One way" checked>One way</label><label><input type="radio" name="ftrip" value="Round trip">Round trip</label><label><input type="radio" name="ftrip" value="Multi-city">Multi-city</label></div>
<div class="fgrid">
<label class="fcell">From<input name="from" list="fapts" required placeholder="Mumbai (BOM)" value="Mumbai (BOM)" autocomplete="off"></label>
<button type="button" class="fswap" aria-label="Swap from and to">⇄</button>
<label class="fcell">To<input name="to" list="fapts" required placeholder="City or airport" autocomplete="off"></label>
<label class="fcell">Departure<input name="depart" type="date" required></label>
<label class="fcell fret">Return<input name="ret" type="date"></label>
<label class="fcell">Travellers &amp; class<span class="fpax">{_sel("adults","Adults",range(1,10),AD)}{_sel("children","Children",range(0,10),CH)}{_sel("infants","Infants",range(0,10),INF)}<select name="cabin" aria-label="Class"><option>Economy</option><option>Premium Economy</option><option>Business</option><option>First</option></select></span></label>
</div>{_contact("Get Flight Quote")}</form>"""
    hotel = f"""<form class="fform" data-kind="hotel" novalidate hidden>
<div class="fgrid fg-h">
<label class="fcell">City, area or hotel name<input name="dest" required maxlength="80" placeholder="e.g. Dubai, Manali, Taj Lands End" list="hcities" autocomplete="off"></label>
<label class="fcell">Check-in<input name="in" type="date" required></label>
<label class="fcell">Check-out<input name="out" type="date" required></label>
<label class="fcell">Rooms &amp; guests<span class="fpax f3">{_sel("rooms","Rooms",range(1,11),RM)}{_sel("adults","Adults",range(1,21),AD)}{_sel("children","Children",range(0,11),CH)}</span></label>
<label class="fcell">Hotel category<select name="cat"><option>Any</option><option>3 Star</option><option>4 Star</option><option>5 Star</option><option>Luxury / Resort</option><option>Villa / Homestay</option></select></label>
</div>{_contact("Get Hotel Quote")}</form>"""
    cruise = f"""<form class="fform" data-kind="cruise" novalidate hidden>
<div class="fgrid fg-c">
<label class="fcell">Cruise line<select name="line">{"".join(f"<option>{x}</option>" for x in CRUISE_LINES)}</select></label>
<label class="fcell">Departure port<select name="port">{"".join(f"<option>{x}</option>" for x in PORTS)}</select></label>
<label class="fcell">Month of travel<input name="month" type="month" required></label>
<label class="fcell">Nights<select name="nights"><option value="2">2–3 nights</option><option value="4">4–5 nights</option><option value="6">6–7 nights</option><option value="8">8–10 nights</option><option value="11">11+ nights</option></select></label>
<label class="fcell">Guests &amp; cabin<span class="fpax f3">{_sel("adults","Adults",range(1,21),AD)}{_sel("children","Children",range(0,11),CH)}<select name="cabin" aria-label="Cabin"><option>Interior</option><option>Ocean view</option><option>Balcony</option><option>Suite</option></select></span></label>
</div>{_contact("Get Cruise Quote")}</form>"""
    hc = "".join(f'<option value="{c}">' for c in ["Dubai","Singapore","Bangkok","Pattaya","Phuket","Bali","Maldives","Kuala Lumpur","London","Paris","Srinagar","Gulmarg","Manali","Shimla","Goa","Jaipur","Udaipur","Munnar","Alleppey","Darjeeling","Gangtok","Port Blair","Havelock","Leh","Lonavala","Mahabaleshwar","Mumbai"])
    return f"""
<div class="fbar" id="flight-search">
<div class="ftabs" role="tablist"><button type="button" class="ftab on" data-k="flight">✈️ Flights</button><button type="button" class="ftab" data-k="hotel">🏨 Hotels</button><button type="button" class="ftab" data-k="cruise">🛳️ Cruise</button></div>
{flight}{hotel}{cruise}
<datalist id="fapts">{opts}</datalist><datalist id="hcities">{hc}</datalist>
<p class="fnote">Tell us what you need – we check all airlines, hotels and cruise lines and reply with the best options on WhatsApp or email. Bookings and tickets issued by The Real Tours and Travels.<br><span class="gstline">GST as applicable: airline &amp; hotel taxes as charged by the supplier (hotel rooms up to ₹7,500/night 5%, above 18%; economy air 5%, premium classes 18%) + 18% GST on our service fee. Overseas tour packages attract 2% TCS.</span></p>
</div>
<script>
(function(){{
const SB="{SB_URL}",KEY="{SB_KEY}";
const notify=(s,t,r)=>{{try{{fetch('https://formsubmit.co/ajax/enquiry@therealtoursandtravels.com',{{method:'POST',headers:{{'Content-Type':'application/json',Accept:'application/json'}},body:JSON.stringify({{_subject:s,message:t,_replyto:r||'',_template:'table',_captcha:'false',source:location.href}})}}).catch(()=>{{}});}}catch(_){{}}}};
const box=document.getElementById('flight-search');
const forms={{}};box.querySelectorAll('form').forEach(x=>forms[x.dataset.kind]=x);
const NOTE={{flight:'Preferred airline, timings, baggage…',hotel:'e.g. sea view, near beach, Jain food, early check-in',cruise:'e.g. dates flexible, senior citizens, Jain food'}};
Object.entries(forms).forEach(([k,x])=>x.notes.placeholder=NOTE[k]);
box.querySelectorAll('.ftab').forEach(t=>t.addEventListener('click',()=>{{box.querySelectorAll('.ftab').forEach(b=>b.classList.toggle('on',b===t));Object.entries(forms).forEach(([k,x])=>x.hidden=k!==t.dataset.k);}}));
const HK={{flights:'flight',flight:'flight',hotels:'hotel',hotel:'hotel',cruise:'cruise'}};function fromHash(){{const k=HK[location.hash.slice(1)];if(!k)return;const t=box.querySelector('.ftab[data-k='+k+']');if(t){{t.click();const y=box.getBoundingClientRect().top+scrollY-(document.querySelector('header.site')?.offsetHeight||0)-12;scrollTo({{top:y,behavior:'smooth'}});}}}}if(location.hash)setTimeout(fromHash,250);addEventListener('hashchange',fromHash);
const today=new Date(Date.now()+330*60000).toISOString().slice(0,10);
const F=forms.flight,H=forms.hotel,C=forms.cruise;
F.depart.min=F.ret.min=H['in'].min=H.out.min=today;C.month.min=today.slice(0,7);
function trip(){{return F.querySelector('input[name=ftrip]:checked').value;}}
function sync(){{const t=trip();F.querySelector('.fret').style.opacity=t==='Round trip'?1:.45;F.ret.required=t==='Round trip';F.notes.placeholder=t==='Multi-city'?'Add other cities & dates, e.g. Dubai → London on 12 Jan':NOTE.flight;}}
F.querySelectorAll('input[name=ftrip]').forEach(r=>r.addEventListener('change',sync));sync();
F.ret.addEventListener('focus',()=>{{if(trip()==='One way'){{F.querySelector('input[value="Round trip"]').checked=true;sync();}}}});
F.depart.addEventListener('change',()=>{{F.ret.min=F.depart.value||today;}});
H['in'].addEventListener('change',()=>{{H.out.min=H['in'].value||today;if(H.out.value&&H.out.value<=H['in'].value)H.out.value='';}});
F.querySelector('.fswap').addEventListener('click',()=>{{const a=F.from.value;F.from.value=F.to.value;F.to.value=a;}});
function uuid(){{return crypto.randomUUID?crypto.randomUUID():'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,c=>{{const r=Math.random()*16|0;return (c=='x'?r:(r&3|8)).toString(16);}});}}
const fd=d=>new Date(d+'T00:00').toLocaleDateString('en-IN',{{day:'numeric',month:'short',year:'numeric'}});
const pl=(n,w,p)=>n+' '+(n==1?w:p);
Object.entries(forms).forEach(([kind,f])=>f.addEventListener('submit',async e=>{{
 e.preventDefault();const msg=f.querySelector('.fmsg');msg.className='fmsg vmsg';
 const c=f.contact.value.trim();const isEmail=/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(c),digits=c.replace(/[^0-9]/g,''),isPhone=!isEmail&&digits.length>=10&&digits.length<=13;
 const id=uuid(),name=f.name.value.trim()||null,notes=f.notes.value.trim()||null;let err='',table,row,ref,lines;
 if(kind==='flight'){{
  const from=f.from.value.trim(),to=f.to.value.trim(),t=trip(),ad=+f.adults.value,ch=+f.children.value,inf=+f.infants.value;
  if(from.length<2||to.length<2)err='Please enter both From and To cities.';
  else if(from.toLowerCase()===to.toLowerCase())err='From and To cannot be the same.';
  else if(!f.depart.value)err='Please choose your departure date.';
  else if(t==='Round trip'&&!f.ret.value)err='Please choose your return date.';
  else if(t==='Round trip'&&f.ret.value<f.depart.value)err='Return date must be after the departure date.';
  else if(inf>ad)err='Each infant must travel with an adult.';
  table='flight_enquiries';ref='FL-'+id.slice(0,6).toUpperCase();
  row={{id,trip_type:t,from_city:from.slice(0,80),to_city:to.slice(0,80),depart_date:f.depart.value||null,return_date:t==='Round trip'?f.ret.value:null,adults:ad,children:ch,infants:inf,cabin:f.cabin.value,full_name:name,notes}};
  lines=['✈️ Flight quote request ('+ref+')',t+': '+from+' → '+to,'Depart: '+(f.depart.value?fd(f.depart.value):''),row.return_date?'Return: '+fd(row.return_date):'',pl(ad,'Adult','Adults')+(ch?', '+pl(ch,'Child','Children'):'')+(inf?', '+pl(inf,'Infant','Infants'):'')+' · '+f.cabin.value];
 }}else if(kind==='hotel'){{
  const dest=f.dest.value.trim(),ci=f['in'].value,co=f.out.value,rooms=+f.rooms.value,ad=+f.adults.value,ch=+f.children.value;
  if(dest.length<2)err='Please enter the city, area or hotel name.';
  else if(!ci||!co)err='Please choose check-in and check-out dates.';
  else if(co<=ci)err='Check-out must be after check-in.';
  else if(rooms>ad)err='Each room needs at least one adult.';
  const nights=ci&&co?Math.round((new Date(co)-new Date(ci))/864e5):null;
  table='booking_enquiries';ref='HT-'+id.slice(0,6).toUpperCase();
  row={{id,kind:'hotel',destination:dest.slice(0,80),start_date:ci||null,end_date:co||null,nights,rooms,adults:ad,children:ch,category:f.cat.value,full_name:name,notes}};
  lines=['🏨 Hotel quote request ('+ref+')','Where: '+dest,ci&&co?'Stay: '+fd(ci)+' → '+fd(co)+' ('+pl(nights,'night','nights')+')':'',pl(rooms,'Room','Rooms')+' · '+pl(ad,'Adult','Adults')+(ch?', '+pl(ch,'Child','Children'):'')+' · '+f.cat.value];
 }}else{{
  const m=f.month.value,ad=+f.adults.value,ch=+f.children.value,nt=f.nights.options[f.nights.selectedIndex].text;
  if(!m)err='Please choose your month of travel.';
  const mon=m?new Date(m+'-01T00:00').toLocaleDateString('en-IN',{{month:'long',year:'numeric'}}):'';
  table='booking_enquiries';ref='CR-'+id.slice(0,6).toUpperCase();
  row={{id,kind:'cruise',destination:('From '+f.port.value).slice(0,80),travel_month:mon||null,nights:+f.nights.value,adults:ad,children:ch,category:f.cabin.value,provider:f.line.value,full_name:name,notes}};
  lines=['🛳️ Cruise quote request ('+ref+')','Cruise line: '+f.line.value,'Departure port: '+f.port.value,'Month: '+mon+' · '+nt,pl(ad,'Adult','Adults')+(ch?', '+pl(ch,'Child','Children'):'')+' · '+f.cabin.value+' cabin'];
 }}
 if(!err&&!isEmail&&!isPhone)err='Please enter a valid 10-digit mobile number or email so we can send your quote.';
 if(err){{msg.textContent=err;msg.classList.add('err');return;}}
 row.phone=isPhone?digits:null;row.email=isEmail?c:null;
 const btn=f.querySelector('.fgo');btn.disabled=true;msg.textContent='Sending your enquiry…';
 let w=null;try{{w=window.open('','_blank');if(w)w.document.write('<p style="font:16px sans-serif;padding:20px">Opening WhatsApp…</p>');}}catch(_){{w=null;}}
 try{{const r=await fetch(SB+'/rest/v1/'+table,{{method:'POST',headers:{{apikey:KEY,Authorization:'Bearer '+(window.RTT_TOKEN||KEY),'Content-Type':'application/json',Prefer:'return=minimal'}},body:JSON.stringify(row)}});if(!r.ok)throw 0;}}
 catch(_){{if(w)w.close();btn.disabled=false;msg.textContent='Sorry, something went wrong. Please WhatsApp us on 98431 21212.';msg.classList.add('err');return;}}
 if(notes)lines.push('Notes: '+notes);if(name)lines.push('Name: '+name);lines.push('Contact: '+c);
 const wa='https://wa.me/919843121212?text='+encodeURIComponent(lines.filter(Boolean).join('\\n'));
 notify('New '+kind+' enquiry '+ref+' – '+(name||c),lines.filter(Boolean).join('\\n'),isEmail?c:'');
 if(w){{try{{w.location.href=wa;}}catch(_){{}}}}
 msg.innerHTML='✅ Enquiry received (Ref <b>'+ref+'</b>). Please press <b>Send</b> in WhatsApp so our team gets it instantly. If WhatsApp did not open: <a class="btn gold" style="margin-top:10px" href="'+wa+'" target="_blank" rel="noopener">💬 Send on WhatsApp</a>';
 msg.classList.add('ok');btn.disabled=false;
}}));
}})();
</script>"""

FLIGHT_CSS = """
.gstline{display:block;margin-top:6px;font-size:12px;color:var(--muted)}
.btabs{display:flex;gap:6px;margin:-4px 0 14px;border-bottom:1px solid var(--line)}
.btab{border:0;background:none;font:600 16px 'Jost',sans-serif;color:var(--muted);padding:8px 16px 12px;cursor:pointer;border-bottom:3px solid transparent;margin-bottom:-1px}
.btab.on{color:var(--crimson);border-bottom-color:var(--red)}
.hgrid{display:grid;grid-template-columns:1.6fr 1fr 1fr 2fr 1.1fr;gap:10px;align-items:end}.hpax{grid-template-columns:repeat(3,1fr)}
.fbar{background:#fff;border:1px solid var(--line);border-radius:22px;padding:22px 24px;box-shadow:0 22px 50px rgba(0,0,0,.08);border-top:5px solid var(--red)}
.ftabs{display:flex;gap:6px;margin-bottom:14px;border-bottom:1px solid var(--line)}.ftab{border:0;background:none;padding:10px 16px;font:600 15.5px 'Jost',sans-serif;color:var(--muted);cursor:pointer;border-bottom:3px solid transparent;margin-bottom:-1px}.ftab.on{color:var(--red);border-bottom-color:var(--red)}
.fform[hidden]{display:none!important}.fgrid.fg-h{grid-template-columns:1.6fr 1fr 1fr 1.8fr 1fr}.fgrid.fg-c{grid-template-columns:1.2fr 1.2fr 1.1fr 1fr 1.6fr}.fpax.f3{grid-template-columns:repeat(3,1fr)}
.ftop{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:14px}.ftop b{font-family:'Playfair Display',serif;font-size:21px;color:var(--wine)}
.ftrip{display:flex;gap:8px;flex-wrap:wrap}.ftrip label{border:1px solid var(--line);border-radius:999px;padding:6px 14px;font-size:14px;cursor:pointer;display:flex;gap:6px;align-items:center}
.ftrip input{accent-color:var(--red)}.ftrip label:has(input:checked){border-color:var(--red);background:#fdf0f0;color:var(--crimson)}
.fform{display:grid;gap:12px}
.fgrid{display:grid;grid-template-columns:1.2fr 36px 1.2fr 1fr 1fr 2fr;gap:10px;align-items:end}
.fgrid2{display:grid;grid-template-columns:1fr 1.2fr 1.4fr auto;gap:10px;align-items:end}
.fcell{display:grid;gap:5px;font-size:12.5px;font-weight:600;letter-spacing:.6px;text-transform:uppercase;color:var(--muted)}
.fcell input,.fcell select{font:500 15.5px 'Jost',sans-serif;text-transform:none;letter-spacing:0;color:var(--ink);padding:11px 12px;border:1px solid var(--line);border-radius:12px;background:#fff;width:100%;min-width:0}
.fcell input:focus,.fcell select:focus{outline:2px solid var(--red);border-color:var(--red)}
.fpax{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}.fpax select{padding:11px 6px;font-size:14px}
.fswap{height:44px;width:36px;border:1px solid var(--line);border-radius:50%;background:#fff;color:var(--red);font-size:18px;cursor:pointer}
.fgo{border:0;cursor:pointer;font-family:inherit;height:46px;white-space:nowrap}.fgo[disabled]{opacity:.6}
.fnote{margin:10px 0 0;font-size:13px;color:var(--muted)}.fmsg:empty{display:none}.fmsg .btn{display:inline-flex}
.fsec{margin-top:-60px;position:relative;z-index:3;padding-top:0}
@media(max-width:1100px){.fgrid{grid-template-columns:1fr 36px 1fr 1fr 1fr}.fgrid .fcell:last-child{grid-column:1/-1}.fgrid.fg-h,.fgrid.fg-c{grid-template-columns:1fr 1fr}.fgrid.fg-h .fcell:first-child,.fgrid.fg-c .fcell:last-child{grid-column:1/-1}.hgrid{grid-template-columns:1fr 1fr}.hgrid .fcell:first-child,.hgrid .fcell:nth-child(4){grid-column:1/-1}.fgrid2{grid-template-columns:1fr 1fr}.fgrid2 .fcell:nth-child(3){grid-column:1/-1}.fgo{grid-column:1/-1}}
@media(max-width:700px){.ftab{padding:10px 10px;font-size:14.5px}.fbar{padding:18px 16px}.fsec{margin-top:-30px}.fgrid,.fgrid.fg-h,.fgrid.fg-c{grid-template-columns:1fr 1fr}.fgrid .fcell{grid-column:auto!important}.fgrid .fswap{display:none}.fgrid .fpax,.fgrid .fcell:has(.fpax){grid-column:1/-1!important}.fgrid.fg-h .fcell:first-child{grid-column:1/-1!important}.fgrid2{grid-template-columns:1fr}.fgrid2 .fcell{grid-column:auto!important}.fpax{grid-template-columns:1fr 1fr}.fpax.f3{grid-template-columns:1fr 1fr 1fr}}
"""
