#!/usr/bin/env python3
"""Static site generator for The Real Tours and Travels (SEO site)."""
import json, os, datetime, re
from articles import ARTICLES
from visa import visa_page, passport_page, VISA_CSS
from planner import planner_page, PLANNER_CSS
from flights import flight_widget, FLIGHT_CSS
from tools import gst_tool_page, TOOL_CSS
import pwa
from insurance import insurance_page
import account
import admin
from svcform import svc_form, SVC_CSS
import fx

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
  intro="Travelling abroad with family should be exciting, not stressful. We plan international holidays end to end – flights from Mumbai, visas, hotels, transfers, sightseeing and travel insurance – and stay in touch with you throughout the trip.",
  points=["Dubai & Abu Dhabi – desert safari, Burj Khalifa, theme parks","Thailand – Bangkok, Pattaya, Phuket and Krabi","Bali, Singapore, Malaysia and Vietnam","Sri Lanka, Maldives and Mauritius","Europe – Switzerland, Paris, Italy, London and Scandinavia","Japan, Australia, New Zealand and the USA"],
  why="Since 1981 we have sent thousands of families abroad – from Mumbai, across India and beyond. We take care of the paperwork you worry about – visas, insurance, arrival cards – and suggest family-friendly hotels in the right locations.",
  faqs=[("Do you help with visas for international packages?","Yes. Our visa team guides you on documents and files tourist visas for Dubai, Singapore, Schengen/Europe, UK, USA, Australia and more."),
        ("Can you customise an international package?","Absolutely. Every package can be changed – hotels, number of nights, activities and pace – to suit your family."),
        ("Do you provide vegetarian and Jain food abroad?","We can recommend and pre-arrange vegetarian and Jain meals in most popular destinations.")]),
 dict(slug="passport-visa-services", short="Passport & Visa", icon="🛂", img="passport.jpg",
  title="Passport & Visa Services in Mulund, Mumbai | Tourist Visa Assistance",
  h1="Passport & Visa Services in Mulund, Mumbai",
  desc="Fresh passport and renewal appointments, and tourist and business visa assistance for Dubai, Singapore, Thailand, Schengen, UK, USA, Canada and Australia. Visit The Real Tours and Travels, Mulund West.",
  intro="Visa rules change often and a small mistake in documents can delay your trip. Our team in Mulund West helps you prepare the right documents, books appointments and tracks your application – for passports and visas alike.",
  points=["Fresh passport and passport renewal appointment assistance","Tourist and business visas – Dubai/UAE, Singapore, Thailand, Malaysia","Schengen (Europe), UK, USA, Canada, Australia and New Zealand visas","e-Visas and arrival cards, including the Thailand Digital Arrival Card","Document checklist, form filling and appointment booking","Travel insurance required for Schengen and other visas"],
  why="We have been handling visas for travellers for decades, so we know what embassies look for and how to present your file correctly.",
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
  h1="Yatra Tour Packages from Mumbai",
  desc="Yatra packages from Mumbai – Char Dham, Kedarnath, Badrinath, Vaishno Devi, Amarnath, Kashi, Ayodhya, Shirdi, Dwarka and Jain tirth yatras – with comfortable stays and senior-friendly planning.",
  intro="A yatra is a journey of faith, and it deserves careful planning. We organise comfortable, well-paced yatras for families, senior citizens and groups, taking care of travel, stays, darshan planning and food.",
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
 dict(slug="wildlife-safari-tours", short="Wildlife Safaris", icon="🐅", img=None,
  title="Wildlife Safari Tours | Tadoba, Ranthambore, Jim Corbett, Gir, Kenya",
  h1="Wildlife Safari Tours in India and Africa",
  desc="Wildlife safari holidays – Tadoba, Ranthambore, Jim Corbett, Kanha, Bandhavgarh and Gir in India, and Kenya and Tanzania in Africa – with jungle lodges, safari permits and naturalist-led drives.",
  intro="See tigers, lions and elephants in the wild. We plan safari holidays with comfortable jungle lodges, safari permits booked in advance where available, and drives with experienced naturalists – for families, couples, photographers and school groups.",
  points=["Tadoba Andhari – the closest big tiger reserve from Mumbai","Ranthambore, Jim Corbett, Kanha and Bandhavgarh","Gir – home of the Asiatic lion","Kenya – Masai Mara and the great migration","Tanzania – Serengeti and Ngorongoro","Jungle lodges, safari permits and transfers in one package"],
  why="Safari permits at popular parks open well in advance and sell out quickly in peak season. Plan with us early and we handle permits, stays and transfers together.",
  faqs=[("When is the best time for a tiger safari in India?","Most Indian parks are open roughly from October to June, and sightings are often better in the warmer months when animals come to waterholes. Core zones usually close during the monsoon."),
        ("Do you book the safari permits?","Yes, we book safari permits along with your stay, as per each park's booking rules. Permits are limited, so early booking is best."),
        ("Are safaris suitable for children and seniors?","Yes. We choose comfortable lodges and suggest the right number of drives for your family. Some parks have age rules for certain activities – we check them for you.")]),
 dict(slug="women-only-group-tours", short="Women-only Tours", icon="👭", img=None,
  title="Women-only Group Tours | Safe, Fun Trips in India and Abroad",
  h1="Women-only Group Tours",
  desc="Women-only group tours from Mumbai to destinations in India and abroad – safe, well-planned trips with handpicked hotels, trusted transport and a woman tour manager on request. Join a group or start one with your friends.",
  intro="Travel with friends, sisters, mothers and daughters – or join like-minded women from your city. We plan comfortable, safe trips with handpicked hotels, trusted transport and a relaxed pace, so you can simply enjoy the journey.",
  points=["Fixed-departure women-only group trips","Private trips for your own group of friends or kitty / society group","Handpicked, well-reviewed hotels in safe locations","Trusted drivers and transport throughout","Woman tour manager on request for groups","Pure veg and Jain food arrangements"],
  why="Safety and comfort come first. We share full hotel, transport and contact details before you travel, and our team stays reachable throughout your trip.",
  faqs=[("Can I join alone?","Yes – on our women-only group departures you can join on your own and travel with other women. Ask us about upcoming dates."),
        ("Can you plan a private trip for our friends' group?","Yes, we plan private trips for kitty, society, college and office groups of women, on your dates."),
        ("Do you arrange room sharing?","On group tours we can arrange twin-sharing with another traveller, or a single room if you prefer.")]),
 dict(slug="adventure-trekking-tours", short="Adventure & Trekking", icon="🧗", img=None,
  title="Adventure & Trekking Tours | Himalayan Treks, Ladakh, Spiti, Bhutan",
  h1="Adventure & Trekking Tours",
  desc="Adventure and trekking tours – Himalayan treks like Kedarkantha, Hampta Pass and Tungnath, Ladakh and Spiti road trips, river rafting, paragliding, Bhutan and Nepal – planned with experienced local guides.",
  intro="From your first Himalayan trek to a Ladakh road trip, we plan adventure holidays with experienced local trek partners, proper acclimatisation days and the right gear list – for beginners, families, colleges and seasoned trekkers.",
  points=["Beginner Himalayan treks – Kedarkantha, Tungnath–Chandrashila, Brahmatal","Moderate treks – Hampta Pass, Valley of Flowers, Sar Pass","Ladakh and Spiti road trips","River rafting in Rishikesh, paragliding in Bir Billing","Bhutan and Nepal treks and adventure holidays","Sahyadri treks and camping near Mumbai"],
  why="Safety first: we work with experienced local trek operators, plan acclimatisation for high altitude, and share a fitness and packing checklist before you go.",
  faqs=[("I have never trekked. Where should I start?","Start with an easy trek like Tungnath–Chandrashila or Brahmatal. We suggest a few weeks of walking or jogging to build stamina before you go."),
        ("Is a medical check needed for high-altitude trips?","For high-altitude trips like Ladakh or longer treks, we recommend checking with your doctor first, especially for children, seniors and anyone with a medical condition."),
        ("Do you arrange trekking gear?","We share a packing list and can arrange rental gear such as jackets, trekking poles and sleeping bags with the local trek partner.")]),
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
 dict(slug="fit-mice-tours", short="FIT & MICE", icon="💼", img=None,
  title="FIT & MICE Tours | Corporate Travel, Incentive Trips & Conferences",
  h1="FIT & MICE Tours – Corporate Travel and Events",
  desc="FIT travel for individual travellers and MICE services – meetings, incentive trips, conferences and events – for companies in Mumbai, across India and abroad. The Real Tours and Travels, since 1981.",
  intro="We handle independent (FIT) travel for individuals and couples, and corporate MICE travel – meetings, incentive tours, conferences and events – with reliable logistics and a single point of contact.",
  points=["FIT – flexible independent itineraries for individuals and couples","Dealer and employee incentive trips","Conferences, offsites and annual meets","Venue, hotel and banquet sourcing","Group flights, visas and travel insurance","On-ground coordination and event support"],
  why="We combine personal service with the experience to manage group logistics, so your team or guests travel smoothly.",
  faqs=[("What does MICE stand for?","Meetings, Incentives, Conferences and Exhibitions/Events – business travel for groups."),
        ("Do you arrange corporate offsites near Mumbai?","Yes, as well as domestic and international incentive trips."),
        ("Can you handle visas for a corporate group?","Yes, we coordinate group visas, flights and insurance.")]),
 dict(slug="airport-transfers-outstation-cabs", short="Airport Transfers & Cabs", icon="🚖", img=None,
  title="Mumbai Airport Transfers & Outstation Cabs | Car Hire from Mulund",
  h1="Airport Transfers & Outstation Cabs from Mumbai",
  desc="Mumbai airport pick-up and drop, outstation cabs and car hire from Mulund and Thane – sedans, SUVs, Innova and tempo travellers with experienced drivers. Book with The Real Tours and Travels.",
  intro="On-time airport pick-ups and drops at Mumbai (BOM) and Navi Mumbai airports, and comfortable cars for weekend trips, pilgrimages and outstation journeys – with experienced drivers and one number to call.",
  points=["Mumbai and Navi Mumbai airport pick-up and drop","Outstation one-way and round trips – Pune, Nashik, Shirdi, Lonavala, Goa and more","Sedan, SUV, Innova Crysta and tempo traveller options","Meet & greet with name board on arrival","Full-day and half-day local car hire","Cars for weddings, groups and corporate guests"],
  why="We have arranged travel for families for over four decades. Every booking is confirmed with the driver's details in advance, and we are on call if plans change.",
  faqs=[("Do you track flight delays for pick-ups?","Share your flight number and we plan the pick-up around the actual arrival time."),
        ("Can I book a cab for a multi-day trip?","Yes – outstation round trips for any number of days, with the same car and driver."),
        ("Which cars are available?","Sedans, SUVs, Innova Crysta and tempo travellers for larger groups. Tell us the number of passengers and luggage and we suggest the right car.")]),
 dict(slug="weekend-getaways-from-mumbai", short="Weekend Getaways", icon="🏞️", img=None,
  title="Weekend Getaways from Mumbai | Lonavala, Mahabaleshwar, Alibaug, Igatpuri",
  h1="Weekend Getaways from Mumbai",
  desc="Short weekend trips from Mumbai – Lonavala, Mahabaleshwar, Alibaug, Igatpuri, Matheran, Karjat, Panchgani and Dapoli – with resorts, villas and car transfers planned by The Real Tours and Travels.",
  intro="Need a quick break? We plan relaxed 1–3 night getaways close to Mumbai – the right resort or villa, a comfortable car from your doorstep and a simple plan for the weekend.",
  points=["Lonavala and Khandala","Mahabaleshwar and Panchgani","Alibaug, Kashid and Dapoli beaches","Igatpuri, Karjat and Matheran","Pool villas and family resorts","Doorstep car pick-up from Mumbai and Thane"],
  why="We know the hotels and resorts around Mumbai well and match them to your family – kids, seniors, pets or a quiet couple's break.",
  faqs=[("Can you plan a trip for this weekend?","Often yes – WhatsApp us your dates and we check what's available right away."),
        ("Do you arrange villas for large families?","Yes, private villas and bungalows for family and friends' groups."),
        ("Is transport included?","We can include a car from your home, or you can drive yourself – your choice.")]),
 dict(slug="senior-citizen-tours", short="Senior Citizen Tours", icon="👴", img=None,
  title="Senior Citizen Tours from Mumbai | Slow-paced, Wheelchair-friendly Holidays",
  h1="Senior Citizen Tours – Comfortable, Slow-paced Holidays",
  desc="Holidays and yatras planned for senior citizens from Mumbai – relaxed pacing, wheelchair-friendly hotels, airport assistance, lifts and ground-floor rooms, and pure veg or Jain food.",
  intro="Travel at a pace that suits you. We plan trips for parents and grandparents with fewer hotel changes, shorter drives, wheelchair and airport assistance, and someone to call at any time.",
  points=["Relaxed itineraries with rest time every day","Wheelchair and airport assistance arranged with airlines","Hotels with lifts, ground-floor or accessible rooms","Pure vegetarian and Jain food arrangements","Domestic tours, yatras and international holidays","Travel insurance for senior citizens"],
  why="Many of our travellers have been with us for decades. We plan every senior citizen trip as carefully as we would for our own parents.",
  faqs=[("Can you arrange a wheelchair at the airport?","Yes, we request wheelchair assistance with the airline when booking the tickets."),
        ("Do you have group tours only for seniors?","We plan both private family trips and group tours for senior citizens – ask us about upcoming groups."),
        ("Is travel insurance available for people above 70?","Yes, there are plans for travellers above 60 and 70. Pre-existing conditions must be declared.")]),
 dict(slug="destination-weddings-family-functions", short="Destination Weddings", icon="💍", img=None,
  title="Destination Weddings & Family Functions | Venues, Room Blocks, Guest Travel",
  h1="Destination Weddings & Family Functions",
  desc="Destination weddings, engagements, anniversaries and family functions in India and abroad – venues, hotel room blocks, guest flights, transfers and Jain or vegetarian catering, planned by The Real Tours and Travels.",
  intro="Celebrate with everyone together. We handle the travel side of your wedding or family function – venue and hotel options, room blocks for guests, flights and trains, transfers and on-ground coordination.",
  points=["Wedding and function venues in India and abroad","Hotel room blocks for all your guests","Group flights, trains and coaches for guests","Airport and venue transfers","Jain and vegetarian catering arrangements","One coordinator for the families from start to finish"],
  why="Big family events need calm planning. With 45+ years of group travel experience, we take care of the logistics so the family can enjoy the occasion.",
  faqs=[("Where can we plan a destination wedding?","Popular choices include Udaipur, Jaipur, Goa, Kerala, Dubai, Bali and Thailand – we suggest venues to suit your guest list and budget."),
        ("Can you book rooms for 100+ guests?","Yes, we arrange room blocks and group rates with hotels and resorts."),
        ("Do you arrange guest travel from different cities?","Yes, we book flights and trains for guests travelling from different cities.")]),
 dict(slug="school-college-educational-tours", short="Educational Tours", icon="🎓", img=None,
  title="School & College Educational Tours from Mumbai | Study Trips & Industrial Visits",
  h1="School & College Educational Tours",
  desc="Educational tours for schools and colleges from Mumbai – study trips, industrial visits, heritage and science tours, adventure camps and international student tours with safe transport and supervised stays.",
  intro="Learning trips that are safe, well-organised and fun. We plan educational tours for schools, colleges and coaching institutes – with student-friendly stays, safe transport and a clear day-by-day plan for teachers.",
  points=["Heritage and history tours","Science, space and industrial visits","Nature, wildlife and adventure camps","College and university tours abroad","Safe AC coaches and train bookings","Supervised stays and pure veg meals"],
  why="Safety comes first. We share the full itinerary, hotel and transport details with the school in advance and stay in touch with the teachers throughout.",
  faqs=[("Do you provide a tour manager?","Yes, a tour manager can travel with the group to coordinate stays, meals and visits."),
        ("Can you handle permissions and documents?","We help with the travel documents and ID lists needed for trains, flights and hotels; school approvals are handled by the institution."),
        ("Do you arrange international student tours?","Yes, including visas and travel insurance for students and teachers.")]),
 dict(slug="police-clearance-certificate-pcc-document-services", short="PCC & Documents", icon="📄", img="passport.jpg",
  title="Police Clearance Certificate (PCC) & Document Help | Mulund, Mumbai",
  h1="Police Clearance Certificate (PCC) & Document Help",
  desc="Help with the Police Clearance Certificate (PCC) for Indian passport holders – for visas, emigration, study or jobs abroad – plus help with document attestation and apostille. The Real Tours and Travels, Mulund West.",
  intro="Many countries ask for a Police Clearance Certificate (PCC) for long-stay visas, study, work or permanent residence. We help you fill the application, book the appointment and prepare the right documents.",
  points=["PCC application for Indian passport holders via Passport Seva","Appointment booking at the Passport Seva Kendra / POPSK","Document checklist for your case (current address, passport details)","Help with attestation and apostille of certificates through authorised agencies","Visa file preparation for long-stay, study and work visas","Reminders and follow-up until your certificate is ready"],
  why="We have helped families with passports and visas for decades. We check your documents before your appointment, so you go once and go prepared.",
  faqs=[("Who needs a Police Clearance Certificate?","It is usually asked for long-stay, work, study, emigration or permanent residence visas. The embassy or employer will tell you if you need one."),
        ("How long does a PCC take?","It depends on your address and whether police verification is needed. We tell you the expected time for your case before you apply."),
        ("Can you help with apostille?","Yes, we help with attestation and apostille of documents through authorised agencies, as required by the country you are going to.")]),
 dict(slug="jain-yatra-tours-with-maharaj", short="Jain Yatra with Maharaj", icon="🙏", img="jain.jpg",
  title="Jain Yatra Tours with Maharaj | Pure Jain Food on Tour from Mumbai",
  h1="Jain Yatra Tours with Maharaj (Pure Jain Food)",
  desc="Jain tirth yatras and holidays with our own travelling Maharaj cooking pure Jain food – Palitana, Shikharji, Girnar, Ranakpur and more. Ideal for families, senior citizens and Jain groups from Mumbai.",
  intro="Food is often the biggest concern for Jain families on tour. On our Jain yatra tours, a Maharaj travels with the group and prepares fresh, pure Jain food (no root vegetables, timings respected) throughout the journey.",
  points=["Palitana (Shatrunjay) and Girnar yatra","Sammed Shikharji and eastern tirth yatra","Ranakpur, Nakoda and Rajasthan tirths","Shankheshwar and Gujarat tirths","Custom family and community group yatras","Holidays with Jain food in India and abroad"],
  why="We are a family business from Mumbai that has looked after Jain travellers for over four decades – comfortable stays, sensible pacing for elders and food you can trust.",
  faqs=[("Does the Maharaj travel with the group?","Yes, the Maharaj travels with the group and cooks fresh Jain food daily."),
        ("Is chauvihar / sunset meal timing followed?","Yes, meal timings are planned to respect chauvihar and other observances."),
        ("Can you arrange Jain food on international trips?","Yes, we arrange Jain food options for many international destinations too.")]),
]

