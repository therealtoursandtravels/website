#!/usr/bin/env python3
"""Static site generator for The Real Tours and Travels (SEO site)."""
import json, os, datetime
from articles import ARTICLES
from visa import visa_page, passport_page, VISA_CSS
from planner import planner_page, PLANNER_CSS
from flights import flight_widget, FLIGHT_CSS
from tools import gst_tool_page, TOOL_CSS

SITE = "https://www.therealtoursandtravels.com"
NAME = "The Real Tours and Travels"
PHONE = "+91 98431 21212"
PHONE_RAW = "+919843121212"
EMAIL = "enquiry@therealtoursandtravels.com"
WA = "https://wa.me/919843121212?text=Hi%20The%20Real%20Tours%20and%20Travels%2C%20I%27d%20like%20to%20plan%20a%20trip"
IG = "https://www.instagram.com/therealtoursandtravels/"
FB = "https://www.facebook.com/657186054138837"
MAPS = "https://maps.google.com/maps?cid=6174258107225017089"
REVIEW = "https://search.google.com/local/writereview?placeid=ChIJn8v1TlS45zsRAQu5MAlfr1U"
ADDR = ["204, B10, Rachana Building", "Govardhan Nagar, Lal Bahadur Shastri Marg", "Mulund West, Mumbai 400080"]
GST = "27AMUPK4723E1ZU"
TODAY = datetime.date.today().isoformat()

