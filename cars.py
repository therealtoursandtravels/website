"""Car rental page (/car-rental/): domestic & international cabs, airport transfers, chauffeur cars and self-drive.
Booked by our team with trusted car partners in India and abroad."""

CAR_EXTRA = """<div class="sf-row"><label>Where?*<select name="x_reg" data-lbl="Region"><option>Within India</option><option>Abroad (international)</option></select></label>
<label>Type of booking*<select name="x_type" data-lbl="Booking"><option>Airport pick-up / drop</option><option>Outstation – round trip</option><option>Outstation – one way</option><option>Local car with driver (hourly / full day)</option><option>Car with driver for the whole tour</option><option>Self-drive car (abroad)</option></select></label></div>
<div class="sf-row"><label>Pick-up date &amp; time<input name="x_dt" data-lbl="Pick-up" type="datetime-local"></label>
<label>Drop / return date (if any)<input name="x_ret" data-lbl="Return" type="date"></label></div>
<div class="sf-row"><label>Car<select name="x_car" data-lbl="Car"><option value="">Please suggest</option><option>Hatchback / small car</option><option>Sedan (4 seats)</option><option>SUV (6–7 seats)</option><option>Innova Crysta</option><option>Tempo Traveller (12–17 seats)</option><option>Mini bus / coach</option><option>Luxury car</option></select></label>
<label>Flight number (for airport trips)<input name="x_flt" data-lbl="Flight" maxlength="12" placeholder="e.g. EK 501" autocomplete="off"></label></div>
<label class="sf-chk1"><input type="checkbox" name="x_child" value="Child seat needed"> Child seat needed</label>"""

CFG_ENTRY = ("Car rental", "Pick-up and drop (city, airport or hotel)", "e.g. Mumbai Airport T2 → Lonavala, or Dubai Airport → hotel", CAR_EXTRA)