# Upcoming group yatras with Maharaj – add (title, dates, short note) to publish them. No prices.
UPCOMING_YATRAS = [
]

REVIEWS = [
 ("Nitya K.", "Our Thailand trip was a great experience, thanks to Pratik. The arrangements were seamless and he was just a call away throughout the trip."),
 ("Neeteish J.", "I am a frequent traveller and have never faced any hassle with their bookings. Services are personal and full of effort."),
 ("Aahana K.", "Excellent service! Very professional, helpful and well-organised team. Had a smooth and comfortable travel experience."),
 ("Annu S.", "One stop for all your travelling requirements. Would personally recommend."),
]

CSS = """.about-story h2{margin:6px 0 14px}.about-story .kicker{display:flex;margin:40px 0 0}.about-story .kicker:first-child{margin-top:0}.about-story p{font-size:17px;line-height:1.75}.about-quote{margin:24px 0;padding:18px 24px;border-left:4px solid var(--red);background:#fdf0f0;border-radius:0 14px 14px 0;font-style:italic;font-weight:600;font-size:19px;line-height:1.6;color:var(--crimson)}.about-sign{margin-top:34px;text-align:center;padding:28px 18px;border-top:1px solid var(--line)}.about-sign b{display:block;font-size:22px;letter-spacing:2px;color:var(--crimson)}.about-sign span{display:block;color:var(--muted);letter-spacing:3px;text-transform:uppercase;font-size:13px;margin:4px 0 14px}.about-sign strong{display:block;font-size:18px}.about-sign em{display:block;margin-top:8px;color:var(--muted);font-size:17px}

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
header.site .hrow{display:flex;align-items:center;justify-content:space-between;padding:10px 22px;max-width:1320px}@media(min-width:1101px){header.site .hrow{justify-content:center}}header.site{position:sticky}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none;color:var(--wine)}
.brand img{width:64px;height:64px}
.brand b{white-space:nowrap;font-family:'Playfair Display',serif;font-size:22px;letter-spacing:.2px;line-height:1.1;color:var(--crimson)}
.brand small{display:block;color:var(--muted);font-weight:500;font-size:12px;letter-spacing:2px;text-transform:uppercase;margin-top:3px}
nav.main{border-top:1px solid var(--line)}.navrow{display:flex;justify-content:center;flex-wrap:wrap;gap:2px 22px;padding-top:9px!important;padding-bottom:9px!important;max-width:1320px}
nav.main a{color:var(--wine);text-decoration:none;font-weight:500;font-size:15px;white-space:nowrap;padding:2px 0;border-bottom:2px solid transparent}nav.main a:hover{border-bottom-color:var(--red)}
.hact{display:flex;align-items:center;gap:10px}.hcta{background:linear-gradient(135deg,var(--red),var(--crimson));color:#fff;text-decoration:none;font-weight:600;padding:10px 20px;border-radius:999px;box-shadow:0 6px 16px rgba(142,14,22,.25);white-space:nowrap}
nav.main a:hover{color:var(--red)}
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
.float-wa{transition:opacity .2s;position:fixed;right:18px;bottom:18px;z-index:60;background:#25D366;color:#fff;width:60px;height:60px;border-radius:50%;display:grid;place-items:center;box-shadow:0 8px 22px rgba(0,0,0,.3);text-decoration:none;font-size:28px}
.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:40px}
.info{background:var(--bg);border:1px solid var(--line);border-radius:18px;padding:32px}
.info p{margin:0 0 14px}
.map{border:0;width:100%;min-height:380px;height:100%;border-radius:18px;outline:1px solid var(--line)}
:focus-visible{outline:3px solid var(--red);outline-offset:3px}
@media(max-width:1100px){nav.main{display:none;position:absolute;left:0;right:0;top:100%;background:#fff;box-shadow:0 10px 24px rgba(0,0,0,.1)}nav.main.open{display:block}.navrow{flex-direction:column;align-items:flex-start;padding:10px 22px 16px!important}nav.main a{display:block;padding:10px 0;font-size:16px;border-bottom:1px solid var(--line);width:100%}.menu-btn{display:block}}
@media(max-width:900px){.hero .wrap{grid-template-columns:1fr;gap:28px;padding:36px 18px 56px;text-align:left}.seal{width:200px;height:200px;order:-1;box-shadow:0 0 0 8px #fdf0f0,0 14px 30px rgba(0,0,0,.10)}
.two,.contact-grid,footer .wrap{grid-template-columns:1fr}section{padding:52px 0}.brand b{font-size:16px}.brand img{width:48px;height:48px}.brand small{font-size:10px;letter-spacing:1.2px}
.wrap{padding-left:18px;padding-right:18px}header.site .wrap{padding:8px 18px}.topbar .wrap{justify-content:center;gap:6px 14px;font-size:12.5px}
.hero h1{font-size:clamp(28px,8vw,38px)}.hero p{font-size:16.5px;margin-bottom:22px}.kicker{font-size:11px;letter-spacing:1.2px;flex-wrap:wrap;row-gap:4px}
.btns{flex-direction:column}.btns .btn{justify-content:center;width:100%}
.trust{gap:18px 28px;margin-top:28px}.trust b{font-size:24px}
.head{margin-bottom:30px}.card{padding:24px 20px}.emblem{padding:34px 22px}.emblem img{width:150px}
.float-wa.tuck{opacity:0;pointer-events:none}
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
      "areaServed":[{"@type":"City","name":n} for n in ["Mulund","Bhandup","Nahur","Thane","Vikhroli","Ghatkopar","Powai","Kanjurmarg","Navi Mumbai","Mumbai"]]+[{"@type":"Country","name":"India"},{"@type":"Place","name":"Worldwide"}],
      "slogan":"Crafting Journeys Since 1981","alternateName":["Real Tours and Travels","The Real Tours & Travels","Real Tours Mulund"],
      "priceRange":"₹₹","currenciesAccepted":"INR","paymentAccepted":"Cash, UPI, Credit Card, Debit Card, Net Banking",
      "knowsLanguage":["en","hi","gu","mr"],
      "hasMap":MAPS,"sameAs":[IG,FB,MAPS],
      "makesOffer":[{"@type":"Offer","itemOffered":{"@type":"Service","name":s["h1"],"url":f"{SITE}/{s['slug']}/"}} for s in SERVICES]}

from svcform import CFG as _SVC_CFG
SVC_SLUGS = set(_SVC_CFG)

def jain_extra(s):
    if UPCOMING_YATRAS:
        up = "".join(f'<div class="yd"><div><b>{t}</b><br><span class="meta">{d}{(" · " + n) if n else ""}</span></div><a class="btn outline" href="#enquire" data-yatra="{t}">Register interest</a></div>' for t, d, n in UPCOMING_YATRAS)
    else:
        up = '<div class="ynone"><p style="margin:0 0 10px">New <b>group yatra dates with Maharaj</b> are announced here and on our Instagram <b>@therealtoursandtravels</b>.</p><a class="btn gold" href="#enquire" data-yatra="">🔔 Tell me about the next group yatra</a></div>'
    return f'''<section class="alt" id="upcoming"><div class="wrap" style="max-width:960px"><div class="head"><span class="kicker">Group yatras</span><h2>Upcoming group yatras with Maharaj</h2><p class="lead">Join a group yatra with pure Jain food cooked fresh every day – or plan a private yatra for your family.</p></div>
<div class="yup">{up}</div></div></section>
<section><div class="wrap"><div class="head"><span class="kicker">On tour</span><h2>What to expect on our Jain yatras</h2></div>
<div class="yexp">
<div><h3>🍲 Food &amp; kitchen</h3><ul><li>Our Maharaj travels with the group and cooks fresh Jain food every day</li><li>No onion, garlic, potatoes or other root vegetables</li><li>Meal times planned for chovihar, with tithi days respected</li><li>Boiled or filtered drinking water arranged</li></ul></div>
<div><h3>🛕 A day on yatra</h3><ul><li>Early starts for darshan and puja, before the heat</li><li>Sensible daily distances and rest breaks for elders</li><li>Help with dolis / palkis for climbs such as Palitana and Girnar</li><li>One tour manager looking after the group throughout</li></ul></div>
<div><h3>🏨 Stays &amp; travel</h3><ul><li>Clean dharamshalas or hotels close to the tirth – your choice</li><li>Comfortable AC coach, tempo traveller or car, as per group size</li><li>Train or flight tickets arranged from Mumbai</li><li>Travel insurance available for senior citizens</li></ul></div>
<div><h3>🎒 What to pack</h3><ul><li>Puja clothes and a small puja kit</li><li>Comfortable footwear that is easy to remove</li><li>Personal medicines and a copy of prescriptions</li><li>Light woollens for early mornings in winter</li><li>Original photo ID (Aadhaar / passport) for every traveller</li></ul></div>
</div></div></section>'''

SVC_PHOTO = {"domestic-holiday-packages":"kashmir","international-holiday-packages":"dubai","passport-visa-services":"passport","travel-insurance":"airport",
 "yatra-tours":"yatra","group-tours":"group","honeymoon-packages":"honeymoon","fit-mice-tours":"mice","airport-transfers-outstation-cabs":"cab",
 "weekend-getaways-from-mumbai":"weekend","senior-citizen-tours":"senior","destination-weddings-family-functions":"wedding",
 "school-college-educational-tours":"heritage","police-clearance-certificate-pcc-document-services":"pcc","jain-yatra-tours-with-maharaj":"jain",
 "wildlife-safari-tours":"safari","women-only-group-tours":"women","adventure-trekking-tours":"trek"}
PAGE_PHOTO = {f"/{k}/": v for k, v in SVC_PHOTO.items()}
PAGE_PHOTO.update({"/visa/":"passport","/passport/":"planning","/insurance/":"airport","/flights-hotels/":"maldives","/customize-your-package/":"swiss",
 "/contact/":"mumbai","/about/":"mumbai","/blog/":"heritage"})

def seo_title(t, limit=65):
    """Keep titles short enough for Google results: drop secondary parts before cutting."""
    if len(t) <= limit:
        return t
    brand = " | The Real Tours and Travels"
    base = t[:-len(brand)] if t.endswith(brand) else t
    for sep in (" | ", " – ", ": "):
        while len(base + brand) > limit and sep in base:
            base = base.rsplit(sep, 1)[0]
    if len(base + brand) <= limit:
        return base + brand
    return base if len(base) <= limit else base[:limit - 1].rsplit(" ", 1)[0] + "…"

def seo_desc(d, limit=158):
    if len(d) <= limit:
        return d
    cut = d[:limit].rsplit(" ", 1)[0].rstrip(",;–- ")
    return cut + "…"

def page(path, title, desc, body, extra_ld=None, hero_img=None):
    title, desc = seo_title(title), seo_desc(desc)
    canonical = SITE + path
    _ph = PAGE_PHOTO.get(path)
    if _ph:
        _root = "../" * path.strip("/").count("/") + "../"
        body = re.sub(r'<section class="hero"(?: style="[^"]*")?>', f'<section class="hero home-hero photo-hero" style="--hero:url({_root}img/h-{_ph}.jpg)">', body, count=1)
        hero_img = f"h-{_ph}.jpg"
    lds = [jsonld_org()] + (extra_ld or [])
    if path == "/":
        lds.append({"@context":"https://schema.org","@type":"WebSite","@id":SITE+"/#website","name":NAME,"alternateName":["Real Tours and Travels","The Real Tours & Travels"],"url":SITE+"/","publisher":{"@id":SITE+"/#agency"},"inLanguage":"en-IN"})
    elif not any(isinstance(x, dict) and x.get("@type") == "BreadcrumbList" for x in lds):
        _name = title.split(" | ")[0].split(" – ")[0]
        lds.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},{"@type":"ListItem","position":2,"name":_name,"item":SITE+path}]})
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    depth = path.strip("/").count("/") + (1 if path.strip("/") else 0)
    root = "../" * depth if depth else ""
    og = SITE + "/img/" + (hero_img or "logo-512.png")
    nav = "".join(f'<li><a href="{root}{s["slug"]}/">{s["short"]}</a></li>' for s in SERVICES) + f'<li><a href="{root}customize-your-package/">Customized Packages</a></li>'
    return f"""<!doctype html>
