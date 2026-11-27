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
 ("Agartala","IXA","Maharaja Bir Bikram"),("Imphal","IMF","Bir Tikendrajit Intl"),("Dibrugarh","DIB","Dibrugarh"),("Silchar","IXS","Silchar"),
 ("Tirupati","TIR","Tirupati"),("Vijayawada","VGA","Vijayawada"),("Rajahmundry","RJA","Rajahmundry"),("Belagavi","IXG","Belagavi"),("Hubballi","HBX","Hubballi"),
 ("Kannur","CNN","Kannur Intl"),("Tiruchirappalli","TRZ","Tiruchirappalli Intl"),("Kolhapur","KLH","Kolhapur"),("Shirdi","SAG","Shirdi"),("Jabalpur","JLR","Jabalpur"),
 ("Gwalior","GWL","Rajmata Vijaya Raje Scindia"),("Prayagraj","IXD","Prayagraj"),("Gorakhpur","GOP","Gorakhpur"),("Darbhanga","DBR","Darbhanga"),
 ("Kullu Manali","KUU","Bhuntar"),("Dharamshala","DHM","Kangra Gaggal"),("Jaisalmer","JSA","Jaisalmer"),("Bikaner","BKB","Nal"),("Jamnagar","JGA","Jamnagar"),
 ("Bhuj","BHJ","Bhuj"),("Porbandar","PBD","Porbandar"),("Diu","DIU","Diu"),("Mysuru","MYQ","Mysuru"),("Puducherry","PNY","Puducherry"),("Thoothukudi","TCR","Tuticorin"),
 ("Agatti (Lakshadweep)","AGX","Agatti"),
 ("Ras Al Khaimah","RKT","Ras Al Khaimah Intl"),("Dammam","DMM","King Fahd Intl"),("Medina","MED","Prince Mohammad bin Abdulaziz"),("Salalah","SLL","Salalah"),
 ("Amman","AMM","Queen Alia Intl"),("Tel Aviv","TLV","Ben Gurion"),("Cairo","CAI","Cairo Intl"),("Baku","GYD","Heydar Aliyev Intl"),("Almaty","ALA","Almaty Intl"),
 ("Tashkent","TAS","Islam Karimov Tashkent Intl"),("Tbilisi","TBS","Tbilisi Intl"),("Yerevan","EVN","Zvartnots Intl"),("Dhaka","DAC","Hazrat Shahjalal Intl"),
 ("Paro","PBH","Paro Intl"),("Yangon","RGN","Yangon Intl"),("Krabi","KBV","Krabi Intl"),("Chiang Mai","CNX","Chiang Mai Intl"),("Bangkok (Don Mueang)","DMK","Don Mueang Intl"),
 ("Penang","PEN","Penang Intl"),("Langkawi","LGK","Langkawi Intl"),("Jakarta","CGK","Soekarno-Hatta Intl"),("Manila","MNL","Ninoy Aquino Intl"),("Taipei","TPE","Taoyuan Intl"),
 ("Shanghai","PVG","Pudong Intl"),("Beijing","PEK","Capital Intl"),("Guangzhou","CAN","Baiyun Intl"),("Osaka","KIX","Kansai Intl"),("Perth","PER","Perth"),
 ("Brisbane","BNE","Brisbane"),("Gold Coast","OOL","Gold Coast"),("Cairns","CNS","Cairns"),("Christchurch","CHC","Christchurch"),("Queenstown","ZQN","Queenstown"),
 ("Seychelles","SEZ","Seychelles Intl"),("Zanzibar","ZNZ","Abeid Amani Karume Intl"),("Dar es Salaam","DAR","Julius Nyerere Intl"),("Mombasa","MBA","Moi Intl"),
 ("Cape Town","CPT","Cape Town Intl"),("London (Gatwick)","LGW","Gatwick"),("Manchester","MAN","Manchester"),("Edinburgh","EDI","Edinburgh"),("Birmingham","BHX","Birmingham"),
 ("Dublin","DUB","Dublin"),("Munich","MUC","Munich"),("Geneva","GVA","Geneva"),("Milan","MXP","Malpensa"),("Venice","VCE","Marco Polo"),("Barcelona","BCN","El Prat"),
 ("Madrid","MAD","Barajas"),("Lisbon","LIS","Humberto Delgado"),("Athens","ATH","Athens Intl"),("Prague","PRG","Vaclav Havel"),("Budapest","BUD","Ferenc Liszt Intl"),
 ("Brussels","BRU","Brussels"),("Copenhagen","CPH","Kastrup"),("Stockholm","ARN","Arlanda"),("Helsinki","HEL","Helsinki-Vantaa"),("Oslo","OSL","Gardermoen"),
 ("Los Angeles","LAX","Los Angeles Intl"),("Washington DC","IAD","Dulles Intl"),("Boston","BOS","Logan Intl"),("Dallas","DFW","Dallas Fort Worth Intl"),
 ("Houston","IAH","George Bush Intercontinental"),("Atlanta","ATL","Hartsfield-Jackson Atlanta Intl"),("Seattle","SEA","Seattle-Tacoma Intl"),
 ("Montreal","YUL","Montreal-Trudeau Intl"),("Calgary","YYC","Calgary Intl"),
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