def cars_page(root, svc_form, cta_band):
    from visa import SB_URL, SB_KEY
    return f"""<section class="hero"><div class="wrap"><div><div class="crumbs"><a href="{root}">Home</a> › Car Rental</div><h1>Car Rental – India &amp; Abroad</h1><p>Airport transfers, outstation cabs, cars with driver and self-drive cars – in India and abroad, booked by one team.</p></div></div></section>
{svc_form}
<section class="alt" id="carpay" hidden><div class="wrap" style="max-width:720px"><div class="paybox"><span class="kicker" style="justify-content:center">Secure payment</span><h2 style="margin:4px 0 10px">Pay for your car booking</h2>
<div id="cp_body" class="meta">Loading your quote…</div>
<div id="cp_pay" hidden><form><script src="https://checkout.razorpay.com/v1/payment-button.js" data-payment_button_id="pl_U3RKkNsxkSYwez" async></script></form>
<p style="font-size:13px;color:var(--muted);margin:6px 0 0">🔒 Secured by Razorpay · By paying you agree to our <a href="{root}terms/">Terms</a> and <a href="{root}cancellation-refund-policy/">Cancellation &amp; Refund Policy</a>.</p></div></div></div></section>
<script>(function(){{const ref=new URLSearchParams(location.search).get('pay');if(!ref)return;const sec=document.getElementById('carpay');sec.hidden=false;
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,x=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}})[x]);const inr=n=>'₹'+Number(n).toLocaleString('en-IN',{{maximumFractionDigits:2}});
const enq=document.getElementById('enquire');if(enq)enq.hidden=true;setTimeout(()=>sec.scrollIntoView({{behavior:'smooth'}}),300);
fetch("{SB_URL}/rest/v1/rpc/get_car_quote",{{method:'POST',headers:{{apikey:"{SB_KEY}",Authorization:"Bearer {SB_KEY}",'Content-Type':'application/json'}},body:JSON.stringify({{p_ref:ref}})}}).then(r=>r.json()).then(d=>{{const q=Array.isArray(d)&&d[0];const b=document.getElementById('cp_body');
 if(!q){{b.innerHTML='Sorry, we could not find this quote. Please WhatsApp us on <a href="https://wa.me/919843121212">98431 21212</a>.';return;}}
 if(q.status!=='sent'){{b.innerHTML='Quote <b>'+esc(q.ref)+'</b> is already <b>'+esc(q.status)+'</b>. For help, WhatsApp us on <a href="https://wa.me/919843121212">98431 21212</a>.';return;}}
 b.innerHTML='<table class="gtab"><tr><td>Reference</td><td><b>'+esc(q.ref)+'</b></td></tr>'+(q.customer_name?'<tr><td>Name</td><td>'+esc(q.customer_name)+'</td></tr>':'')+'<tr><td>Trip</td><td>'+esc(q.trip)+'</td></tr>'+(q.pickup_at?'<tr><td>Pick-up</td><td>'+esc(q.pickup_at)+'</td></tr>':'')+(q.car?'<tr><td>Car</td><td>'+esc(q.car)+'</td></tr>':'')+(q.pax?'<tr><td>Passengers</td><td>'+q.pax+'</td></tr>':'')+'<tr class="gtot"><td>Total to pay</td><td>'+inr(q.total)+'</td></tr></table><p class="gnote">In the payment window, enter <b>'+inr(q.total)+'</b> as the amount and <b>'+esc(q.ref)+'</b> as the reference. After paying, please WhatsApp the payment screenshot to <a href="https://wa.me/919843121212?text='+encodeURIComponent('Paid for car booking '+q.ref)+'">98431 21212</a> – we confirm your car and share driver details.</p>';
 document.getElementById('cp_pay').hidden=false;}}).catch(()=>{{document.getElementById('cp_body').textContent='Could not load your quote. Please WhatsApp us on 98431 21212.';}});}})();</script>
<section><div class="wrap">
<div class="fxgrid">
<div class="fxcard"><span>🇮🇳</span><h3>Within India</h3><p>Airport pick-ups and drops, one-way and round-trip outstation cabs, local cars by the hour, and Tempo Travellers for groups – in cities across India.</p></div>
<div class="fxcard"><span>🌍</span><h3>Abroad</h3><p>Airport transfers in Dubai, Thailand, Singapore, Bali, Europe and more; cars with driver for sightseeing; and self-drive cars where you hold a valid licence.</p></div>
<div class="fxcard"><span>🧳</span><h3>With your trip</h3><p>Add cars to your flights, hotels and holiday package – one booking, one point of contact.</p></div>
</div>
<div class="fxsteps"><h2>How it works</h2><ol>
<li><b>Send your enquiry</b> – pick-up, drop, date and car type.</li>
<li><b>Get the fare</b> – we send you a secure payment link with the confirmed fare and what is included (fuel, tolls, parking, driver allowance).</li>
<li><b>Pay online</b> through the link to confirm.</li>
<li><b>Get driver details</b> before your trip.</li></ol></div>
<div class="fxdocs"><h2>For self-drive cars abroad</h2><ul class="ticks"><li>Valid Indian driving licence (held for the period the rental company requires)</li><li>International Driving Permit where the country requires it</li><li>Passport and a credit card in the driver's name for the security deposit</li></ul></div>
<div class="faq" style="margin-top:22px"><h2>Car rental FAQs</h2>
<details><summary>Do you arrange airport pick-ups abroad?</summary><p>Yes – airport transfers can be arranged in most international cities. Share your flight number so the driver can track delays.</p></details>
<details><summary>Are tolls and parking included in outstation fares?</summary><p>It depends on the fare – we tell you exactly what is included before you pay.</p></details>
<details><summary>Can I book a car for the whole tour?</summary><p>Yes, a car with driver can be arranged for your full itinerary in India and in many countries abroad.</p></details>
<details><summary>Can I book a Tempo Traveller for a group?</summary><p>Yes – Tempo Travellers, mini buses and coaches are available for groups, family functions and yatras.</p></details>
</div></div></section>
{cta_band()}"""