SERVICES = [
 dict(slug="domestic-holiday-packages", short="Domestic Holidays", icon="🏔️", img="gulmarg.jpg",
  title="Domestic Holiday Packages from Mumbai | Kashmir, Kerala, Manali",
  h1="Domestic Holiday Packages from Mumbai",
  desc="Family-friendly domestic holiday packages from Mumbai to Kashmir, Kerala, Manali, Shimla, Goa, Rajasthan, Andaman and the North East. Planned by The Real Tours and Travels, Mulund West, since 1981.",
  intro="India has a holiday for every family, every season and every budget. From the snow of Kashmir and Manali to the backwaters of Kerala and the beaches of Goa and the Andamans, we plan complete domestic holidays from Mumbai with flights or trains, hotels, private cab transfers and sightseeing – so all you have to do is pack.",
  points=["Kashmir – Srinagar houseboats, Gulmarg, Pahalgam and Sonamarg","Himachal – Manali, Shimla, Dharamshala and the Atal Tunnel","Kerala – Munnar, Thekkady, Alleppey houseboats and Kovalam","Rajasthan – Jaipur, Udaipur, Jodhpur and Jaisalmer","Goa, Andaman, Darjeeling–Gangtok, Ladakh and the North East","Weekend getaways near Mumbai – Lonavala, Mahabaleshwar, Matheran"],
  why="Every itinerary is checked for travel time, kid- and senior-friendly pacing and good-quality family hotels. You get one point of contact who is on call throughout the trip.",
  faqs=[("Which is the best domestic holiday for a family from Mumbai in winter?","December–February is ideal for snow in Kashmir and Manali, and for pleasant weather in Kerala, Goa and Rajasthan. Call us and we will suggest the best fit for your dates and family."),
        ("Do your packages include flights or trains from Mumbai?","Yes. We can include flights or train tickets from Mumbai, or plan land-only packages if you prefer to book travel yourself."),
        ("Can you arrange Jain or vegetarian food on domestic tours?","Yes. We regularly arrange pure vegetarian and Jain food, and offer special Jain yatra tours with our own Maharaj.")]),
 dict(slug="international-holiday-packages", short="International Holidays", icon="🌍", img="dubai.jpg",
  title="International Holiday Packages from Mumbai | Dubai, Thailand, Bali, Europe",
  h1="International Holiday Packages from Mumbai",
  desc="International tour packages from Mumbai to Dubai, Thailand, Bali, Singapore, Malaysia, Vietnam, Sri Lanka, Maldives, Europe and more – with flights, hotels, visas and travel insurance handled by The Real Tours and Travels.",
  intro="Travelling abroad with family should be exciting, not stressful. We plan international holidays end to end – flights from Mumbai, visas, hotels, transfers, sightseeing, travel insurance and forex – and stay in touch with you throughout the trip.",
  points=["Dubai & Abu Dhabi – desert safari, Burj Khalifa, theme parks","Thailand – Bangkok, Pattaya, Phuket and Krabi","Bali, Singapore, Malaysia and Vietnam","Sri Lanka, Maldives and Mauritius","Europe – Switzerland, Paris, Italy, London and Scandinavia","Japan, Australia, New Zealand and the USA"],
  why="Since 1981 we have sent thousands of Mumbai families abroad. We take care of the paperwork you worry about – visas, insurance, arrival cards – and suggest family-friendly hotels in the right locations.",
  faqs=[("Do you help with visas for international packages?","Yes. Our visa team guides you on documents and files tourist visas for Dubai, Singapore, Schengen/Europe, UK, USA, Australia and more."),
        ("Can you customise an international package?","Absolutely. Every package can be changed – hotels, number of nights, activities and pace – to suit your family."),
        ("Do you provide vegetarian and Jain food abroad?","We can recommend and pre-arrange vegetarian and Jain meals in most popular destinations.")]),
 dict(slug="passport-visa-services", short="Passport & Visa", icon="🛂", img="passport.jpg",
  title="Passport & Visa Services in Mulund, Mumbai | Tourist Visa Assistance",
  h1="Passport & Visa Services in Mulund, Mumbai",
  desc="Fresh passport and renewal appointments, and tourist and business visa assistance for Dubai, Singapore, Thailand, Schengen, UK, USA, Canada and Australia. Visit The Real Tours and Travels, Mulund West.",
  intro="Visa rules change often and a small mistake in documents can delay your trip. Our team in Mulund West helps you prepare the right documents, books appointments and tracks your application – for passports and visas alike.",
  points=["Fresh passport and passport renewal appointment assistance","Tourist and business visas – Dubai/UAE, Singapore, Thailand, Malaysia","Schengen (Europe), UK, USA, Canada, Australia and New Zealand visas","e-Visas and arrival cards, including the Thailand Digital Arrival Card","Document checklist, form filling and appointment booking","Travel insurance required for Schengen and other visas"],
  why="We have been handling visas for Mumbai travellers for decades, so we know what embassies look for and how to present your file correctly.",
  faqs=[("How early should I apply for a Schengen or UK visa?","Ideally 6–8 weeks before travel, especially in peak season. Contact us early and we will plan the timeline."),
        ("Can you help with a passport renewal?","Yes. We help with the online form, documents and Passport Seva appointment booking for fresh and renewal passports."),
        ("Do you guarantee visa approval?","No agent can guarantee a visa – the decision is the embassy's. We make sure your application is complete and correctly presented to give it the best chance.")]),
 dict(slug="travel-insurance", short="Travel Insurance", icon="🛡️", img="flight.jpg",
  title="Travel Insurance for International & Domestic Trips | Mumbai",
  h1="Travel Insurance for Every Trip",
  desc="Overseas and domestic travel insurance for families, seniors and students – medical cover, trip cancellation, lost baggage and Schengen-compliant policies. Arranged by The Real Tours and Travels, Mumbai.",
  intro="A medical emergency or lost baggage abroad can be expensive and stressful. The right travel insurance protects your family and your holiday. We help you choose a suitable policy and issue it quickly.",
  points=["Overseas medical and hospitalisation cover","Trip cancellation, delay and missed connection","Loss of baggage and passport","Senior citizen and family floater policies","Schengen-compliant policies for visa applications","Student and multi-trip annual policies"],
  why="We explain what is and isn't covered in simple language, so you can choose with confidence.",
  faqs=[("Is travel insurance compulsory?","It is mandatory for Schengen visas and some other countries, and strongly recommended for every international trip."),
        ("Can senior citizens get travel insurance?","Yes, there are policies designed for senior travellers. We will help you find suitable cover."),
        ("How quickly can a policy be issued?","Usually the same day once we have your travel details.")]),
 dict(slug="yatra-tours", short="Yatra Tours", icon="🛕", img=None,
  title="Yatra Tour Packages from Mumbai | Char Dham, Kedarnath, Vaishno Devi",
  h1="Yatra & Pilgrimage Tour Packages from Mumbai",
  desc="Pilgrimage yatra packages from Mumbai – Char Dham, Kedarnath, Badrinath, Vaishno Devi, Amarnath, Kashi, Ayodhya, Shirdi, Dwarka and Jain tirth yatras – with comfortable stays and senior-friendly planning.",
  intro="A yatra is a journey of faith, and it deserves careful planning. We organise comfortable, well-paced pilgrimage tours for families, senior citizens and groups, taking care of travel, stays, darshan planning and food.",
  points=["Char Dham Yatra – Yamunotri, Gangotri, Kedarnath, Badrinath","Vaishno Devi and Amarnath Yatra","Kashi Vishwanath, Prayagraj and Ayodhya","Shirdi, Trimbakeshwar and Jyotirlinga tours","Dwarka, Somnath and Gujarat pilgrimages","Jain tirth yatras – Palitana, Shikharji, Girnar, Ranakpur"],
  why="We plan yatras with senior citizens in mind – sensible daily distances, clean stays and help with helicopter, pony or palki bookings where available.",
  faqs=[("Are your yatras suitable for senior citizens?","Yes. We pace itineraries for elders and can arrange assistance where needed."),
        ("Do you arrange group yatras?","Yes, for families, societies and community groups of any size."),
        ("Can you arrange Jain food on yatras?","Yes – see our Jain Yatra Tours with Maharaj for pure Jain food throughout the trip.")]),
 dict(slug="group-tours", short="Group Tours", icon="👨‍👩‍👧‍👦", img=None,
  title="Group Tour Packages from Mumbai | Family, Society & Corporate Groups",
  h1="Group Tours for Families, Friends & Societies",
  desc="Group tour packages from Mumbai for extended families, friends, housing societies, women-only and senior citizen groups – in India and abroad. Planned by The Real Tours and Travels.",
  intro="Travelling as a group is more fun – and more complicated to plan. We handle the coordination: transport, rooms, meals, sightseeing and a single itinerary that works for everyone.",
  points=["Extended family and friends' trips","Housing society and community group tours","Women-only and senior citizen group tours","School, college and educational trips","Group yatras and pilgrimages","Corporate offsites (see FIT & MICE)"],
  why="One coordinator, one plan and clear communication for the whole group – before and during the trip.",
  faqs=[("What is the minimum size for a group tour?","We plan for groups of all sizes, from 8–10 people to large community groups."),
        ("Can you arrange a coach or tempo traveller?","Yes, along with drivers and tour managers where needed."),
        ("Do you offer women-only tours?","Yes, we plan women-only and senior citizen group tours.")]),
 dict(slug="honeymoon-packages", short="Honeymoon", icon="💑", img=None,
  title="Honeymoon Packages from Mumbai | Maldives, Bali, Kashmir, Europe",
  h1="Honeymoon Packages from Mumbai",
  desc="Romantic honeymoon packages from Mumbai to the Maldives, Bali, Thailand, Mauritius, Switzerland, Kashmir, Kerala and Andaman – with handpicked couple-friendly hotels and special experiences.",
  intro="Your honeymoon should feel effortless and special. We design romantic itineraries with couple-friendly resorts, private transfers and thoughtful extras – in India and abroad.",
  points=["Maldives overwater villas","Bali, Thailand and Mauritius beach escapes","Switzerland, Paris and Europe","Kashmir, Manali and Kerala","Andaman and Goa beach honeymoons","Candlelight dinners, cake and room decoration on request"],
  why="We match the destination and hotels to your style – relaxed, adventurous or luxurious – and handle visas and insurance too.",
  faqs=[("When should we book our honeymoon?","2–3 months before the wedding is ideal, especially for peak wedding season dates."),
        ("Can you include honeymoon extras?","Yes – room decoration, cake, candlelight dinner and other surprises can be arranged with most hotels."),
        ("Do you plan honeymoons in India too?","Yes, Kashmir, Himachal, Kerala, Andaman and Goa are all popular choices.")]),
 dict(slug="customised-tours", short="Customised Tours", icon="🧭", img=None,
  title="Customised Tour Packages | Tailor-made Holidays from Mumbai",
  h1="Customised Tours – Planned Around You",
  desc="Tailor-made holiday packages from Mumbai built around your dates, interests and travel style – for families, couples, seniors and solo travellers, in India and worldwide.",
  intro="Not every family fits a fixed package. Tell us how you like to travel and we will build an itinerary from scratch – the destinations, hotels, pace, food preferences and activities you want.",
  points=["Your dates and number of nights","Hotel category and room types of your choice","Relaxed pacing for kids and senior citizens","Vegetarian and Jain food arrangements","Special interests – wildlife, adventure, culture, shopping","Multi-country and multi-city itineraries"],
  why="Since 1981 we have planned journeys personally. You speak directly to the people who plan your trip.",
  faqs=[("How do I start a customised tour?","Call or WhatsApp 98431 21212 with your dates, number of travellers and ideas – we will send a suggested itinerary."),
        ("Can you combine two countries in one trip?","Yes, multi-country trips are a speciality."),
        ("Can changes be made after booking?","Within the rules of airlines and hotels, yes – we will help you with any changes.")]),
 dict(slug="fit-mice-tours", short="FIT & MICE", icon="💼", img=None,
  title="FIT & MICE Tours | Corporate Travel, Incentive Trips & Conferences",
  h1="FIT & MICE Tours – Corporate Travel and Events",
  desc="FIT travel for individual travellers and MICE services – meetings, incentive trips, conferences and events – for Mumbai companies, in India and abroad. The Real Tours and Travels, since 1981.",
  intro="We handle independent (FIT) travel for individuals and couples, and corporate MICE travel – meetings, incentive tours, conferences and events – with reliable logistics and a single point of contact.",
  points=["FIT – flexible independent itineraries for individuals and couples","Dealer and employee incentive trips","Conferences, offsites and annual meets","Venue, hotel and banquet sourcing","Group flights, visas and travel insurance","On-ground coordination and event support"],
  why="We combine personal service with the experience to manage group logistics, so your team or guests travel smoothly.",
  faqs=[("What does MICE stand for?","Meetings, Incentives, Conferences and Exhibitions/Events – business travel for groups."),
        ("Do you arrange corporate offsites near Mumbai?","Yes, as well as domestic and international incentive trips."),
        ("Can you handle visas for a corporate group?","Yes, we coordinate group visas, flights and insurance.")]),
 dict(slug="jain-yatra-tours-with-maharaj", short="Jain Yatra with Maharaj", icon="🙏", img="jain.jpg",
  title="Jain Yatra Tours with Maharaj | Pure Jain Food on Tour from Mumbai",
  h1="Jain Yatra Tours with Maharaj (Pure Jain Food)",
  desc="Jain tirth yatras and holidays with our own travelling Maharaj cooking pure Jain food – Palitana, Shikharji, Girnar, Ranakpur and more. Ideal for families, senior citizens and Jain groups from Mumbai.",
  intro="Food is often the biggest concern for Jain families on tour. On our Jain yatra tours, a Maharaj travels with the group and prepares fresh, pure Jain food (no root vegetables, timings respected) throughout the journey.",
  points=["Palitana (Shatrunjay) and Girnar yatra","Sammed Shikharji and eastern tirth yatra","Ranakpur, Nakoda and Rajasthan tirths","Shankheshwar and Gujarat tirths","Custom family and community group yatras","Holidays with Jain food in India and abroad"],
  why="We are a Mumbai family business that has looked after Jain travellers for over four decades – comfortable stays, sensible pacing for elders and food you can trust.",
  faqs=[("Does the Maharaj travel with the group?","Yes, the Maharaj travels with the group and cooks fresh Jain food daily."),
        ("Is chauvihar / sunset meal timing followed?","Yes, meal timings are planned to respect chauvihar and other observances."),
        ("Can you arrange Jain food on international trips?","Yes, we arrange Jain food options for many international destinations too.")]),
]