<html lang="en-IN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}"><link rel="alternate" hreflang="en-IN" href="{canonical}"><link rel="alternate" hreflang="x-default" href="{canonical}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{og}">
<meta property="og:locale" content="en_IN"><meta property="og:image:alt" content="{NAME}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{og}">
<meta name="geo.region" content="IN-MH"><meta name="geo.placename" content="Mulund West, Mumbai">{'<link rel="preload" as="image" href="img/hero-travel.jpg" fetchpriority="high">' if path=="/" else ''}
<meta name="theme-color" content="#ffffff">
{pwa.HEAD}
{account.SITE_JS}
<link rel="icon" type="image/png" href="{root}favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600&family=Playfair+Display:ital,wght@0,600;0,700;1,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}style.css?v={CSSV}">
{ld}
</head><body>

<header class="site"><div class="wrap hrow">
<a class="brand" href="{root or './'}"><img src="{root}img/logo.png" alt="The Real Tours and Travels logo – Estd. 1981" width="64" height="64"><span><b>The Real Tours and Travels</b><small>Crafting Journeys Since 1981</small></span></a>
<a class="acct-link" id="acctLink" href="{root}account/">👤 Login</a>
<div class="hact"><button class="menu-btn" aria-label="Menu" aria-expanded="false" onclick="const n=document.querySelector('nav.main');n.classList.toggle('open');this.setAttribute('aria-expanded',n.classList.contains('open'))">☰</button></div></div>
<nav class="main" aria-label="Main"><div class="wrap navrow"><a href="{root}flights-hotels/#flights">Flights</a><a href="{root}flights-hotels/#hotels">Hotels</a><a href="{root}flights-hotels/#cruise">Cruise</a><a href="{root}visa/">Visa</a><a href="{root}passport/">Passport</a><a href="{root}insurance/">Travel Insurance</a><a href="{root}customize-your-package/">Customized Packages</a><a href="{root}jain-yatra-tours-with-maharaj/">Jain Yatra</a><a href="{root or './'}#services">Services</a><a href="{root}contact/">Contact Us</a><a href="{root}about/">About Us</a></div></nav>
</header>
<main>
{body}
</main>
<footer><div class="wrap">
<div><a class="brand" href="{root or './'}" ><img src="{root}img/logo.png" alt="" width="52" height="52"><span><b>The Real Tours and Travels</b><small>Crafting Journeys Since 1981</small></span></a>
<p>Trusted travel agency since 1981 for family holidays, international tours, visas, yatras and Jain tours since 1981.</p>
<p>{'<br>'.join(ADDR)}<br><span class="gst">GSTIN: {GST}</span></p>
<p><a href="tel:{PHONE_RAW}">📞 {PHONE}</a><br><a href="mailto:{EMAIL}">✉️ {EMAIL}</a><br>
<a href="{IG}" target="_blank" rel="noopener">📸 @therealtoursandtravels</a> · <a href="{FB}" target="_blank" rel="noopener">Facebook</a></p></div>
<div><h4>Our Services</h4><ul>{nav}</ul></div>
<div><h4>Visit Us</h4><ul><li>Open every day, 9 am – 10 pm</li><li><a href="{MAPS}" target="_blank" rel="noopener">Get directions on Google Maps</a></li><li><a href="{REVIEW}" target="_blank" rel="noopener">⭐ Review us on Google</a></li><li><a href="{root}flights-hotels/">✈️ Flights, hotels &amp; cruise</a></li><li><a href="{root}customize-your-package/">✨ Customized Packages</a></li><li><a href="{root}visa/">Visa documents &amp; upload</a></li><li><a href="{root}passport/">Passport services</a></li><li><a href="{root}insurance/">Travel insurance quote</a></li><li><a href="{root}blog/">Travel guides &amp; tips</a></li><li><a href="{root}account/">👤 My account / Login</a></li><li><a href="{root}about/">About us</a></li><li><a href="{root}contact/">Contact us</a></li></ul>
</div>
 </div><div class="topbar"><div class="wrap"><span>📍 Mulund West, Mumbai · Open daily 9 am – 10 pm</span><span><a href="tel:{PHONE_RAW}">📞 {PHONE}</a> · <a href="mailto:{EMAIL}">✉️ {EMAIL}</a></span></div></div><div class="copy">© {datetime.date.today().year} The Real Tours and Travels, Mulund West, Mumbai · GSTIN {GST} · All rights reserved.<br><a href="{root}terms/">Terms &amp; Conditions</a> · <a href="{root}privacy-policy/">Privacy Policy</a> · <a href="{root}cancellation-refund-policy/">Cancellation &amp; Refund Policy</a></div></footer>
