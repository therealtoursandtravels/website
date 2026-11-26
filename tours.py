"""SEO landing pages: destination tour packages (/tours/<slug>/) and country visa guides (/visa/<slug>/)."""
import html, json, re

E = html.escape

DEST = [
 dict(slug="kashmir-tour-package", name="Kashmir", img="c-kashmir", type="India", nights="5 Nights / 6 Days",
  best="March–June for gardens and meadows; October for autumn colours; December–February for snow in Gulmarg",
  intro="Kashmir is the most-asked-for hill holiday in India – houseboats on Dal Lake, snow at Gulmarg, the Lidder river at Pahalgam and the Thajiwas glacier at Sonmarg. We plan Kashmir trips for families, honeymooners and senior citizens with trusted houseboats and hotels, a private cab and a relaxed pace.",
  days=["Arrive Srinagar – shikara ride on Dal Lake, night in a houseboat","Srinagar – Mughal Gardens (Nishat, Shalimar), Shankaracharya temple","Day trip to Gulmarg – gondola ride (on your own), snow activities","Pahalgam – Betaab Valley, Aru Valley, Chandanwari","Day trip to Sonmarg – Thajiwas glacier","Departure from Srinagar"],
  hl=["Houseboat stay and shikara ride","Gulmarg gondola (Phase 1 & 2)","Pahalgam valleys and pony rides","Jain and vegetarian food on request"],
  faqs=[("Is Kashmir safe for a family holiday?","Tourist areas like Srinagar, Gulmarg, Pahalgam and Sonmarg see lakhs of visitors every year. We plan with local partners we have worked with for years and keep in touch through the trip."),("When is the best time to see snow in Kashmir?","December to February in Gulmarg and Sonmarg; Gulmarg often has snow until March."),("Can you arrange Jain food in Kashmir?","Yes – we brief hotels in advance and choose places that can serve Jain and pure vegetarian food.")]),
 dict(slug="kerala-tour-package", name="Kerala", img="g-kerala", type="India", nights="5 Nights / 6 Days",
  best="September–March for pleasant weather; June–August for monsoon greenery and lower hotel rates",
  intro="Kerala – God's Own Country – combines tea hills in Munnar, wildlife and spice gardens in Thekkady, an overnight houseboat on the Alleppey backwaters and the old charm of Fort Kochi. It is ideal for families, couples and senior citizens who want a relaxed, green holiday.",
  days=["Arrive Kochi – drive to Munnar","Munnar – tea gardens, Eravikulam National Park, Mattupetty Dam","Thekkady – spice plantation, Periyar lake boat ride","Alleppey – overnight private houseboat on the backwaters","Kochi – Fort Kochi, Chinese fishing nets, Kathakali show","Departure from Kochi"],
  hl=["Overnight private houseboat","Munnar tea estates","Periyar wildlife boat ride","Ayurvedic massage on request"],
  faqs=[("How many days are enough for Kerala?","5–6 nights covers Munnar, Thekkady, Alleppey and Kochi comfortably. Add Kovalam or Varkala beaches with 2 more nights."),("Is a houseboat stay safe for kids and seniors?","Yes – we book licensed houseboats with a crew and cook; the boat docks for the night."),("Which airport should I fly to?","Kochi (COK) is best for this route; Thiruvananthapuram (TRV) suits trips that end at Kovalam.")]),
 dict(slug="manali-tour-package", name="Manali", img="c-trek", type="India", nights="4 Nights / 5 Days",
  best="March–June for summer; December–February for snow; avoid peak monsoon landslide weeks in July–August",
  intro="Manali is a favourite for families and honeymooners – snow at Solang Valley and Atal Tunnel, apple orchards, the old Hadimba temple and cafés in Old Manali. Combine it with Shimla or Kasol for a longer Himachal holiday.",
  days=["Arrive Manali (Volvo from Delhi or flight to Bhuntar) – rest","Manali local – Hadimba temple, Vashisht hot springs, Mall Road","Solang Valley and Atal Tunnel to Sissu (Rohtang Pass on permit days)","Naggar Castle and Kullu – river rafting on the Beas","Departure"],
  hl=["Snow point at Solang / Sissu","Atal Tunnel drive","River rafting in Kullu","Combine with Shimla"],
  faqs=[("Do I need a permit for Rohtang Pass?","Yes – Rohtang needs an online permit for each vehicle and is closed on Tuesdays; we arrange it with your cab."),("Is there snow in Manali in December?","Usually from late December to February at Solang and beyond the Atal Tunnel."),("Volvo or flight to Manali?","Overnight Volvo from Delhi is the most common; flights to Bhuntar (Kullu) save time but are weather-dependent.")]),
 dict(slug="leh-ladakh-tour-package", name="Leh Ladakh", img="c-ladakh", type="India", nights="6 Nights / 7 Days",
  best="May–September when roads to Nubra and Pangong are open",
  intro="Ladakh is a high-altitude desert of monasteries, blue lakes and the world's highest motorable passes. Our Ladakh trips include a full acclimatisation day, permits and experienced local drivers so the whole family travels safely.",
  days=["Arrive Leh – complete rest to acclimatise","Leh local – Shanti Stupa, Leh Palace, Hall of Fame","Sham valley – Magnetic Hill, Gurudwara Pathar Sahib, Sangam","Leh → Nubra via Khardung La – Hunder sand dunes","Nubra → Pangong Lake via Shyok route – camp by the lake","Pangong → Leh via Chang La – Thiksey and Hemis monasteries","Departure from Leh"],
  hl=["Acclimatisation planned in","Inner-line permits arranged","Camp at Pangong Lake","Monasteries of Thiksey and Hemis"],
  faqs=[("Is Ladakh suitable for senior citizens?","With a doctor's go-ahead, yes – we keep a slow pace, a full rest day on arrival and can carry oxygen in the cab."),("Do Indians need permits for Ladakh?","Yes – inner-line permits for Nubra and Pangong; we arrange them for you."),("Can we drive to Ladakh from Manali?","Yes, from June to September; we plan the Manali–Leh road trip with a night halt at Jispa or Sarchu.")]),
 dict(slug="goa-tour-package", name="Goa", img="c-honeymoon", type="India", nights="3 Nights / 4 Days",
  best="November–February for beaches and nightlife; monsoon (June–September) for greenery and quiet resorts",
  intro="Goa is the easiest beach holiday from anywhere in India – sunny beaches in the north, quiet resorts in the south, Portuguese churches in Old Goa and great seafood and vegetarian food alike.",
  days=["Arrive Goa – check in, evening at the beach","North Goa – Fort Aguada, Calangute, Baga, Anjuna, Chapora","South Goa – Old Goa churches, Miramar, Colva and Palolem; river cruise","Departure"],
  hl=["Beach resorts for families and couples","North and South Goa sightseeing","Mandovi river cruise","Water sports on request"],
  faqs=[("North Goa or South Goa?","North Goa is lively with beaches, markets and nightlife; South Goa is quieter with cleaner beaches and luxury resorts."),("Is Goa good in the monsoon?","Yes for a relaxed, green holiday with lower prices; sea activities stop from June to September."),("Can you arrange Jain food in Goa?","Yes – we choose hotels that can serve Jain and pure vegetarian meals.")]),
 dict(slug="rajasthan-tour-package", name="Rajasthan", img="g-jaipur", type="India", nights="6 Nights / 7 Days",
  best="October–March",
  intro="Rajasthan is forts, palaces and desert camps – Jaipur, Udaipur, Jodhpur and Jaisalmer. We plan heritage hotels, camel safaris and comfortable drives for families, groups and senior citizens.",
  days=["Arrive Jaipur – Hawa Mahal, City Palace, Jantar Mantar","Amber Fort, Jal Mahal, local bazaars","Jaipur → Udaipur – City Palace, Lake Pichola boat ride","Udaipur → Jodhpur via Ranakpur Jain temple","Jodhpur – Mehrangarh Fort → Jaisalmer","Jaisalmer fort, Patwon ki Haveli, Sam dunes camel safari and desert camp","Departure"],
  hl=["Ranakpur Jain temple on the way","Desert camp with cultural evening","Heritage hotel stays","Lake Pichola boat ride"],
  faqs=[("How many days do I need for Rajasthan?","6–8 nights covers Jaipur, Udaipur, Jodhpur and Jaisalmer; 4 nights covers the Golden Triangle with Agra."),("Is Rajasthan hot in summer?","Yes – April to June is very hot; October to March is best."),("Can we visit Jain temples in Rajasthan?","Yes – Ranakpur, Dilwara (Mount Abu) and Jaisalmer Jain temples fit easily into the route.")]),
 dict(slug="andaman-tour-package", name="Andaman", img="g-maldives", type="India", nights="5 Nights / 6 Days",
  best="October–May",
  intro="The Andaman Islands have India's clearest water – Radhanagar beach on Havelock, coral at Neil Island and the history of the Cellular Jail in Port Blair. Great for honeymooners and families who love the sea.",
  days=["Arrive Port Blair – Corbyn's Cove, Cellular Jail light & sound show","Ferry to Havelock – Radhanagar beach sunset","Havelock – Elephant beach snorkelling","Ferry to Neil Island – Bharatpur beach, natural bridge","Back to Port Blair – Ross Island","Departure"],
  hl=["Private ferry tickets booked in advance","Snorkelling at Elephant beach","Radhanagar beach","Scuba diving on request"],
  faqs=[("Do I need a permit for Andaman?","Indian citizens do not need a permit for Port Blair, Havelock and Neil."),("Which ferry is best?","Private ferries like Makruzz or Nautika are faster and more comfortable; we book them in advance."),("Is Andaman good for kids?","Yes – calm beaches, glass-bottom boats and short ferry rides.")]),
 dict(slug="char-dham-yatra-package", name="Char Dham Yatra", img="c-yatra", type="Yatra", nights="9 Nights / 10 Days",
  best="May–June and September–October (temples open late April/May to Diwali)",
  intro="The Char Dham Yatra covers Yamunotri, Gangotri, Kedarnath and Badrinath in Uttarakhand. We handle registration, hotels near the temples, helicopter or pony bookings where needed and a pace that suits senior citizens.",
  days=["Haridwar – Ganga aarti at Har Ki Pauri","Haridwar → Barkot","Yamunotri darshan (trek, pony or palki)","Barkot → Uttarkashi","Gangotri darshan","Uttarkashi → Guptkashi / Sitapur","Kedarnath darshan (trek, pony or helicopter)","Guptkashi → Badrinath darshan","Badrinath → Rudraprayag / Srinagar (Garhwal)","Return to Haridwar"],
  hl=["Yatra registration help","Helicopter / pony / palki bookings","Pure vegetarian meals","Senior-citizen friendly pace"],
  faqs=[("Is registration compulsory for Char Dham?","Yes – every pilgrim must register with the Uttarakhand government; we help you do it."),("Can senior citizens do the Char Dham Yatra?","Yes – with ponies, palkis or helicopters for Yamunotri and Kedarnath, and a slower itinerary."),("Do you do Do Dham (Kedarnath–Badrinath) only?","Yes – a 5–6 night Do Dham yatra is very popular.")]),
 dict(slug="jain-yatra-package", name="Jain Yatra with Maharaj", img="c-jain", type="Yatra", nights="6 Nights / 7 Days",
  best="October–March",
  intro="Our Jain yatras travel with our own Maharaj who cooks pure Jain food throughout the trip – no onion, garlic or root vegetables, and meals served before sunset. Popular routes include Shikharji (Sammed Shikharji), Palitana, Girnar and the Rajasthan Jain temples.",
  days=["Arrive Kolkata / Ranchi – travel to Madhuban","Shikharji parvat vandana (doli available)","Rest day in Madhuban – temples","Pawapuri Jal Mandir","Rajgir temples and hills","Kundalpur and Nalanda","Departure"],
  hl=["Our own Maharaj – pure Jain food","Choviyar (before sunset) meals","Dharamshala or hotel stays near temples","Groups and families"],
  faqs=[("Is the food really pure Jain throughout?","Yes – our Maharaj travels with the group and cooks every meal: no onion, garlic or root vegetables."),("Which Jain yatras do you run?","Shikharji, Palitana, Girnar, Rajasthan Jain temples (Ranakpur, Dilwara), South India Jain temples and custom routes."),("Can you arrange a doli for Shikharji?","Yes – we book dolis for elders who cannot walk the full parvat.")]),
 dict(slug="dubai-tour-package", name="Dubai", img="g-dubai", type="International", nights="4 Nights / 5 Days",
  best="November–March",
  intro="Dubai is the number-one family holiday abroad from India – desert safari, Burj Khalifa, theme parks, shopping and an easy short flight. We arrange the visa, hotel, transfers and tours together.",
  days=["Arrive Dubai – evening dhow cruise dinner at the Marina","Dubai city tour – Burj Khalifa 124th floor, Dubai Mall fountain","Desert safari with BBQ dinner","Abu Dhabi day trip – grand mosque, Ferrari World or Yas Island (optional)","Departure"],
  hl=["Visa assistance included","Desert safari","Burj Khalifa","Theme parks on request"],
  faqs=[("How early should I apply for the Dubai visa?","At least 2–3 weeks before travel."),("Is Dubai good for kids?","Yes – theme parks, aquariums, beaches and desert safaris make it ideal for families."),("Can you arrange vegetarian or Jain food in Dubai?","Yes – Dubai has many Indian vegetarian restaurants and we can include meals.")]),
 dict(slug="thailand-tour-package", name="Thailand", img="c-safari", type="International", nights="5 Nights / 6 Days",
  best="November–April",
  intro="Thailand offers beaches, islands, temples and shopping at great value – Bangkok and Pattaya for first-timers, Phuket and Krabi for island hopping. Indian travellers must file the Thailand Digital Arrival Card (TDAC) before arrival – we take care of it with your booking.",
  days=["Arrive Bangkok – transfer to Pattaya","Pattaya – Coral Island by speedboat","Pattaya – Nong Nooch garden / Tiger park → Bangkok","Bangkok – temple and city tour, shopping","Bangkok – Safari World and Marine Park","Departure"],
  hl=["TDAC arrival card help","Coral Island speedboat","Safari World","Phuket & Krabi add-ons"],
  faqs=[("What documents do Indians need for Thailand?","A passport valid for 6 months, return tickets, hotel bookings and the Thailand Digital Arrival Card (TDAC) filed within 3 days before arrival. Entry rules can change – we confirm the current rules before you travel."),("Pattaya or Phuket?","Pattaya with Bangkok suits first-timers; Phuket and Krabi are better for beaches and islands."),("Is Thailand good for vegetarians?","Yes – Bangkok, Pattaya and Phuket have many Indian vegetarian restaurants.")]),
 dict(slug="bali-tour-package", name="Bali", img="g-bali", type="International", nights="5 Nights / 6 Days",
  best="April–October (dry season)",
  intro="Bali is a top honeymoon and family destination – rice terraces and temples in Ubud, cliff-top Uluwatu, beach clubs in Seminyak and day trips to Nusa Penida. Private villas with pools are great value.",
  days=["Arrive Bali – Kuta / Seminyak","Ubud – rice terraces, monkey forest, swing","Kintamani volcano view and coffee plantation","Nusa Penida island day tour","Uluwatu temple sunset and Kecak dance","Departure"],
  hl=["Private pool villa options","Nusa Penida day trip","Ubud rice terraces","Honeymoon inclusions on request"],
  faqs=[("Do Indians need a visa for Bali?","Yes – Indian passport holders need a visa for Indonesia; we help with the documents."),("Is Bali good for a honeymoon?","Yes – private pool villas, sunsets and candle-light dinners make it one of the best."),("How many days for Bali?","5–6 nights covers Ubud, Kintamani, Nusa Penida and the beaches.")]),
 dict(slug="singapore-tour-package", name="Singapore", img="c-wedding", type="International", nights="4 Nights / 5 Days",
  best="All year (February–April is driest)",
  intro="Singapore is clean, safe and full of attractions for every age – Sentosa, Universal Studios, Gardens by the Bay and the Night Safari. It combines well with Malaysia or a cruise.",
  days=["Arrive Singapore – evening at Marina Bay","City tour, Gardens by the Bay, Singapore Flyer","Sentosa – cable car, SEA Aquarium, Wings of Time","Universal Studios Singapore / Night Safari","Departure"],
  hl=["Visa assistance included","Universal Studios","Sentosa island","Add a cruise or Malaysia"],
  faqs=[("How early should I apply for the Singapore visa?","At least 3–4 weeks before travel."),("Is Singapore good for senior citizens?","Yes – excellent public transport, clean streets and lots of vegetarian food."),("Can we combine Singapore and Malaysia?","Yes – a 6–7 night Singapore–Malaysia trip is very popular.")]),
 dict(slug="maldives-tour-package", name="Maldives", img="g-maldives", type="International", nights="4 Nights / 5 Days",
  best="November–April",
  intro="The Maldives is the classic island escape – water villas, coral reefs and white sand. We help you choose the right resort, meal plan and transfer (speedboat or seaplane) for your budget.",
  days=["Arrive Malé – speedboat / seaplane to the resort","Resort day – snorkelling on the house reef","Sunset cruise / dolphin trip","Spa or water sports day","Departure"],
  hl=["Beach or water villa","Meal plans up to all-inclusive","Seaplane or speedboat transfers","Honeymoon inclusions"],
  faqs=[("What documents do Indians need for the Maldives?","A passport valid for 6 months, a confirmed resort booking, return tickets and the IMUGA traveller declaration filed before travel – we help with all of it."),("Which meal plan should I choose?","Full board or all-inclusive is usually best value because resort restaurants are the only option on most islands."),("Speedboat or seaplane?","Resorts near Malé use speedboats; farther atolls need a seaplane – it's part of the experience but costs more.")]),
 dict(slug="europe-tour-package", name="Europe (Switzerland & Paris)", img="g-swiss", type="International", nights="7 Nights / 8 Days",
  best="April–October; December for Christmas markets",
  intro="Switzerland and Paris are the dream Europe trip – the Eiffel Tower, Jungfraujoch (Top of Europe), Mt. Titlis and Lake Lucerne. We plan Schengen visa documents, Swiss Travel Pass, hotels and Indian / Jain meals.",
  days=["Arrive Paris – Seine river cruise","Paris – Eiffel Tower, Louvre, Montmartre","Disneyland Paris or Versailles","Train to Switzerland – Interlaken","Jungfraujoch – Top of Europe","Lucerne – Mt. Titlis","Zurich – Rhine Falls","Departure"],
  hl=["Schengen visa documents help","Swiss Travel Pass","Jungfraujoch & Mt. Titlis","Indian / Jain meals arranged"],
  faqs=[("When should I apply for the Schengen visa?","Apply 6–8 weeks before travel; appointments fill fast in April–June."),("Is Europe good for senior citizens?","Yes – trains and lifts make Switzerland easy; we keep hotel changes to a minimum."),("Can you arrange Jain food in Europe?","Yes – we plan Indian restaurants and Jain meal packs in advance.")]),
 dict(slug="sri-lanka-tour-package", name="Sri Lanka", img="g-kerala", type="International", nights="5 Nights / 6 Days",
  best="December–April for the west and south coast; May–September for the east coast",
  intro="Sri Lanka is close, affordable and beautiful – the Ramayana trail, Kandy's Temple of the Tooth, tea country at Nuwara Eliya and beaches at Bentota. A great first international trip for families.",
  days=["Arrive Colombo – Kandy, Pinnawala elephant orphanage","Kandy – Temple of the Tooth, botanical garden","Nuwara Eliya – tea estates, Ramayana sites (Sita Amman temple)","Bentota – beach, river safari","Colombo city tour and shopping","Departure"],
  hl=["Ramayana trail temples","Tea country","Beach stay","Short flight from India"],
  faqs=[("Do Indians need a visa for Sri Lanka?","Yes – Indian travellers need an entry authorisation before travel; we help with the documents."),("Is Sri Lanka good for vegetarians?","Yes – plenty of South and North Indian vegetarian food is available."),("How many days for Sri Lanka?","5–7 nights covers Kandy, Nuwara Eliya and the beaches.")]),
]

