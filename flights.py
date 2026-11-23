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

def _contact(btn, root=""):
    return f"""<div class="fgrid2">
<label class="fcell">Your name<input name="name" maxlength="120" autocomplete="name"></label>
<label class="fcell">Mobile or email*<input name="contact" required maxlength="160" placeholder="98xxxxxxxx, +971… or you@example.com" autocomplete="tel"></label>
<label class="fcell">Notes<input name="notes" maxlength="200" placeholder=""></label>
<button class="btn gold fgo" type="submit">{btn} on WhatsApp</button></div>
<div class="hp" aria-hidden="true"><label>Leave this empty<input name="company_website" tabindex="-1" autocomplete="off"></label></div>
<p class="fmsg vmsg" role="status" aria-live="polite"></p>
<p class="fpriv">🔒 We use your details only to reply to this enquiry – never shared or sold. <a href="{root}privacy-policy/">Privacy Policy</a></p>"""

AD = lambda i: "Adult" + ("s" if i > 1 else "")
CH = lambda i: "Child" + ("ren" if i != 1 else "")
INF = lambda i: "Infant" + ("s" if i != 1 else "")
RM = lambda i: "Room" + ("s" if i > 1 else "")

CRUISE_LINES = ["Any cruise line", "Cordelia Cruises", "Royal Caribbean", "Costa Cruises", "MSC Cruises", "Norwegian Cruise Line", "Celebrity Cruises", "Princess Cruises", "Disney Cruise Line", "Resorts World Cruises", "Viking (river cruises)", "Other – type below"]
PORTS = ["Mumbai", "Goa", "Kochi", "Chennai", "Singapore", "Dubai", "Abu Dhabi", "Miami / Florida", "Barcelona", "Rome (Civitavecchia)", "Southampton", "Sydney", "Other – type below"]

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
</div>{_contact("Get Flight Quote", root)}</form>"""
    hotel = f"""<form class="fform" data-kind="hotel" novalidate hidden>
<div class="fgrid fg-h">
<label class="fcell">City, area or hotel name<input name="dest" required maxlength="80" placeholder="e.g. Dubai, Manali, Taj Lands End" list="hcities" autocomplete="off"></label>
<label class="fcell">Check-in<input name="in" type="date" required></label>
<label class="fcell">Check-out<input name="out" type="date" required></label>
<label class="fcell">Rooms &amp; guests<span class="fpax f3">{_sel("rooms","Rooms",range(1,11),RM)}{_sel("adults","Adults",range(1,21),AD)}{_sel("children","Children",range(0,11),CH)}</span></label>
<label class="fcell">Hotel category<select name="cat"><option>Any</option><option>3 Star</option><option>4 Star</option><option>5 Star</option><option>Luxury / Resort</option><option>Villa / Homestay</option></select></label>
</div><div class="fages" hidden><span>Age of each child (at check-in)</span><div class="fagesel"></div></div>{_contact("Get Hotel Quote", root)}</form>"""
    cruise = f"""<form class="fform" data-kind="cruise" novalidate hidden>
