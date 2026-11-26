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
    return f"""<section class="hero"><div class="wrap"><div><div class="crumbs"><a href="{root}">Home</a> › Car Rental</div><h1>Car Rental – India &amp; Abroad</h1><p>Airport transfers, outstation cabs, cars with driver and self-drive cars – in India and abroad, booked by one team.</p></div></div></section>
{svc_form}
<section><div class="wrap">
<div class="fxgrid">
<div class="fxcard"><span>🇮🇳</span><h3>Within India</h3><p>Airport pick-ups and drops, one-way and round-trip outstation cabs, local cars by the hour, and Tempo Travellers for groups – in cities across India.</p></div>
<div class="fxcard"><span>🌍</span><h3>Abroad</h3><p>Airport transfers in Dubai, Thailand, Singapore, Bali, Europe and more; cars with driver for sightseeing; and self-drive cars where you hold a valid licence.</p></div>
<div class="fxcard"><span>🧳</span><h3>With your trip</h3><p>Add cars to your flights, hotels and holiday package – one booking, one point of contact.</p></div>
</div>
<div class="fxsteps"><h2>How it works</h2><ol>
<li><b>Send your enquiry</b> – pick-up, drop, date and car type.</li>
<li><b>Get the fare</b> – we share the confirmed fare and what is included (fuel, tolls, parking, driver allowance).</li>
<li><b>Pay online</b> to confirm.</li>
<li><b>Get driver details</b> before your trip.</li></ol></div>
<div class="fxdocs"><h2>For self-drive cars abroad</h2><ul class="ticks"><li>Valid Indian driving licence (held for the period the rental company requires)</li><li>International Driving Permit where the country requires it</li><li>Passport and a credit card in the driver's name for the security deposit</li></ul></div>
<div class="faq" style="margin-top:22px"><h2>Car rental FAQs</h2>
<details><summary>Do you arrange airport pick-ups abroad?</summary><p>Yes – airport transfers can be arranged in most international cities. Share your flight number so the driver can track delays.</p></details>
<details><summary>Are tolls and parking included in outstation fares?</summary><p>It depends on the fare – we tell you exactly what is included before you pay.</p></details>
<details><summary>Can I book a car for the whole tour?</summary><p>Yes, a car with driver can be arranged for your full itinerary in India and in many countries abroad.</p></details>
<details><summary>Can I book a Tempo Traveller for a group?</summary><p>Yes – Tempo Travellers, mini buses and coaches are available for groups, family functions and yatras.</p></details>
</div></div></section>
{cta_band()}"""