REVIEWS = [
 ("Nitya K.", "Our Thailand trip was a great experience, thanks to Pratik. The arrangements were seamless and he was just a call away throughout the trip."),
 ("Neeteish J.", "I am a frequent traveller and have never faced any hassle with their bookings. Services are personal and full of effort."),
 ("Aahana K.", "Excellent service! Very professional, helpful and well-organised team. Had a smooth and comfortable travel experience."),
 ("Annu S.", "One stop for all your travelling requirements. Would personally recommend."),
]

CSS = """
/* VOICE: refined, warm, trustworthy family luxury
   IDEA: an engraved travel certificate / luggage-tag seal
   PICTURE: the red seal logo large on a white field with a soft red halo
   COLOUR+TYPE: logo red #D7191F + charcoal on white/light grey only; Playfair Display + Jost
   LAYOUT: full-bleed light bands, centred editorial headings, red hairlines */
:root{--red:#D7191F;--crimson:#B3121A;--wine:#1e1e1e;--gold:#D7191F;--gold2:#D7191F;--ink:#222;--muted:#666;--bg:#f7f7f7;--line:#e6e6e6}
*{box-sizing:border-box;min-width:0}html{scroll-behavior:smooth;scroll-padding-top:90px}
body{margin:0;font-family:'Jost',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;font-size:17px;color:var(--ink);background:#fff;line-height:1.7;overflow-x:clip}
a{color:var(--crimson)}img{max-width:100%;display:block}
h1,h2,h3{font-family:'Playfair Display',Georgia,serif;font-weight:600;line-height:1.15;text-wrap:balance}
.wrap{max-width:1180px;margin:0 auto;padding:0 22px}
.topbar{background:var(--red);color:#fff;font-size:13.5px;letter-spacing:.2px}
.topbar .wrap{display:flex;gap:18px;justify-content:space-between;flex-wrap:wrap;padding:7px 22px}
.topbar a{color:#fff;text-decoration:none}
header.site{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.97);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
header.site .wrap{display:flex;align-items:center;justify-content:space-between;padding:10px 22px}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none;color:var(--wine)}
.brand img{width:64px;height:64px}
.brand b{font-family:'Playfair Display',serif;font-size:22px;letter-spacing:.2px;line-height:1.1;color:var(--crimson)}
.brand small{display:block;color:var(--muted);font-weight:500;font-size:12px;letter-spacing:2px;text-transform:uppercase;margin-top:3px}
nav.main a{color:var(--wine);text-decoration:none;font-weight:500;margin-left:16px;font-size:14.5px;white-space:nowrap}
nav.main a:hover{color:var(--red)}
nav.main a.cta{background:linear-gradient(135deg,var(--red),var(--crimson));color:#fff;padding:10px 20px;border-radius:999px;box-shadow:0 6px 16px rgba(142,14,22,.25)}
.menu-btn{display:none;background:none;border:0;font-size:28px;color:var(--crimson);width:44px;height:44px}
.hero{position:relative;color:var(--ink);overflow:hidden;background:radial-gradient(900px 500px at 85% 30%,rgba(215,25,31,.07),transparent 65%),#fff;border-bottom:1px solid var(--line)}
.hero:before{content:"";position:absolute;inset:0;background:var(--hero,none) center/cover no-repeat;opacity:.12}
.hero .wrap{position:relative;display:grid;grid-template-columns:1.25fr .75fr;gap:40px;align-items:center;padding:88px 22px 96px}
.hero h1{font-size:clamp(34px,5vw,58px);margin:0 0 18px;color:var(--wine)}
.hero p{font-size:19px;color:var(--muted);margin:0 0 30px;max-width:640px}
.kicker{display:inline-flex;align-items:center;gap:10px;color:var(--red);font-size:14px;font-weight:500;letter-spacing:2.5px;text-transform:uppercase;margin-bottom:18px}
.kicker:before{content:"";width:34px;height:1px;background:var(--gold)}
.seal{justify-self:center;align-self:center;position:relative;width:340px;height:340px;max-width:80vw;max-height:80vw;aspect-ratio:1/1;flex:none;border-radius:50%;overflow:hidden;background:#fff;display:grid;place-items:center;box-shadow:0 0 0 12px #fdf0f0,0 24px 50px rgba(0,0,0,.10)}
.seal img{width:86%;height:auto;aspect-ratio:1/1;object-fit:contain;display:block}
img{max-width:100%;height:auto}
html,body{overflow-x:hidden}
.ridge{display:none}
.paybox{max-width:620px;margin:0 auto;text-align:center;background:#fff;border:1px solid var(--line);border-radius:22px;padding:40px 28px;box-shadow:0 20px 44px rgba(0,0,0,.07)}.paybox form{margin:22px 0 8px;min-height:50px}.copy a{color:var(--muted)}
.article{max-width:780px;margin:0 auto}.article h2{margin-top:38px}.article h3{font-size:22px;color:var(--crimson);margin:26px 0 8px}.article p{font-size:17px}
.cover{border-radius:20px;overflow:hidden;margin:0 0 34px;box-shadow:0 20px 44px rgba(0,0,0,.10)}.cover img{width:100%;display:block}
.meta{color:var(--muted);font-size:14px;margin-bottom:6px}
.card.post-card{padding:0;overflow:hidden}.post-card img{width:100%;aspect-ratio:16/10;object-fit:cover;display:block}.post-card .in{padding:22px 24px 26px}
.btns{display:flex;gap:14px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;gap:9px;min-height:48px;padding:12px 26px;border-radius:999px;font-weight:600;text-decoration:none;font-size:16px;letter-spacing:.3px;transition:transform .15s}
.btn:hover{transform:translateY(-2px)}
.btn.gold{background:var(--red);color:#fff;box-shadow:0 8px 20px rgba(215,25,31,.22)}
.btn.red{background:var(--red);color:#fff}
.btn.ghost{border:1.5px solid var(--ink);color:var(--ink)}
.btn.outline{border:1.5px solid var(--crimson);color:var(--crimson)}
.trust{display:flex;gap:40px;flex-wrap:wrap;margin-top:40px;padding-top:26px;border-top:1px solid var(--line);font-size:14px;color:var(--muted)}
.trust b{display:block;font-family:'Playfair Display',serif;font-size:30px;color:var(--red);font-weight:600}
section{padding:84px 0}section.alt{background:var(--bg)}
.head{text-align:center;max-width:760px;margin:0 auto 44px}
.head .kicker{color:var(--gold);justify-content:center}.head .kicker:after{content:"";width:34px;height:1px;background:var(--gold)}
h2{font-size:clamp(28px,3.6vw,42px);color:var(--wine);margin:0 0 14px}
.lead{color:var(--muted);margin:0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,260px),1fr));gap:24px}
.card{position:relative;background:#fff;border:1px solid var(--line);border-radius:18px;padding:30px 26px;text-decoration:none;color:var(--ink);transition:transform .2s,box-shadow .2s,border-color .2s}
.card:hover{transform:translateY(-4px);box-shadow:0 18px 40px rgba(0,0,0,.08);border-color:var(--red)}
.card .ic{width:52px;height:52px;border-radius:50%;display:grid;place-items:center;background:#fdf0f0;font-size:24px}
.card h3{margin:16px 0 8px;color:var(--crimson);font-size:21px}.card p{margin:0;color:var(--muted);font-size:15px}
.card .more{display:inline-block;margin-top:14px;color:var(--red);font-weight:600;font-size:14px;letter-spacing:1px;text-transform:uppercase}
.two{display:grid;grid-template-columns:1.1fr 1fr;gap:56px;align-items:center}
.photo{border-radius:22px;overflow:hidden;box-shadow:0 24px 50px rgba(0,0,0,.12)}
.emblem{border-radius:22px;padding:56px;text-align:center;color:var(--muted);background:#fff;border:1px solid var(--line);box-shadow:0 24px 50px rgba(0,0,0,.07)}
.emblem img{width:190px;margin:0 auto 20px}
.emblem b{display:block;font-family:'Playfair Display',serif;font-size:26px;color:var(--red)}
ul.ticks{list-style:none;padding:0;margin:0}ul.ticks li{padding:9px 0 9px 36px;position:relative;border-bottom:1px solid var(--line)}
ul.ticks li:before{content:"✓";position:absolute;left:4px;top:9px;color:var(--red);font-weight:700}
.review{background:#fff;border:1px solid var(--line);border-radius:18px;padding:28px}
.review .stars{color:var(--red);letter-spacing:3px;font-size:18px}.review p{margin:10px 0 14px;font-family:'Playfair Display',serif;font-style:italic;font-size:17.5px;color:#3b2f2f}.review b{color:var(--crimson);font-weight:600}
.band{background:#fdf0f0;color:var(--ink);text-align:center}
.band h2{color:var(--wine)}.band p{color:var(--muted);margin:0 0 28px}
.faq details{background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px 22px;margin-bottom:14px}
.faq summary{font-weight:600;color:var(--wine);cursor:pointer;font-size:17px}
.faq details[open]{border-color:var(--red)}
.crumbs{font-size:14px;color:var(--muted);margin-bottom:16px}.crumbs a{color:var(--red)}
footer{background:var(--bg);color:var(--muted);font-size:15px;border-top:1px solid var(--line)}
footer .wrap{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:40px;padding:64px 22px 36px}
footer a{color:var(--ink);text-decoration:none}footer a:hover{color:var(--red)}footer h4{font-family:'Playfair Display',serif;color:var(--wine);font-size:20px;margin:0 0 14px}
footer ul{list-style:none;padding:0;margin:0}footer li{margin:7px 0}

.copy{border-top:1px solid var(--line);text-align:center;padding:18px;font-size:13.5px;color:var(--muted)}
.gst{display:inline-block;margin-top:6px;padding:4px 12px;border:1px solid var(--line);border-radius:999px;color:var(--ink);background:#fff;font-size:13px;letter-spacing:.5px}
.float-wa{position:fixed;right:18px;bottom:18px;z-index:60;background:#25D366;color:#fff;width:60px;height:60px;border-radius:50%;display:grid;place-items:center;box-shadow:0 8px 22px rgba(0,0,0,.3);text-decoration:none;font-size:28px}
.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:40px}
.info{background:var(--bg);border:1px solid var(--line);border-radius:18px;padding:32px}
.info p{margin:0 0 14px}
.map{border:0;width:100%;min-height:380px;height:100%;border-radius:18px;outline:1px solid var(--line)}
:focus-visible{outline:3px solid var(--red);outline-offset:3px}
@media(max-width:1180px){nav.main{display:none;position:absolute;top:84px;left:0;right:0;background:#fff;padding:14px 22px;box-shadow:0 10px 24px rgba(0,0,0,.1)}nav.main.open{display:block}nav.main a{display:block;margin:12px 0}.menu-btn{display:block}}
@media(max-width:900px){.hero .wrap{grid-template-columns:1fr;gap:28px;padding:36px 18px 56px;text-align:left}.seal{width:200px;height:200px;order:-1;box-shadow:0 0 0 8px #fdf0f0,0 14px 30px rgba(0,0,0,.10)}
nav.main{display:none;position:absolute;top:84px;left:0;right:0;background:#fff;padding:14px 22px;box-shadow:0 10px 24px rgba(0,0,0,.1)}
nav.main.open{display:block}nav.main a{display:block;margin:12px 0}.menu-btn{display:block}
.two,.contact-grid,footer .wrap{grid-template-columns:1fr}section{padding:52px 0}.brand b{font-size:16px}.brand img{width:48px;height:48px}.brand small{font-size:10px;letter-spacing:1.2px}
.wrap{padding-left:18px;padding-right:18px}header.site .wrap{padding:8px 18px}.topbar .wrap{justify-content:center;gap:6px 14px;font-size:12.5px}
.hero h1{font-size:clamp(28px,8vw,38px)}.hero p{font-size:16.5px;margin-bottom:22px}.kicker{font-size:12px;letter-spacing:1.6px}
.btns{flex-direction:column}.btns .btn{justify-content:center;width:100%}
.trust{gap:18px 28px;margin-top:28px}.trust b{font-size:24px}
.head{margin-bottom:30px}.card{padding:24px 20px}.emblem{padding:34px 22px}.emblem img{width:150px}
.map{min-height:300px}footer .wrap{gap:28px;padding:44px 18px 28px}.float-wa{width:54px;height:54px;right:14px;bottom:14px;font-size:25px}
.faq summary{font-size:16px}.review{padding:22px}}
@media(max-width:380px){.seal{width:170px;height:170px}.brand small{display:none}}
@media(prefers-reduced-motion:reduce){*{transition:none!important}html{scroll-behavior:auto}}
"""