<a class="float-wa" href="{WA}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">💬</a>
<script>(function(){{const w=document.querySelector('.float-wa');if(!w)return;let q=0;
function chk(){{q=0;w.style.pointerEvents='none';const r=w.getBoundingClientRect(),m=r.left+r.width/2,c=r.top+r.height/2;
const hit=[.15,.5,.85].flatMap(fx=>[.15,.5,.85].map(fy=>[r.left+r.width*fx,r.top+r.height*fy])).some(([x,y])=>{{const e=document.elementFromPoint(x,y);return e&&e!==w&&e.closest('a,button,input,select,textarea,label,summary');}});
w.style.pointerEvents='';w.classList.toggle('tuck',hit);}} /* hide the WhatsApp bubble while it would cover a button or form field */
addEventListener('scroll',()=>{{if(!q)q=requestAnimationFrame(chk);}},{{passive:true}});addEventListener('resize',chk);addEventListener('load',chk);chk();}})();</script>
{fx.jain_popup(root)}
{pwa.BODY}
{fx.JS}
</body></html>"""

_IMG_SRC = re.compile(r'((?:src|href)="[^"]*img/[^"]+)\.jpg"')
_IMG_URL = re.compile(r'(url\([^)]*img/[^)]+)\.jpg\)')
def webpify(html):
    head, sep, rest = html.partition("</head>")
    if not sep:
        return html
    head = head.replace('href="img/hero-travel.jpg" fetchpriority', 'href="img/hero-travel.webp" type="image/webp" fetchpriority')
    rest = _IMG_SRC.sub(lambda m: m.group(1) + '.webp"' if os.path.exists(os.path.join(os.path.dirname(__file__), "img", m.group(1).split("img/")[-1] + ".webp")) else m.group(0), rest)
    rest = _IMG_URL.sub(lambda m: m.group(1) + '.webp)', rest)
    return head + sep + rest

def write(path, html):
    html = webpify(html)
    fp = os.path.join(os.path.dirname(__file__), path.strip("/"), "index.html") if path != "/" else os.path.join(os.path.dirname(__file__), "index.html")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w").write(html)

RIDGE = '<svg class="ridge" viewBox="0 0 1440 120" preserveAspectRatio="none" aria-hidden="true"><path d="M0 120 L0 70 L120 40 L210 75 L330 20 L450 80 L560 45 L690 90 L820 30 L930 70 L1050 15 L1170 75 L1290 40 L1440 80 L1440 120 Z" fill="#fff"/><path d="M0 70 L120 40 L210 75 L330 20 L450 80 L560 45 L690 90 L820 30 L930 70 L1050 15 L1170 75 L1290 40 L1440 80" fill="none" stroke="#C8A25A" stroke-width="2"/></svg>'

def seal(root):
    return f'<div class="seal"><img src="{root}img/logo.png" alt="The Real Tours and Travels – Estd. 1981" width="300" height="300"></div>'

def cta_band():
    return f"""<section class="band"><div class="wrap"><span class="kicker">Since 1981</span><h2>Plan your next holiday with us</h2><p>Tell us where you want to go – we'll handle the rest. No obligation.</p>