def _wa(n):
    return "https://wa.me/919843121212?text=" + __import__("urllib.parse").parse.quote(f"Hi The Real Tours and Travels, I want a quote for a {n} trip. Travel date:  Travellers: ")

def dest_page(d, root):
    days = "".join(f'<li><b>Day {i+1}</b> – {E(x)}</li>' for i, x in enumerate(d["days"]))
    hl = "".join(f"<li>{E(x)}</li>" for x in d["hl"])
    faqs = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in d["faqs"])
    others = "".join(f'<a class="tlink" href="{root}tours/{o["slug"]}/">{E(o["name"])}</a>' for o in DEST if o is not d)
    body = f"""<section class="hero"><div class="wrap"><div><div class="crumbs"><a href="{root}">Home</a> › <a href="{root}holiday-packages/">Holiday Packages</a> › {E(d['name'])}</div>
<h1>{E(d['name'])} Tour Package</h1><p>{E(d['intro'])}</p></div></div></section>
<section class="tsec"><div class="wrap tgrid">
<div class="tmain">
<div class="tfacts"><div><small>Duration</small><b>{E(d['nights'])}</b></div><div><small>Best time</small><b>{E(d['best'].split(';')[0])}</b></div><div><small>Price</small><b>On request</b></div></div>
<h2>Sample {E(d['name'])} itinerary</h2><ol class="tdays">{days}</ol>
<p class="meta">Every trip is customised – add or remove days, change hotels or add flights, visas and insurance.</p>
<h2>Highlights</h2><ul class="ticks">{hl}</ul>
<h2>Best time to visit {E(d['name'])}</h2><p>{E(d['best'])}.</p>
<h2>{E(d['name'])} – frequently asked questions</h2><div class="faq tfaq">{faqs}</div>
</div>
<aside class="tside"><div class="tbook"><b>Plan your {E(d['name'])} trip</b><p class="meta">Tell us your dates and travellers – we reply with a detailed itinerary and price.</p>
<a class="btn gold" href="{root}customize-your-package/">✨ Customise this trip</a><a class="btn outline" href="{_wa(d['name'])}" target="_blank" rel="noopener">💬 Get a quote on WhatsApp</a><a class="btn ghost" href="tel:+919843121212">📞 Call 98431 21212</a>
<p class="meta">🎁 Earn 500 reward points on holiday packages. <a href="{root}offers/">Offers</a></p></div></aside>
</div></section>
<section class="alt"><div class="wrap"><h2>More holiday ideas</h2><div class="tlinks">{others}</div></div></section>"""
    ld = [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faqs"]]},
          {"@context": "https://schema.org", "@type": "TouristTrip", "name": f"{d['name']} Tour Package", "description": d["intro"], "touristType": "Families, couples, groups",
           "itinerary": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": x} for i, x in enumerate(d["days"])]},
           "provider": {"@type": "TravelAgency", "name": "The Real Tours and Travels", "telephone": "+91-98431-21212", "url": "https://www.therealtoursandtravels.com/"}}]
    return body, ld