<div class="fgrid fg-c">
<label class="fcell">Cruise line<select name="line">{"".join(f"<option>{x}</option>" for x in CRUISE_LINES)}</select></label>
<label class="fcell cr-oline" hidden>Which cruise line?<input name="line_other" maxlength="50" placeholder="e.g. Silversea, Oceania" autocomplete="off"></label>
<label class="fcell">Route / destination<input name="route" maxlength="60" placeholder="e.g. Singapore–Penang, Mediterranean, Lakshadweep" autocomplete="off"></label>
<label class="fcell">Departure port<select name="port">{"".join(f"<option>{x}</option>" for x in PORTS)}</select></label>
<label class="fcell cr-oport" hidden>Which port?<input name="port_other" maxlength="40" placeholder="e.g. Visakhapatnam, Venice" autocomplete="off"></label>
<label class="fcell">Nights<select name="nights"><option value="2">2–3 nights</option><option value="4">4–5 nights</option><option value="6">6–7 nights</option><option value="8">8–10 nights</option><option value="11">11+ nights</option></select></label>
</div>
<div class="fgrid fg-c2">
<div class="fcell">When<span class="crwhen"><label><input type="radio" name="when" value="date" checked> Exact sailing date</label><label><input type="radio" name="when" value="month"> Flexible – month</label></span></div>
<label class="fcell cr-date">Sailing date<input name="sail" type="date"></label>
<label class="fcell cr-month" hidden>Month of travel<input name="month" type="month"></label>
<label class="fcell">Guests, cabins &amp; type<span class="fpax">{_sel("adults","Adults",range(1,21),AD)}{_sel("children","Children",range(0,11),CH)}{_sel("cabins","Cabins",range(1,11),lambda i: "Cabin" + ("s" if i > 1 else ""))}<select name="cabin" aria-label="Cabin type"><option>Interior</option><option>Ocean view</option><option>Balcony</option><option>Suite</option></select></span></label>
</div>
<div class="fages" hidden><span>Age of each child (on sailing date)</span><div class="fagesel"></div></div>
<div class="cradd"><span>Also arrange for me:</span><label><input type="checkbox" name="addon" value="Flights to / from the port"> ✈️ Flights to the port</label><label><input type="checkbox" name="addon" value="Hotel before / after the cruise"> 🏨 Hotel before / after</label><label><input type="checkbox" name="addon" value="Visas for the ports of call"> 🛂 Visas</label><label><input type="checkbox" name="addon" value="Travel insurance"> 🛡️ Travel insurance</label><label><input type="checkbox" name="addon" value="Local transport (transfers, port to hotel / airport)"> 🚐 Local transport</label><label><input type="checkbox" name="addon" value="Entry passes / tickets to attractions at the ports"> 🎟️ Attraction entry passes</label><label><input type="checkbox" class="cr-oth"> ➕ Others</label></div>
<div class="cradd crothers" hidden><span>Others:</span><label><input type="checkbox" name="other_addon" value="Shore excursions at the ports"> 🧭 Shore excursions</label><label><input type="checkbox" name="other_addon" value="Onboard packages (drinks / specialty dining / Wi-Fi / spa)"> 🍽️ Onboard packages</label><label><input type="checkbox" name="other_addon" value="Jain / vegetarian meals confirmed with the cruise line"> 🥗 Jain / veg meals</label><label><input type="checkbox" name="other_addon" value="Celebration onboard (birthday / anniversary)"> 🎂 Celebration onboard</label><label><input type="checkbox" name="other_addon" value="Forex / travel card"> 💱 Forex & travel card</label><label><input type="checkbox" name="other_addon" value="International SIM / eSIM"> 📶 International SIM / eSIM</label><label><input type="checkbox" name="other_addon" value="Airport meet & assist (porter / wheelchair)"> 🛬 Airport meet & assist</label><label><input type="checkbox" name="other_addon" value="Special assistance onboard (accessible cabin / medical / seniors)"> ♿ Special assistance onboard</label><label><input type="checkbox" name="other_addon" value="Pre / post-cruise city tour"> 🏙️ Pre/post-cruise city tour</label><label class="fcell crotxt">Anything else? Tell us<input name="other_text" maxlength="150" placeholder="e.g. photographer onboard, kids' club, visa for a stopover country" autocomplete="off"></label></div>
<p class="crpass">🛳️ <b>Sailing abroad?</b> Passports should be valid for at least 6 months after the cruise ends, and a visa may be needed for each country the ship stops in – we will check and arrange them for you.</p>
{_contact("Get Cruise Quote", root)}</form>"""
    hc = "".join(f'<option value="{c}">' for c in ["Dubai","Singapore","Bangkok","Pattaya","Phuket","Bali","Maldives","Kuala Lumpur","London","Paris","Srinagar","Gulmarg","Manali","Shimla","Goa","Jaipur","Udaipur","Munnar","Alleppey","Darjeeling","Gangtok","Port Blair","Havelock","Leh","Lonavala","Mahabaleshwar","Mumbai"])
    return f"""