<div class="btns" style="justify-content:center"><a class="btn gold" href="{WA}" target="_blank" rel="noopener">💬 WhatsApp 98431 21212</a><a class="btn ghost" href="tel:{PHONE_RAW}">📞 Call now</a></div></div></section>"""

CSSV = "0"

def build():
    root = os.path.dirname(os.path.abspath(__file__))
    global CSSV
    css_all = CSS + VISA_CSS + PLANNER_CSS + FLIGHT_CSS + TOOL_CSS + pwa.CSS + account.ACCOUNT_CSS + SVC_CSS + fx.CSS
    CSSV = __import__("hashlib").md5(css_all.encode()).hexdigest()[:8]
    open(os.path.join(root, "style.css"), "w").write(css_all)
    imgs = set(os.listdir(os.path.join(root, "img")))
    # Home
    cards = "".join(f'<a class="card pcard" href="{s["slug"]}/"><img class="cimg" src="img/c-{SVC_PHOTO.get(s["slug"],"swiss")}.jpg" alt="{s["short"]} – The Real Tours and Travels" loading="lazy" width="640" height="420"><div class="ic">{s["icon"]}</div><h3>{s["h1"]}</h3><p>{s["desc"][:120].rsplit(" ",1)[0]}…</p><span class="more">Explore →</span></a>' for s in SERVICES)
    cards += '<a class="card pcard" href="customize-your-package/"><img class="cimg" src="img/c-swiss.jpg" alt="Customized Packages – The Real Tours and Travels" loading="lazy" width="640" height="420"><div class="ic">✨</div><h3>Customized Packages – Plan Your Own Trip</h3><p>Type the places you want to visit, choose your dates and hotels, and get an instant day-by-day itinerary…</p><span class="more">Explore →</span></a>'
    revs = "".join(f'<div class="review"><div class="stars">★★★★★</div><p>“{t}”</p><b>— {n}</b></div>' for n, t in REVIEWS)
    hero = "hero-travel.jpg" if "hero-travel.jpg" in imgs else None
    RJ = fx.load_reviews()
    hero_style = f' style="--hero:url(img/{hero})"' if hero else ""
    side = "dubai.jpg" if "dubai.jpg" in imgs else None
    side_html = f'<div class="photo"><img src="img/{side}" alt="Indian family holiday in Dubai planned by The Real Tours and Travels" loading="lazy" width="800" height="600"></div>' if side else '<div class="emblem"><img src="img/logo.png" alt="The Real Tours and Travels emblem"><b>Crafting Journeys Since 1981</b><p>A Mulund family business trusted by generations of travellers in India and abroad.</p></div>'
    home = f"""