def jsonld_org():
    return {
      "@context":"https://schema.org","@type":"TravelAgency","@id":SITE+"/#agency",
      "name":NAME,"url":SITE+"/","logo":SITE+"/img/logo-512.png",
      "image":SITE+"/img/logo-512.png","telephone":PHONE_RAW,"email":EMAIL,"foundingDate":"1981","taxID":GST,"vatID":GST,
      "address":{"@type":"PostalAddress","streetAddress":"204, B10, Rachana Building, Govardhan Nagar, Lal Bahadur Shastri Marg","addressLocality":"Mulund West, Mumbai","addressRegion":"Maharashtra","postalCode":"400080","addressCountry":"IN"},
      "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"09:00","closes":"22:00"}],
      "areaServed":["Mulund","Thane","Bhandup","Nahur","Powai","Ghatkopar","Mumbai"],
      "hasMap":MAPS,"sameAs":[IG,FB,MAPS],
      "makesOffer":[{"@type":"Offer","itemOffered":{"@type":"Service","name":s["h1"],"url":f"{SITE}/{s['slug']}/"}} for s in SERVICES]}

def page(path, title, desc, body, extra_ld=None, hero_img=None):
    canonical = SITE + path
    lds = [jsonld_org()] + (extra_ld or [])
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    depth = path.strip("/").count("/") + (1 if path.strip("/") else 0)
    root = "../" * depth if depth else ""
    og = SITE + "/img/" + (hero_img or "logo-512.png")
    nav = "".join(f'<li><a href="{root}{s["slug"]}/">{s["short"]}</a></li>' for s in SERVICES)
    return f"""<!doctype html>
<html lang="en-IN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#ffffff">
<link rel="icon" type="image/png" href="{root}favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600&family=Playfair+Display:ital,wght@0,600;0,700;1,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}style.css">
{ld}
</head><body>
<div class="topbar"><div class="wrap"><span>📍 Mulund West, Mumbai · Open daily 9 am – 10 pm</span><span><a href="tel:{PHONE_RAW}">📞 {PHONE}</a> · <a href="mailto:{EMAIL}">✉️ {EMAIL}</a></span></div></div>
<header class="site"><div class="wrap">
<a class="brand" href="{root or './'}"><img src="{root}img/logo.png" alt="The Real Tours and Travels logo – Estd. 1981" width="64" height="64"><span><b>The Real Tours and Travels</b><small>Crafting Journeys Since 1981</small></span></a>
<button class="menu-btn" aria-label="Menu" onclick="document.querySelector('nav.main').classList.toggle('open')">☰</button>
<nav class="main"><a href="{root or './'}#services">Services</a><a href="{root}flights-hotels/">Flights · Hotels · Cruise</a><a href="{root}customize-your-package/">Customize Trip</a><a href="{root}visa/">Visa</a><a href="{root}passport/">Passport</a><a href="{root}jain-yatra-tours-with-maharaj/">Jain Yatra</a><a href="{root}contact/">Contact</a><a class="cta" href="{WA}" target="_blank" rel="noopener">WhatsApp Us</a></nav>
</div></header>
<main>
{body}
</main>
<footer><div class="wrap">
<div><a class="brand" href="{root or './'}" ><img src="{root}img/logo.png" alt="" width="52" height="52"><span><b>The Real Tours and Travels</b><small>Crafting Journeys Since 1981</small></span></a>
<p>Trusted Mumbai travel agency for family holidays, international tours, visas, yatras and Jain tours since 1981.</p>
<p>{'<br>'.join(ADDR)}<br><span class="gst">GSTIN: {GST}</span></p>
<p><a href="tel:{PHONE_RAW}">📞 {PHONE}</a><br><a href="mailto:{EMAIL}">✉️ {EMAIL}</a><br>
<a href="{IG}" target="_blank" rel="noopener">📸 @therealtoursandtravels</a> · <a href="{FB}" target="_blank" rel="noopener">Facebook</a></p></div>
<div><h4>Our Services</h4><ul>{nav}</ul></div>
<div><h4>Visit Us</h4><ul><li>Open every day, 9 am – 10 pm</li><li><a href="{MAPS}" target="_blank" rel="noopener">Get directions on Google Maps</a></li><li><a href="{REVIEW}" target="_blank" rel="noopener">⭐ Review us on Google</a></li><li><a href="{root}flights-hotels/">✈️ Flights, hotels &amp; cruise</a></li><li><a href="{root}customize-your-package/">✨ Customize your package</a></li><li><a href="{root}visa/">Visa documents &amp; upload</a></li><li><a href="{root}passport/">Passport services</a></li><li><a href="{root}blog/">Travel guides &amp; tips</a></li><li><a href="{root}contact/">Contact us</a></li></ul>
<p style="margin-top:14px">Serving Mulund, Thane, Bhandup, Nahur, Powai, Ghatkopar and all of Mumbai.</p></div>
</div><div class="copy">© {datetime.date.today().year} The Real Tours and Travels, Mulund West, Mumbai · GSTIN {GST} · All rights reserved.<br><a href="{root}terms/">Terms &amp; Conditions</a> · <a href="{root}privacy-policy/">Privacy Policy</a> · <a href="{root}cancellation-refund-policy/">Cancellation &amp; Refund Policy</a></div></footer>
<a class="float-wa" href="{WA}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">💬</a>
</body></html>"""