def _slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

VISA_SLUG = {"uae": "dubai-uae", "uk": "uk", "usa": "usa", "schengen": "schengen", "southkorea": "south-korea", "newzealand": "new-zealand", "srilanka": "sri-lanka", "hongkong": "hong-kong"}

def visa_pages(ITEMS, clean_docs, WHEN, CARD_WHEN, BIOMETRICS, ENTRY, catalog):
    """Return list of (slug, name, flag, card, body, ld)."""
    cat = {k["code"]: k for k in catalog.get("countries", [])}
    out = []
    for (c, f, n, _how, docs) in ITEMS:
        if c in ("nepal",):
            continue
        slug = VISA_SLUG.get(c, _slug(n.split("/")[0]))
        card = ENTRY.get(c, ("visa",))[0] == "card"
        what = "Arrival Card" if card else "Visa"
        nm = n.replace(" / UAE", "").strip()
        dl = clean_docs(docs)
        when = (CARD_WHEN.get(c) if card else WHEN.get(c)) or "as early as possible – at least 3–4 weeks before travel"
        bio = BIOMETRICS.get(c)
        opts = cat.get(c, {}).get("options", [])
        def price(o):
            return f'₹{(o["price"] + 295):,}' if o.get("price") else "On request"
        rows = "".join(f'<tr><td>{E(o["name"])}{" ("+E(o["entry"].lower())+" entry)" if o.get("entry") in ("Single","Multiple") else ""}</td><td>{E(o["stay"])}</td><td>{E(o["proc"])}</td><td>{price(o)}</td></tr>' for o in opts[:8])
        table = f'<h2>{E(nm)} visa options &amp; price</h2><div style="overflow:auto"><table class="vtab2"><thead><tr><th>Visa</th><th>Stay</th><th>Processing</th><th>Price per person*</th></tr></thead><tbody>{rows}</tbody></table></div><p class="meta">*Includes the visa fee and our service charge with GST. Prices can change with embassy fees – confirmed before you pay.</p>' if opts else ""
        faqs = [(f"How early should I apply for the {nm} {what.lower()}?", f"Apply {when}."),
                (f"What documents do I need for the {nm} {what.lower()}?", "; ".join(re.sub('<[^>]+>', '', x) for x in dl[:6]) + "."),
                (f"Can I apply for the {nm} {what.lower()} through The Real Tours and Travels?", "Yes – choose the visa on our Visa page, upload your documents securely and pay online. Our visa team checks everything and keeps you updated on WhatsApp.")]
        if bio:
            faqs.insert(2, (f"Are biometrics needed for the {nm} visa?", bio + "."))
        fq = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faqs)
        body = f"""<section class="hero"><div class="wrap"><div><div class="crumbs"><a href="../../">Home</a> › <a href="../">Visa</a> › {E(nm)}</div>
<h1>{f} {E(nm)} {what} for Indians</h1><p>Documents required, when to apply{', biometrics' if bio else ''} and {'price' if opts else 'how to apply'} for the {E(nm)} {what.lower()} – checked and updated by our visa team.</p></div></div></section>
<section class="tsec"><div class="wrap tgrid"><div class="tmain">
<div class="tfacts"><div><small>Apply</small><b>{E(when.split('(')[0].strip())}</b></div>{f'<div><small>Biometrics</small><b>{E(bio.split("–")[0].strip())}</b></div>' if bio else ''}<div><small>Apply from</small><b>Anywhere in India</b></div></div>
{table}
<h2>Documents required</h2><ul class="ticks">{''.join(f'<li>{x}</li>' for x in dl)}</ul>
<h2>{E(nm)} {what.lower()} – frequently asked questions</h2><div class="faq tfaq">{fq}</div></div>
<aside class="tside"><div class="tbook"><b>Apply for your {E(nm)} {what.lower()}</b><p class="meta">Choose your visa, upload documents and pay online – our team takes it from there.</p>
<a class="btn gold" href="../?country={c}#find">Apply now</a><a class="btn ghost" href="tel:+919843121212">📞 Call 98431 21212</a><p class="meta">🎁 Earn reward points on every visa. <a href="../../offers/">Offers</a></p></div></aside>
</div></section>"""
        ld = [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}]
        out.append((slug, nm, f, card, body, ld))
    return out

