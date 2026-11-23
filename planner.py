"""Customized Packages: trip form -> saves lead -> branded day-by-day itinerary (no prices)."""
import json
from visa import SB_URL, SB_KEY

# Each destination: airport, rail (None = no rail), intl flag, ordered stops: (base, nights_weight, [activity lines])
DEST = {
 "Kashmir": {"air": "Srinagar Airport", "rail": "Jammu Tawi / Katra railway station (then road transfer to Srinagar)", "stops": [
   ("Srinagar", ["Arrive and check in; evening shikara ride on Dal Lake", "Mughal Gardens – Nishat Bagh, Shalimar Bagh and Chashme Shahi", "Local markets of Lal Chowk for Kashmiri handicrafts and dry fruits"]),
   ("Gulmarg", ["Drive to Gulmarg through pine forests", "Gulmarg Gondola cable car ride (Phase 1 & 2, subject to weather)", "Snow activities, sledging and walks in the meadows"]),
   ("Pahalgam", ["Drive to Pahalgam via saffron fields and Awantipora ruins", "Betaab Valley, Aru Valley and Chandanwari", "Leisure walk along the Lidder River"]),
   ("Sonamarg", ["Day excursion to Sonamarg – the 'Meadow of Gold'", "Thajiwas Glacier (pony ride optional)"])]},
 "Himachal (Shimla–Manali)": {"air": "Chandigarh Airport", "rail": "Chandigarh / Kalka railway station", "stops": [
   ("Shimla", ["Drive from Chandigarh to Shimla", "The Ridge, Mall Road and Christ Church", "Excursion to Kufri and Fagu"]),
   ("Manali", ["Scenic drive to Manali via Kullu valley and Beas river", "Hadimba Temple, Vashisht hot springs and Old Manali", "Solang Valley – adventure activities and snow point", "Atal Tunnel and Sissu (subject to permits and weather)"]),
   ("Kullu", ["Kullu shawl factories and river rafting (seasonal)", "Manikaran Sahib on the way back"])]},
 "Kerala": {"air": "Kochi (Cochin) Airport", "rail": "Ernakulam railway station", "stops": [
   ("Kochi", ["Arrive in Kochi; Chinese fishing nets and Fort Kochi walk", "Jew Town, Mattancherry Palace and Kathakali show (evening)"]),
   ("Munnar", ["Drive to Munnar via Cheeyappara and Valara waterfalls", "Eravikulam National Park and tea museum", "Mattupetty Dam, Echo Point and tea gardens"]),
   ("Thekkady", ["Drive to Thekkady – spice plantation tour", "Periyar Lake boat ride and optional elephant interaction"]),
   ("Alleppey", ["Board a private houseboat on the backwaters", "Cruise through villages, paddy fields and canals; overnight on houseboat"]),
   ("Kovalam", ["Beach day at Kovalam", "Excursion to Thiruvananthapuram – Padmanabhaswamy Temple"])]},
 "Goa": {"air": "Goa (Dabolim / Mopa) Airport", "rail": "Madgaon / Thivim railway station", "stops": [
   ("North Goa", ["Arrive and check in; evening at Baga / Calangute", "Fort Aguada, Sinquerim and Candolim beaches", "Anjuna and Vagator, Chapora Fort sunset"]),
   ("Old Goa & Panjim", ["Basilica of Bom Jesus and Se Cathedral", "Fontainhas Latin quarter walk and Mandovi river cruise"]),
   ("South Goa", ["Colva, Benaulim and Palolem beaches", "Cabo de Rama fort and leisure by the sea"])]},
 "Rajasthan": {"air": "Jaipur Airport", "rail": "Jaipur railway station", "stops": [
   ("Jaipur", ["Arrive in the Pink City; evening at Chokhi Dhani (cultural village)", "Amber Fort, Jal Mahal and Hawa Mahal", "City Palace, Jantar Mantar and bazaar shopping"]),
   ("Udaipur", ["Drive / train to Udaipur – City of Lakes", "City Palace and boat ride on Lake Pichola", "Saheliyon ki Bari, Fateh Sagar and Bagore ki Haveli show"]),
   ("Jodhpur", ["Mehrangarh Fort and Jaswant Thada", "Clock Tower market"]),
   ("Jaisalmer", ["Golden Fort and Patwon ki Haveli", "Sam sand dunes – camel safari and desert camp evening"])]},
 "Andaman": {"air": "Port Blair (Sri Vijaya Puram) Airport", "rail": None, "stops": [
   ("Port Blair", ["Arrive; Cellular Jail and Light & Sound show", "Ross Island and North Bay (seasonal)"]),
   ("Havelock (Swaraj Dweep)", ["Ferry to Havelock; Radhanagar Beach sunset", "Elephant Beach – snorkelling and water sports", "Kalapathar Beach and leisure"]),
   ("Neil (Shaheed Dweep)", ["Ferry to Neil Island; Natural Bridge and Laxmanpur Beach", "Bharatpur Beach – glass-bottom boat ride"])]},
 "Darjeeling & Sikkim": {"air": "Bagdogra Airport", "rail": "New Jalpaiguri (NJP) railway station", "stops": [
   ("Gangtok", ["Transfer to Gangtok; MG Marg evening walk", "Tsomgo Lake and Baba Mandir (permits required)", "Rumtek Monastery, Banjhakri Falls and Ganesh Tok"]),
   ("Pelling", ["Drive to Pelling – views of Kanchenjunga", "Pemayangtse Monastery and Khecheopalri Lake"]),
   ("Darjeeling", ["Drive to Darjeeling; Mall Road and tea gardens", "Tiger Hill sunrise, Batasia Loop and Ghoom Monastery", "Toy train joy ride and Himalayan Mountaineering Institute"])]},
 "Ladakh": {"air": "Leh Airport", "rail": None, "stops": [
   ("Leh", ["Arrive in Leh – full day rest to acclimatise", "Shanti Stupa, Leh Palace and local market", "Hall of Fame, Magnetic Hill and Sangam (Indus–Zanskar)"]),
   ("Nubra Valley", ["Drive over Khardung La to Nubra; Diskit Monastery", "Hunder sand dunes – double-hump camel ride"]),
   ("Pangong Lake", ["Drive to Pangong Lake via Shyok; lakeside sunset", "Return to Leh via Chang La"])]},
 "Dubai": {"intl": True, "air": "Dubai International Airport", "stops": [
   ("Dubai", ["Arrive; evening Dhow cruise dinner at Dubai Marina / Creek", "Dubai city tour – Jumeirah, Palm Jumeirah, Dubai Frame and Gold Souk", "Burj Khalifa observation deck and Dubai Mall fountain show", "Desert safari with dune bashing and BBQ dinner (vegetarian options)", "Museum of the Future or Miracle Garden (seasonal) and Global Village (seasonal)", "Theme parks – IMG Worlds, Ferrari World or Warner Bros. World"]),
   ("Abu Dhabi", ["Day trip to Abu Dhabi – Sheikh Zayed Grand Mosque and BAPS Hindu Mandir", "Yas Island attractions"])]},
 "Thailand": {"intl": True, "air": "Bangkok / Phuket Airport", "stops": [
   ("Pattaya", ["Arrive Bangkok; transfer to Pattaya", "Coral Island tour by speedboat with water sports", "Nong Nooch Garden and Alcazar show"]),
   ("Bangkok", ["Bangkok city & temple tour – Golden Buddha and Marble Temple", "Safari World & Marine Park", "Shopping at Pratunam, MBK and Indra market"]),
   ("Phuket / Krabi", ["Phi Phi Island tour by speedboat", "Phuket city tour – Big Buddha, Karon viewpoint and Patong beach"])]},
 "Singapore & Malaysia": {"intl": True, "air": "Singapore Changi Airport", "stops": [
   ("Singapore", ["Arrive; evening Night Safari", "City tour – Merlion Park, Marina Bay and Gardens by the Bay", "Sentosa Island – cable car, S.E.A. Aquarium and Wings of Time", "Universal Studios Singapore"]),
   ("Kuala Lumpur", ["Coach / flight to Kuala Lumpur; Petronas Twin Towers", "Batu Caves and Genting Highlands cable car"])]},
 "Bali": {"intl": True, "air": "Bali (Denpasar) Airport", "stops": [
   ("Kuta / Seminyak", ["Arrive; evening at Kuta beach", "Tanah Lot temple sunset and Uluwatu Kecak dance"]),
   ("Ubud", ["Ubud – Tegallalang rice terraces and Monkey Forest", "Kintamani volcano view and coffee plantation", "Bali swing and waterfalls"]),
   ("Nusa Dua", ["Water sports at Tanjung Benoa", "Leisure day at the beach"])]},
 "Maldives": {"intl": True, "nocar": True, "air": "Malé (Velana) International Airport", "stops": [
   ("Maldives resort", ["Arrive Malé; speedboat / seaplane transfer to your island resort", "Snorkelling on the house reef and leisure", "Sunset cruise with dolphin spotting (optional)", "Spa, water sports or a sandbank picnic (optional)"])]},
 "Vietnam": {"intl": True, "air": "Hanoi / Da Nang Airport", "stops": [
   ("Hanoi", ["Arrive Hanoi; Old Quarter and Hoan Kiem Lake", "Ho Chi Minh Mausoleum complex and Temple of Literature"]),
   ("Ha Long Bay", ["Day / overnight cruise in Ha Long Bay among limestone islands"]),
   ("Da Nang & Hoi An", ["Ba Na Hills and Golden Bridge", "Hoi An ancient town and lantern evening"])]},
 "Europe (Switzerland & Paris)": {"intl": True, "air": "Zurich / Paris Airport", "stops": [
   ("Paris", ["Arrive Paris; Eiffel Tower (2nd level) and Seine river cruise", "Louvre Museum and Champs-Élysées", "Disneyland Paris (optional)"]),
   ("Switzerland", ["Train / coach to Switzerland – Lucerne, Chapel Bridge", "Mount Titlis excursion with rotating cable car", "Interlaken and Jungfraujoch – Top of Europe (optional)", "Zurich city tour"])]},
}