def write(path, html):
    fp = os.path.join(os.path.dirname(__file__), path.strip("/"), "index.html") if path != "/" else os.path.join(os.path.dirname(__file__), "index.html")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w").write(html)

RIDGE = '<svg class="ridge" viewBox="0 0 1440 120" preserveAspectRatio="none" aria-hidden="true"><path d="M0 120 L0 70 L120 40 L210 75 L330 20 L450 80 L560 45 L690 90 L820 30 L930 70 L1050 15 L1170 75 L1290 40 L1440 80 L1440 120 Z" fill="#fff"/><path d="M0 70 L120 40 L210 75 L330 20 L450 80 L560 45 L690 90 L820 30 L930 70 L1050 15 L1170 75 L1290 40 L1440 80" fill="none" stroke="#C8A25A" stroke-width="2"/></svg>'

def seal(root):
    return f'<div class="seal"><img src="{root}img/logo.png" alt="The Real Tours and Travels – Estd. 1981" width="300" height="300"></div>'

def cta_band():
    return f"""<section class="band"><div class="wrap"><span class="kicker">Since 1981</span><h2>Plan your next holiday with us</h2><p>Tell us where you want to go – we'll handle the rest. No obligation.</p>
<div class="btns" style="justify-content:center"><a class="btn gold" href="{WA}" target="_blank" rel="noopener">💬 WhatsApp 98431 21212</a><a class="btn ghost" href="tel:{PHONE_RAW}">📞 Call now</a></div></div></section>"""