<div class="fbar" id="flight-search">
<div class="ftabs" role="tablist"><button type="button" class="ftab on" data-k="flight">✈️ Flights</button><button type="button" class="ftab" data-k="hotel">🏨 Hotels</button><button type="button" class="ftab" data-k="cruise">🛳️ Cruise</button></div>
{flight}{hotel}{cruise}
<datalist id="fapts">{opts}</datalist><datalist id="hcities">{hc}</datalist>
<div class="grp"><div><b>👥 Group bookings – 10 or more travellers</b><p>Travelling with a corporate team, wedding party, housing society, college or pilgrimage group? Our group desk arranges dedicated group fares, hotel room blocks and cruise cabin allocations, with one point of contact from enquiry to return.</p></div><div class="grpbtn"><a class="btn gold" href="https://wa.me/919843121212?text=Hello%20The%20Real%20Tours%20and%20Travels%2C%20we%20would%20like%20a%20quotation%20for%20a%20group%20booking.%0AService%20%28flights%20/%20hotel%20/%20cruise%29%3A%20%0AGroup%20size%3A%20%0AFrom%20/%20to%3A%20%0ATravel%20dates%3A%20" target="_blank" rel="noopener">💬 WhatsApp the group desk</a><a class="btn outline" href="tel:+919843121212">📞 +91 98431 21212</a><a class="btn outline" href="mailto:enquiry@therealtoursandtravels.com?subject=Group%20booking%20enquiry">✉️ Email us</a></div></div>
<p class="fnote" data-for="flight">Tell us what you need – we check all airlines and reply with the best options on WhatsApp or email. Tickets issued by The Real Tours and Travels.<br><span class="gstline">GST as applicable: airline taxes as charged by the airline (economy 5%, premium classes 18%) + 18% GST on our service fee.</span></p>
<p class="fnote" data-for="hotel" hidden>Tell us what you need – we check hotels, resorts and villas and reply with the best options on WhatsApp or email. Bookings made by The Real Tours and Travels.<br><span class="gstline">GST as applicable: hotel taxes as charged by the hotel (rooms up to ₹7,500/night 5%, above 18%) + 18% GST on our service fee.</span></p>
<p class="fnote" data-for="cruise" hidden>Tell us what you need – we check all major cruise lines and reply with the best sailings on WhatsApp or email. Bookings made by The Real Tours and Travels.<br><span class="gstline">GST as applicable: taxes and port charges as charged by the cruise line + 18% GST on our service fee. Overseas tour packages attract 2% TCS.</span></p>
</div>
<script>
(function(){{
const SB="{SB_URL}",KEY="{SB_KEY}";
const notify=(s,t,r)=>{{try{{fetch('https://formsubmit.co/ajax/enquiry@therealtoursandtravels.com',{{method:'POST',headers:{{'Content-Type':'application/json',Accept:'application/json'}},body:JSON.stringify({{_subject:s,message:t,_replyto:r||'',_template:'table',_captcha:'false',source:location.href}})}}).catch(()=>{{}});}}catch(_){{}}}};
const box=document.getElementById('flight-search');
const forms={{}};box.querySelectorAll('form').forEach(x=>forms[x.dataset.kind]=x);
const NOTE={{flight:'Preferred airline, timings, baggage…',hotel:'e.g. sea view, near beach, Jain food, early check-in',cruise:'e.g. dates flexible, senior citizens, Jain food'}};
Object.entries(forms).forEach(([k,x])=>x.notes.placeholder=NOTE[k]);
box.querySelectorAll('.ftab').forEach(t=>t.addEventListener('click',()=>{{box.querySelectorAll('.ftab').forEach(b=>b.classList.toggle('on',b===t));Object.entries(forms).forEach(([k,x])=>x.hidden=k!==t.dataset.k);box.querySelectorAll('.fnote[data-for]').forEach(n=>n.hidden=n.dataset.for!==t.dataset.k);}}));
const HK={{flights:'flight',flight:'flight',hotels:'hotel',hotel:'hotel',cruise:'cruise'}};function fromHash(){{const k=HK[location.hash.slice(1)];box.querySelectorAll('.ftab').forEach(b=>b.hidden=!!k&&b.dataset.k!==k);if(!k)return;const t=box.querySelector('.ftab[data-k='+k+']');if(t){{t.click();const y=box.getBoundingClientRect().top+scrollY-(document.querySelector('header.site')?.offsetHeight||0)-12;scrollTo({{top:y,behavior:'smooth'}});}}}}if(location.hash)setTimeout(fromHash,250);addEventListener('hashchange',fromHash);
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
const agesBox=H.querySelector('.fages'),agesSel=H.querySelector('.fagesel');
function drawAges(){{const n=+H.children.value,old=[...agesSel.querySelectorAll('select')].map(x=>x.value);let h='';for(let i=0;i<n;i++){{h+='<select name="child_age" aria-label="Age of child '+(i+1)+'"><option value="">Child '+(i+1)+' age</option>'+[...Array(18).keys()].map(a=>'<option value="'+a+'"'+(old[i]==String(a)?' selected':'')+'>'+(a?a+' yr'+(a>1?'s':''):'Under 1')+'</option>').join('')+'</select>';}}agesSel.innerHTML=h;agesBox.hidden=!n;}}
H.children.addEventListener('change',drawAges);drawAges();
// ---- cruise: Other line/port, exact date or month, child ages ----
const crOL=C.querySelector('.cr-oline'),crOP=C.querySelector('.cr-oport');
C.line.addEventListener('change',()=>{{crOL.hidden=!C.line.value.startsWith('Other');}});C.port.addEventListener('change',()=>{{crOP.hidden=!C.port.value.startsWith('Other');}});
const crWhen=()=>C.querySelector('input[name=when]:checked').value;
C.querySelectorAll('input[name=when]').forEach(r=>r.addEventListener('change',()=>{{C.querySelector('.cr-date').hidden=crWhen()!=='date';C.querySelector('.cr-month').hidden=crWhen()!=='month';}}));
C.sail.min=today;
const crOth=C.querySelector('.cr-oth'),crOthers=C.querySelector('.crothers');crOth.addEventListener('change',()=>{{crOthers.hidden=!crOth.checked;}});
const cAgesBox=C.querySelector('.fages'),cAgesSel=C.querySelector('.fagesel');
function drawCAges(){{const n=+C.children.value,old=[...cAgesSel.querySelectorAll('select')].map(x=>x.value);let h='';const opts=[['u6','Under 6 months'],['6-11m','6–11 months']].concat([...Array(17).keys()].map(a=>[String(a+1),(a+1)+' yr'+(a?'s':'')]));
 for(let i=0;i<n;i++){{h+='<select name="child_age" aria-label="Age of child '+(i+1)+'"><option value="">Child '+(i+1)+' age</option>'+opts.map(([v,t])=>'<option value="'+v+'"'+(old[i]===v?' selected':'')+'>'+t+'</option>').join('')+'</select>';}}
 cAgesSel.innerHTML=h;cAgesBox.hidden=!n;}}
C.children.addEventListener('change',drawCAges);drawCAges();
Object.entries(forms).forEach(([kind,f])=>f.addEventListener('submit',async e=>{{
 e.preventDefault();const msg=f.querySelector('.fmsg');msg.className='fmsg vmsg';
 if(f.company_website.value){{msg.textContent='✅ Thank you – enquiry received.';msg.classList.add('ok');return;}} // spam trap: bots fill hidden field
 const c=f.contact.value.trim();const isEmail=/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(c),digits=c.replace(/[^0-9]/g,''),isPhone=!isEmail&&(c.startsWith('+')?digits.length>=8&&digits.length<=15:digits.length>=10&&digits.length<=13);
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
  const cages=[...f.querySelectorAll('select[name=child_age]')].map(x=>x.value);
  if(!err&&cages.some(a=>a===''))err='Please choose the age of each child – hotels price children by age.';
  const nights=ci&&co?Math.round((new Date(co)-new Date(ci))/864e5):null;
  table='booking_enquiries';ref='HT-'+id.slice(0,6).toUpperCase();
  const agesTxt=ch?'Child ages: '+cages.map(a=>a==='0'?'under 1':a).join(', '):'';
  row={{id,kind:'hotel',destination:dest.slice(0,80),start_date:ci||null,end_date:co||null,nights,rooms,adults:ad,children:ch,category:f.cat.value,full_name:name,notes:[agesTxt,notes].filter(Boolean).join(' | ')||null}};
  lines=['🏨 Hotel quote request ('+ref+')','Where: '+dest,ci&&co?'Stay: '+fd(ci)+' → '+fd(co)+' ('+pl(nights,'night','nights')+')':'',pl(rooms,'Room','Rooms')+' · '+pl(ad,'Adult','Adults')+(ch?', '+pl(ch,'Child','Children'):'')+' · '+f.cat.value,agesTxt];
 }}else{{
  const ad=+f.adults.value,ch=+f.children.value,cab=+f.cabins.value,nt=f.nights.options[f.nights.selectedIndex].text,w=crWhen();
  const line=f.line.value.startsWith('Other')?f.line_other.value.trim():f.line.value,port=f.port.value.startsWith('Other')?f.port_other.value.trim():f.port.value,route=f.route.value.trim();
  const sail=f.sail.value,m=f.month.value,ages=[...f.querySelectorAll('select[name=child_age]')].map(x=>x.value),addons=[...f.querySelectorAll('input[name=addon]:checked')].map(x=>x.value);
  if(crOth.checked){{addons.push(...[...f.querySelectorAll('input[name=other_addon]:checked')].map(x=>x.value));const ot=f.other_text.value.trim();if(ot)addons.push('Other: '+ot);}}
  if(f.line.value.startsWith('Other')&&line.length<2)err='Please type the cruise line you have in mind.';
  else if(f.port.value.startsWith('Other')&&port.length<2)err='Please type the departure port.';
  else if(w==='date'&&!sail)err='Please choose your sailing date – or pick "Flexible – month".';
  else if(w==='date'&&sail<today)err='The sailing date cannot be in the past.';
  else if(w==='month'&&!m)err='Please choose your month of travel.';
  else if(cab>ad)err='Each cabin needs at least one adult.';
  else if(ages.some(a=>a===''))err='Please choose the age of each child – cruise lines price children by age.';
  const mon=m?new Date(m+'-01T00:00').toLocaleDateString('en-IN',{{month:'long',year:'numeric'}}):'';
  const when=w==='date'?(sail?fd(sail):''):mon+' (flexible)';
  const agesTxt=ch?'Child ages: '+ages.map(a=>a==='u6'?'under 6 months':a==='6-11m'?'6–11 months':a).join(', '):'';
  table='booking_enquiries';ref='CR-'+id.slice(0,6).toUpperCase();
  row={{id,kind:'cruise',destination:(route?route+' – from '+port:'From '+port).slice(0,80),travel_month:(w==='date'?sail:mon)||null,nights:+f.nights.value,rooms:cab,adults:ad,children:ch,category:f.cabin.value,provider:line.slice(0,60),full_name:name,
   notes:[agesTxt,addons.length?'Also arrange: '+addons.join(', '):'',notes].filter(Boolean).join(' | ').slice(0,1000)||null}};
  lines=['🛳️ Cruise quote request ('+ref+')','Cruise line: '+line,route?'Route: '+route:'','Departure port: '+port,'When: '+when+' · '+nt,pl(ad,'Adult','Adults')+(ch?', '+pl(ch,'Child','Children'):'')+' · '+pl(cab,'cabin','cabins')+' · '+f.cabin.value,agesTxt,addons.length?'Also arrange: '+addons.join(', '):''];
 }}
 if(!err&&!isEmail&&!isPhone)err='Please enter a valid mobile number (outside India, start with your country code, e.g. +971…) or an email so we can send your quote.';
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
.grp{display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center;justify-content:space-between;margin-top:14px;padding:16px 18px;border:1px solid var(--line);border-left:4px solid var(--red);border-radius:14px;background:var(--bg)}
.grp>div:first-child{flex:1 1 360px}.grp b{color:var(--wine);font-size:16px}.grp p{margin:4px 0 0;font-size:14px;color:var(--ink)}
.grpbtn{display:flex;flex-wrap:wrap;gap:8px}.grpbtn .btn{padding:9px 16px;font-size:14.5px;white-space:nowrap}
.fgrid.fg-c,.fgrid.fg-c2{grid-template-columns:repeat(auto-fit,minmax(180px,1fr))!important}.fgrid.fg-c2 .fcell:has(.fpax){grid-column:span 2}.crwhen label{white-space:nowrap}.crwhen{display:flex;flex-wrap:wrap;gap:6px 14px;text-transform:none;letter-spacing:0;font:500 14.5px 'Jost',sans-serif;color:var(--ink);padding:11px 0}.crwhen label{display:flex;gap:6px;align-items:center}.crwhen input{accent-color:var(--red)}
.cradd{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;font-size:14.5px}.cradd>span{font-size:12.5px;font-weight:600;letter-spacing:.6px;text-transform:uppercase;color:var(--muted)}.cradd label{display:flex;gap:6px;align-items:center;cursor:pointer}.cradd input{accent-color:var(--red)}
.crothers{padding:10px 14px;background:var(--bg);border:1px solid var(--line);border-radius:12px}.crotxt{flex:1 1 100%}
.crpass{margin:0;background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:10px 14px;font-size:13.5px}.fcell[hidden]{display:none!important}
.hp{position:absolute!important;left:-10000px!important;top:auto;width:1px;height:1px;overflow:hidden}
.fpriv,.vpriv{margin:2px 0 0;font-size:12.5px;color:var(--muted)}.fpriv a,.vpriv a{color:var(--crimson)}
.fages{display:flex;flex-wrap:wrap;align-items:center;gap:8px;font-size:12.5px;font-weight:600;letter-spacing:.6px;text-transform:uppercase;color:var(--muted)}
.fagesel{display:flex;flex-wrap:wrap;gap:6px}.fagesel select{font:500 14.5px 'Jost',sans-serif;padding:9px 10px;border:1px solid var(--line);border-radius:12px;background:#fff;color:var(--ink)}
.gstline{display:block;margin-top:6px;font-size:12px;color:var(--muted)}
.btabs{display:flex;gap:6px;margin:-4px 0 14px;border-bottom:1px solid var(--line)}
.btab{border:0;background:none;font:600 16px 'Jost',sans-serif;color:var(--muted);padding:8px 16px 12px;cursor:pointer;border-bottom:3px solid transparent;margin-bottom:-1px}
.btab.on{color:var(--crimson);border-bottom-color:var(--red)}
.hgrid{display:grid;grid-template-columns:1.6fr 1fr 1fr 2fr 1.1fr;gap:10px;align-items:end}.hpax{grid-template-columns:repeat(3,1fr)}
.fbar{background:#fff;border:1px solid var(--line);border-radius:22px;padding:22px 24px;box-shadow:0 22px 50px rgba(0,0,0,.08);border-top:5px solid var(--red)}
.ftabs{display:flex;gap:6px;margin-bottom:14px;border-bottom:1px solid var(--line)}.ftab{border:0;background:none;padding:10px 16px;font:600 15.5px 'Jost',sans-serif;color:var(--muted);cursor:pointer;border-bottom:3px solid transparent;margin-bottom:-1px}.ftab.on{color:var(--red);border-bottom-color:var(--red)}.ftab[hidden]{display:none}
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