def planner_page(PHONE, PHONE_RAW, EMAIL, WA, seal, cta_band, ADDR, GST):
    # Suggestions only – customers can type ANY place; these just speed up typing.
    sugg = "".join(f'<option value="{d}"></option>' for d in DEST)
    return f"""
<section class="hero"><div class="wrap"><div><div class="crumbs"><a href="../">Home</a> › Customized Packages</div>
<span class="kicker">✨ Smart trip planner</span>
<h1>Customized Holiday Packages</h1>
<p>Tell us any place you want to go – a corner of India or anywhere in the world, one destination or several – plus your days, travellers, hotel, car and how you want to travel. Get an instant day-by-day itinerary from The Real Tours and Travels; our team will then personalise it for you.</p>
<div class="btns"><a class="btn gold" href="#planner">Start planning</a></div>
</div>{seal("../")}</div></section>

<section class="alt" id="planner"><div class="wrap" style="max-width:860px">
<div class="head"><span class="kicker">Customized Packages</span><h2>Tell us about your trip</h2><p class="lead">Takes a minute. We'll create your itinerary instantly.</p></div>
<form id="pform" class="vform" novalidate>
<fieldset><legend>Where do you want to go?*</legend><div class="chips scope">
<label><input type="radio" name="scope" value="Domestic" checked>🇮🇳 Domestic (India)</label><label><input type="radio" name="scope" value="International">🌍 International</label></div></fieldset>
<div class="pfield"><label for="pin">Places you want to visit*</label>
<div class="pbox" id="pbox"><ol class="plist" id="plist"></ol><div class="padd"><input id="pin" list="psug" maxlength="60" autocomplete="off" enterkeyhint="done" placeholder="Type any place and press Enter – e.g. Kutch, Thimphu, Paris"><button type="button" class="btn outline" id="paddbtn">+ Add</button></div></div>
<small class="phint">Any city, state, region or country – in India or abroad. Going to more than one place? Add them in the order you'd like to travel, e.g. Paris → Rome → Barcelona.</small>
<datalist id="psug">{sugg}</datalist>
<div id="pnights" class="pnights" hidden><div class="pnhead"><b>Nights in each place</b><small>Change these and the number of days updates automatically.</small></div><div id="pnrows" class="pnrows"></div></div></div>
<div class="row"><label>Departing from*<input name="origin" maxlength="60" value="Mumbai" required list="porig" autocomplete="off"></label>
<label>1) Number of days*<input name="days" type="number" min="2" max="30" value="6" required></label></div>
<datalist id="porig"><option value="Mumbai"></option><option value="Pune"></option><option value="Ahmedabad"></option><option value="Surat"></option><option value="Nashik"></option><option value="Delhi"></option><option value="Bengaluru"></option><option value="Hyderabad"></option><option value="Chennai"></option><option value="Kolkata"></option><option value="Indore"></option><option value="Nagpur"></option></datalist>
<div class="row"><div class="pdate"><label id="dwrap">Start date<input name="start_date" type="date"></label>
<label id="mwrap" hidden>Month of travel<input name="travel_month" type="month"></label>
<label class="chk psm"><input type="checkbox" name="flexible"><span>Not sure of exact dates? Pick a month instead</span></label></div>
<label>Number of rooms*<input name="rooms" type="number" min="1" max="30" value="1" required></label></div>
<div>
<label>2) Number of passengers*<span class="pax pax3"><span><small>Adults (12+ yrs)</small><input name="adults" type="number" min="1" max="60" value="2" required></span><span><small>Children (2–11 yrs)</small><input name="children" type="number" min="0" max="30" value="0"></span><span><small>Infants (under 2)</small><input name="infants" type="number" min="0" max="20" value="0"></span></span></label>
<div id="cages" class="cages" hidden><small>Age of each child – hotels and airlines price children by age</small><div id="cagesel" class="cagesel"></div></div></div>
<fieldset><legend>Type of trip <small>(choose any that apply)</small></legend><div class="chips">
<label><input type="checkbox" name="ttype" value="Family">👨‍👩‍👧 Family</label><label><input type="checkbox" name="ttype" value="Honeymoon">💑 Honeymoon</label><label><input type="checkbox" name="ttype" value="Senior Citizens">👴 Senior Citizens</label><label><input type="checkbox" name="ttype" value="Group">👥 Group</label><label><input type="checkbox" name="ttype" value="Pilgrimage / Yatra">🛕 Pilgrimage / Yatra</label><label><input type="checkbox" name="ttype" value="Jain food with Maharaj">🍽️ Jain food with Maharaj</label><label><input type="checkbox" name="ttype" value="Adventure">🧗 Adventure</label><label><input type="checkbox" name="ttype" value="Corporate (MICE)">💼 Corporate (MICE)</label></div></fieldset>
<fieldset><legend>3) Hotel category*</legend><div class="chips">
<label><input type="radio" name="hotel" value="3 Star" required>3 Star</label><label><input type="radio" name="hotel" value="4 Star" checked>4 Star</label><label><input type="radio" name="hotel" value="5 Star">5 Star</label><label><input type="radio" name="hotel" value="Luxury / Boutique">Luxury / Boutique</label></div></fieldset>
<fieldset id="carset"><legend>4) Car</legend><div class="chips">
<label><input type="radio" name="car" value="SUV" checked>🚙 SUV</label><label><input type="radio" name="car" value="Hatchback">🚗 Hatchback</label><label><input type="radio" name="car" value="Sedan">🚘 Sedan</label><label><input type="radio" name="car" value="Tempo Traveller">🚐 Tempo Traveller (groups)</label></div></fieldset>
<p id="carintl" class="pnote" hidden><b>4) Transfers</b> – for international trips we arrange transfers as per your itinerary: private car, coach or train, whichever suits each place best.</p>
<fieldset><legend>5) Travel by</legend><div class="chips">
<label><input type="radio" name="mode" value="Flight" checked>✈️ Flight</label><label><input type="radio" name="mode" value="Railway">🚆 Railway</label></div></fieldset>
<label>Budget per person <small>(optional – helps us suggest the right hotels)</small><select name="budget"><option value="">Prefer not to say</option><option>Under ₹25,000</option><option>₹25,000 – ₹50,000</option><option>₹50,000 – ₹1 lakh</option><option>₹1 – 2 lakh</option><option>₹2 – 3 lakh</option><option>Above ₹3 lakh</option></select></label>
<div class="row"><label>Your name<input name="full_name" maxlength="120" autocomplete="name"></label>
<label>Mobile or email* <small>(any one – to send your itinerary)</small><input name="contact" required maxlength="160" autocomplete="tel" placeholder="98xxxxxxxx, +971… or you@example.com"></label></div>
<label>Special requests<textarea name="notes" rows="2" maxlength="1000" placeholder="e.g. wheelchair access, connecting rooms, a birthday on the trip"></textarea></label>
<div class="hp" aria-hidden="true"><label>Leave this empty<input name="company_website" tabindex="-1" autocomplete="off"></label></div>
<button class="btn gold" type="submit" id="psubmit">✨ Create my itinerary</button>
<p id="pmsg" class="vmsg" role="status" aria-live="polite"></p>
<p class="vpriv">🔒 We use your details only to plan your trip and reply to you – never shared or sold. <a href="../privacy-policy/">Privacy Policy</a></p>
</form></div></section>

<section id="result" hidden><div class="wrap" style="max-width:900px">
<div id="itin" class="itin"></div>
<div class="btns no-print" style="justify-content:center;margin-top:24px">
<a class="btn gold" id="wabtn" target="_blank" rel="noopener" href="{WA}">💬 Send to our team on WhatsApp</a>
<button class="btn ghost" type="button" onclick="window.print()">🖨️ Save as PDF / Print</button>
<a class="btn outline" href="#planner">Change details</a></div>
</div></section>
{cta_band()}
<script>
(function(){{
const SB="{SB_URL}",KEY="{SB_KEY}";
const notify=(s,t,r)=>{{try{{fetch('https://formsubmit.co/ajax/enquiry@therealtoursandtravels.com',{{method:'POST',headers:{{'Content-Type':'application/json',Accept:'application/json'}},body:JSON.stringify({{_subject:s,message:t,_replyto:r||'',_template:'table',_captcha:'false',source:location.href}})}}).catch(()=>{{}});}}catch(_){{}}}};
const DEST={json.dumps(DEST, ensure_ascii=False)};
const esc=s=>String(s).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}})[c]);
const f=document.getElementById('pform'),msg=document.getElementById('pmsg');
const scope=()=>f.querySelector('input[name=scope]:checked').value;
f.querySelectorAll('input[name=scope]').forEach(r=>r.addEventListener('change',()=>{{const sc=scope();
 const rail=f.querySelector('input[name=mode][value=Railway]');rail.disabled=sc==='International';rail.closest('label').style.opacity=sc==='International'?.4:1;if(sc==='International')f.querySelector('input[name=mode][value=Flight]').checked=true;
 document.getElementById('carset').hidden=sc==='International';document.getElementById('carintl').hidden=sc!=='International';}}));
// ---- Free-text places (any destination, one or many, in travel order) ----
const places=[],MAXP=10,pin=document.getElementById('pin'),plist=document.getElementById('plist');
const norm=s=>String(s).toLowerCase().replace(/&/g,' and ').replace(/[^a-z0-9]+/g,' ').trim();
const ALIAS={{"Kashmir":["srinagar","jammu and kashmir","gulmarg","pahalgam"],"Himachal (Shimla–Manali)":["himachal","himachal pradesh","shimla","manali","shimla manali","shimla and manali"],"Andaman":["andaman and nicobar","andamans","andaman islands","port blair","havelock"],"Darjeeling & Sikkim":["sikkim","darjeeling","gangtok"],"Ladakh":["leh","leh ladakh"],"Dubai":["uae","dubai and abu dhabi"],"Singapore & Malaysia":["singapore"],"Europe (Switzerland & Paris)":["switzerland and paris","paris and switzerland"]}};
function match(p){{const n=norm(p);for(const k in DEST){{if(norm(k)===n||(ALIAS[k]||[]).includes(n))return k;}}return null;}}
function drawPlaces(){{plist.innerHTML=places.map((p,i)=>'<li><span>'+esc(p)+'</span>'+(places.length>1?'<button type="button" data-mv="'+i+'" aria-label="Move '+esc(p)+' earlier" '+(i?'':'disabled')+'>↑</button>':'')+'<button type="button" data-rm="'+i+'" aria-label="Remove '+esc(p)+'">×</button></li>').join('');
 plist.hidden=!places.length;pin.placeholder=places.length?'Add another place (optional)':'Type any place and press Enter – e.g. Kutch, Thimphu, Paris';syncNights();}}
function addPlace(){{const v=pin.value.replace(/\\s+/g,' ').trim();if(!v)return true;
 if(places.length>=MAXP){{msg.className='vmsg err';msg.textContent='You can add up to '+MAXP+' places – tell us the rest in Special requests.';return false;}}
 if(!places.some(p=>norm(p)===norm(v)))places.push(v.charAt(0).toUpperCase()+v.slice(1));pin.value='';msg.textContent='';drawPlaces();return true;}}
pin.addEventListener('keydown',e=>{{if(e.key==='Enter'){{e.preventDefault();addPlace();}}}});
pin.addEventListener('change',()=>{{if(pin.value&&match(pin.value))addPlace();}}); // picked from suggestions
document.getElementById('paddbtn').addEventListener('click',()=>{{addPlace();pin.focus();}});
plist.addEventListener('click',e=>{{const b=e.target.closest('button');if(!b)return;
 if(b.dataset.rm){{places.splice(+b.dataset.rm,1);}}else if(b.dataset.mv){{const i=+b.dataset.mv;if(i>0)[places[i-1],places[i]]=[places[i],places[i-1]];}}drawPlaces();}});
// ---- Nights in each place (multi-destination) ----
let nEdited=false;const nmap={{}},pnights=document.getElementById('pnights'),pnrows=document.getElementById('pnrows');
function split(){{const tot=Math.max(places.length,(parseInt(f.days.value)||2)-1);places.forEach((p,i)=>nmap[p]=Math.floor(tot/places.length)+(i<tot%places.length?1:0));}}
function setDaysFromNights(){{f.days.value=Math.min(30,places.reduce((a,p)=>a+(nmap[p]||1),0)+1);}}
function syncNights(){{
 if(places.length<2){{pnights.hidden=true;nEdited=false;return;}}
 if(nEdited){{places.forEach(p=>{{if(!(nmap[p]>=1))nmap[p]=1;}});setDaysFromNights();}}else split();
 pnights.hidden=false;
 pnrows.innerHTML=places.map((p,i)=>'<label><span>'+esc(p)+'</span><input type="number" min="1" max="29" data-ni="'+i+'" value="'+nmap[p]+'" aria-label="Nights in '+esc(p)+'"><small>nights</small></label>').join('');}}
pnrows.addEventListener('input',e=>{{const i=e.target.dataset.ni;if(i==null)return;const v=parseInt(e.target.value);if(v>=1){{nmap[places[+i]]=v;nEdited=true;setDaysFromNights();}}}});
f.days.addEventListener('input',()=>{{if(places.length>1){{nEdited=false;split();pnrows.querySelectorAll('input').forEach((x,i)=>x.value=nmap[places[i]]);}}}});
// ---- Child ages ----
const cbox=document.getElementById('cages'),csel=document.getElementById('cagesel');
function drawCAges(){{const n=Math.min(30,Math.max(0,parseInt(f.children.value)||0)),old=[...csel.querySelectorAll('select')].map(x=>x.value);let h='';
 for(let i=0;i<n;i++){{h+='<select data-ca aria-label="Age of child '+(i+1)+'"><option value="">Child '+(i+1)+' age</option>'+[2,3,4,5,6,7,8,9,10,11].map(a=>'<option value="'+a+'"'+(old[i]==String(a)?' selected':'')+'>'+a+' yrs</option>').join('')+'</select>';}}
 csel.innerHTML=h;cbox.hidden=!n;}}
f.children.addEventListener('input',drawCAges);drawCAges();
// ---- Exact date or flexible month ----
const today=new Date(Date.now()+330*60000).toISOString().slice(0,10);f.start_date.min=today;f.travel_month.min=today.slice(0,7);
f.flexible.addEventListener('change',()=>{{document.getElementById('dwrap').hidden=f.flexible.checked;document.getElementById('mwrap').hidden=!f.flexible.checked;}});
drawPlaces();
function uuid(){{return crypto.randomUUID?crypto.randomUUID():'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,c=>{{const r=Math.random()*16|0;return (c=='x'?r:(r&3|8)).toString(16);}});}}
function fmt(d){{return d.toLocaleDateString('en-IN',{{weekday:'short',day:'numeric',month:'short'}});}}
function hotelLine(h){{return {{'3 Star':'comfortable 3-star hotel','4 Star':'4-star hotel','5 Star':'5-star hotel','Luxury / Boutique':'luxury / boutique property'}}[h]||'hotel';}}
function build(o){{
 const D=DEST[o.dest];const N=o.days;const days=[];
 if(!D){{ // any place(s) typed by the customer – one or a multi-stop route in their order
  const P=o.places,nights=N-1;
  const alloc=o.nights&&o.nights.length===P.length?o.nights.slice():P.map((_,i)=>Math.floor(nights/P.length)+(i<nights%P.length?1:0));
  const pool=p=>{{const k=match(p);return k?DEST[k].stops.flatMap(s=>s[1]).map(x=>x.replace(/^Arrive[^;]*;\\s*/,'')).filter(x=>!/^(Arrive|Drive|Transfer|Ferry|Coach|Train|Board|Scenic drive)\\b/.test(x)).map(x=>x.charAt(0).toUpperCase()+x.slice(1)):[];}};
  P.forEach((p,pi)=>{{const acts=pool(p);for(let n=0;n<alloc[pi];n++){{
   let t,a;
   if(days.length===0){{t='Arrival in '+p;a=['Travel from '+o.origin+' and arrive in '+p,'Transfer to your hotel; evening at leisure'];}}
   else if(n===0){{t=P[pi-1]+' → '+p;a=['Check out and travel to '+p+(o.scope==='International'?' – by flight, train or road, whichever connects best':' – by road, train or flight, whichever connects best'),'Check in and explore at your own pace'];}}
   else{{t='Explore '+p;a=acts.length?[acts[(n-1)%acts.length]]:['Sightseeing in '+p+' – our team will plan this day around your interests'];}}
   days.push({{t,a,s:p}});}}}});
  days.push({{t:'Departure from '+P[P.length-1],a:['Breakfast and check out','Transfer for your journey home to '+o.origin+' with beautiful memories'],s:''}});
  return days;
 }}
 const stops=D.stops;const total=stops.reduce((a,s)=>a+s[1].length,0);
 const nights=N-1;let alloc=stops.map(s=>Math.max(1,Math.round(s[1].length/total*nights)));
 while(alloc.reduce((a,b)=>a+b,0)>nights&&alloc.length>1){{const i=alloc.lastIndexOf(Math.max(...alloc));if(alloc[i]>1)alloc[i]--;else{{alloc.pop();}}}}
 let used=stops.slice(0,alloc.length);let sum=alloc.reduce((a,b)=>a+b,0);let k=0;
 while(sum<nights){{alloc[k%alloc.length]++;sum++;k++;}}
 const arrive=o.mode==='Railway'&&D.rail?D.rail:D.air;
 used.forEach((s,si)=>{{const acts=s[1];for(let n=0;n<alloc[si];n++){{
   const first=days.length===0;let title=s[0],a=[];
   if(first){{title='Arrival – '+s[0];a.push('Arrive at '+arrive+'; meet our representative'+(D.nocar?'':(o.car?' and transfer by private '+o.car:' and transfer to your hotel')));}}
   else if(n===0){{title='Transfer to '+s[0];}}
   const per=alloc[si],st=Math.floor(n*acts.length/per),en=Math.floor((n+1)*acts.length/per);
   const chunk=acts.slice(st,en);
   if(first&&chunk.length){{let c0=chunk[0].replace(/^Arrive[^;]*;\\s*/,'');chunk[0]=c0.charAt(0).toUpperCase()+c0.slice(1);}}
   if(chunk.length)a.push(...chunk);else a.push('Leisure day – relax at the hotel or explore at your own pace');
   days.push({{t:title,a:a,s:s[0]}});}}}});
 days.push({{t:'Departure',a:['Breakfast and check out','Transfer to '+arrive+' for your journey home to '+o.origin+' with beautiful memories'],s:''}});
 return days.slice(0,N);
}}
function render(o,days,ref){{
 const start=o.start?new Date(o.start+'T00:00'):null;
 const rows=days.map((d,i)=>{{const dt=start?' · '+fmt(new Date(start.getTime()+i*864e5)):'';
  return '<div class="iday"><div class="inum">Day '+(i+1)+'</div><div><h4>'+esc(d.t)+'<span>'+dt+'</span></h4><ul>'+d.a.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul>'+(d.s?'<p class="istay">🏨 Overnight: '+esc(d.s)+' – '+hotelLine(o.hotel)+'</p>':'')+'</div></div>';}}).join('');
 const D=DEST[o.dest];const intl=(D&&D.intl)||o.scope==='International';
 const travel=o.mode==='Railway'&&D&&!D.rail&&!intl?'Flight (no rail connection)':(intl&&o.mode==='Railway'?'Flight (international)':o.mode);
 return '<div class="ihead"><img src="../img/logo.png" alt="The Real Tours and Travels" width="72" height="72"><div><b>The Real Tours and Travels</b><small>Crafting Journeys Since 1981 · Mulund West, Mumbai</small></div><span class="iref">Ref '+ref+'</span></div>'+
 '<h2 class="ititle">'+esc(o.destName)+' – '+(o.days-1)+' Nights / '+o.days+' Days</h2>'+
 '<div class="ifacts"><span>'+(o.scope==='International'?'🌍':'🇮🇳')+' '+o.scope+'</span><span>👥 '+o.adults+' Adult'+(o.adults>1?'s':'')+(o.children?' + '+o.children+' Child'+(o.children>1?'ren':''):'')+(o.infants?' + '+o.infants+' Infant'+(o.infants>1?'s':''):'')+'</span><span>🏨 '+esc(o.hotel)+'</span>'+'<span>🛫 From '+esc(o.origin)+'</span><span>🛏️ '+o.rooms+' Room'+(o.rooms>1?'s':'')+'</span>'+(D&&D.nocar||!o.car?'':'<span>🚗 '+esc(o.car)+'</span>')+'<span>'+(travel.startsWith('Rail')?'🚆':'✈️')+' '+esc(travel)+'</span>'+(start?'<span>📅 '+fmt(start)+'</span>':(o.month?'<span>📅 '+esc(o.monthTxt)+' (flexible)</span>':''))+(o.types.length?'<span>⭐ '+esc(o.types.join(', '))+'</span>':'')+'</div>'+
 '<div class="idays">'+rows+'</div>'+
 '<div class="iinc"><div><h4>Package can include</h4><ul><li>'+o.rooms+' room'+(o.rooms>1?'s':'')+' in '+esc(o.hotel)+' accommodation with breakfast</li>'+(o.car?'<li>Private '+esc(o.car)+' for transfers and sightseeing</li>':'<li>Transfers and sightseeing as per itinerary</li>')+'<li>'+(travel.startsWith('Rail')?'Train tickets':'Flight tickets')+' on request</li><li>Visa and travel insurance assistance'+(intl?'':' (if needed)')+'</li><li>Pure veg / Jain meals on request</li></ul></div>'+
 '<div><h4>Next step</h4><p>This is a suggested plan. Our travel expert will call you to personalise it and share the best options for your dates.</p><p><b>📞 {PHONE}</b><br>✉️ {EMAIL}<br>🌐 www.therealtoursandtravels.com<br>📸 @therealtoursandtravels</p></div></div>'+
 '<p class="ifoot" style="margin-top:14px">GST as applicable: '+(intl?'5% GST on the package value + 2% TCS on overseas tour packages (adjustable against your income tax)':'5% GST on the tour package value')+'. Final price shared by our team.</p>'+'<p class="ifoot">The Real Tours and Travels · {", ".join(ADDR)} · GSTIN {GST} · Sightseeing subject to weather, permits and local conditions.</p>';
}}
f.addEventListener('submit',async e=>{{
 e.preventDefault();msg.className='vmsg';msg.textContent='';
 if(f.company_website.value){{msg.textContent='✅ Thank you – request received.';msg.classList.add('ok');return;}} // spam trap
 const d=new FormData(f);const contact=(d.get('contact')||'').trim();
 const fail=(t,el)=>{{msg.textContent=t;msg.classList.add('err');if(el)el.focus();}};
 const isEmail=/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(contact);const digits=contact.replace(/[^0-9]/g,'');
 const isPhone=!isEmail&&(contact.startsWith('+')?digits.length>=8&&digits.length<=15:digits.length>=10&&digits.length<=13);
 if(!addPlace())return;
 if(!places.length){{msg.textContent='Please type at least one place you want to visit, then press Enter or + Add.';msg.classList.add('err');pin.focus();return;}}
 const nd=Math.min(30,Math.max(2,parseInt(d.get('days'))||6));
 if(places.length>nd-1){{msg.textContent=places.length+' places need at least '+(places.length+1)+' days (one night in each). Please add days or remove a place.';msg.classList.add('err');f.days.focus();return;}}
 const origin=(d.get('origin')||'').trim();if(origin.length<2)return fail('Please tell us which city you are travelling from.',f.origin);
 const adults=Math.max(1,parseInt(d.get('adults'))||1),rooms=Math.max(1,parseInt(d.get('rooms'))||1);
 if(rooms>adults)return fail('Each room needs at least one adult – please check the number of rooms.',f.rooms);
 const cages=[...csel.querySelectorAll('select')].map(x=>x.value);
 if(cages.some(a=>a===''))return fail('Please choose the age of each child.',csel.querySelector('select'));
 const nightsArr=places.length>1?places.map(p=>nmap[p]||1):null;
 if(nightsArr&&nightsArr.reduce((a,b)=>a+b,0)>29)return fail('A trip can be up to 30 days – please reduce the nights in some places.');
 const flex=!!f.flexible.checked,month=flex?(d.get('travel_month')||''):'';
 if(!isEmail&&!isPhone)return fail('Please enter a valid mobile number (outside India, start with your country code, e.g. +971…) or an email address.',f.contact);
 const one=places.length===1?match(places[0]):null;
 const o={{dest:one,places:places.slice(),destName:places.join(' → '),days:Math.min(30,Math.max(2,parseInt(d.get('days'))||6)),adults:Math.max(1,parseInt(d.get('adults'))||1),children:Math.max(0,parseInt(d.get('children'))||0),infants:Math.max(0,parseInt(d.get('infants'))||0),scope:scope(),hotel:d.get('hotel')||'4 Star',car:scope()==='International'?'':(d.get('car')||'SUV'),mode:d.get('mode')||'Flight',start:flex?'':(d.get('start_date')||''),origin,rooms,childAges:cages,nights:nightsArr,month,monthTxt:month?new Date(month+'-01T00:00').toLocaleDateString('en-IN',{{month:'long',year:'numeric'}}):'',types:d.getAll('ttype'),budget:d.get('budget')||''}};
 const extra=['Departing from: '+o.origin,'Rooms: '+o.rooms,o.childAges.length?'Child ages: '+o.childAges.join(', '):'',o.nights?'Nights: '+o.places.map((p,i)=>p+' '+o.nights[i]).join(', '):'',o.month?'Travel month (flexible): '+o.monthTxt:'',o.types.length?'Trip type: '+o.types.join(', '):'',o.budget?'Budget per person: '+o.budget:'',o.destName.length>80?'Full route: '+o.destName:''].filter(Boolean);
 const btn=document.getElementById('psubmit');btn.disabled=true;msg.textContent='✨ Creating your itinerary…';
 const id=uuid(),ref=id.slice(0,8).toUpperCase();
 const row={{id,full_name:(d.get('full_name')||'').trim()||null,phone:isPhone?digits:null,email:isEmail?contact:null,destination:o.destName.slice(0,80),days:o.days,adults:o.adults,children:o.children,infants:o.infants,trip_scope:o.scope,hotel_category:o.hotel,car_type:o.car||'Transfers as per itinerary',travel_mode:o.mode,start_date:o.start||null,notes:[extra.join('\\n'),(d.get('notes')||'').trim()].filter(Boolean).join('\\n')||null}};
 try{{const r=await fetch(SB+'/rest/v1/trip_requests',{{method:'POST',headers:{{apikey:KEY,Authorization:'Bearer '+(window.RTT_TOKEN||KEY),'Content-Type':'application/json',Prefer:'return=minimal'}},body:JSON.stringify(row)}});if(!r.ok)throw 0;}}
 catch(_){{btn.disabled=false;msg.textContent='Sorry, something went wrong. Please try again or WhatsApp us on 98431 21212.';msg.classList.add('err');return;}}
 const days=build(o);
 document.getElementById('itin').innerHTML=render(o,days,ref);
 const wa='Hi The Real Tours and Travels, I created an itinerary on your website (Ref '+ref+'): '+o.destName+', '+o.days+' days, '+o.adults+' adults'+(o.children?' + '+o.children+' children':'')+(o.infants?' + '+o.infants+' infants':'')+', '+o.scope+', '+o.hotel+(o.car?', '+o.car:'')+', '+o.mode+(o.start?', start '+o.start:'')+'. '+extra.join('; ')+'. Please share the best price.';
 document.getElementById('wabtn').href='https://wa.me/919843121212?text='+encodeURIComponent(wa);
 notify('New itinerary request '+ref+' – '+(row.full_name||contact),wa.replace('Hi The Real Tours and Travels, I created an itinerary on your website ','')+(row.full_name?'\\nName: '+row.full_name:'')+'\\nContact: '+contact+(row.notes?'\\nNotes: '+row.notes:''),isEmail?contact:'');
 const res=document.getElementById('result');res.hidden=false;res.scrollIntoView({{behavior:'smooth'}});
 btn.disabled=false;msg.innerHTML='✅ Your itinerary is ready below (Ref <b>'+ref+'</b>).';msg.classList.add('ok');
}});
}})();
</script>"""

