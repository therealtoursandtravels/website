"""Customize Your Package: trip form -> saves lead -> branded day-by-day itinerary (no prices)."""
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
    opts = "".join(f'<option value="{d}">{d}</option>' for d in DEST) + '<option value="Other">Other – type below</option>'
    return f"""
<section class="hero"><div class="wrap"><div><div class="crumbs"><a href="../">Home</a> › Customize Your Package</div>
<span class="kicker">✨ Smart trip planner</span>
<h1>Customize Your Holiday Package</h1>
<p>Choose your destination, days, travellers, hotel, car and how you want to travel – get an instant day-by-day itinerary from The Real Tours and Travels. Our team will then personalise it for you.</p>
<div class="btns"><a class="btn gold" href="#planner">Start planning</a></div>
</div>{seal("../")}</div></section>

<section class="alt" id="planner"><div class="wrap" style="max-width:860px">
<div class="head"><span class="kicker">Customize your package</span><h2>Tell us about your trip</h2><p class="lead">Takes 30 seconds. We'll create your itinerary instantly.</p></div>
<form id="pform" class="vform" novalidate>
<div class="row"><label>Destination*<select name="destination" required>{opts}</select></label>
<label>Start date<input name="start_date" type="date"></label></div>
<label id="otherwrap" hidden>Which destination?<input name="other" maxlength="60" placeholder="e.g. Coorg, Japan, Kenya"></label>
<div class="row"><label>1) Number of days*<input name="days" type="number" min="2" max="21" value="6" required></label>
<label>2) Number of passengers*<span class="pax"><span><small>Adults</small><input name="adults" type="number" min="1" max="60" value="2" required></span><span><small>Children</small><input name="children" type="number" min="0" max="30" value="0"></span></span></label></div>
<fieldset><legend>3) Hotel category*</legend><div class="chips">
<label><input type="radio" name="hotel" value="3 Star" required>3 Star</label><label><input type="radio" name="hotel" value="4 Star" checked>4 Star</label><label><input type="radio" name="hotel" value="5 Star">5 Star</label><label><input type="radio" name="hotel" value="Luxury / Boutique">Luxury / Boutique</label></div></fieldset>
<fieldset><legend>4) Car</legend><div class="chips">
<label><input type="radio" name="car" value="SUV" checked>🚙 SUV</label><label><input type="radio" name="car" value="Hatchback">🚗 Hatchback</label><label><input type="radio" name="car" value="Sedan">🚘 Sedan</label><label><input type="radio" name="car" value="Tempo Traveller">🚐 Tempo Traveller (groups)</label></div></fieldset>
<fieldset><legend>5) Travel by</legend><div class="chips">
<label><input type="radio" name="mode" value="Flight" checked>✈️ Flight</label><label><input type="radio" name="mode" value="Railway">🚆 Railway</label></div></fieldset>
<div class="row"><label>Your name<input name="full_name" maxlength="120" autocomplete="name"></label>
<label>Mobile or email* <small>(any one – to send your itinerary)</small><input name="contact" required maxlength="160" autocomplete="tel" placeholder="98xxxxxxxx or you@example.com"></label></div>
<label>Special requests<textarea name="notes" rows="2" maxlength="1000" placeholder="e.g. Jain food, senior citizens, honeymoon, wheelchair access"></textarea></label>
<button class="btn gold" type="submit" id="psubmit">✨ Create my itinerary</button>
<p id="pmsg" class="vmsg" role="status" aria-live="polite"></p>
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
const DEST={json.dumps(DEST, ensure_ascii=False)};
const f=document.getElementById('pform'),msg=document.getElementById('pmsg');
f.destination.addEventListener('change',()=>{{document.getElementById('otherwrap').hidden=f.destination.value!=='Other';}});
const esc=s=>String(s).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}})[c]);
function uuid(){{return crypto.randomUUID?crypto.randomUUID():'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,c=>{{const r=Math.random()*16|0;return (c=='x'?r:(r&3|8)).toString(16);}});}}
function fmt(d){{return d.toLocaleDateString('en-IN',{{weekday:'short',day:'numeric',month:'short'}});}}
function hotelLine(h){{return {{'3 Star':'comfortable 3-star hotel','4 Star':'4-star hotel','5 Star':'5-star hotel','Luxury / Boutique':'luxury / boutique property'}}[h]||'hotel';}}
function build(o){{
 const D=DEST[o.dest];const N=o.days;const days=[];
 if(!D){{ // generic plan for other destinations
  for(let i=1;i<=N;i++){{days.push({{t:i==1?'Arrival in '+o.destName:(i==N?'Departure':'Explore '+o.destName),a:i==1?['Arrive and transfer to your hotel','Evening at leisure']:(i==N?['Check out and transfer for your journey home']:['Sightseeing as per your interests – our team will customise this day']),s:i==N?'':o.destName}});}}
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
   if(first){{title='Arrival – '+s[0];a.push('Arrive at '+arrive+'; meet our representative'+(D.nocar?'':' and transfer by private '+o.car));}}
   else if(n===0){{title='Transfer to '+s[0];}}
   const per=alloc[si],st=Math.floor(n*acts.length/per),en=Math.floor((n+1)*acts.length/per);
   const chunk=acts.slice(st,en);
   if(first&&chunk.length){{let c0=chunk[0].replace(/^Arrive[^;]*;\\s*/,'');chunk[0]=c0.charAt(0).toUpperCase()+c0.slice(1);}}
   if(chunk.length)a.push(...chunk);else a.push('Leisure day – relax at the hotel or explore at your own pace');
   days.push({{t:title,a:a,s:s[0]}});}}}});
 days.push({{t:'Departure',a:['Breakfast and check out','Transfer to '+arrive+' for your journey home with beautiful memories'],s:''}});
 return days.slice(0,N);
}}
function render(o,days,ref){{
 const start=o.start?new Date(o.start+'T00:00'):null;
 const rows=days.map((d,i)=>{{const dt=start?' · '+fmt(new Date(start.getTime()+i*864e5)):'';
  return '<div class="iday"><div class="inum">Day '+(i+1)+'</div><div><h4>'+esc(d.t)+'<span>'+dt+'</span></h4><ul>'+d.a.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul>'+(d.s?'<p class="istay">🏨 Overnight: '+esc(d.s)+' – '+hotelLine(o.hotel)+'</p>':'')+'</div></div>';}}).join('');
 const D=DEST[o.dest];const intl=D&&D.intl;
 const travel=o.mode==='Railway'&&D&&!D.rail&&!intl?'Flight (no rail connection)':(intl&&o.mode==='Railway'?'Flight (international)':o.mode);
 return '<div class="ihead"><img src="../img/logo.png" alt="The Real Tours and Travels" width="72" height="72"><div><b>The Real Tours and Travels</b><small>Crafting Journeys Since 1981 · Mulund West, Mumbai</small></div><span class="iref">Ref '+ref+'</span></div>'+
 '<h2 class="ititle">'+esc(o.destName)+' – '+(o.days-1)+' Nights / '+o.days+' Days</h2>'+
 '<div class="ifacts"><span>👥 '+o.adults+' Adult'+(o.adults>1?'s':'')+(o.children?' + '+o.children+' Child'+(o.children>1?'ren':''):'')+'</span><span>🏨 '+esc(o.hotel)+'</span>'+(D&&D.nocar?'':'<span>🚗 '+esc(o.car)+'</span>')+'<span>'+(travel.startsWith('Rail')?'🚆':'✈️')+' '+esc(travel)+'</span>'+(start?'<span>📅 '+fmt(start)+'</span>':'')+'</div>'+
 '<div class="idays">'+rows+'</div>'+
 '<div class="iinc"><div><h4>Package can include</h4><ul><li>'+esc(o.hotel)+' accommodation with breakfast</li><li>Private '+esc(o.car)+' for transfers and sightseeing</li><li>'+(travel.startsWith('Rail')?'Train tickets':'Flight tickets')+' on request</li><li>Visa and travel insurance assistance'+(intl?'':' (if needed)')+'</li><li>Pure veg / Jain meals on request</li></ul></div>'+
 '<div><h4>Next step</h4><p>This is a suggested plan. Our travel expert will call you to personalise it and share the best options for your dates.</p><p><b>📞 {PHONE}</b><br>✉️ {EMAIL}<br>🌐 www.therealtoursandtravels.com<br>📸 @therealtoursandtravels</p></div></div>'+
 '<p class="ifoot">The Real Tours and Travels · {", ".join(ADDR)} · GSTIN {GST} · Sightseeing subject to weather, permits and local conditions.</p>';
}}
f.addEventListener('submit',async e=>{{
 e.preventDefault();msg.className='vmsg';msg.textContent='';
 const d=new FormData(f);const contact=(d.get('contact')||'').trim();
 const isEmail=/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(contact);const digits=contact.replace(/[^0-9]/g,'');
 const isPhone=!isEmail&&digits.length>=10&&digits.length<=13;
 if(!isEmail&&!isPhone){{msg.textContent='Please enter a valid 10-digit mobile number or email address.';msg.classList.add('err');f.contact.focus();return;}}
 let dest=d.get('destination');const other=(d.get('other')||'').trim();
 if(dest==='Other'&&!other){{msg.textContent='Please type the destination you want to visit.';msg.classList.add('err');return;}}
 const o={{dest,destName:dest==='Other'?other:dest,days:Math.min(21,Math.max(2,parseInt(d.get('days'))||6)),adults:Math.max(1,parseInt(d.get('adults'))||1),children:Math.max(0,parseInt(d.get('children'))||0),hotel:d.get('hotel')||'4 Star',car:d.get('car')||'SUV',mode:d.get('mode')||'Flight',start:d.get('start_date')||''}};
 const btn=document.getElementById('psubmit');btn.disabled=true;msg.textContent='✨ Creating your itinerary…';
 const id=uuid(),ref=id.slice(0,8).toUpperCase();
 const row={{id,full_name:(d.get('full_name')||'').trim()||null,phone:isPhone?digits:null,email:isEmail?contact:null,destination:o.destName.slice(0,80),days:o.days,adults:o.adults,children:o.children,hotel_category:o.hotel,car_type:o.car,travel_mode:o.mode,start_date:o.start||null,notes:(d.get('notes')||'').trim()||null}};
 try{{const r=await fetch(SB+'/rest/v1/trip_requests',{{method:'POST',headers:{{apikey:KEY,Authorization:'Bearer '+KEY,'Content-Type':'application/json',Prefer:'return=minimal'}},body:JSON.stringify(row)}});if(!r.ok)throw 0;}}
 catch(_){{btn.disabled=false;msg.textContent='Sorry, something went wrong. Please try again or WhatsApp us on 98431 21212.';msg.classList.add('err');return;}}
 const days=build(o);
 document.getElementById('itin').innerHTML=render(o,days,ref);
 const wa='Hi The Real Tours and Travels, I created an itinerary on your website (Ref '+ref+'): '+o.destName+', '+o.days+' days, '+o.adults+' adults'+(o.children?' + '+o.children+' children':'')+', '+o.hotel+', '+o.car+', '+o.mode+(o.start?', from '+o.start:'')+'. Please share the best price.';
 document.getElementById('wabtn').href='https://wa.me/919843121212?text='+encodeURIComponent(wa);
 const res=document.getElementById('result');res.hidden=false;res.scrollIntoView({{behavior:'smooth'}});
 btn.disabled=false;msg.innerHTML='✅ Your itinerary is ready below (Ref <b>'+ref+'</b>).';msg.classList.add('ok');
}});
}})();
</script>"""

PLANNER_CSS = """
.vform [hidden],[hidden]{display:none!important}
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