<section class="hero home-hero"{hero_style}><div class="wrap"><div>
<span class="kicker">Trusted travel experts · Since 1981</span>
<h1>Travel Agency in Mulund, Mumbai for All Your Travel Needs</h1>
<p>Domestic and international holiday packages, honeymoons, yatras, Jain tours with Maharaj, group tours, passport &amp; visa services and travel insurance – planned personally by The Real Tours and Travels.</p>
<div class="btns"><a class="btn gold" href="customize-your-package/">✨ Customized Packages</a><a class="btn ghost" href="{WA}" target="_blank" rel="noopener">💬 WhatsApp 98431 21212</a></div>
<div class="trust"><div><b>45+ years</b>serving travellers since 1981</div><div><b>{RJ["rating"]} ★</b>rating on Google</div><div><b>10+</b>travel services under one roof</div></div>
</div>{seal("")}</div>{RIDGE}</section>
<section class="fsec"><div class="wrap">{flight_widget("")}</div></section>
<section id="services"><div class="wrap">
<div class="head"><span class="kicker">What we do</span><h2>Our Travel Services</h2><p class="lead">Everything you need for a stress-free trip – from the first idea to the day you return home.</p></div>
<div class="grid">{cards}</div></div></section>
{fx.gallery("")}
<section class="alt"><div class="wrap two">
<div><h2>Why travellers choose The Real Tours and Travels</h2>
<span class="kicker">Our promise</span><p class="lead" style="margin-bottom:20px">We are a family-run travel agency in Mulund West. For over four decades we have planned holidays, yatras and business trips – in India and around the world.</p>
<ul class="ticks"><li>Personal service – one point of contact, on call during your trip</li><li>Family-friendly hotels and comfortable pacing for kids and seniors</li><li>Visas, travel insurance, flights and hotels handled in one place</li><li>Pure vegetarian and Jain food arrangements, including tours with our own Maharaj</li><li>Transparent planning – no hidden surprises</li></ul></div>
{side_html}</div></section>
{fx.reviews_carousel(MAPS, REVIEW)}
<section class="alt"><div class="wrap" style="max-width:960px"><div class="head"><span class="kicker">Near you</span><h2>Travel agent in Mulund serving Mumbai, Thane and beyond</h2>
<p class="lead">Visit our office in Mulund West, or plan everything on call and WhatsApp. We look after travellers from Mulund, Bhandup, Nahur, Kanjurmarg, Vikhroli, Ghatkopar, Powai, Thane and Navi Mumbai – and clients across India and abroad, including NRIs.</p></div>
<div class="areas"><a href="flights-hotels/#flights">Flight tickets</a><a href="visa/">Visa agent in Mulund</a><a href="passport/">Passport services</a><a href="international-holiday-packages/">International tour packages</a><a href="domestic-holiday-packages/">Domestic tour packages</a><a href="honeymoon-packages/">Honeymoon packages</a><a href="jain-yatra-tours-with-maharaj/">Jain yatra with Maharaj</a><a href="yatra-tours/">Char Dham &amp; yatra tours</a><a href="travel-insurance/">Travel insurance</a><a href="airport-transfers-outstation-cabs/">Airport cabs</a><a href="weekend-getaways-from-mumbai/">Weekend getaways</a><a href="group-tours/">Group tours</a></div></div></section>
<section class="faq"><div class="wrap" style="max-width:860px"><div class="head"><span class="kicker">Good to know</span><h2>Frequently asked questions</h2></div>
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
    revs3 = "".join(f'<div class="review"><div class="stars">★★★★★</div><p>“{t}”</p><b>— {n}</b></div>' for n, t in REVIEWS[:3])
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
<div class="btns">{'<a class="btn gold" href="#enquire">📝 Send an enquiry</a>' if s['slug'] in SVC_SLUGS else ''}{'<a class="btn gold" href="../visa/">📄 Visa documents &amp; upload</a><a class="btn outline" href="../passport/">🛂 Passport services</a>' if s['slug']=='passport-visa-services' else ('<a class="btn gold" href="../insurance/#ins-form">🛡️ Get insurance quotation</a>' if s['slug']=='travel-insurance' else '')}<a class="btn gold" href="{WA}" target="_blank" rel="noopener">💬 Get a free plan on WhatsApp</a><a class="btn ghost" href="tel:{PHONE_RAW}">📞 98431 21212</a></div>
</div>{seal("../")}</div>{RIDGE}</section>
<section><div class="wrap two"><div><h2>What we offer</h2><ul class="ticks">{pts}</ul></div>
<div><h2>Why book with us</h2><p>{s['why']}</p><p>Visit our office in <b>Mulund West, Mumbai</b> (open daily 9 am – 10 pm), or plan everything over call and WhatsApp.</p>
<p><a class="btn red" href="{'#enquire' if s['slug'] in SVC_SLUGS else WA}"{'' if s['slug'] in SVC_SLUGS else ' target="_blank" rel="noopener"'}>Plan my trip</a></p></div></div></section>
{jain_extra(s) if s['slug']=='jain-yatra-tours-with-maharaj' else ''}{svc_form(s['slug'])}
{fx.reviews_carousel(MAPS, REVIEW)}
<section class="faq"><div class="wrap" style="max-width:860px"><div class="head"><span class="kicker">Good to know</span><h2>Frequently asked questions</h2></div>{faqs}</div></section>
<section><div class="wrap"><div class="head"><span class="kicker">More from us</span><h2>Explore our other services</h2></div><div class="grid">{others}</div></div></section>
{cta_band()}"""
        faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in s["faqs"]]}
        svc_ld = {"@context":"https://schema.org","@type":"Service","name":s["h1"],"description":s["desc"],"provider":{"@id":SITE+"/#agency"},"areaServed":{"@type":"Country","name":"India"},"url":f"{SITE}/{s['slug']}/"}
        crumbs = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},{"@type":"ListItem","position":2,"name":s["short"],"item":f"{SITE}/{s['slug']}/"}]}
        write(f"/{s['slug']}/", page(f"/{s['slug']}/", s["title"] + " | The Real Tours and Travels", s["desc"], body, [svc_ld, faq_ld, crumbs], img))
    write("/customised-tours/", '<!doctype html><html lang="en-IN"><head><meta charset="utf-8"><title>Customized Packages | The Real Tours and Travels</title><link rel="canonical" href="'+SITE+'/customize-your-package/"><meta name="robots" content="noindex,follow"><meta http-equiv="refresh" content="0; url=../customize-your-package/"><script>location.replace("../customize-your-package/"+location.hash)</script></head><body><p>This page has moved to <a href="../customize-your-package/">Customized Packages</a>.</p></body></html>')
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
    blog = f"""<section class="hero"><div class="wrap"><div><div class="crumbs"><a href="../">Home</a> › Travel Guides</div><span class="kicker">Travel guides &amp; tips</span><h1>Travel Guides from The Real Tours and Travels</h1><p>Practical advice from 45+ years of planning holidays, yatras and visas for travellers in India and abroad.</p></div>{seal("../")}</div></section>
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
    # Customized Packages
    write("/customize-your-package/", page("/customize-your-package/", "Customized Holiday Packages – Instant Itinerary | The Real Tours and Travels", "Customized holiday packages from Mumbai to any destination in India or abroad – one place or a multi-city tour. Choose days, travellers, hotel, car and flight or train and get an instant day-by-day itinerary.", planner_page(PHONE, PHONE_RAW, EMAIL, WA, seal, cta_band, ADDR, GST), None, "gulmarg.jpg"))
    # Visa section
    write("/visa/", page("/visa/", "Visa Services in Mulund, Mumbai – Documents Required & Upload | The Real Tours and Travels", "Visa services in Mulund West, Mumbai for Dubai, Thailand, Singapore, Europe (Schengen), UK, USA, Canada, Australia, Japan and more. See documents required, request the price and upload documents securely.", visa_page(PHONE, PHONE_RAW, EMAIL, seal, cta_band), None, "passport.jpg"))
    write("/account/", page("/account/", "My Account – Login or Sign up | The Real Tours and Travels", "Log in or create your free The Real Tours and Travels account to save your details and see your enquiries.", account.account_page(PHONE, PHONE_RAW, EMAIL, WA, seal, cta_band)).replace('<meta name="robots" content="index,follow,max-image-preview:large">','<meta name="robots" content="noindex">'))
    # About us
    about = f"""<section class="hero"><div class="wrap"><div><div class="crumbs"><a href="../">Home</a> › About Us</div>
<span class="kicker">Crafting Journeys Since 1981</span><h1>About The Real Tours and Travels</h1>
<p><b>45 Years of Trust. Generations of Memories. A Legacy That Continues.</b></p></div>{seal("../")}</div></section>
<section class="about-story"><div class="wrap" style="max-width:900px">
<span class="kicker">1981</span><h2>Our Story – A Journey That Began in 1981</h2>
<p>Every great journey begins with a vision. The story of <b>THE REAL TOURS AND TRAVELS</b> began in 1981, when our founder, <b>Mr. Deepak Devji Kotak</b>, laid the foundation of a travel business built on trust, commitment, personal relationships and a passion for serving travellers.</p>
<p>At a time when the travel industry operated very differently from today, Mr. Deepak Devji Kotak envisioned creating a reliable travel service that people could confidently turn to for their travel requirements. With determination, dedication and years of hard work, he transformed that vision into a business that gradually earned the confidence of its customers.</p>
<p>His philosophy was simple: travel was not merely about booking tickets or arranging holidays; it was about understanding people, fulfilling their expectations and making every journey comfortable and memorable.</p>
<p>What started as a humble initiative became the foundation of a legacy that continues to inspire us even today.</p>

<span class="kicker">2015</span><h2>A New Chapter – Continuing the Legacy After 2015</h2>
<p class="lead"><b>Every legacy has a story, and every story has a responsibility to continue.</b></p>
<p>In 2015, our company faced one of its most challenging and emotional moments when our founder, Mr. Deepak Devji Kotak, left us. His absence created a void that could never truly be filled. Along with the personal loss came the responsibility of protecting and carrying forward everything he had built since 1981.</p>
<p>It was then that <b>Mr. Pratik Deepak Kotak</b> stepped forward to take charge of the business and shoulder the responsibility of continuing his father's vision.</p>
<p>Taking over an established business is never easy, especially when it carries decades of relationships, expectations and trust. The challenge was not simply to manage an existing business, but to preserve its identity, uphold its values and prepare it for a rapidly changing travel industry.</p>
<p>With determination, patience and a strong sense of responsibility, Mr. Pratik Deepak Kotak took the journey forward.</p>
<p>His approach was to respect the foundations laid by his father while recognising that the future of travel demanded a fresh outlook. He focused on strengthening customer relationships, improving service standards, expanding travel offerings and adapting to the evolving expectations of modern travellers.</p>
<p>The traditional values of personal attention, honest communication and customer satisfaction remained unchanged, while the company's approach continued to evolve with time.</p>
<p>For Mr. Pratik Deepak Kotak, this was more than taking over a family business. It was about preserving his father's dream, protecting a name built over decades and creating something meaningful for the next generation.</p>
<blockquote class="about-quote">The founder may no longer be with us, but his vision continues to live through every journey we organise and every customer we serve.</blockquote>

<span class="kicker">Today</span><h2>Where We Stand Today – Tradition Meets Modern Travel</h2>
<p>Today, under the leadership of <b>Mr. Pratik Deepak Kotak</b>, THE REAL TOURS AND TRAVELS continues its journey with the same founding principles while embracing the opportunities of the modern travel industry.</p>
<p>From its beginnings in 1981, the company has developed its service portfolio to cater to a wide range of travel requirements. We serve individuals, families, corporate organisations, large groups and religious communities with comprehensive travel solutions.</p>
<p>Our services extend across domestic and international holiday packages, flight and railway ticketing, hotel and resort reservations, cruise bookings, group tours, corporate travel, Jain pilgrimage tours, specialised religious tours, visa and passport assistance, travel insurance, bus ticketing and car rentals.</p>
<p>We also understand the unique requirements of group and pilgrimage travel, including Jain food arrangements, specialised itineraries, transportation coordination and other essential arrangements that make large-scale journeys comfortable and organised.</p>
<p>As the travel industry moves towards digitalisation, we are equally focused on modernising the way customers discover, plan and book their journeys. Our vision is to combine the reliability of a travel company established in 1981 with the convenience, accessibility and efficiency of modern technology.</p>
<p>We are working towards building a stronger digital presence, improving customer accessibility and bringing more travel services together under one platform.</p>
<p>Our objective is not just to keep pace with the changing industry, but to create better and more convenient travel experiences for the generations ahead.</p>
</div></section>
<section class="alt"><div class="wrap" style="max-width:1000px"><div class="head"><span class="kicker">Our values</span><h2>What We Believe In</h2></div>
<p style="text-align:center;max-width:760px;margin:0 auto 22px">At THE REAL TOURS AND TRAVELS, we believe that every traveller deserves attention, every requirement deserves a thoughtful solution and every journey deserves careful planning. Our foundation rests on five important values:</p>
<div class="grid">
<div class="card"><div class="ic">🤝</div><h3>Trust</h3><p>Building relationships that last beyond a single booking.</p></div>
<div class="card"><div class="ic">🧭</div><h3>Experience</h3><p>Applying decades of industry understanding to every travel arrangement.</p></div>
<div class="card"><div class="ic">💬</div><h3>Personal Attention</h3><p>Understanding the individual needs of every customer.</p></div>
<div class="card"><div class="ic">🌍</div><h3>Adaptability</h3><p>Embracing new destinations, technology and changing travel trends.</p></div>
<div class="card"><div class="ic">🙏</div><h3>Commitment</h3><p>Carrying forward the principles on which our company was established.</p></div>
</div></div></section>
<section class="about-story"><div class="wrap" style="max-width:900px">
<span class="kicker">Tomorrow</span><h2>Our Vision for the Future</h2>
<p>Our vision is to establish THE REAL TOURS AND TRAVELS as a trusted name in the domestic and international travel industry, recognised for its experience, personalised service and comprehensive travel solutions.</p>
<p>We aim to expand our reach, strengthen our partnerships, introduce modern booking facilities and continue creating memorable experiences for travellers across generations.</p>
<p>While our methods may evolve with time, our founding values will always remain the same.</p>

<span class="kicker">1981 – 2026</span><h2>45 Years of Trust – One Legacy, Many Journeys</h2>
<p>From 1981 to 2026, our journey has been shaped by dedication, challenges, learning and the trust of thousands of travellers.</p>
<p>We began with the vision of Mr. Deepak Devji Kotak. We continued through the determination and leadership of Mr. Pratik Deepak Kotak. Today, we stand committed to taking that legacy forward with renewed energy and a vision for tomorrow.</p>
<p>We are grateful to every customer, associate, business partner and well-wisher who has been part of our journey. Your confidence has been our greatest strength and your satisfaction continues to be our greatest reward.</p>
<p>As we look ahead, our promise remains unchanged: to serve with honesty, plan with care and make every journey worthwhile.</p>
<div class="about-sign"><b>THE REAL TOURS AND TRAVELS</b><span>Crafting Journeys Since 1981</span><strong>45 Years of Trust. A Legacy That Moves Forward.</strong><em>We don't just carry people to destinations; we carry forward a legacy built on trust.</em></div>
</div></section>
<section class="alt"><div class="wrap"><div class="head"><span class="kicker">What we do</span><h2>Our services</h2></div>
<div class="grid">
<a class="card" href="../flights-hotels/#flights"><div class="ic">✈️</div><h3>Flights</h3><p>Domestic and international air tickets at the best available fares.</p></a>
<a class="card" href="../flights-hotels/#hotels"><div class="ic">🏨</div><h3>Hotels</h3><p>Handpicked family-friendly hotels, resorts and villas in India and abroad.</p></a>
<a class="card" href="../flights-hotels/#cruise"><div class="ic">🛳️</div><h3>Cruises</h3><p>Cordelia, Royal Caribbean, Costa, MSC and more – from Mumbai and abroad.</p></a>
<a class="card" href="../visa/"><div class="ic">🛂</div><h3>Visa</h3><p>Documents, forms and appointments for tourist and business visas.</p></a>
<a class="card" href="../passport/"><div class="ic">📘</div><h3>Passport</h3><p>New passport, renewal, minor, Tatkaal and lost passport assistance.</p></a>
<a class="card" href="../insurance/"><div class="ic">🛡️</div><h3>Travel insurance</h3><p>Plans for families, seniors, students and Schengen visas.</p></a>
<a class="card" href="../customize-your-package/"><div class="ic">✨</div><h3>Customized packages</h3><p>Your dates, your pace, your budget – an itinerary made for you.</p></a>
<a class="card" href="../jain-yatra-tours-with-maharaj/"><div class="ic">🙏</div><h3>Jain yatra</h3><p>Tirth yatras with our own Maharaj and pure Jain food.</p></a>
</div></div></section>
<section><div class="wrap two"><div><h2>Visit us</h2><p>{'<br>'.join(ADDR)}</p><p>Open every day, 9 am – 10 pm</p><p>📞 <a href="tel:{PHONE_RAW}">{PHONE}</a><br>✉️ <a href="mailto:{EMAIL}">{EMAIL}</a><br>📸 <a href="{IG}" target="_blank" rel="noopener">@therealtoursandtravels</a></p>
<p><span class="gst">GSTIN: {GST}</span></p><div class="btns"><a class="btn gold" href="{WA}" target="_blank" rel="noopener">💬 WhatsApp us</a><a class="btn outline" href="{MAPS}" target="_blank" rel="noopener">📍 Directions</a></div></div>
<div class="emblem"><img src="../img/logo.png" alt="The Real Tours and Travels emblem"><b>Crafting Journeys Since 1981</b><p>A Mulund family business trusted by generations of travellers in India and abroad.</p></div></div></section>{cta_band()}"""
    about_ld = {"@context":"https://schema.org","@type":"AboutPage","name":"About The Real Tours and Travels","url":SITE+"/about/","about":{"@id":SITE+"/#agency"}}
    write("/about/", page("/about/", "About Us | The Real Tours and Travels – Mulund, Mumbai, Since 1981", "The story of The Real Tours and Travels – founded in 1981 by Mr. Deepak Devji Kotak and led today by Mr. Pratik Deepak Kotak. 45 years of trust in holidays, flights, hotels, cruises, visas, passports, insurance and Jain yatras.", about, [about_ld]))
    write("/insurance/", page("/insurance/", "Travel Insurance Quotation – International & Domestic | The Real Tours and Travels, Mumbai", "Get a travel insurance quotation for international, Schengen visa, USA, domestic, senior citizen, student and annual multi-trip plans from The Real Tours and Travels, Mulund West, Mumbai.", insurance_page(PHONE, PHONE_RAW, EMAIL, seal, cta_band), None, "flight.jpg"))
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
    # Private office admin panel (noindex, not in sitemap, access enforced by Supabase RLS)
    write("/admin/", admin.admin_page())
    # sitemap / robots / CNAME
    urls = ["/"] + [f"/{s['slug']}/" for s in SERVICES] + ["/blog/", "/visa/", "/passport/", "/insurance/", "/about/", "/flights-hotels/", "/customize-your-package/"] + [f"/blog/{a['slug']}/" for a in ARTICLES] + ["/contact/", "/terms/", "/privacy-policy/", "/cancellation-refund-policy/"]
    def _img(u):
        k = "hero-travel.jpg" if u == "/" else (f"h-{PAGE_PHOTO[u]}.jpg" if u in PAGE_PHOTO else None)
        return f"<image:image><image:loc>{SITE}/img/{k}</image:loc></image:image>" if k else ""
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{'1.0' if u=='/' else '0.8'}</priority>{_img(u)}</url>\n" for u in urls) + "</urlset>\n"
    open(os.path.join(root, "sitemap.xml"), "w").write(sm)
    # Installable app (PWA)
    open(os.path.join(root, "manifest.webmanifest"), "w").write(pwa.manifest(NAME))
    open(os.path.join(root, "sw.js"), "w").write(pwa.service_worker(urls, CSSV))
    write("/offline/", page("/offline/", "Offline | The Real Tours and Travels", "You are offline.", pwa.offline_body(PHONE, PHONE_RAW, WA)).replace('<meta name="robots" content="index,follow,max-image-preview:large">','<meta name="robots" content="noindex">'))
    open(os.path.join(root, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /tools/\nDisallow: /admin/\n\nSitemap: {SITE}/sitemap.xml\n")
    open(os.path.join(root, "CNAME"), "w").write("www.therealtoursandtravels.com\n")
    print("built", len(urls), "pages")

if __name__ == "__main__":
    build()