FSEARCH_JS = r"""
// ---- airport picker: type a city, airport name or 3-letter code ----
(function(){
const box=document.getElementById('flight-search');if(!box)return;
const AP=[...document.querySelectorAll('#fapts option')].map(o=>{const m=o.value.match(/^(.*) \(([A-Z]{3})\)$/);return m?{v:o.value,city:m[1],code:m[2],name:o.textContent}:null;}).filter(Boolean);
const norm=t=>(t||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').trim();
const esc=t=>String(t).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function find(q){q=norm(q).replace(/\s*\([a-z]{3}\)\s*$/,'');if(!q)return AP.slice(0,8);
 const out=[];for(const a of AP){const c=a.code.toLowerCase(),ci=norm(a.city),n=norm(a.name);let s=-1;
  if(c===q)s=0;else if(ci.startsWith(q))s=1;else if(q.length<=3&&c.startsWith(q))s=2;else if(ci.split(/[\s(]+/).some(w=>w.startsWith(q)))s=3;else if(n.includes(q))s=4;else if(ci.includes(q))s=5;
  if(s>=0)out.push([s,a]);}
 out.sort((x,y)=>x[0]-y[0]);const r=out.slice(0,8).map(x=>x[1]);
 if(/^[a-z]{3}$/.test(q)&&!r.length)r.push({v:q.toUpperCase(),city:'Airport code '+q.toUpperCase(),code:q.toUpperCase(),name:'Search this airport code',raw:1});
 return r;}
const isAp=t=>t&&t.matches&&t.matches('form[data-kind=flight] input[name=from],form[data-kind=flight] input[name=to],form[data-kind=flight] input[data-l=from],form[data-kind=flight] input[data-l=to]');
let dd=null,cur=null,idx=-1,items=[];
function close(){if(dd){dd.remove();}dd=null;cur=null;idx=-1;items=[];}
function hl(i){idx=i;if(!dd)return;[...dd.children].forEach((b,j)=>b.classList.toggle('on',j===i));const b=dd.children[i];if(b)b.scrollIntoView({block:'nearest'});}
function pick(inp,a){inp.value=a.v;inp.dispatchEvent(new Event('input',{bubbles:true}));inp.dispatchEvent(new Event('change',{bubbles:true}));close();}
function open(inp){const list=find(inp.value);if(dd&&cur!==inp)close();if(!list.length){close();return;}
 if(!dd){dd=document.createElement('div');dd.className='fac';dd.setAttribute('role','listbox');dd.addEventListener('mousedown',e=>e.preventDefault());(inp.closest('.fcell')||inp.parentNode).appendChild(dd);}
 cur=inp;items=list;
 dd.innerHTML=list.map(a=>'<button type="button" role="option" tabindex="-1"><span class="facm"><b>'+esc(a.city)+'</b><small>'+esc(a.name)+'</small></span><span class="facc">'+esc(a.code)+'</span></button>').join('');
 [...dd.children].forEach((b,j)=>b.addEventListener('click',()=>pick(inp,items[j])));hl(norm(inp.value)?0:-1);}
// on leaving the field, turn "bom" or "mumbai" into "Mumbai (BOM)"
function settle(inp){const q=norm(inp.value);if(!q||/\([a-z]{3}\)$/.test(q))return;const a=AP.find(x=>x.code.toLowerCase()===q)||AP.find(x=>norm(x.city)===q);if(a&&a.v!==inp.value){inp.value=a.v;inp.dispatchEvent(new Event('input',{bubbles:true}));inp.dispatchEvent(new Event('change',{bubbles:true}));}}
box.addEventListener('input',e=>{if(isAp(e.target)&&e.isTrusted)open(e.target);});
box.addEventListener('focusin',e=>{if(isAp(e.target)){open(e.target);try{e.target.select();}catch(_){}}});
box.addEventListener('focusout',e=>{if(isAp(e.target)){const t=e.target;setTimeout(()=>{if(document.activeElement!==t){if(cur===t)close();settle(t);}},120);}});
box.addEventListener('keydown',e=>{if(!isAp(e.target)||!dd||cur!==e.target)return;
 if(e.key==='ArrowDown'){e.preventDefault();hl(Math.min(items.length-1,idx+1));}
 else if(e.key==='ArrowUp'){e.preventDefault();hl(Math.max(0,idx-1));}
 else if(e.key==='Enter'||e.key==='Tab'){if(idx>=0&&items[idx]){if(e.key==='Enter')e.preventDefault();pick(e.target,items[idx]);}}
 else if(e.key==='Escape'){close();}});
document.addEventListener('click',e=>{if(dd&&!dd.contains(e.target)&&e.target!==cur)close();});
})();
(function(){
const F=document.querySelector('#flight-search form[data-kind=flight]');if(!F)return;
const SB='__SB__',KEY='__KEY__';
const AL={AI:'Air India',IX:'Air India Express','6E':'IndiGo',SG:'SpiceJet',QP:'Akasa Air',UK:'Vistara',I5:'AIX Connect','9I':'Alliance Air',S5:'Star Air',EK:'Emirates',EY:'Etihad Airways',QR:'Qatar Airways',FZ:'flydubai',G9:'Air Arabia',WY:'Oman Air',GF:'Gulf Air',KU:'Kuwait Airways',SV:'Saudia',XY:'flynas',J9:'Jazeera Airways',SQ:'Singapore Airlines',TR:'Scoot',TG:'Thai Airways',FD:'Thai AirAsia',AK:'AirAsia',D7:'AirAsia X',MH:'Malaysia Airlines',OD:'Batik Air',VN:'Vietnam Airlines',VJ:'VietJet Air',GA:'Garuda Indonesia',CX:'Cathay Pacific',UL:'SriLankan Airlines',KB:'Druk Air',RA:'Nepal Airlines',BG:'Biman',MU:'China Eastern',CA:'Air China',CZ:'China Southern',JL:'Japan Airlines',NH:'ANA',KE:'Korean Air',OZ:'Asiana',QF:'Qantas',VA:'Virgin Australia',NZ:'Air New Zealand',BA:'British Airways',VS:'Virgin Atlantic',LH:'Lufthansa',LX:'SWISS',OS:'Austrian',AF:'Air France',KL:'KLM',AZ:'ITA Airways',IB:'Iberia',TK:'Turkish Airlines',PC:'Pegasus',SU:'Aeroflot',AA:'American Airlines',UA:'United Airlines',DL:'Delta',AC:'Air Canada',ET:'Ethiopian Airlines',KQ:'Kenya Airways',MS:'EgyptAir',SA:'South African Airways',MK:'Air Mauritius',HY:'Uzbekistan Airways',KC:'Air Astana',J2:'Azerbaijan Airlines',LO:'LOT',SK:'SAS',AY:'Finnair',EI:'Aer Lingus',TP:'TAP Portugal'};
const an=c=>AL[c]||c;
const box=F.querySelector('.fres'),btn=F.querySelector('.fshow'),bar=btn.closest('.fsr');
if(bar.hidden){fetch(SB+'/functions/v1/flight-search',{headers:{apikey:KEY,Authorization:'Bearer '+KEY}}).then(r=>r.ok?r.json():{}).then(j=>{if(j.ready)bar.hidden=false;}).catch(()=>{});}
let legs=[],sel=[],src='';
const BAGS=['No extra baggage','+5 kg per person','+10 kg per person','+15 kg per person','+20 kg per person','+25 kg per person','+30 kg per person','1 extra bag (23 kg) per person'];
const code=v=>{v=(v||'').trim();const m=v.match(/\(([A-Za-z]{3})\)\s*$/);if(m)return m[1].toUpperCase();if(/^[A-Za-z]{3}$/.test(v))return v.toUpperCase();const o=[...document.querySelectorAll('#fapts option')].find(o=>o.textContent.toLowerCase()===v.toLowerCase()||o.value.toLowerCase().startsWith(v.toLowerCase()+' ('));return o?(o.value.match(/\(([A-Z]{3})\)/)||[])[1]:'';};
const tm=s=>s.slice(11,16);
const hr=s=>+s.slice(11,13);
const dd=s=>{const d=new Date(s.slice(0,10)+'T00:00');return d.toLocaleDateString('en-IN',{day:'numeric',month:'short'});};
const plus=(a,b)=>{const n=Math.round((new Date(b.slice(0,10))-new Date(a.slice(0,10)))/864e5);return n>0?'<sup>+'+n+'</sup>':'';};
const esc=t=>String(t==null?'':t).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const pl=(n,w,p)=>n+' '+(n==1?w:p);
const CAB={'Economy':'ECONOMY','Premium Economy':'PREMIUM_ECONOMY','Business':'BUSINESS','First':'FIRST'};
const nm=f=>AL[f.airline]||f.airline_name||f.airline;
const inr=n=>'₹'+Math.round(n).toLocaleString('en-IN');
const fareTxt=o=>o&&o.fare&&o.fare.total?(o.fare.currency==='INR'?inr(o.fare.total):o.fare.currency+' '+Math.round(o.fare.total).toLocaleString('en-IN')):'';
const hasFares=()=>legs.some(l=>l.some(o=>o.fare&&o.fare.total));
const bagTxt=b=>b.baggage||(src==='timetable'?'Baggage allowance confirmed in your quote':'Check-in baggage: we will confirm');
function boundHtml(b,label){const f0=b.flights[0],fl=b.flights[b.flights.length-1];const names=[...new Set(b.flights.map(nm))];
 return '<div class="fob">'+(label?'<span class="fobl">'+label+'</span>':'')+'<div class="foa"><b>'+esc(names.join(' + '))+'</b><small>'+esc(b.flights.map(x=>x.number).join(', '))+'</small></div>'+
 '<div class="fot"><b>'+tm(f0.departs)+'</b><small>'+esc(f0.from)+(f0.from_terminal?' · T'+esc(f0.from_terminal):'')+'</small></div><div class="fod"><small>'+esc(b.total||'&nbsp;')+'</small><i></i><small>'+(b.stops?b.stops+' stop'+(b.stops>1?'s':'')+' · '+esc(b.via.join(', ')):'Non-stop')+'</small></div><div class="fot"><b>'+tm(fl.arrives)+plus(f0.departs,fl.arrives)+'</b><small>'+esc(fl.to)+(fl.to_terminal?' · T'+esc(fl.to_terminal):'')+'</small></div>'+
 '<div class="fobag">🧳 '+esc(bagTxt(b))+'<br><span>👜 Cabin bag as per airline</span></div></div>';}
function summary(o,label){return o.bounds.map((b,i)=>{const f0=b.flights[0],fl=b.flights[b.flights.length-1];return (label||(o.bounds.length>1?(i?'Return':'Onward'):''))+(label||o.bounds.length>1?': ':'')+[...new Set(b.flights.map(nm))].join(' + ')+' '+b.flights.map(x=>x.number).join(', ')+' · '+f0.from+' '+dd(f0.departs)+' '+tm(f0.departs)+' → '+fl.to+' '+tm(fl.arrives)+(dd(fl.arrives)!==dd(f0.departs)?' ('+dd(fl.arrives)+')':'')+' · '+(b.stops?b.stops+' stop'+(b.stops>1?'s':'')+' via '+b.via.join(', '):'non-stop')+(b.total?' · '+b.total:'')+(b.baggage?' · Included: '+b.baggage:'')+(i===0&&fareTxt(o)?' · Fare seen online: '+fareTxt(o)+' (approx.)':'');});}
const FL=[['early','🌅','Early morning','Before 6 am',h=>h<6],['morning','☀️','Morning','6 am – 12 pm',h=>h>=6&&h<12],['afternoon','🌤️','Afternoon','12 pm – 6 pm',h=>h>=12&&h<18],['night','🌙','Evening & night','After 6 pm',h=>h>=18]];
const SORTS=[['price','Cheapest first'],['dep','Earliest departure'],['late','Latest departure'],['dur','Shortest duration'],['arr','Earliest arrival']];
let st=[];// per leg: {t:Set, a:Set, sort, n}
const dep0=o=>o.bounds[0].flights[0].departs,arrL=o=>{const b=o.bounds[0];return b.flights[b.flights.length-1].arrives;};
const mins=o=>o.bounds.reduce((s,b)=>s+(b.total_min||0),0);
const pass=(o,s)=>{const h=hr(dep0(o));if(s.t.size&&!FL.some(f=>s.t.has(f[0])&&f[4](h)))return false;if(s.a.size&&!s.a.has(o.bounds[0].flights[0].airline))return false;return true;};
const srt=(a,b,k)=>k==='price'?((a.fare&&a.fare.total||1e12)-(b.fare&&b.fare.total||1e12))||dep0(a).localeCompare(dep0(b)):k==='late'?dep0(b).localeCompare(dep0(a)):k==='dur'?(mins(a)-mins(b))||dep0(a).localeCompare(dep0(b)):k==='arr'?arrL(a).localeCompare(arrL(b)):dep0(a).localeCompare(dep0(b));
function legLabel(i){return legs.length>1?(i?'Return flight':'Onward flight'):'';}
const DAYS=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],MONS=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const longd=s=>{const d=new Date(s.slice(0,10)+'T00:00');return DAYS[d.getDay()]+', '+d.getDate()+' '+MONS[d.getMonth()];};
function logo(c,name){return '<span class="flogo"><em>'+esc(c)+'</em><img src="https://pics.avs.io/96/96/'+encodeURIComponent(c)+'.png" alt="" loading="lazy" onerror="this.remove()"></span>';}
function card(o,i,k){const b=o.bounds[0],f0=b.flights[0],fl=b.flights[b.flights.length-1],name=[...new Set(b.flights.map(nm))].join(' + '),on=sel[i]===k;
 const leg=x=>{const a=x.flights[0],z=x.flights[x.flights.length-1];return '<div class="fotimes"><div class="fot"><b>'+tm(a.departs)+'</b><small>'+esc(a.from)+(a.from_terminal?' · T'+esc(a.from_terminal):'')+'</small></div><div class="fod"><small>'+esc(x.total||'')+'</small><span class="fline"><i></i><svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z" transform="rotate(90 12 12)"/></svg></span><small class="'+(x.stops?'fstop':'fns')+'">'+(x.stops?x.stops+' stop'+(x.stops>1?'s':'')+' · '+esc(x.via.join(', ')):'Non-stop')+'</small></div><div class="fot r"><b>'+tm(z.arrives)+plus(a.departs,z.arrives)+'</b><small>'+esc(z.to)+(z.to_terminal?' · T'+esc(z.to_terminal):'')+'</small></div></div>';};
 return '<label class="fo'+(on?' on':'')+'"><input type="radio" name="fpick'+i+'" value="'+k+'"'+(on?' checked':'')+'>'+
  '<div class="foal">'+logo(f0.airline,name)+'<div><b>'+esc(name)+'</b><small>'+esc(b.flights.map(x=>x.number).join(' · '))+(f0.aircraft?' · '+esc(f0.aircraft):'')+'</small></div></div>'+
  '<div class="fomid">'+o.bounds.map((x,j)=>(o.bounds.length>1?'<span class="fobl">'+(j?'Return':'Onward')+'</span>':'')+leg(x)).join('')+'</div>'+
  '<div class="foact">'+(fareTxt(o)?'<span class="fopr" style="display:block;margin-bottom:6px;line-height:1.15"><b style="display:block;font:700 20px Jost,sans-serif;color:var(--ink)">'+fareTxt(o)+'</b><small style="font-size:11.5px;color:var(--muted)">approx. · '+(F.adults.value*1+F.children.value*1+F.infants.value*1>1?'all travellers':'per person')+'</small></span>':'')+'<span class="fopk">'+(on?'✓ Selected':'Select')+'</span></div>'+
  (b.baggage?'<div class="fofoot"><span>🧳 Included: '+esc(b.baggage)+'</span><span>👜 Cabin bag as per airline</span></div>':'<div class="fofoot fofs"></div>')+'</label>';}
function draw(){
 const allSel=legs.every((_,i)=>sel[i]!=null),pax=+F.adults.value+ +F.children.value+ +F.infants.value;
 const fr=code(F.from.value),to=code(F.to.value);
 let h='<div class="frtop"><div class="frroute"><span><b>'+esc(fr)+'</b><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" d="M4 12h15m-5-5 5 5-5 5"/></svg><b>'+esc(to)+'</b>'+(legs.length>1?'<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" d="M4 12h15m-5-5 5 5-5 5"/></svg><b>'+esc(fr)+'</b>':'')+'</span><small>'+longd(F.depart.value)+(legs.length>1&&F.ret.value?' – '+longd(F.ret.value):'')+' · '+pl(pax,'Traveller','Travellers')+' · '+esc(F.cabin.value)+'</small></div><button type="button" class="frmod">✎ Modify search</button></div>'+
 '<div class="frinfo"><span>ℹ️</span><p>'+(hasFares()?'<b>Fares shown are approximate</b> public airline fares, checked just now. Select your flight'+(legs.length>1?'s':'')+' – we confirm the final fare before you pay.':'<b>Pick your flight'+(legs.length>1?'s':'')+'</b> and we will send you the best fare on WhatsApp / email.')+(src==='timetable'?' Showing direct flights – need a connecting flight? Mention it in Notes. Baggage allowance is confirmed with your quote.':'')+'</p></div>';
 h+=legs.map((opts,i)=>{const s=st[i];const list=opts.filter(o=>pass(o,s)).sort((a,b)=>srt(a,b,s.sort));const shown=list.slice(0,s.n);
  const acount={};opts.forEach(o=>{const c=o.bounds[0].flights[0].airline;acount[c]=(acount[c]||0)+1;});
  const anames={};opts.forEach(o=>{const f=o.bounds[0].flights[0];anames[f.airline]=nm(f);});
  return '<div class="frleg" data-l="'+i+'">'+(legLabel(i)?'<div class="frlh"><span class="frstep">'+(i+1)+'</span><b>'+legLabel(i)+'</b><small>'+esc(i?to+' → '+fr:fr+' → '+to)+' · '+longd(i?F.ret.value:F.depart.value)+'</small>'+(sel[i]!=null?'<em>✓ Selected</em>':'')+'</div>':'')+
  (opts.length?'<div class="frbar"><div class="frtime">'+FL.map(f=>{const c=opts.filter(o=>f[4](hr(dep0(o)))).length;return '<button type="button" data-t="'+f[0]+'" class="'+(s.t.has(f[0])?'on':'')+'"'+(c?'':' disabled')+'><span>'+f[1]+'</span><b>'+f[2]+'</b><small>'+f[3]+'</small></button>';}).join('')+'</div>'+
   '<div class="fral"><span class="fralh">Airlines</span>'+Object.keys(acount).sort((a,b)=>acount[b]-acount[a]).map(c=>'<button type="button" data-a="'+esc(c)+'" class="'+(s.a.has(c)?'on':'')+'">'+logo(c,anames[c])+esc(anames[c])+' <small>'+acount[c]+'</small></button>').join('')+'</div>'+
   '<div class="frsort"><span><b>'+list.length+'</b> flight'+(list.length!==1?'s':'')+(list.length!==opts.length?' of '+opts.length:'')+'</span><label>Sort by <select data-s>'+SORTS.map(([k,t])=>'<option value="'+k+'"'+(s.sort===k?' selected':'')+'>'+t+'</option>').join('')+'</select></label>'+(s.t.size||s.a.size?'<button type="button" class="frclr">Clear filters</button>':'')+'</div></div>'+
   '<div class="frl">'+(shown.length?shown.map(o=>card(o,i,opts.indexOf(o))).join(''):'<p class="frempty">No flights match these filters. <button type="button" class="frclr">Clear filters</button></p>')+'</div>'+
   (list.length>shown.length?'<button type="button" class="frmore">Show '+Math.min(10,list.length-shown.length)+' more flights <small>('+(list.length-shown.length)+' left)</small></button>':'')
  :'<p class="frempty">No direct flights found for this date. Press <b>Get Flight Quote</b> – we will check connecting flights for you.</p>')+'</div>';}).join('');
 if(sel.some(x=>x!=null))h+='<div class="fsel"><div class="fselh"><span class="frstep">✓</span><div><b>Your selected flight'+(legs.length>1?'s':'')+'</b><small>Add baggage and preferences, then send your quote request</small></div></div>'+
  legs.map((o,i)=>sel[i]!=null?'<div class="fselc">'+summary(o[sel[i]],legLabel(i)).map(esc).join('<br>')+'</div>':'').join('')+
  (allSel?'':'<p class="frwarn">Please also select your '+(sel[0]==null?'onward':'return')+' flight above.</p>')+
  '<div class="fselg"><label>🧳 Extra check-in baggage<select class="fxbag">'+BAGS.map(b=>'<option>'+b+'</option>').join('')+'</select></label><label>💺 Seat preference<select class="fxseat"><option>No preference</option><option>Window</option><option>Aisle</option><option>Seats together (family)</option><option>Extra legroom</option></select></label><label>🍽️ Meal<select class="fxmeal"><option>As per airline</option><option>Jain meal</option><option>Vegetarian meal</option><option>Non-vegetarian meal</option><option>Child meal</option><option>Diabetic meal</option></select></label></div>'+
  '<button type="button" class="btn gold frgo">Book this flight – continue ↓</button></div>';
 box.innerHTML=h;
 box.querySelector('.frmod').onclick=()=>{const y=F.getBoundingClientRect().top+scrollY-(document.querySelector('header.site')?.offsetHeight||0)-12;scrollTo({top:y,behavior:'smooth'});};
 box.querySelectorAll('.frleg').forEach(L=>{const i=+L.dataset.l,s=st[i];
  L.querySelectorAll('[data-t]').forEach(b=>b.onclick=()=>{s.t.has(b.dataset.t)?s.t.delete(b.dataset.t):s.t.add(b.dataset.t);s.n=10;keep(draw);});
  L.querySelectorAll('[data-a]').forEach(b=>b.onclick=()=>{s.a.has(b.dataset.a)?s.a.delete(b.dataset.a):s.a.add(b.dataset.a);s.n=10;keep(draw);});
  const so=L.querySelector('[data-s]');if(so)so.onchange=()=>{s.sort=so.value;keep(draw);};
  L.querySelectorAll('.frclr').forEach(b=>b.onclick=()=>{s.t.clear();s.a.clear();s.n=10;keep(draw);});
  const mo=L.querySelector('.frmore');if(mo)mo.onclick=()=>{s.n+=10;keep(draw);};
  L.querySelectorAll('input[type=radio]').forEach(r=>r.onchange=()=>{sel[i]=+r.value;keep(draw);
   const next=legs.findIndex((_,j)=>sel[j]==null);const tgt=next>=0?box.querySelector('.frleg[data-l="'+next+'"]'):box.querySelector('.fsel');if(tgt)tgt.scrollIntoView({behavior:'smooth',block:'start'});});});
 const go=box.querySelector('.frgo');if(go)go.onclick=()=>{const sh=F.querySelector('.fcontact');if(sh)sh.hidden=false;const c=F.querySelector('.fgrid2:not(.fselg)')||F.contact;c.scrollIntoView({behavior:'smooth',block:'center'});setTimeout(()=>{(F.name.value?F.contact:F.name).focus({preventScroll:true});},450);};
}
function keep(fn){const g=c=>{const x=box.querySelector(c);return x?x.value:null;};const v=[g('.fxbag'),g('.fxseat'),g('.fxmeal')];fn();[['.fxbag',v[0]],['.fxseat',v[1]],['.fxmeal',v[2]]].forEach(([c,x])=>{const e=box.querySelector(c);if(e&&x)e.value=x;});}
window.RTT_FSEL=()=>{if(!legs.length||!sel.some(x=>x!=null))return null;const g=c=>{const x=box.querySelector(c);return x?x.value:'';};const out=[];legs.forEach((o,i)=>{if(sel[i]!=null)out.push(...summary(o[sel[i]],legLabel(i)));});const xb=g('.fxbag'),st=g('.fxseat'),ml=g('.fxmeal');if(xb&&xb!==BAGS[0])out.push('Extra baggage: '+xb);if(st&&st!=='No preference')out.push('Seat: '+st);if(ml&&ml!=='As per airline')out.push('Meal: '+ml);return out;};
function reset(){if(legs.length){legs=[];sel=[];st=[];box.hidden=true;box.innerHTML='';}}
['from','to','depart','ret','adults','children','infants','cabin'].forEach(n=>F[n]&&F[n].addEventListener('change',reset));
F.querySelectorAll('input[name=ftrip]').forEach(r=>r.addEventListener('change',reset));
btn.addEventListener('click',async()=>{
 const t=F.querySelector('input[name=ftrip]:checked').value,msg=F.querySelector('.fmsg');msg.className='fmsg vmsg';msg.textContent='';
 const show=e=>{box.hidden=false;box.innerHTML='<div class="frinfo"><span>ℹ️</span><p>'+e+'</p></div>';};
 if(t==='Multi-city')return show('For multi-city trips, fill in all your flights and press <b>Get Flight Quote</b> – we will send the best routing and fare.');
 const fr=code(F.from.value),to=code(F.to.value);
 if(!fr||!to)return show('Please choose the From and To cities from the list (e.g. Mumbai (BOM)) to see flights.');
 if(fr===to)return show('From and To cannot be the same.');
 if(!F.depart.value)return show('Please choose your departure date.');
 if(t==='Round trip'&&!F.ret.value)return show('Please choose your return date.');
 if(t==='Round trip'&&F.ret.value<F.depart.value)return show('Return date must be after the departure date.');
 if(+F.infants.value>+F.adults.value)return show('Each infant must travel with an adult.');
 btn.disabled=true;box.hidden=false;box.innerHTML='<div class="frload"><div class="frlt"><span class="frspin"></span><b>Finding flights '+esc(fr)+' → '+esc(to)+'</b><small>Checking all airlines – this takes a few seconds</small></div>'+'<div class="fsk"><i></i><i></i><i></i></div>'.repeat(3)+'</div>';box.scrollIntoView({behavior:'smooth',block:'start'});
 try{const r=await fetch(SB+'/functions/v1/flight-search',{method:'POST',headers:{apikey:KEY,Authorization:'Bearer '+KEY,'Content-Type':'application/json'},body:JSON.stringify({from:fr,to,depart:F.depart.value,ret:t==='Round trip'?F.ret.value:'',adults:+F.adults.value,children:+F.children.value,infants:+F.infants.value,cabin:CAB[F.cabin.value]||'ECONOMY',nonstop:!!F.querySelector('input[name=fpref][value="Non-stop flights only"]:checked')})});
  const j=await r.json().catch(()=>({}));
  if(!r.ok)throw j.error||r.status;
  src=j.source||'';legs=j.legs||[];sel=legs.map(()=>null);st=legs.map(()=>({t:new Set(),a:new Set(),sort:hasFares()?'price':'dep',n:10}));
  if(!legs.length||legs.every(l=>!l.length))show('We could not load flights for this date online. Just press <b>Get Flight Quote</b> – our team will check all airlines and send you the options.');else draw();
 }catch(e){show('Live flight list is not available right now. Just press <b>Get Flight Quote</b> – our team will check all airlines and send you the options.');}
 btn.disabled=false;
});
})();
"""