CSS = """
.tsec{padding-top:28px!important}
.tgrid{display:grid;grid-template-columns:1fr 320px;gap:28px;align-items:start}
.tmain h2{margin:26px 0 10px;font-size:clamp(22px,2.6vw,28px)}
.tfacts{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}.tfacts>div{background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px 14px;display:grid}.tfacts small{color:var(--muted);font-size:12.5px}.tfacts b{font-size:15.5px}
.tdays{padding-left:0;list-style:none;display:grid;gap:8px;counter-reset:d}.tdays li{background:#fff;border:1px solid var(--line);border-left:4px solid var(--red);border-radius:10px;padding:10px 14px}
.tside{position:sticky;top:170px}.tbook{background:#fff;border:1px solid var(--line);border-radius:18px;padding:18px;display:grid;gap:10px;box-shadow:0 12px 30px rgba(60,20,25,.08)}.tbook>b{font-size:18px}.tbook .btn{justify-content:center}
.tlinks{display:flex;flex-wrap:wrap;gap:8px}.tlink{border:1px solid var(--line);background:#fff;border-radius:999px;padding:8px 14px;text-decoration:none;color:var(--ink)}.tlink:hover{border-color:var(--red);color:var(--red)}
.tfaq details{background:#fff}
.vtab2{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line)}.vtab2 th,.vtab2 td{padding:9px 12px;border-bottom:1px solid var(--line);text-align:left;font-size:14.5px}.vtab2 th{background:var(--bg)}
@media(max-width:900px){.tgrid{grid-template-columns:1fr}.tside{position:static}}
"""