def build():
    root = os.path.dirname(os.path.abspath(__file__))
    open(os.path.join(root, "style.css"), "w").write(CSS + VISA_CSS + PLANNER_CSS + FLIGHT_CSS + TOOL_CSS)
    imgs = set(os.listdir(os.path.join(root, "img")))
    # Home
    cards = "".join(f'<a class="card" href="{s["slug"]}/"><div class="ic">{s["icon"]}</div><h3>{s["h1"]}</h3><p>{s["desc"][:120].rsplit(" ",1)[0]}…</p><span class="more">Explore →</span></a>' for s in SERVICES)
    revs = "".join(f'<div class="review"><div class="stars">★★★★★</div><p>“{t}”</p><b>— {n}</b></div>' for n, t in REVIEWS)
    hero = "gulmarg.jpg" if "gulmarg.jpg" in imgs else None
    hero_style = f' style="--hero:url(img/{hero})"' if hero else ""
    side = "dubai.jpg" if "dubai.jpg" in imgs else None
    side_html = f'<div class="photo"><img src="img/{side}" alt="Indian family holiday in Dubai planned by The Real Tours and Travels" loading="lazy" width="800" height="600"></div>' if side else '<div class="emblem"><img src="img/logo.png" alt="The Real Tours and Travels emblem"><b>Crafting Journeys Since 1981</b><p>A Mulund family business trusted by generations of Mumbai travellers.</p></div>'
    home = f"""
<section class="hero"{hero_style}><div class="wrap"><div>
<span class="kicker">Mumbai's family travel experts · Since 1981</span>
<h1>Travel Agency in Mulund, Mumbai for Family Holidays, Tours &amp; Visas</h1>
<p>Domestic and international holiday packages, honeymoons, yatras, Jain tours with Maharaj, group tours, passport &amp; visa services and travel insurance – planned personally by The Real Tours and Travels.</p>
<div class="btns"><a class="btn gold" href="customize-your-package/">✨ Customize your package</a><a class="btn ghost" href="{WA}" target="_blank" rel="noopener">💬 WhatsApp 98431 21212</a></div>
<div class="trust"><div><b>45+ years</b>serving travellers since 1981</div><div><b>4.8 ★</b>rating on Google</div><div><b>10+</b>travel services under one roof</div></div>
</div>{seal("")}</div>{RIDGE}</section>
<section class="fsec"><div class="wrap">{flight_widget("")}</div></section>
<section id="services"><div class="wrap">
<div class="head"><span class="kicker">What we do</span><h2>Our Travel Services</h2><p class="lead">Everything you need for a stress-free trip – from the first idea to the day you return home.</p></div>
<div class="grid">{cards}</div></div></section>
<section class="alt"><div class="wrap two">
<div><h2>Why Mumbai families choose The Real Tours and Travels</h2>
<span class="kicker">Our promise</span><p class="lead" style="margin-bottom:20px">We are a family-run travel agency in Mulund West. For over four decades we have planned holidays, pilgrimages and business trips for families across Mulund, Thane, Bhandup, Powai and Ghatkopar.</p>
<ul class="ticks"><li>Personal service – one point of contact, on call during your trip</li><li>Family-friendly hotels and comfortable pacing for kids and seniors</li><li>Visas, travel insurance, flights and hotels handled in one place</li><li>Pure vegetarian and Jain food arrangements, including tours with our own Maharaj</li><li>Transparent planning – no hidden surprises</li></ul></div>
{side_html}</div></section>
<section><div class="wrap"><div class="head"><span class="kicker">Reviews</span><h2>What our travellers say</h2><p class="lead">Rated 4.8 ★ on Google by our customers.</p></div>
<div class="grid">{revs}</div>
<p style="margin-top:30px;text-align:center"><a class="btn outline" href="{MAPS}" target="_blank" rel="noopener">Read all reviews on Google</a></p></div></section>
<section class="alt faq"><div class="wrap" style="max-width:860px"><div class="head"><span class="kicker">Good to know</span><h2>Frequently asked questions</h2></div>
<details><summary>Where is The Real Tours and Travels located?</summary><p>We are at 204, B10, Rachana Building, Govardhan Nagar, LBS Marg, Mulund West, Mumbai 400080, open every day from 9 am to 10 pm.</p></details>
<details><summary>Do you plan both domestic and international holidays?</summary><p>Yes – from Kashmir, Kerala and Manali to Dubai, Thailand, Bali and Europe, with flights, hotels, visas and insurance.</p></details>
<details><summary>Do you offer Jain food on tours?</summary><p>Yes. We arrange Jain and vegetarian food, and run Jain yatra tours with our own Maharaj cooking pure Jain food.</p></details>
<details><summary>How do I get a quote?</summary><p>Call or WhatsApp us on 98431 21212 or email {EMAIL} with your travel dates and number of travellers.</p></details>
</div></section>
{cta_band()}"""
    faq_home = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":"Where is The Real Tours and Travels located?","acceptedAnswer":{"@type":"Answer","text":"204, B10, Rachana Building, Govardhan Nagar, LBS Marg, Mulund West, Mumbai 400080, open every day 9 am to 10 pm."}},
        {"@type":"Question","name":"Do you offer Jain food on tours?","acceptedAnswer":{"@type":"Answer","text":"Yes. We arrange Jain and vegetarian food and run Jain yatra tours with our own Maharaj."}}]}
    write("/", page("/", "Travel Agency in Mulund, Mumbai | The Real Tours and Travels – Since 1981",
        "Trusted travel agency in Mulund West, Mumbai since 1981. Domestic & international holiday packages, honeymoons, yatras, Jain tours with Maharaj, group tours, visas and travel insurance. Call/WhatsApp 98431 21212.",
        home, [faq_home], hero))
    # Service pages
    for s in SERVICES:
        others = "".join(f'<a class="card" href="../{o["slug"]}/"><div class="ic">{o["icon"]}</div><h3>{o["h1"]}</h3><span class="more">Explore →</span></a>' for o in SERVICES if o is not s)[:100000]
        pts = "".join(f"<li>{p}</li>" for p in s["points"])
        faqs = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in s["faqs"])
        img = s["img"] if s["img"] and s["img"] in imgs else None
        hs = f' style="--hero:url(../img/{img})"' if img else ""
        body = f"""
<section class="hero"{hs}><div class="wrap"><div>
<div class="crumbs"><a href="../">Home</a> › {s['short']}</div>
<span class="kicker">{s['icon']} {s['short']}</span>
<h1>{s['h1']}</h1><p>{s['intro']}</p>
<div class="btns">{'<a class="btn gold" href="../visa/">📄 Visa documents &amp; upload</a><a class="btn outline" href="../passport/">🛂 Passport services</a>' if s['slug']=='passport-visa-services' else ''}<a class="btn gold" href="{WA}" target="_blank" rel="noopener">💬 Get a free plan on WhatsApp</a><a class="btn ghost" href="tel:{PHONE_RAW}">📞 98431 21212</a></div>
</div>{seal("../")}</div>{RIDGE}</section>
<section><div class="wrap two"><div><h2>What we offer</h2><ul class="ticks">{pts}</ul></div>
<div><h2>Why book with us</h2><p>{s['why']}</p><p>Visit our office in <b>Mulund West, Mumbai</b> (open daily 9 am – 10 pm), or plan everything over call and WhatsApp. We serve travellers across Mulund, Thane, Bhandup, Nahur, Powai, Ghatkopar and the rest of Mumbai.</p>
<p><a class="btn red" href="{WA}" target="_blank" rel="noopener">Plan my trip</a></p></div></div></section>
<section class="alt faq"><div class="wrap" style="max-width:860px"><div class="head"><span class="kicker">Good to know</span><h2>Frequently asked questions</h2></div>{faqs}</div></section>
<section><div class="wrap"><div class="head"><span class="kicker">More from us</span><h2>Explore our other services</h2></div><div class="grid">{others}</div></div></section>
{cta_band()}"""
        faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in s["faqs"]]}
        svc_ld = {"@context":"https://schema.org","@type":"Service","name":s["h1"],"description":s["desc"],"provider":{"@id":SITE+"/#agency"},"areaServed":"Mumbai","url":f"{SITE}/{s['slug']}/"}
        crumbs = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},{"@type":"ListItem","position":2,"name":s["short"],"item":f"{SITE}/{s['slug']}/"}]}
        write(f"/{s['slug']}/", page(f"/{s['slug']}/", s["title"] + " | The Real Tours and Travels", s["desc"], body, [svc_ld, faq_ld, crumbs], img))
    # Contact
    contact = f"""
<section class="hero"><div class="wrap"><div><div class="crumbs"><a href="../">Home</a> › Contact</div>
<span class="kicker">Visit · Call · WhatsApp</span><h1>Contact The Real Tours and Travels, Mulund West</h1><p>Call, WhatsApp, email or visit our office – we're open every day from 9 am to 10 pm.</p></div>{seal("../")}</div>{RIDGE}</section>
<section><div class="wrap contact-grid"><div class="info">
<h2>Get in touch</h2>
<p><b>Phone / WhatsApp:</b> <a href="tel:{PHONE_RAW}">{PHONE}</a></p>
<p><b>Email:</b> <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p><b>Address:</b><br>{'<br>'.join(ADDR)}</p>
<p><b>Hours:</b> Monday – Sunday, 9:00 am – 10:00 pm</p>
<p><b>GSTIN:</b> {GST}</p>
<p><b>Instagram:</b> <a href="{IG}" target="_blank" rel="noopener">@therealtoursandtravels</a></p>
<div class="btns"><a class="btn gold" href="{WA}" target="_blank" rel="noopener">💬 WhatsApp us</a><a class="btn outline" href="{MAPS}" target="_blank" rel="noopener">📍 Directions</a></div></div>
<iframe class="map" loading="lazy" title="Map to The Real Tours and Travels, Mulund West" src="https://www.google.com/maps?cid=6174258107225017089&output=embed"></iframe>
</div></section>{cta_band()}"""
    write("/contact/", page("/contact/", "Contact | The Real Tours and Travels, Mulund West, Mumbai", "Contact The Real Tours and Travels in Mulund West, Mumbai. Call/WhatsApp 98431 21212, email enquiry@therealtoursandtravels.com. Open daily 9 am – 10 pm.", contact))
    # 404
    open(os.path.join(root, "404.html"), "w").write(page("/404.html", "Page not found | The Real Tours and Travels", "Page not found.", f'<section><div class="wrap"><h1>Page not found</h1><p><a href="/">Go to the home page</a> or WhatsApp us on 98431 21212.</p></div></section>').replace('<meta name="robots" content="index,follow,max-image-preview:large">','<meta name="robots" content="noindex">'))
    # Blog
    svc = {x["slug"]: x for x in SERVICES}
    cards_b = "".join(f'<a class="card post-card" href="{a["slug"]}/"><img src="../img/{a["img"]}" alt="{a["img_alt"]}" loading="lazy" width="1200" height="744"><div class="in"><h3>{a["h1"]}</h3><p>{a["desc"][:140].rsplit(" ",1)[0]}…</p><span class="more">Read guide →</span></div></a>' for a in ARTICLES)
    blog = f"""<section class="hero"><div class="wrap"><div><div class="crumbs"><a href="../">Home</a> › Travel Guides</div><span class="kicker">Travel guides &amp; tips</span><h1>Travel Guides from The Real Tours and Travels</h1><p>Practical advice from 45+ years of planning holidays, yatras and visas for Mumbai families.</p></div>{seal("../")}</div></section>
<section><div class="wrap"><div class="grid">{cards_b}</div></div></section>{cta_band()}"""
    write("/blog/", page("/blog/", "Travel Guides & Tips | The Real Tours and Travels, Mumbai", "Travel guides and tips from The Real Tours and Travels, Mulund West, Mumbai – holiday ideas, Jain yatras, passport and visa checklists, travel insurance.", blog))
    for a in ARTICLES:
        rel = "".join(f'<a class="card" href="../../{r}/"><div class="ic">{svc[r]["icon"]}</div><h3>{svc[r]["h1"]}</h3><span class="more">Explore →</span></a>' for r in a["related"] if r in svc)
        faqs = "".join(f"<details><summary>{q}</summary><p>{x}</p></details>" for q, x in a["faqs"])
        d = datetime.date.fromisoformat(a["date"]).strftime("%-d %B %Y")
        body = f"""<section style="padding-top:44px"><div class="wrap"><div class="article">
<div class="crumbs"><a href="../../">Home</a> › <a href="../">Travel Guides</a></div>
<h1 style="font-size:clamp(30px,4.4vw,46px);color:var(--wine);margin:0 0 10px">{a["h1"]}</h1>
<p class="meta">By The Real Tours and Travels · Mulund West, Mumbai · {d}</p>
<div class="cover"><img src="../../img/{a["img"]}" alt="{a["img_alt"]}" width="1200" height="744"></div>
<p class="lead" style="font-size:19px">{a["intro"]}</p>
{a["body"]}
<p><a class="btn gold" href="{WA}" target="_blank" rel="noopener">💬 Plan with us on WhatsApp</a></p>
</div></div></section>
<section class="alt faq"><div class="wrap" style="max-width:860px"><div class="head"><span class="kicker">Quick answers</span><h2>Frequently asked questions</h2></div>{faqs}</div></section>
<section><div class="wrap"><div class="head"><span class="kicker">Related services</span><h2>How we can help</h2></div><div class="grid">{rel}</div></div></section>{cta_band()}"""
        url = f"{SITE}/blog/{a['slug']}/"
        art_ld = {"@context":"https://schema.org","@type":"Article","headline":a["h1"],"description":a["desc"],"image":f"{SITE}/img/{a['img']}","datePublished":a["date"],"dateModified":a["date"],"author":{"@type":"Organization","name":NAME,"url":SITE},"publisher":{"@id":SITE+"/#agency"},"mainEntityOfPage":url}
        faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":x}} for q,x in a["faqs"]]}
        crumbs = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"Travel Guides","item":SITE+"/blog/"},{"@type":"ListItem","position":3,"name":a["h1"],"item":url}]}
        write(f"/blog/{a['slug']}/", page(f"/blog/{a['slug']}/", a["title"] + " | The Real Tours and Travels", a["desc"], body, [art_ld, faq_ld, crumbs], a["img"]))
    # Flights & hotels enquiry page
    fh = f"""<section class="hero"><div class="wrap"><div><div class="crumbs"><a href="../">Home</a> › Flights, Hotels &amp; Cruise</div><span class="kicker">✈️ Flights · 🏨 Hotels · 🛳️ Cruise</span><h1>Flight Tickets, Hotels &amp; Cruise Bookings</h1><p>Search your flight or hotel and request a quote – our team checks all airlines and hotels and replies with the best options on WhatsApp or email. Domestic and international.</p></div>{seal("../")}</div></section>
<section class="fsec"><div class="wrap">{flight_widget("../")}</div></section>
<section><div class="wrap two"><div><h2>Why book with The Real Tours and Travels</h2><ul class="ticks"><li>We compare fares across airlines and hotels for you</li><li>Group bookings, family seats together and special meals arranged</li><li>Changes, cancellations and web check-in help – one call away</li><li>Visas and travel insurance in the same place</li></ul></div>
<div><h2>How it works</h2><ul class="ticks"><li>1. Enter your trip details and tap <b>Get Quote</b></li><li>2. We reply with the best options on WhatsApp / email</li><li>3. Confirm and pay – your tickets and vouchers are issued by our team</li></ul></div></div></section>{cta_band()}"""
    write("/flights-hotels/", page("/flights-hotels/", "Flight Tickets, Hotel & Cruise Booking in Mulund, Mumbai | The Real Tours and Travels", "Book domestic and international flight tickets and hotels with The Real Tours and Travels, Mulund West, Mumbai. Search and request a quote – we reply with the best fares on WhatsApp.", fh, None, "flight.jpg"))
    # Customize your package
    write("/customize-your-package/", page("/customize-your-package/", "Customize Your Holiday Package – Instant Itinerary | The Real Tours and Travels", "Customize your holiday package from Mumbai – choose destination, days, travellers, hotel category, car (SUV, Sedan, Hatchback) and flight or train, and get an instant day-by-day itinerary.", planner_page(PHONE, PHONE_RAW, EMAIL, WA, seal, cta_band, ADDR, GST), None, "gulmarg.jpg"))
    # Visa section
    write("/visa/", page("/visa/", "Visa Services in Mulund, Mumbai – Documents Required & Upload | The Real Tours and Travels", "Visa services in Mulund West, Mumbai for Dubai, Thailand, Singapore, Europe (Schengen), UK, USA, Canada, Australia, Japan and more. See documents required, request the price and upload documents securely.", visa_page(PHONE, PHONE_RAW, EMAIL, seal, cta_band), None, "passport.jpg"))
    write("/passport/", page("/passport/", "Passport Services in Mulund, Mumbai – New, Renewal, Tatkaal | The Real Tours and Travels", "Passport services in Mulund West, Mumbai – fresh passport, renewal, minor, Tatkaal and lost passport. See documents required, request the price and upload documents securely.", passport_page(PHONE, PHONE_RAW, EMAIL, seal, cta_band), None, "passport.jpg"))
    def legal(slug, title, html):
        body = f"""<section style="padding-top:44px"><div class="wrap"><div class="article"><div class="crumbs"><a href="../">Home</a> › {title}</div><h1 style="font-size:clamp(30px,4.4vw,44px);color:var(--wine)">{title}</h1><p class="meta">Last updated: {datetime.date.today().strftime("%-d %B %Y")}</p>{html}
<h2>Contact us</h2><p>The Real Tours and Travels<br>{'<br>'.join(ADDR)}<br>Phone/WhatsApp: {PHONE}<br>Email: <a href="mailto:{EMAIL}">{EMAIL}</a><br>GSTIN: {GST}</p></div></div></section>"""
        write(f"/{slug}/", page(f"/{slug}/", f"{title} | The Real Tours and Travels", f"{title} of The Real Tours and Travels, Mulund West, Mumbai.", body))
    legal("terms", "Terms & Conditions", """
<p>These terms apply to all bookings and payments made with The Real Tours and Travels ("we", "us"), a travel agency in Mulund West, Mumbai. By making a booking or payment you agree to these terms.</p>
<h2>Bookings</h2><ul class="ticks"><li>A booking is confirmed only after we receive the required payment and send you written confirmation.</li><li>Itineraries, hotels and services are subject to availability at the time of confirmation.</li><li>Travellers must provide correct names (as per passport/ID), contact details and documents. We are not responsible for losses caused by incorrect information provided by the customer.</li></ul>
<h2>Payments</h2><ul class="ticks"><li>Online payments are processed securely by Razorpay. We do not store your card or bank details.</li><li>Please pay only the amount confirmed by our team for your booking. The balance, if any, must be paid by the date shared with you.</li><li>Applicable taxes (including GST/TCS where applicable) are charged as per government rules.</li></ul>
<h2>Travel documents and visas</h2><p>Travellers are responsible for holding a valid passport, visas and other documents. We assist with visa applications, but the decision to grant a visa rests solely with the embassy or authority, and we cannot guarantee approval.</p>
<h2>Third-party services</h2><p>Airlines, hotels, transport operators and other suppliers provide services under their own terms. We act as an agent and are not liable for delays, cancellations, changes or deficiencies caused by these suppliers or by events beyond our control (such as weather, strikes, natural events or government restrictions).</p>
<h2>Changes</h2><p>We may update these terms from time to time. The version on this page applies at the time of your booking.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of India, and courts in Mumbai shall have jurisdiction.</p>""")
    legal("privacy-policy", "Privacy Policy", """
<p>The Real Tours and Travels respects your privacy. This policy explains what information we collect and how we use it.</p>
<h2>Information we collect</h2><ul class="ticks"><li>Name, phone number, email address and booking details you share with us by call, WhatsApp, email, our website or in person.</li><li>Traveller details and documents (such as passport copies) needed to make bookings and visa applications.</li><li>Payment information is collected and processed by our payment partner Razorpay; we do not store card or bank details.</li></ul>
<h2>How we use your information</h2><ul class="ticks"><li>To plan and book your travel, apply for visas and insurance, and contact you about your trip.</li><li>To send payment receipts and service updates.</li><li>To share travel offers, only if you have agreed to receive them. You can opt out at any time.</li></ul>
<h2>Sharing</h2><p>We share your details only with airlines, hotels, insurers, embassies/visa centres and other service providers as needed for your booking, or when required by law. We do not sell your personal information.</p>
<h2>Security and retention</h2><p>We take reasonable steps to protect your information and keep it only as long as needed for your bookings and legal requirements.</p>
<h2>Your choices</h2><p>You may ask us to access, correct or delete your personal information by contacting us using the details below.</p>""")
    legal("cancellation-refund-policy", "Cancellation & Refund Policy", """
<p>This policy explains how cancellations and refunds work for bookings and payments made with The Real Tours and Travels.</p>
<h2>Cancellation by the customer</h2><ul class="ticks"><li>Cancellation requests must be sent in writing by email to enquiry@therealtoursandtravels.com or on WhatsApp at 98431 21212.</li><li>Cancellation charges depend on the airline, hotel and other suppliers' rules and on how close to the travel date you cancel. The applicable charges for your booking will be shared with you at the time of booking and on request.</li><li>Visa fees, service fees, insurance premiums and non-refundable tickets or hotel bookings are not refundable once processed.</li></ul>
<h2>Refunds</h2><ul class="ticks"><li>Eligible refunds are processed after deducting applicable cancellation charges and once we receive the refund from the supplier.</li><li>Refunds for online payments are made to the original payment method. Once initiated, a refund usually reaches your account within 5–10 working days, depending on your bank.</li><li>Payments made by mistake or in excess of the confirmed amount will be refunded in full after verification.</li></ul>
<h2>Cancellation or changes by us or suppliers</h2><p>If a service is cancelled by us or a supplier, we will offer an alternative or refund the amount received for that service, as per the supplier's policy.</p>""")
    # Private GST quote tool (noindex, not in sitemap)
    write("/tools/gst-quote/", page("/tools/gst-quote/", "GST Quote & Invoice Maker | The Real Tours and Travels", "Internal tool.", gst_tool_page(NAME, ADDR, GST, PHONE, EMAIL)).replace('<meta name="robots" content="index,follow,max-image-preview:large">','<meta name="robots" content="noindex,nofollow">'))
    # sitemap / robots / CNAME
    urls = ["/"] + [f"/{s['slug']}/" for s in SERVICES] + ["/blog/", "/visa/", "/passport/", "/flights-hotels/", "/customize-your-package/"] + [f"/blog/{a['slug']}/" for a in ARTICLES] + ["/contact/", "/terms/", "/privacy-policy/", "/cancellation-refund-policy/"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{'1.0' if u=='/' else '0.8'}</priority></url>\n" for u in urls) + "</urlset>\n"
    open(os.path.join(root, "sitemap.xml"), "w").write(sm)
    open(os.path.join(root, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: {SITE}/sitemap.xml\n")
    open(os.path.join(root, "CNAME"), "w").write("www.therealtoursandtravels.com\n")
    print("built", len(urls), "pages")

if __name__ == "__main__":
    build()