PLANNER_CSS = """
.pax.pax3{grid-template-columns:1fr 1fr 1fr}.chips.scope label{font-size:16px;padding:11px 20px}
@media(max-width:520px){.pax.pax3{grid-template-columns:1fr 1fr 1fr;gap:6px}.pax.pax3 small{font-size:11px}}
.vform [hidden],[hidden]{display:none!important}
.pnights{background:#fdf0f0;border-radius:14px;padding:12px 14px;display:grid;gap:10px}.pnhead{display:flex;flex-wrap:wrap;gap:4px 10px;align-items:baseline}.pnhead b{color:var(--wine)}.pnhead small{color:var(--muted);font-size:13px}
.pnrows{display:flex;flex-wrap:wrap;gap:8px 14px}.pnrows label{display:flex;align-items:center;gap:6px;font-weight:500;background:#fff;border:1px solid var(--line);border-radius:12px;padding:6px 10px}
.pnrows input{width:64px!important;padding:6px 8px!important}.pnrows small{color:var(--muted)}
.pdate{display:grid;gap:8px;align-content:start}.pdate+label{align-self:start}.chk.psm{font-size:13.5px;color:var(--muted)}
.cages{display:grid;gap:6px;margin-top:10px}.cages small{color:var(--muted)}.cagesel{display:flex;flex-wrap:wrap;gap:8px}.cagesel select{width:auto;min-width:130px}
.pnote{margin:0;background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:12px 14px;font-size:14.5px}.pnote b{color:var(--wine)}
.pfield{display:grid;gap:8px}.pfield>label{font-weight:500}.phint{color:var(--muted);font-size:13.5px;line-height:1.45}
.pbox{border:1px solid var(--line);border-radius:14px;background:#fff;padding:8px}.pbox:focus-within{border-color:var(--red)}
.plist{list-style:none;counter-reset:pl;display:flex;flex-wrap:wrap;gap:8px;margin:0 0 8px;padding:0}
.plist li{counter-increment:pl;display:flex;align-items:center;gap:4px;background:#fdf0f0;border:1px solid var(--red);color:var(--crimson);border-radius:999px;padding:5px 6px 5px 12px;font-weight:500}
.plist li::before{content:counter(pl);background:var(--red);color:#fff;border-radius:50%;width:20px;height:20px;display:grid;place-items:center;font-size:12px;margin-right:4px}
.plist li+li{margin-left:14px;position:relative}.plist li+li::after{content:'→';position:absolute;left:-17px;color:var(--muted)}
.plist button{border:0;background:none;color:var(--crimson);font-size:16px;line-height:1;width:26px;height:26px;border-radius:50%;cursor:pointer;padding:0}
.plist button:hover:not(:disabled){background:#fff}.plist button:disabled{opacity:.3;cursor:default}
.padd{display:flex;gap:8px}.padd input{flex:1;min-width:0;border:0!important;box-shadow:none!important;outline:0}.padd .btn{padding:9px 16px;white-space:nowrap}
.vform fieldset{border:0;padding:0;margin:0;display:grid;gap:8px}.vform legend{font-weight:500;font-size:15px;color:var(--wine);margin-bottom:8px}
.chips{display:flex;flex-wrap:wrap;gap:10px}.chips label{display:flex;align-items:center;gap:8px;border:1px solid var(--line);border-radius:999px;padding:9px 16px;cursor:pointer;font-weight:500;background:#fff}
.chips input{accent-color:var(--red);width:auto}.chips label:has(input:checked){border-color:var(--red);background:#fdf0f0;color:var(--crimson)}
.pax{display:grid;grid-template-columns:1fr 1fr;gap:10px}.pax small{display:block;margin-bottom:4px}
.itin{background:#fff;border:1px solid var(--line);border-radius:22px;padding:34px;box-shadow:0 20px 44px rgba(0,0,0,.07);border-top:6px solid var(--red)}
.ihead{display:flex;align-items:center;gap:14px;border-bottom:1px solid var(--line);padding-bottom:16px}
.ihead b{display:block;font-family:'Playfair Display',serif;font-size:22px;color:var(--crimson)}.ihead small{color:var(--muted);font-size:13px;letter-spacing:.5px}
.iref{margin-left:auto;font-size:13px;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 12px;white-space:nowrap}
.ititle{margin:22px 0 12px;font-size:clamp(24px,3.4vw,34px)}
.ifacts{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:22px}.ifacts span{background:var(--bg);border:1px solid var(--line);border-radius:999px;padding:6px 14px;font-size:14px}
.iday{display:grid;grid-template-columns:78px 1fr;gap:16px;padding:16px 0;border-top:1px dashed var(--line)}
.inum{background:var(--red);color:#fff;border-radius:12px;text-align:center;font-weight:600;padding:10px 4px;height:max-content;font-size:14px}
.iday h4{margin:2px 0 6px;font-family:'Playfair Display',serif;font-size:19px;color:var(--wine)}.iday h4 span{font-family:'Jost',sans-serif;font-size:13px;color:var(--muted);font-weight:400}
.iday ul{margin:0;padding-left:18px;color:var(--ink)}.iday li{margin:3px 0}.istay{margin:8px 0 0;font-size:14px;color:var(--muted)}
.iinc{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:20px;background:#fdf0f0;border-radius:16px;padding:22px}
.iinc h4{margin:0 0 8px;font-family:'Playfair Display',serif;font-size:19px;color:var(--crimson)}.iinc ul{margin:0;padding-left:18px}.iinc p{margin:0 0 8px}
.ifoot{font-size:12.5px;color:var(--muted);margin:18px 0 0;text-align:center}
@media(max-width:700px){.itin{padding:20px}.iinc{grid-template-columns:1fr}.iday{grid-template-columns:62px 1fr;gap:12px}.ihead img{width:54px;height:54px}.iref{display:none}}
@media print{.topbar,header.site,footer,.float-wa,.hero,#planner,.band,.no-print{display:none!important}#result{display:block!important;padding:0}.itin{box-shadow:none;border:0;border-top:6px solid #D7191F}body{background:#fff}}
"""