# Turn on once a flight data key is saved in Supabase (Edge Functions > Secrets)
FSEARCH_ON = False  # the button also appears automatically once the function reports ready

def flight_widget(root):
    opts = "".join(f'<option value="{c} ({k})">{n}</option>' for c,k,n in AIRPORTS)
    flight = f"""<form class="fform" data-kind="flight" novalidate>
<div class="ftrip" role="radiogroup"><label><input type="radio" name="ftrip" value="One way" checked>One way</label><label><input type="radio" name="ftrip" value="Round trip">Round trip</label><label><input type="radio" name="ftrip" value="Multi-city">Multi-city</label><span class="ftripr">Domestic &amp; international flights</span></div>
<div class="fgrid fmain">
<label class="fcell">From<input name="from" required placeholder="City or airport code" autocomplete="off"></label>
<button type="button" class="fswap" aria-label="Swap from and to">⇄</button>
<label class="fcell">To<input name="to" required maxlength="80" placeholder="City or airport code" autocomplete="off"></label>
<label class="fcell">Departure<input name="depart" type="date" required></label>
<label class="fcell fret">Return<input name="ret" type="date"></label>
<label class="fcell">Travellers<span class="fpax">{_sel("adults","Adults",range(1,10),AD)}{_sel("children","Children",range(0,10),CH)}{_sel("infants","Infants",range(0,10),INF)}</span></label>
<label class="fcell fcab">Cabin class<select name="cabin" aria-label="Cabin class"><option>Economy</option><option>Premium Economy</option><option>Business</option><option>First</option></select><small class="fsub">Tap to change</small></label>
</div>
<div class="ffare" role="radiogroup" aria-label="Special fare"><span class="ffh">Select a<br>special fare</span><label><input type="radio" name="ffare" value="" checked><b>Regular</b><small>Standard fares</small></label><label><input type="radio" name="ffare" value="Student fare"><b>Student</b><small>Valid student ID</small></label><label><input type="radio" name="ffare" value="Armed forces fare"><b>Armed Forces</b><small>Serving &amp; retired</small></label><label><input type="radio" name="ffare" value="Senior citizen fare"><b>Senior Citizen</b><small>Age 60 and above</small></label><label><input type="radio" name="ffare" value="Doctors &amp; nurses fare"><b>Doctors &amp; Nurses</b><small>Valid ID required</small></label></div><div class="flegs" hidden><span class="flh">Next flights in this trip</span><div class="flegrows"></div><button type="button" class="btn outline flegadd">➕ Add another flight</button></div><details class="fmore"><summary>➕ More options – airline, non-stop, meals &amp; special requests</summary><div class="fmoreg"><label class="fcell">Preferred airline<input name="airline" maxlength="60" placeholder="Any airline" autocomplete="off"></label><div class="cradd"><span>Preferences:</span><label><input type="checkbox" name="fpref" value="Non-stop flights only"> Non-stop only</label><label><input type="checkbox" name="fpref" value="Dates flexible (± 3 days)"> Dates flexible ± 3 days</label></div><div class="cradd"><span>Special requests:</span><label><input type="checkbox" name="fspec" value="Jain meal"> 🥗 Jain meal</label><label><input type="checkbox" name="fspec" value="Vegetarian meal"> 🥦 Veg meal</label><label><input type="checkbox" name="fspec" value="Wheelchair assistance"> ♿ Wheelchair</label><label><input type="checkbox" name="fspec" value="Extra baggage"> 🧳 Extra baggage</label></div></div></details><div class="fsr"{"" if FSEARCH_ON else " hidden"}><button type="button" class="btn outline fshow">🔍 Search</button><span class="fsrh">See flights and fares for your date – no sign-up needed. Pick one when you are ready to book.</span></div><div class="fres" hidden></div>{_contact("Get Flight Quote", root)}</form>"""
    hotel = f"""<form class="fform" data-kind="hotel" novalidate hidden>
<div class="fgrid fg-h fmain">
<label class="fcell">City, area or hotel name<input name="dest" required maxlength="80" placeholder="City or hotel" list="hcities" autocomplete="off"></label>
<label class="fcell">Check-in<input name="in" type="date" required></label>
<label class="fcell">Check-out<input name="out" type="date" required></label>
<label class="fcell">Rooms &amp; guests<span class="fpax f3">{_sel("rooms","Rooms",range(1,11),RM)}{_sel("adults","Adults",range(1,21),AD)}{_sel("children","Children",range(0,11),CH)}</span></label>
<label class="fcell">Hotel category<select name="cat"><option>Any</option><option>3 Star</option><option>4 Star</option><option>5 Star</option><option>Luxury / Resort</option><option>Villa / Homestay</option></select></label>
</div><div class="fgrid fg-h2"><label class="fcell">Meal plan<select name="meal"><option>Room only</option><option selected>Breakfast included</option><option>Breakfast + dinner</option><option>All meals</option><option>All-inclusive</option></select></label><label class="fcell">Budget per room per night<select name="hbudget"><option value="">Any budget</option><option>Under ₹5,000</option><option>₹5,000 – ₹10,000</option><option>₹10,000 – ₹20,000</option><option>₹20,000 – ₹40,000</option><option>Above ₹40,000</option></select></label><label class="fcell">Preferred location<input name="hloc" maxlength="80" placeholder="e.g. near the beach, city centre, near the airport" autocomplete="off"></label><label class="fcell">Special occasion<select name="occ"><option value="">None</option><option>Birthday</option><option>Anniversary</option><option>Honeymoon</option><option>Family celebration</option></select></label></div><div class="flegs hlegs"><div class="flegrows"></div><button type="button" class="btn outline flegadd">➕ Add another city / hotel</button></div><div class="fages" hidden><span>Age of each child (at check-in)</span><div class="fagesel"></div></div>{_contact("Get Hotel Quote", root)}</form>"""
    cruise = f"""<form class="fform" data-kind="cruise" novalidate hidden>
<div class="fgrid fg-c fmain">
<label class="fcell">Cruise line<select name="line">{"".join(f"<option>{x}</option>" for x in CRUISE_LINES)}</select></label>
<label class="fcell cr-oline" hidden>Which cruise line?<input name="line_other" maxlength="50" placeholder="e.g. Silversea, Oceania" autocomplete="off"></label>
<label class="fcell">Route / destination<input name="route" maxlength="60" placeholder="e.g. Singapore" autocomplete="off"></label>
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
<div class="crdet" hidden><p class="crdh">We will include these in your quote – add details if you like (optional):</p><div class="crd" data-for="Flights to / from the port" hidden><b>✓ ✈️ Flights added</b> <label>Flying from <input data-d maxlength="40" placeholder="e.g. your city"></label></div><div class="crd" data-for="Hotel before / after the cruise" hidden><b>✓ 🏨 Hotel added</b> <label>When <select data-d><option>Before the cruise</option><option>After the cruise</option><option>Before and after</option></select><input data-d2 type="number" min="1" max="10" value="1" aria-label="Nights"> <small>night(s)</small></label></div><div class="crd" data-for="Visas for the ports of call" hidden><b>✓ 🛂 Visas added</b> <label>Visas you already hold <input data-d maxlength="60" placeholder="e.g. US, Schengen – or none"></label></div><div class="crd" data-for="Travel insurance" hidden><b>✓ 🛡️ Travel insurance added</b> <label>Any senior citizens or medical conditions? <input data-d maxlength="60" placeholder="optional"></label></div><div class="crd" data-for="Local transport (transfers, port to hotel / airport)" hidden><b>✓ 🚐 Local transport added</b> <label>What you need <select data-d><option>Transfers (port ↔ hotel / airport)</option><option>Transport at the ports for sightseeing</option><option>Both</option></select></label></div><div class="crd" data-for="Entry passes / tickets to attractions at the ports" hidden><b>✓ 🎟️ Attraction passes added</b> <label>Which attractions? <input data-d maxlength="80" placeholder="e.g. Universal Studios, Burj Khalifa – or suggest"></label></div></div>
<div class="cradd crothers" hidden><span>Others:</span><label><input type="checkbox" name="other_addon" value="Shore excursions at the ports"> 🧭 Shore excursions</label><label><input type="checkbox" name="other_addon" value="Onboard packages (drinks / specialty dining / Wi-Fi / spa)"> 🍽️ Onboard packages</label><label><input type="checkbox" name="other_addon" value="Jain / vegetarian meals confirmed with the cruise line"> 🥗 Jain / veg meals</label><label><input type="checkbox" name="other_addon" value="Celebration onboard (birthday / anniversary)"> 🎂 Celebration onboard</label><label><input type="checkbox" name="other_addon" value="International SIM / eSIM"> 📶 International SIM / eSIM</label><label><input type="checkbox" name="other_addon" value="Airport meet & assist (porter / wheelchair)"> 🛬 Airport meet & assist</label><label><input type="checkbox" name="other_addon" value="Special assistance onboard (accessible cabin / medical / seniors)"> ♿ Special assistance onboard</label><label><input type="checkbox" name="other_addon" value="Pre / post-cruise city tour"> 🏙️ Pre/post-cruise city tour</label><label class="fcell crotxt">Anything else? Tell us<input name="other_text" maxlength="150" placeholder="e.g. photographer onboard, kids' club, visa for a stopover country" autocomplete="off"></label></div>
<p class="crpass">🛳️ <b>Sailing abroad?</b> Passports should be valid for at least 6 months after the cruise ends, and a visa may be needed for each country the ship stops in – we will check and arrange them for you.</p>
{_contact("Get Cruise Quote", root)}</form>"""
    hc = "".join(f'<option value="{c}">' for c in ["Dubai","Singapore","Bangkok","Pattaya","Phuket","Bali","Maldives","Kuala Lumpur","London","Paris","Srinagar","Gulmarg","Manali","Shimla","Goa","Jaipur","Udaipur","Munnar","Alleppey","Darjeeling","Gangtok","Port Blair","Havelock","Leh","Lonavala","Mahabaleshwar","Mumbai"])
    return f"""
<div class="fbar" id="flight-search">
<div class="ftabs mtabs" role="tablist"><button type="button" class="ftab on" data-k="flight"><svg viewBox="0 0 24 24" width="30" height="30" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/></svg><span>Flights</span></button><button type="button" class="ftab" data-k="hotel"><svg viewBox="0 0 24 24" width="30" height="30" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21V7l9-4 9 4v14"/><path d="M9 21v-5h6v5"/><path d="M7 10h2M11 10h2M15 10h2M7 13h2M11 13h2M15 13h2"/></svg><span>Hotels</span></button><button type="button" class="ftab" data-k="cruise"><svg viewBox="0 0 24 24" width="30" height="30" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2 20c2 1.2 4 1.2 6 0s4-1.2 6 0 4 1.2 6 0"/><path d="M4 17 3 12h18l-2 5"/><path d="M6 12V8h12v4"/><path d="M10 8V5h4v3"/></svg><span>Cruise</span></button><a class="ftab-l" href="{root}customize-your-package/"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22V11"/><path d="M12 11C9 7 5 7 3 9c3-.5 6 .5 9 2zM12 11c3-4 7-4 9-2-3-.5-6 .5-9 2zM12 11c-1-4-4-6-7-6 2 1 5 3 7 6zM12 11c1-4 4-6 7-6-2 1-5 3-7 6z"/><path d="M6 22h12"/></svg><span>Holiday Packages</span></a></div>
{flight}{hotel}{cruise}
<datalist id="fapts">{opts}</datalist><datalist id="hcities">{hc}</datalist>
<p class="fnote" data-for="flight">Tell us what you need – we check all airlines and reply with the best options on WhatsApp or email. Tickets issued by The Real Tours and Travels. Email: <a href="mailto:bookings@therealtoursandtravels.com">bookings@therealtoursandtravels.com</a><br><span class="gstline">GST as applicable: airline taxes as charged by the airline (economy 5%, premium classes 18%) + 18% GST on our service fee.</span></p>
<p class="fnote" data-for="hotel" hidden>Tell us what you need – we check hotels, resorts and villas and reply with the best options on WhatsApp or email. Bookings made by The Real Tours and Travels. Email: <a href="mailto:hotels@therealtoursandtravels.com">hotels@therealtoursandtravels.com</a><br><span class="gstline">GST as applicable: hotel taxes as charged by the hotel (rooms up to ₹7,500/night 5%, above 18%) + 18% GST on our service fee.</span></p>
<p class="fnote" data-for="cruise" hidden>Tell us what you need – we check all major cruise lines and reply with the best sailings on WhatsApp or email. Bookings made by The Real Tours and Travels. Email: <a href="mailto:bookings@therealtoursandtravels.com">bookings@therealtoursandtravels.com</a><br><span class="gstline">GST as applicable: taxes and port charges as charged by the cruise line + 18% GST on our service fee. Overseas tour packages attract 2% TCS.</span></p>
</div>
<div class="grp"><div><b>👥 Group bookings – 10 or more travellers</b><p>Travelling with a corporate team, wedding party, housing society, college or pilgrimage group? Our group desk arranges dedicated group fares, hotel room blocks and cruise cabin allocations, with one point of contact from enquiry to return.</p></div><div class="grpbtn"><a class="btn gold" href="https://wa.me/919843121212?text=Hello%20The%20Real%20Tours%20and%20Travels%2C%20we%20would%20like%20a%20quotation%20for%20a%20group%20booking.%0AService%20%28flights%20/%20hotel%20/%20cruise%29%3A%20%0AGroup%20size%3A%20%0AFrom%20/%20to%3A%20%0ATravel%20dates%3A%20" target="_blank" rel="noopener">💬 WhatsApp the group desk</a><a class="btn outline" href="tel:+919843121212">📞 +91 98431 21212</a><a class="btn outline" href="mailto:bookings@therealtoursandtravels.com?subject=Group%20booking%20enquiry">✉️ Email us</a></div></div>
<script>
(function(){{
const SB="{SB_URL}",KEY="{SB_KEY}";
const notify=(s,t,r)=>{{try{{fetch('https://formsubmit.co/ajax/enquiry@therealtoursandtravels.com',{{method:'POST',headers:{{'Content-Type':'application/json',Accept:'application/json'}},body:JSON.stringify((()=>{{const o={{_subject:s,message:t,_replyto:r||'',_template:'table',_captcha:'false',source:location.href}};const m=(s.match(/(\\S+) – /)||[])[1]||'';const ref=/^[A-Z0-9-]{{6,}}$/.test(m)?m:'';if(r&&/@/.test(r)&&ref){{o.email=r;o._autoresponse='Thank you for contacting The Real Tours and Travels. We have received your request (reference '+ref+') and our team will get back to you shortly. Please quote this reference in any message to us. For anything urgent, call or WhatsApp +91 98431 21212. – The Real Tours and Travels · www.therealtoursandtravels.com';}}return o;}})())}}).catch(()=>{{}});}}catch(_){{}}}};
const box=document.getElementById('flight-search');
const forms={{}};box.querySelectorAll('form').forEach(x=>forms[x.dataset.kind]=x);
const NOTE={{flight:'Preferred timings, anything else…',hotel:'e.g. sea view, near beach, Jain food, early check-in',cruise:'e.g. dates flexible, senior citizens, Jain food'}};
Object.entries(forms).forEach(([k,x])=>x.notes.placeholder=NOTE[k]);
box.querySelectorAll('.ftab').forEach(t=>t.addEventListener('click',()=>{{box.querySelectorAll('.ftab').forEach(b=>b.classList.toggle('on',b===t));Object.entries(forms).forEach(([k,x])=>x.hidden=k!==t.dataset.k);box.querySelectorAll('.fnote[data-for]').forEach(n=>n.hidden=n.dataset.for!==t.dataset.k);}}));
const HK={{flights:'flight',flight:'flight',hotels:'hotel',hotel:'hotel',cruise:'cruise'}};function fromHash(){{const k=HK[location.hash.slice(1)];if(!k)return;const t=box.querySelector('.ftab[data-k='+k+']');if(t){{t.click();const y=box.getBoundingClientRect().top+scrollY-(document.querySelector('header.site')?.offsetHeight||0)-12;scrollTo({{top:y,behavior:'smooth'}});}}}}if(location.hash)setTimeout(fromHash,250);addEventListener('hashchange',fromHash);
const today=new Date(Date.now()+330*60000).toISOString().slice(0,10);
const F=forms.flight,H=forms.hotel,C=forms.cruise;
F.depart.min=F.ret.min=H['in'].min=H.out.min=today;C.month.min=today.slice(0,7);
function trip(){{return F.querySelector('input[name=ftrip]:checked').value;}}
function sync(){{const t=trip();F.querySelector('.fret').style.opacity=t==='Round trip'?1:.45;F.ret.required=t==='Round trip';F.notes.placeholder=NOTE.flight;if(typeof FL!=='undefined'){{FL.hidden=t!=='Multi-city';if(t==='Multi-city'&&!FLR.children.length)addLeg();}}}}
F.querySelectorAll('input[name=ftrip]').forEach(r=>r.addEventListener('change',sync));
// ---- multi-city legs (flights) and extra stays (hotels) ----
const FL=F.querySelector('.flegs'),FLR=FL.querySelector('.flegrows');
function addLeg(){{const n=FLR.children.length;if(n>=4)return;const prev=n?FLR.lastElementChild.querySelector('[data-l=to]').value:F.to.value;const d=document.createElement('div');d.className='fleg';
 d.innerHTML='<label class="fcell">From<input data-l="from" maxlength="80" placeholder="City or code" autocomplete="off"></label><label class="fcell">To<input data-l="to" maxlength="80" placeholder="Type the city" autocomplete="off"></label><label class="fcell">Date<input data-l="date" type="date"></label><button type="button" class="flegx" aria-label="Remove this flight">✕</button>';
 FLR.appendChild(d);const lf=d.querySelector('[data-l=from]');lf.value=prev||'';if(!n)lf.dataset.auto='1';d.querySelector('[data-l=date]').min=today;d.querySelector('.flegx').onclick=()=>{{d.remove();legBtn();}};legBtn();}}
function legBtn(){{FL.querySelector('.flegadd').hidden=FLR.children.length>=4;}}
FL.querySelector('.flegadd').addEventListener('click',addLeg);
F.to.addEventListener('input',()=>{{const l=FLR.querySelector('[data-l=from]');if(l&&(!l.value||l.dataset.auto)){{l.value=F.to.value;l.dataset.auto='1';}}}});
FLR.addEventListener('input',e=>{{if(e.target.dataset.l==='from'&&e.isTrusted)delete e.target.dataset.auto;}});
const HL=H.querySelector('.hlegs'),HLR=HL.querySelector('.flegrows');
function addStay(){{if(HLR.children.length>=4)return;const d=document.createElement('div');d.className='fleg';
 d.innerHTML='<label class="fcell">Next city / hotel<input data-l="city" maxlength="80" list="hcities" placeholder="e.g. Abu Dhabi" autocomplete="off"></label><label class="fcell">Check-in<input data-l="in" type="date"></label><label class="fcell">Check-out<input data-l="out" type="date"></label><button type="button" class="flegx" aria-label="Remove this stay">✕</button>';
 HLR.appendChild(d);const last=HLR.children.length>1?HLR.children[HLR.children.length-2].querySelector('[data-l=out]').value:H.out.value;d.querySelector('[data-l=in]').value=last||'';d.querySelectorAll('input[type=date]').forEach(x=>x.min=today);d.querySelector('.flegx').onclick=()=>{{d.remove();HL.querySelector('.flegadd').hidden=false;}};HL.querySelector('.flegadd').hidden=HLR.children.length>=4;}}
HL.querySelector('.flegadd').addEventListener('click',addStay);
sync();
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
const crDet=C.querySelector('.crdet');
function syncDet(){{let any=false;C.querySelectorAll('.crd').forEach(d=>{{const on=!!C.querySelector('input[name=addon][value="'+d.dataset.for+'"]:checked');d.hidden=!on;any=any||on;}});crDet.hidden=!any;}}
C.querySelectorAll('input[name=addon]').forEach(x=>x.addEventListener('change',syncDet));syncDet();
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
  const legs=t==='Multi-city'?[...FLR.querySelectorAll('.fleg')].map(d=>({{from:d.querySelector('[data-l=from]').value.trim(),to:d.querySelector('[data-l=to]').value.trim(),date:d.querySelector('[data-l=date]').value}})).filter(l=>l.from||l.to||l.date):[];
  if(!err&&t==='Multi-city'&&!legs.length)err='Please add the next flight of your multi-city trip (or choose One way).';
  if(!err)legs.forEach((l,i)=>{{if(err)return;const pd=i?legs[i-1].date:f.depart.value;if(l.from.length<2||l.to.length<2)err='Please enter From and To for flight '+(i+2)+'.';else if(!l.date)err='Please choose the date of flight '+(i+2)+'.';else if(pd&&l.date<pd)err='Flight '+(i+2)+' cannot be before the previous flight.';}});
  const legTxt=legs.map((l,i)=>'Flight '+(i+2)+': '+l.from+' → '+l.to+(l.date?' on '+fd(l.date):'')).join('; ');
  const prefs=[...f.querySelectorAll('input[name=fpref]:checked')].map(x=>x.value),spec=[...f.querySelectorAll('input[name=fspec]:checked')].map(x=>x.value),air=f.airline.value.trim();{{const sf=f.querySelector('input[name=ffare]:checked');if(sf&&sf.value)spec.unshift(sf.value+' (ID to be shown at check-in)');}}
  const extra=[legTxt,prefs.length?'Preferences: '+prefs.join(', '):'',spec.length?'Special requests: '+spec.join(', '):''].filter(Boolean);
  table='flight_enquiries';ref='FL-'+id.slice(0,6).toUpperCase();
  row={{id,trip_type:t,airline_pref:air?air.slice(0,60):null,from_city:from.slice(0,80),to_city:to.slice(0,80),depart_date:f.depart.value||null,return_date:t==='Round trip'?f.ret.value:null,adults:ad,children:ch,infants:inf,cabin:f.cabin.value,full_name:name,notes:[...extra,notes].filter(Boolean).join(' | ').slice(0,1000)||null}};
  lines=['✈️ Flight quote request ('+ref+')',t+': '+from+' → '+to,'Depart: '+(f.depart.value?fd(f.depart.value):''),row.return_date?'Return: '+fd(row.return_date):'',pl(ad,'Adult','Adults')+(ch?', '+pl(ch,'Child','Children'):'')+(inf?', '+pl(inf,'Infant','Infants'):'')+' · '+f.cabin.value].concat(legs.map((l,i)=>'Flight '+(i+2)+': '+l.from+' → '+l.to+' · '+fd(l.date)),air?['Preferred airline: '+air]:[],prefs.length?['Preferences: '+prefs.join(', ')]:[],spec.length?['Special requests: '+spec.join(', ')]:[]);
  const fsel=window.RTT_FSEL&&window.RTT_FSEL();if(fsel&&fsel.length){{lines.push('— Selected flight —',...fsel);row.notes=[fsel.join(' | '),row.notes].filter(Boolean).join(' | ').slice(0,1000);}}
 }}else if(kind==='hotel'){{
  const dest=f.dest.value.trim(),ci=f['in'].value,co=f.out.value,rooms=+f.rooms.value,ad=+f.adults.value,ch=+f.children.value;
  if(dest.length<2)err='Please enter the city, area or hotel name.';
  else if(!ci||!co)err='Please choose check-in and check-out dates.';
  else if(co<=ci)err='Check-out must be after check-in.';
  else if(rooms>ad)err='Each room needs at least one adult.';
  const cages=[...f.querySelectorAll('select[name=child_age]')].map(x=>x.value);
  if(!err&&cages.some(a=>a===''))err='Please choose the age of each child – hotels price children by age.';
  const nights=ci&&co?Math.round((new Date(co)-new Date(ci))/864e5):null;
  const stays=[...HLR.querySelectorAll('.fleg')].map(d=>({{city:d.querySelector('[data-l=city]').value.trim(),ci:d.querySelector('[data-l=in]').value,co:d.querySelector('[data-l=out]').value}})).filter(x=>x.city||x.co);
  if(!err)stays.forEach((x,i)=>{{if(err)return;if(x.city.length<2)err='Please enter the city or hotel for stay '+(i+2)+'.';else if(!x.ci||!x.co)err='Please choose check-in and check-out for '+x.city+'.';else if(x.co<=x.ci)err='Check-out must be after check-in for '+x.city+'.';}});
  const stayTxt=stays.map((x,i)=>'Stay '+(i+2)+': '+x.city+' '+fd(x.ci)+' → '+fd(x.co)).join('; ');
  const hx=['Meal plan: '+f.meal.value,f.hbudget.value?'Budget per room per night: '+f.hbudget.value:'',f.hloc.value.trim()?'Location: '+f.hloc.value.trim():'',f.occ.value?'Occasion: '+f.occ.value:'',stayTxt].filter(Boolean);
  table='booking_enquiries';ref='HT-'+id.slice(0,6).toUpperCase();
  const agesTxt=ch?'Child ages: '+cages.map(a=>a==='0'?'under 1':a).join(', '):'';
  row={{id,kind:'hotel',destination:dest.slice(0,80),start_date:ci||null,end_date:co||null,nights,rooms,adults:ad,children:ch,category:f.cat.value,full_name:name,notes:[agesTxt,...hx,notes].filter(Boolean).join(' | ').slice(0,1000)||null}};
  lines=['🏨 Hotel quote request ('+ref+')','Where: '+dest,ci&&co?'Stay: '+fd(ci)+' → '+fd(co)+' ('+pl(nights,'night','nights')+')':'',pl(rooms,'Room','Rooms')+' · '+pl(ad,'Adult','Adults')+(ch?', '+pl(ch,'Child','Children'):'')+' · '+f.cat.value,agesTxt].concat(hx);
 }}else{{
  const ad=+f.adults.value,ch=+f.children.value,cab=+f.cabins.value,nt=f.nights.options[f.nights.selectedIndex].text,w=crWhen();
  const line=f.line.value.startsWith('Other')?f.line_other.value.trim():f.line.value,port=f.port.value.startsWith('Other')?f.port_other.value.trim():f.port.value,route=f.route.value.trim();
  const sail=f.sail.value,m=f.month.value,ages=[...f.querySelectorAll('select[name=child_age]')].map(x=>x.value),addons=[...f.querySelectorAll('input[name=addon]:checked')].map(x=>{{const d=f.querySelector('.crd[data-for="'+x.value+'"]');if(!d)return x.value;const a=d.querySelector('[data-d]'),b=d.querySelector('[data-d2]');let v=(a&&a.value||'').trim();if(b)v+=' – '+b.value+' night(s)';return v?x.value+' ('+v+')':x.value;}});
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

// ---- MMT-style display layer: big dates, airport names, traveller popovers ----
(function(){{
 const MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],DAY=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
 box.querySelectorAll('.fmain input[type=date]').forEach(inp=>{{const c=inp.closest('.fcell');c.classList.add('fdate');
  const v=document.createElement('span');v.className='fdv';inp.after(v);
  const draw=()=>{{if(!inp.value){{v.innerHTML='<b class="fdph">Select date</b><small>'+(inp.name==='ret'?'Tap to add a return date':'&nbsp;')+'</small>';return;}}const d=new Date(inp.value+'T00:00');v.innerHTML='<b><big>'+d.getDate()+'</big> '+MON[d.getMonth()]+"'"+String(d.getFullYear()).slice(2)+'</b><small>'+DAY[d.getDay()]+'</small>';}};
  inp.addEventListener('change',draw);inp.addEventListener('input',draw);draw();
  c.addEventListener('click',()=>{{try{{inp.showPicker();}}catch(_){{inp.focus();}}}});}});
 const AP={{}};document.querySelectorAll('#fapts option').forEach(o=>AP[o.value.toLowerCase()]=o.textContent);
 box.querySelectorAll('.fmain input[name=from],.fmain input[name=to]').forEach(inp=>{{const c=inp.closest('.fcell');const sub=document.createElement('small');sub.className='fsub';inp.after(sub);const big=document.createElement('span');big.className='fcity';inp.before(big);
  const draw=()=>{{const v=inp.value.trim(),t=AP[v.toLowerCase()],m=v.match(/^(.*) \\(([A-Z]{{3}})\\)$/);if(t&&m){{big.textContent=m[1];sub.textContent=m[2]+', '+t;c.classList.add('hascity');}}else{{big.textContent='';sub.textContent=t||(v?'':'City or airport');c.classList.remove('hascity');}}}};inp.addEventListener('input',draw);inp.addEventListener('change',draw);draw();}});
 box.querySelector('.fswap').addEventListener('click',()=>box.querySelectorAll('.fmain input[name=from],.fmain input[name=to]').forEach(x=>x.dispatchEvent(new Event('input'))));
 box.querySelectorAll('.fmain .fpax').forEach(px=>{{const c=px.closest('.fcell');c.classList.add('fpaxc');
  const sum=document.createElement('span');sum.className='fsum';const pop=document.createElement('div');pop.className='fpop';pop.hidden=true;
  px.before(sum);px.before(pop);pop.appendChild(px);const done=document.createElement('button');done.type='button';done.className='btn gold fdone';done.textContent='Done';pop.appendChild(done);
  const sels=[...px.querySelectorAll('select')];
  const draw=()=>{{const t=sels.map(x=>x.options[x.selectedIndex].text);const n=t[0].split(' ');sum.innerHTML='<b><big>'+n[0]+'</big> '+n.slice(1).join(' ')+'</b><small>'+t.slice(1).filter(x=>!/^0 /.test(x)).join(', ')+'</small>';}};
  sels.forEach(x=>x.addEventListener('change',draw));draw();
  c.addEventListener('click',e=>{{if(pop.contains(e.target)&&e.target!==done)return;e.preventDefault();if(e.target===done){{pop.hidden=true;return;}}box.querySelectorAll('.fpop').forEach(p=>{{if(p!==pop)p.hidden=true;}});pop.hidden=!pop.hidden;}});
  document.addEventListener('click',e=>{{if(!c.contains(e.target))pop.hidden=true;}});
  px.closest('form').addEventListener('reset',()=>setTimeout(draw,0));}});
}})();
// mobile: Search button right under the main fields; name & mobile asked in a bottom sheet
(function(){{if(!matchMedia('(max-width:700px)').matches)return;
 box.querySelectorAll('form').forEach(f=>{{const b=f.querySelector('.fgo'),main=f.querySelector('.fmain'),g2=f.querySelector('.fgrid2'),msg=f.querySelector('.fmsg');if(!b||!main||!g2)return;
  const kind=f.dataset.kind||'flight';const full=b.textContent;
  const wrap=document.createElement('div');wrap.className='fmsearch';const hint=document.createElement('p');hint.className='fmhint';
  b.textContent=kind==='hotel'?'Search hotels':kind==='cruise'?'Search cruises':'Search flights';main.after(wrap);wrap.appendChild(b);wrap.appendChild(hint);
  const sh=document.createElement('div');sh.className='fcontact';sh.hidden=true;sh.innerHTML='<p class="fct-t"><b>Where should we send your quote?</b></p>';
  wrap.after(sh);sh.appendChild(g2);if(msg)sh.appendChild(msg);
  const go=document.createElement('button');go.type='button';go.className='btn gold fsh-go';go.textContent=full;sh.appendChild(go);
  let pass=false;
  b.addEventListener('click',e=>{{if(pass)return;e.preventDefault();e.stopImmediatePropagation();hint.textContent='';
   const miss=[...main.querySelectorAll('input[required],select[required]')].find(x=>!x.disabled&&!x.value.trim());
   if(miss){{const lab=(miss.closest('.fcell')||{{}}).firstChild;hint.textContent='Please fill '+(lab&&lab.textContent?lab.textContent.trim().replace(/\*$/,''):'all fields')+' first.';miss.focus();return;}}
   const live=kind==='flight'&&f.querySelector('.fsr:not([hidden]) .fshow');
   if(live&&f.querySelector('input[name=ftrip]:checked').value!=='Multi-city'){{live.click();return;}}
   sh.hidden=false;setTimeout(()=>{{sh.scrollIntoView({{behavior:'smooth',block:'start'}});}},30);}},true);
  go.addEventListener('click',()=>{{pass=true;b.click();pass=false;}});
 }});
}})();
}})();
</script><script>"""+FSEARCH_JS.replace("__SB__",SB_URL).replace("__KEY__",SB_KEY)+"""</script>"""

