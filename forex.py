"""Forex page (/forex/): forex travel card & currency notes enquiry. Forex is issued by RBI-authorised partners;
The Real Tours and Travels only arranges it (referral model, no own forex licence)."""

FOREX_EXTRA = """<div class="sf-row"><label>What do you need?*<select name="x_prod" data-lbl="Product"><option>Forex travel card</option><option>Foreign currency notes</option><option>Card + some currency notes</option></select></label>
<label>Currency<select name="x_cur" data-lbl="Currency"><option value="">Please suggest</option><option>US Dollar (USD)</option><option>Euro (EUR)</option><option>UAE Dirham (AED)</option><option>British Pound (GBP)</option><option>Singapore Dollar (SGD)</option><option>Thai Baht (THB)</option><option>Australian Dollar (AUD)</option><option>Canadian Dollar (CAD)</option><option>Japanese Yen (JPY)</option><option>Multi-currency card</option><option>Other</option></select></label></div>
<div class="sf-row"><label>Approx. amount (in that currency)<input name="x_amt" data-lbl="Amount" maxlength="30" placeholder="e.g. 2,000 USD" autocomplete="off"></label>
<label>Purpose of travel<select name="x_pur" data-lbl="Purpose"><option>Holiday / private visit</option><option>Business trip</option><option>Study abroad</option><option>Medical treatment</option><option>Other</option></select></label></div>"""

CFG_ENTRY = ("Forex", "Country you are travelling to", "e.g. USA, Dubai, Europe, Thailand", FOREX_EXTRA)


def forex_page(root, svc_form, cta_band):
    return f"""<section class="hero"><div class="wrap"><div><div class="crumbs"><a href="{root}">Home</a> › Forex</div><h1>Forex Card &amp; Foreign Currency</h1><p>Get a forex travel card or foreign currency notes for your trip abroad – arranged with your flights, visa and insurance.</p></div></div></section>
{svc_form}
<section><div class="wrap">
<div class="fxgrid">
<div class="fxcard"><span>💳</span><h3>Forex travel card</h3><p>A prepaid card loaded with foreign currency. Pay in shops and withdraw cash at ATMs abroad, and top it up online during the trip.</p></div>
<div class="fxcard"><span>💵</span><h3>Currency notes</h3><p>Cash in the currency of your destination for taxis, tips and small shops – useful along with a card.</p></div>
<div class="fxcard"><span>🧳</span><h3>One place for your trip</h3><p>Flights, hotels, visa, travel insurance and forex – planned together by one team.</p></div>
</div>
<div class="fxsteps"><h2>How it works</h2><ol>
<li><b>Send your enquiry</b> – country, currency, amount and travel date.</li>
<li><b>Get the rate</b> – we share the current rate and charges before you decide.</li>
<li><b>Complete KYC</b> – passport, visa, ticket and PAN are verified by the issuing bank or authorised money changer.</li>
<li><b>Receive your card or notes</b> before you fly.</li></ol></div>
<div class="fxdocs"><h2>Documents usually needed</h2><ul class="ticks"><li>Passport (valid)</li><li>Valid visa for the country, where a visa is required</li><li>Air ticket for the trip</li><li>PAN card</li></ul></div>
<p class="fxnote">Forex cards and foreign currency are issued and loaded by RBI-authorised banks and money changers. The Real Tours and Travels helps you arrange them; the exchange rate and charges are confirmed by the issuer at the time of booking.</p>
<div class="faq" style="margin-top:22px"><h2>Forex FAQs</h2>
<details><summary>Is a forex card better than cash?</summary><p>For most trips, yes – it is safer than carrying a lot of cash and can be blocked if lost. Carry a small amount of cash as well for the first day.</p></details>
<details><summary>Can I reload the card during my trip?</summary><p>Yes, forex cards can be reloaded online while you are abroad.</p></details>
<details><summary>What happens to the money left on the card?</summary><p>You can keep it for your next trip or encash the balance back into rupees after you return.</p></details>
<details><summary>How early should I order forex?</summary><p>A few days before travel is ideal, once your visa and tickets are ready, so KYC goes smoothly.</p></details>
</div></div></section>
{cta_band()}"""

CSS = """
.fxgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px}
.fxcard{background:#fff;border:1px solid var(--line);border-radius:18px;padding:20px}.fxcard>span{font-size:28px}.fxcard h3{margin:6px 0;font-size:20px}.fxcard p{margin:0;color:var(--muted)}
.fxsteps,.fxdocs{margin-top:26px}.fxsteps ol{margin:0;padding-left:20px;display:grid;gap:6px}
.fxnote{margin-top:20px;padding:14px 16px;background:var(--bg);border:1px solid var(--line);border-radius:14px;color:var(--muted);font-size:14.5px}
"""