FLIGHT_CSS = """
.grp{display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center;justify-content:space-between;margin-top:14px;padding:16px 18px;border:1px solid var(--line);border-left:4px solid var(--red);border-radius:14px;background:var(--bg)}
.grp>div:first-child{flex:1 1 360px}.grp b{color:var(--wine);font-size:16px}.grp p{margin:4px 0 0;font-size:14px;color:var(--ink)}
.grpbtn{display:flex;flex-wrap:wrap;gap:8px}.grpbtn .btn{padding:9px 16px;font-size:14.5px;white-space:nowrap}
.fgrid.fg-c,.fgrid.fg-c2{grid-template-columns:repeat(auto-fit,minmax(180px,1fr))!important}.fgrid.fg-c2 .fcell:has(.fpax){grid-column:span 2}.crwhen label{white-space:nowrap}.crwhen{display:flex;flex-wrap:wrap;gap:6px 14px;text-transform:none;letter-spacing:0;font:500 14.5px 'Jost',sans-serif;color:var(--ink);padding:11px 0}.crwhen label{display:flex;gap:6px;align-items:center}.crwhen input{accent-color:var(--red)}
.cradd{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;font-size:14.5px}.cradd>span{font-size:12.5px;font-weight:600;letter-spacing:.6px;text-transform:uppercase;color:var(--muted)}.cradd label{display:flex;gap:6px;align-items:center;cursor:pointer}.cradd input{accent-color:var(--red)}
.crdet{display:grid;gap:8px;padding:12px 14px;background:#f2faf4;border:1px solid #cdebd6;border-radius:12px}.crdh{margin:0;font-size:13.5px;color:#17703a}.crd{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:center;font-size:14.5px}.crd b{color:#17703a;font-weight:600;min-width:170px}.crd label{display:flex;flex-wrap:wrap;gap:6px;align-items:center;color:var(--muted)}.crd input,.crd select{font:500 14.5px 'Jost',sans-serif;padding:7px 10px;border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink)}.crd input[data-d2]{width:64px}
.crothers{padding:10px 14px;background:var(--bg);border:1px solid var(--line);border-radius:12px}.crotxt{flex:1 1 100%}
.crpass{margin:0;background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:10px 14px;font-size:13.5px}.fcell[hidden]{display:none!important}
.flegs{display:grid;gap:8px}.flegs[hidden]{display:none}.flh{font-size:12.5px;font-weight:600;letter-spacing:.6px;text-transform:uppercase;color:var(--muted)}.flegrows{display:grid;gap:8px}.flegrows:empty{display:none}.fleg{display:grid;grid-template-columns:1.2fr 1.2fr 1fr 40px;gap:10px;align-items:end}.flegx{height:44px;border:1px solid var(--line);border-radius:12px;background:#fff;color:var(--crimson);cursor:pointer;font-size:16px}.flegadd{justify-self:start;padding:8px 16px;font-size:14.5px}.flegadd[hidden]{display:none}
.fmore{border:1px solid var(--line);border-radius:12px;padding:0 14px;background:var(--bg)}.fmore summary{cursor:pointer;padding:11px 0;font-weight:600;color:var(--wine);font-size:14.5px}.fmore[open]{padding-bottom:12px}.fmoreg{display:grid;gap:10px}.fmoreg .fcell{max-width:340px}
.fgrid.fg-h2{grid-template-columns:repeat(auto-fit,minmax(200px,1fr))!important}
@media(max-width:700px){.fleg{grid-template-columns:1fr 1fr}.fleg .fcell:last-of-type{grid-column:1}.flegx{grid-column:2}}
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

/* ===== booking box look ===== */
.fbar{position:relative;border:0;border-top:0;border-radius:16px;padding:0 26px 54px;margin:24px 0 34px;box-shadow:0 6px 28px rgba(40,10,15,.14)}
.mtabs{display:flex;gap:8px;margin:0 -26px 20px!important;padding:14px 26px!important;border:0!important;border-bottom:1px solid var(--line)!important;background:var(--bg);border-radius:16px 16px 0 0;overflow-x:auto;scrollbar-width:none}
.mtabs::-webkit-scrollbar{display:none}
.mtabs .ftab,.mtabs .ftab-l{display:flex;text-decoration:none;align-items:center;gap:8px;padding:9px 18px!important;border:1px solid var(--line)!important;border-radius:999px;background:#fff;color:#4a4a4a;font:600 15px 'Jost',sans-serif!important;cursor:pointer;white-space:nowrap;margin:0!important}
.mtabs .ftab-l svg{width:22px;height:22px;color:#6b6b6b}.mtabs .ftab-l:hover{border-color:#9b3a3f!important;color:#9b3a3f}.mtabs .ftab svg{width:22px;height:22px;color:#6b6b6b}
.mtabs .ftab.on{background:#9b3a3f;border-color:#9b3a3f!important;color:#fff}.mtabs .ftab.on svg{color:#fff}
.mtabs .ftab:hover:not(.on){border-color:#9b3a3f!important;color:#9b3a3f}
.ftrip{gap:22px;align-items:center;margin-bottom:12px}.ftrip label{border:0!important;background:none!important;padding:0!important;font-weight:600;color:#333;font-size:14.5px}
.ftrip label:has(input:checked){color:var(--ink);background:#f3f3f3!important;border-radius:999px;padding:4px 12px!important}
.ftripr{margin-left:auto;font-size:14px;color:#555}
.fmain{border:1px solid #e3e3e3;border-radius:12px;gap:0!important;align-items:stretch!important;margin-bottom:14px;position:relative}
.fmain>.fcell{max-width:none;padding:12px 18px 14px;border-right:1px solid #e3e3e3;font:500 14px 'Jost',sans-serif;letter-spacing:0;text-transform:none;color:#555;gap:2px;align-content:start;cursor:pointer;position:relative;min-width:0}
.fmain>.fcell:last-child{border-right:0}.fmain>.fcell:hover{background:#fbf6f6}
.fmain>.fcell:first-child{border-radius:12px 0 0 12px}.fmain>.fcell:last-child{border-radius:0 12px 12px 0}
.fmain .fcell input:not([type=date]),.fmain .fcell select{border:0!important;outline:0!important;padding:2px 0!important;background:transparent!important;font:700 26px/1.25 'Jost',sans-serif!important;color:#111;border-radius:0}
.fmain .fcell input::placeholder{color:#b9b9b9;font-weight:600}
.fmain .fcell select{font-size:20px!important;cursor:pointer}
.fsub{display:block;font-size:13px;color:#777;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-height:17px}
.fdate input[type=date]{position:absolute;inset:0;opacity:0;width:100%;height:100%;cursor:pointer;border:0;padding:0}
.fdv{display:grid;pointer-events:none}.fdv b{font:600 18px/1.2 'Jost',sans-serif;color:#111}.fdv b big{font-size:30px;font-weight:800}.fdv small{font-size:13px;color:#777}.fdph{font-size:22px!important;color:#b9b9b9!important;font-weight:600!important;padding:5px 0}
.fsum{display:grid}.fsum b{font:600 18px/1.2 'Jost',sans-serif;color:#111}.fsum b big{font-size:30px;font-weight:800}.fsum small{font-size:13px;color:#777;min-height:17px}
.fpop{position:absolute;top:calc(100% + 6px);right:0;z-index:20;background:#fff;border:1px solid var(--line);border-radius:14px;box-shadow:0 14px 40px rgba(0,0,0,.18);padding:14px;width:280px;display:grid;gap:10px;cursor:default}
.fpop[hidden]{display:none}.fpop .fpax{display:grid!important;grid-template-columns:1fr!important;gap:8px}
.fmain .fpop select{font:500 15.5px 'Jost',sans-serif!important;padding:10px 12px!important;border:1px solid var(--line)!important;border-radius:10px!important;width:100%}
.fdone{justify-self:end;padding:8px 22px;font-size:14px}
.fmain .fswap{align-self:center;justify-self:center;width:38px;height:38px;margin:0 -19px;z-index:2;position:relative;box-shadow:0 2px 8px rgba(0,0,0,.12);border:1px solid #e3e3e3}
.fgrid.fmain{grid-template-columns:1.25fr 0 1.25fr 1fr 1fr 1.3fr}
.fgrid.fg-h.fmain{grid-template-columns:1.6fr 1fr 1fr 1.3fr 1fr}
.fgrid2{border-top:1px dashed #e3e3e3;padding-top:14px}
.fgrid2 .fcell,.fgrid.fg-h2 .fcell,.fgrid.fg-c2 .fcell{text-transform:none;letter-spacing:0;font-size:13px}
.fbar .fgo{position:absolute;left:50%;bottom:-27px;transform:translateX(-50%);height:54px;min-width:250px;padding:0 40px;border-radius:999px;font:700 20px 'Jost',sans-serif;letter-spacing:.6px;text-transform:uppercase;box-shadow:0 8px 22px rgba(155,58,63,.35);z-index:4}
.fbar form{position:static}
.fbar+.grp{margin-top:8px}
@media(max-width:1100px){.fgrid.fmain,.fgrid.fg-h.fmain,.fgrid.fg-c.fmain{grid-template-columns:1fr 0 1fr!important}.fgrid.fg-h.fmain,.fgrid.fg-c.fmain{grid-template-columns:1fr 1fr!important}
 .fmain>.fcell{border-bottom:1px solid #e3e3e3;border-radius:0!important}.fgrid.fmain>.fcell:nth-child(n+4){grid-column:auto}.fgrid.fmain>.fcell:last-child{grid-column:1/-1!important}}
@media(max-width:700px){.fbar{padding:0 14px 50px;margin-top:10px}.mtabs{margin:0 -14px 14px!important;padding:12px 14px!important}.mtabs{display:grid!important;grid-template-columns:1fr 1fr;gap:8px!important}.mtabs .ftab,.mtabs .ftab-l{padding:8px 10px!important;font-size:14px!important;justify-content:center}
 .fgrid.fmain,.fgrid.fg-h.fmain,.fgrid.fg-c.fmain{grid-template-columns:1fr 1fr!important}.fmain .fswap{display:none}.fmain>.fcell:first-child,.fgrid.fmain>.fcell:nth-child(3){grid-column:1/-1!important}
 .fmain .fcell input:not([type=date]){font-size:22px!important}.fdv b big,.fsum b big{font-size:24px}.ftripr{display:none}.fbar .fgo{min-width:0;width:calc(100% - 28px);padding:0 14px;font-size:15px;letter-spacing:.2px}.ftrip{gap:10px}.fpop{left:0;right:auto;width:min(280px,80vw)}}

/* ===== own style (not a copy): separate field cards, button inside the box ===== */
.fmain{border:0!important;gap:10px!important}
.fmain>.fcell{border:1px solid var(--line)!important;border-radius:14px!important;background:var(--bg);padding:12px 16px!important;font-size:12px!important;letter-spacing:.5px!important;text-transform:uppercase!important;color:var(--muted)}
.fmain>.fcell:hover,.fmain>.fcell:focus-within{border-color:var(--wine)!important;background:#fff}
.fmain .fcell input:not([type=date]),.fmain .fcell select{font:600 20px/1.3 'Jost',sans-serif!important;text-transform:none;letter-spacing:0}
.fdv b,.fsum b{font:600 20px/1.3 'Jost',sans-serif!important}.fdv b big,.fsum b big{font-size:20px!important;font-weight:600!important}
.fdv,.fsum,.fsub,.fpop{text-transform:none;letter-spacing:0}
.fmain .fswap{margin:0!important;box-shadow:none!important}
.fgrid.fmain{grid-template-columns:1.25fr 36px 1.25fr 1fr 1fr 1.3fr}
.fbar{padding-bottom:24px!important}
.fbar .fgo{position:static!important;transform:none!important;height:48px!important;min-width:0!important;padding:0 26px!important;border-radius:12px!important;font:600 16px 'Jost',sans-serif!important;letter-spacing:0!important;text-transform:none!important;box-shadow:none!important}
.fbar+.grp{margin-top:0!important}
@media(max-width:1100px){.fgrid.fmain{grid-template-columns:1fr 36px 1fr!important}}
@media(max-width:700px){.fgrid.fmain{grid-template-columns:1fr 1fr!important}.fbar .fgo{width:100%}}

/* ===== flight results (schedules only, no fares) ===== */
.fsr[hidden]{display:none}.fsr{display:flex;flex-wrap:wrap;align-items:center;gap:10px 16px;margin:14px 0 4px}.fsr .fshow{font-weight:600}.fsrh{color:var(--muted);font-size:14px}
.fres{margin:14px 0 18px;scroll-margin-top:90px}
.frtop{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;background:#fff;border:1px solid var(--line);border-radius:16px;padding:14px 18px}
.frroute span{display:flex;align-items:center;gap:8px;font:600 22px 'Jost',sans-serif;color:var(--ink)}.frroute svg{color:var(--muted)}.frroute small{display:block;color:var(--muted);font-size:14px;margin-top:2px}
.frmod{background:none;border:1px solid var(--line);border-radius:999px;padding:8px 16px;font:500 14px 'Jost',sans-serif;color:var(--ink);cursor:pointer}.frmod:hover{border-color:var(--ink)}
.frinfo{display:flex;gap:10px;align-items:flex-start;background:#f6f7f8;border-radius:12px;padding:10px 14px;margin:10px 0 4px;font-size:14px;color:#444}.frinfo p{margin:0;line-height:1.55}.frinfo span{flex:none}
.frleg{margin-top:16px}.frleg+.frleg{margin-top:26px;padding-top:20px;border-top:1px solid var(--line)}
.frlh{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:10px}.frlh b{font:600 18px 'Jost',sans-serif}.frlh small{color:var(--muted);font-size:14px}.frlh em{font-style:normal;font-size:13px;font-weight:600;color:#2e7d5b;background:#eaf5ef;border-radius:999px;padding:3px 10px}
.frstep{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;background:var(--ink);color:#fff;font:600 14px 'Jost',sans-serif;flex:none}
.frbar{background:#fff;border:1px solid var(--line);border-radius:16px;padding:12px;display:grid;gap:12px}
.frtime{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.frtime button{border:1px solid var(--line);background:#fff;border-radius:12px;padding:8px 6px;cursor:pointer;text-align:center;font:inherit;color:var(--ink);transition:border-color .15s,background .15s}
.frtime button span{display:block;font-size:18px;line-height:1.2}.frtime button b{display:block;font:600 13.5px 'Jost',sans-serif}.frtime button small{display:block;color:var(--muted);font-size:11.5px}
.frtime button:hover:not(:disabled){border-color:#bdbdbd}.frtime button.on{border-color:var(--red);background:#fdf3f3}.frtime button:disabled{opacity:.4;cursor:default}
.fral{display:flex;gap:8px;overflow-x:auto;padding-bottom:2px;align-items:center;scrollbar-width:thin}.fralh{font-size:12px;text-transform:uppercase;letter-spacing:.5px;color:var(--muted);flex:none;margin-right:2px}
.fral button{flex:none;display:inline-flex;align-items:center;gap:7px;border:1px solid var(--line);background:#fff;border-radius:999px;padding:4px 12px 4px 4px;font:500 13.5px 'Jost',sans-serif;color:var(--ink);cursor:pointer;white-space:nowrap}
.fral button small{color:var(--muted);font-size:12px}.fral button.on{border-color:var(--red);background:#fdf3f3}.fral .flogo{width:24px;height:24px;border-radius:50%}
.frsort{display:flex;align-items:center;gap:12px;flex-wrap:wrap;font-size:14px;color:var(--muted);border-top:1px solid #f0f0f0;padding-top:10px}.frsort>span b{color:var(--ink)}
.frsort label{margin-left:auto;display:flex;align-items:center;gap:6px}.frsort select{border:1px solid var(--line);border-radius:8px;padding:6px 8px;font:500 14px 'Jost',sans-serif;background:#fff;color:var(--ink)}
.frclr{background:none;border:0;color:var(--red);font:500 14px 'Jost',sans-serif;cursor:pointer;text-decoration:underline;padding:0}
.frl{display:grid;gap:12px;margin-top:12px}
.flogo{position:relative;display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:12px;background:#f4f4f4;border:1px solid #eee;overflow:hidden;flex:none}
.flogo em{font-style:normal;font:600 13px 'Jost',sans-serif;color:#555}.flogo img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain}.flogo img[src]:not([complete]){background:transparent}
.fo{position:relative;display:grid;grid-template-columns:minmax(170px,1.1fr) 2fr auto;align-items:center;gap:8px 18px;background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px 18px 0;cursor:pointer;transition:border-color .15s,box-shadow .15s}
.fo:hover{border-color:#c8c8c8;box-shadow:0 6px 18px rgba(0,0,0,.06)}.fo.on{border-color:var(--red);box-shadow:0 0 0 1px var(--red),0 6px 18px rgba(215,25,31,.08)}
.fo input{position:absolute;opacity:0;pointer-events:none}
.foal{display:flex;align-items:center;gap:12px;min-width:0}.foal b{display:block;font:600 16px 'Jost',sans-serif;color:var(--ink)}.foal small{display:block;color:var(--muted);font-size:12.5px;line-height:1.4}
.fomid{display:grid;gap:10px}.fobl{font-size:11.5px;text-transform:uppercase;letter-spacing:.5px;color:var(--muted)}
.fotimes{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:14px}
.fot b{display:block;font:600 22px/1.1 'Jost',sans-serif;color:var(--ink)}.fot b sup{color:var(--red);font-size:11px;margin-left:2px;font-weight:600}.fot small{display:block;color:var(--muted);font-size:13px;margin-top:3px}.fot.r{text-align:right}
.fod{text-align:center;min-width:90px}.fod small{display:block;font-size:12.5px;color:var(--muted)}
.fline{display:flex;align-items:center;gap:4px;margin:3px 0;color:#9a9a9a}.fline i{flex:1;height:0;border-top:1.5px dashed #cfcfcf}.fline svg{flex:none}
.fod .fns{color:#2e7d5b;font-weight:600}.fod .fstop{color:#a0522d;font-weight:600}
.foact{justify-self:end;min-width:118px;text-align:right}.fopk{display:inline-block;border:1.5px solid var(--ink);color:var(--ink);border-radius:10px;padding:9px 20px;font:600 14px 'Jost',sans-serif;white-space:nowrap}
.fo:hover .fopk{background:#f5f5f5}.fo.on .fopk{background:var(--red);border-color:var(--red);color:#fff}
.fofoot.fofs{padding:0;border:0;margin-top:8px;background:none}.fofoot{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:4px 18px;border-top:1px dashed #ececec;margin:6px -18px 0;padding:9px 18px;font-size:12.5px;color:#666;background:#fafafa;border-radius:0 0 16px 16px}
.frmore{display:block;margin:14px auto 0;background:#fff;border:1px solid var(--line);border-radius:999px;padding:10px 22px;font:600 14px 'Jost',sans-serif;color:var(--ink);cursor:pointer}.frmore:hover{border-color:var(--ink)}.frmore small{color:var(--muted);font-weight:500}
.frempty{background:#fff;border:1px dashed var(--line);border-radius:14px;padding:18px;text-align:center;color:var(--muted);margin:12px 0 0}
.fsel{margin-top:22px;background:#fff;border:1.5px solid var(--red);border-radius:16px;padding:16px 18px;scroll-margin-top:90px}
.fselh{display:flex;align-items:center;gap:12px;margin-bottom:10px}.fselh .frstep{background:var(--red)}.fselh b{display:block;font:600 18px 'Jost',sans-serif}.fselh small{display:block;color:var(--muted);font-size:13.5px}
.fselc{background:#f7f7f7;border-radius:10px;padding:10px 12px;font-size:14px;line-height:1.6;margin-bottom:8px}
.frwarn{color:var(--red);font-size:14px;margin:6px 0}
.fselg{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:12px 0}.fselg label{display:grid;gap:5px;font-size:13px;color:var(--muted)}
.fselg select{border:1px solid var(--line);border-radius:10px;padding:10px;font:500 15px 'Jost',sans-serif;background:#fff;color:var(--ink)}
.frgo{width:100%;height:48px;border-radius:12px;font:600 16px 'Jost',sans-serif}
.frload{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px}.frlt{display:grid;grid-template-columns:auto 1fr;gap:0 12px;align-items:center;margin-bottom:12px}.frlt b{font:600 16px 'Jost',sans-serif}.frlt small{grid-column:2;color:var(--muted);font-size:13px}
.frspin{grid-row:span 2;width:26px;height:26px;border-radius:50%;border:3px solid #eee;border-top-color:var(--red);animation:frspin .8s linear infinite}@keyframes frspin{to{transform:rotate(360deg)}}
.fsk{display:grid;grid-template-columns:44px 1fr 90px;gap:16px;align-items:center;padding:16px 0;border-top:1px solid #f2f2f2}.fsk i{display:block;height:14px;border-radius:7px;background:linear-gradient(90deg,#f1f1f1 25%,#e6e6e6 50%,#f1f1f1 75%);background-size:200% 100%;animation:frsh 1.2s infinite}.fsk i:first-child{height:44px;border-radius:12px}.fsk i:last-child{height:34px;border-radius:10px}
@keyframes frsh{to{background-position:-200% 0}}
@media(max-width:800px){.fo{grid-template-columns:1fr auto;padding:14px 14px 0}.fomid{grid-column:1/-1;order:3}.foact{order:2}.fofoot{order:4;margin:6px -14px 0;padding:9px 14px}.fot b{font-size:20px}
 .frtime{grid-template-columns:repeat(4,1fr);gap:6px}.frtime button{padding:6px 2px}.frtime button small{display:none}.frtime button b{font-size:12px;line-height:1.2}.fselg{grid-template-columns:1fr}.frroute span{font-size:19px}.frsort label{margin-left:0}}
/* ===== airport picker ===== */
.fbar form[data-kind=flight] .fcell{position:relative}
.fac{position:absolute;left:-1px;right:-1px;top:calc(100% + 4px);z-index:60;background:#fff;border:1px solid var(--line);border-radius:12px;box-shadow:0 10px 28px rgba(0,0,0,.12);max-height:340px;overflow:auto;padding:4px;min-width:260px;text-transform:none;letter-spacing:0}
.fac button{display:flex;align-items:center;justify-content:space-between;gap:10px;width:100%;text-align:left;background:none;border:0;border-radius:8px;padding:8px 10px;cursor:pointer;font:inherit;color:var(--ink)}
.fac button:hover,.fac button.on{background:#f3f3f3}
.facm{min-width:0}.facm b{display:block;font:600 15px 'Jost',sans-serif}.facm small{display:block;color:var(--muted);font-size:12.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.facc{flex:none;font:600 13px 'Jost',sans-serif;border:1px solid var(--line);border-radius:6px;padding:2px 7px;color:var(--ink)}

/* ===== flight search bar: one connected bar (own colours) ===== */
.fbar form[data-kind=flight] .fgrid.fmain{display:grid;grid-template-columns:1.35fr 1.35fr 1fr 1fr 1fr 1fr!important;gap:0!important;border:1px solid #dcdcdc!important;border-radius:16px;background:#fff;position:relative}
.fbar form[data-kind=flight] .fmain>.fcell{border:0!important;border-right:1px solid #e6e6e6!important;border-radius:0!important;background:#fff;padding:14px 18px!important;min-height:112px;cursor:pointer;transition:background .15s}
.fbar form[data-kind=flight] .fmain>.fcell:first-of-type{border-radius:15px 0 0 15px!important}
.fbar form[data-kind=flight] .fmain>.fcell:last-of-type{border-right:0!important;border-radius:0 15px 15px 0!important}
.fbar form[data-kind=flight] .fmain>.fcell:hover{background:#fafafa}
.fbar form[data-kind=flight] .fmain>.fcell:focus-within,.fbar form[data-kind=flight] .fmain>.fcell.fpaxc:has(.fpop:not([hidden])){background:#fbf1f1!important}
.fbar form[data-kind=flight] .fmain .fswap{position:absolute;left:calc(1.35 / 6.7 * 100%);top:50%;transform:translate(-50%,-50%);width:38px;height:38px;border-radius:50%;background:#fff;border:1px solid #dcdcdc;z-index:5;margin:0!important;grid-column:auto}
.fbar form[data-kind=flight] .fmain .fswap{grid-row:1}
.fbar form[data-kind=flight] .fmain>.fcell:nth-of-type(n+3)::after{content:'';width:6px;height:6px;border-right:1.8px solid var(--red);border-bottom:1.8px solid var(--red);transform:rotate(45deg);position:absolute;top:17px;right:18px}
.fbar form[data-kind=flight] .fmain>.fcell{position:relative}
.fcity{display:none}
.fbar form[data-kind=flight] .fcell.hascity:not(:focus-within) .fcity{display:block;font:700 28px/1.15 'Jost',sans-serif;color:#111;text-transform:none;letter-spacing:0;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.fbar form[data-kind=flight] .fcell.hascity:not(:focus-within) input{position:absolute!important;opacity:0;pointer-events:none;height:0}
.fbar form[data-kind=flight] .fmain .fdv b big,.fbar form[data-kind=flight] .fmain .fsum b big{font-size:28px!important;font-weight:700!important}
.fbar form[data-kind=flight] .fmain .fdv b,.fbar form[data-kind=flight] .fmain .fsum b{font-size:18px!important}
.fbar form[data-kind=flight] .fcab select{appearance:none;-webkit-appearance:none;border:0;background:transparent;font:700 20px/1.2 'Jost',sans-serif;color:#111;padding:2px 0;margin-top:4px;width:100%;cursor:pointer;text-transform:none;letter-spacing:0}
.fbar form[data-kind=flight] .fmain .fsub{font-size:12.5px}
.ffare{display:flex;align-items:stretch;gap:10px;margin:14px 0 4px;flex-wrap:wrap}
.ffh{font:600 14px/1.25 'Jost',sans-serif;color:#222;align-self:center;margin-right:4px}
.ffare label{position:relative;display:grid;align-content:center;border:1px solid #dcdcdc;border-radius:10px;padding:7px 14px;cursor:pointer;background:#fff;min-width:118px;transition:border-color .15s,background .15s}
.ffare label input{position:absolute;opacity:0;pointer-events:none}
.ffare label b{font:600 14px 'Jost',sans-serif;color:#222}.ffare label small{font-size:12px;color:var(--muted)}
.ffare label:hover{border-color:#bdbdbd}.ffare label:has(input:checked){border-color:var(--red);background:#fbf1f1}.ffare label:has(input:focus-visible){outline:2px solid var(--red);outline-offset:2px}
@media(max-width:1100px){.fbar form[data-kind=flight] .fgrid.fmain{grid-template-columns:1fr 1fr!important}
 .fbar form[data-kind=flight] .fmain>.fcell{border-right:0!important;border-bottom:1px solid #e6e6e6!important;border-radius:0!important;min-height:0}
 .fbar form[data-kind=flight] .fmain>.fcell:nth-of-type(odd){border-right:1px solid #e6e6e6!important}
 .fbar form[data-kind=flight] .fmain>.fcell:first-of-type{border-radius:15px 0 0 0!important}.fbar form[data-kind=flight] .fmain>.fcell:nth-of-type(2){border-radius:0 15px 0 0!important}
 .fbar form[data-kind=flight] .fmain>.fcell:nth-last-of-type(-n+2){border-bottom:0!important}
 .fbar form[data-kind=flight] .fmain .fswap{left:50%;top:56px}
 .fbar form[data-kind=flight] .fcell.hascity:not(:focus-within) .fcity{font-size:24px}}
@media(max-width:700px){.ffh{width:100%}.ffare{gap:8px}.ffare label{min-width:0;flex:1 1 calc(50% - 8px)}
 .fbar form[data-kind=flight] .fmain .fdv b big,.fbar form[data-kind=flight] .fmain .fsum b big{font-size:24px!important}}

@media(max-width:1100px){.fbar form[data-kind=flight] .fgrid.fmain>.fcell{grid-column:auto!important}}
@media(max-width:700px){.fbar form[data-kind=flight] .fgrid.fmain>.fcell:nth-of-type(-n+2){grid-column:1/-1!important;border-right:0!important}
 .fbar form[data-kind=flight] .fmain>.fcell:first-of-type{border-radius:15px 15px 0 0!important}.fbar form[data-kind=flight] .fmain>.fcell:nth-of-type(2){border-radius:0!important}
 .fbar form[data-kind=flight] .fmain>.fcell:nth-of-type(3),.fbar form[data-kind=flight] .fmain>.fcell:nth-of-type(5){border-right:1px solid #e6e6e6!important}
 .fbar form[data-kind=flight] .fmain>.fcell:nth-of-type(4),.fbar form[data-kind=flight] .fmain>.fcell:nth-of-type(6){border-right:0!important}
 .fbar form[data-kind=flight] .fmain>.fcell:nth-of-type(5){border-radius:0 0 0 15px!important}.fbar form[data-kind=flight] .fmain>.fcell:nth-of-type(6){border-radius:0 0 15px 0!important}
 .fbar form[data-kind=flight] .fmain .fswap{display:flex!important;align-items:center;justify-content:center;left:auto;right:16px;top:98px;transform:rotate(90deg)}
 .fbar form[data-kind=flight] .fmain>.fcell{padding:12px 16px!important}.fbar form[data-kind=flight] .fcab select{font-size:18px}}

@media(min-width:1101px){.fbar form[data-kind=flight] .fmain>.fcell:nth-of-type(2){padding-left:32px!important}}

.fmsearch{display:none}.fmhint:empty{display:none}
@media(max-width:700px){.fmsearch{display:block;margin:4px 0 14px}.fmsearch .fgo{width:100%!important;height:52px!important;font-size:17px!important;border-radius:14px!important}.fmhint{margin:8px 2px 0;color:#b3121a;font-size:14px}
.fcontact{display:grid;gap:12px;background:#fff;border:1px solid var(--line);border-radius:16px;padding:14px;margin:0 0 14px;scroll-margin-top:140px}.fcontact[hidden]{display:none}.fct-t{margin:0;font-size:16px}
.fcontact .fgrid2{display:grid!important;grid-template-columns:1fr!important;border:0!important;padding:0!important;margin:0!important}.fsh-go{height:50px;width:100%;border-radius:12px;font-size:16px}}
"""
