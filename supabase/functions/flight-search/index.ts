// Flight schedule search for www.therealtoursandtravels.com
// Calls the Amadeus Travel Builder flight search with the secret AMADEUS_API_KEY
// and returns ONLY schedule details (no fares, no deep links) so the customer can
// pick a flight and request a quote from The Real Tours and Travels.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const GATEWAY = Deno.env.get("AMADEUS_GATEWAY_URL") ?? "https://api.amadeus.com";
const KEY = Deno.env.get("AMADEUS_API_KEY") ?? "";
// AeroDataBox (RapidAPI) – airport timetable, direct flights only, no baggage data
const ADB_KEY = Deno.env.get("AERODATABOX_API_KEY") ?? "";
const ADB_HOST = Deno.env.get("AERODATABOX_HOST") ?? "aerodatabox.p.rapidapi.com";
// AeroDataBox via API.Market (alternative marketplace)
const ADB_AM_KEY = Deno.env.get("AERODATABOX_APIMARKET_KEY") ?? "";
const ADB_AM_BASE = "https://prod.api.market/api/v1/aedbx/aerodatabox";
const ALLOWED = ["https://www.therealtoursandtravels.com", "https://therealtoursandtravels.com"];

function cors(origin: string | null) {
  const o = origin && (ALLOWED.includes(origin) || origin.startsWith("http://localhost")) ? origin : ALLOWED[0];
  return {
    "Access-Control-Allow-Origin": o,
    "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Vary": "Origin",
  };
}

const CODE = /^[A-Z]{3}$/;
const DATE = /^\d{4}-\d{2}-\d{2}$/;
const CABINS = ["ECONOMY", "PREMIUM_ECONOMY", "BUSINESS", "FIRST"];

type Bag = { type?: string; quantity?: number; weight_amount?: number; weight_unit?: string };

function bagText(bags: Bag[] | undefined): string {
  if (!bags || !bags.length) return "";
  const b = bags[0];
  if (b.type === "weight" && b.weight_amount) return `${b.weight_amount} ${(b.weight_unit || "KG").toLowerCase()} check-in`;
  if (b.type === "piece" && b.quantity != null) return b.quantity === 0 ? "No check-in bag" : `${b.quantity} check-in bag${b.quantity > 1 ? "s" : ""}`;
  return "";
}

// "2027-01-03T21:00:00+05:30" -> minutes since epoch (UTC), keeping the offset
function utcMin(s: string): number {
  return Math.round(new Date(s).getTime() / 60000);
}

// ---------- AeroDataBox ----------
// "2026-12-20 06:00+05:30" -> "2026-12-20T06:00:00+05:30"
function iso(local: string): string {
  const m = local.match(/^(\d{4}-\d{2}-\d{2})[ T](\d{2}:\d{2})(?::\d{2})?(Z|[+-]\d{2}:?\d{2})?$/);
  if (!m) return local;
  let off = m[3] || "Z";
  if (/^[+-]\d{4}$/.test(off)) off = off.slice(0, 3) + ":" + off.slice(3);
  return `${m[1]}T${m[2]}:00${off}`;
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

async function adbWindow(from: string, a: string, b: string, tries = 4): Promise<any[]> {
  const path = `/flights/airports/iata/${from}/${a}/${b}?direction=Departure&withLeg=true&withCancelled=false&withCodeshared=false&withCargo=false&withPrivate=false&withLocation=false`;
  const r = ADB_KEY
    ? await fetch(`https://${ADB_HOST}${path}`, { headers: { "X-RapidAPI-Key": ADB_KEY, "X-RapidAPI-Host": ADB_HOST, Accept: "application/json" } })
    : await fetch(`${ADB_AM_BASE}${path}`, { headers: { "x-api-market-key": ADB_AM_KEY, Accept: "application/json" } });
  if (r.status === 204) return [];
  if (r.status === 429 && tries > 1) { await r.body?.cancel(); await sleep(1500); return adbWindow(from, a, b, tries - 1); }
  if (!r.ok) throw new Error(`ADB ${r.status} ${(await r.text()).slice(0, 300)}`);
  const j = await r.json();
  return j?.departures ?? [];
}

async function adbBound(from: string, to: string, date: string) {
  // the timetable endpoint allows up to 12 hours per call -> two calls cover the day.
  // Calls run one after another: lower plans allow only about 1 request per second.
  const am = await adbWindow(from, `${date}T00:00`, `${date}T11:59`);
  await sleep(1100);
  const pm = await adbWindow(from, `${date}T12:00`, `${date}T23:59`);
  const seen = new Set<string>();
  const out: any[] = [];
  for (const f of [...am, ...pm]) {
    const dep = f.departure, arr = f.arrival;
    if (!dep?.scheduledTime?.local || arr?.airport?.iata !== to || f.isCargo) continue;
    const number = String(f.number || "").replace(/\s+/g, " ").trim();
    if (!number || seen.has(number)) continue;
    seen.add(number);
    const departs = iso(dep.scheduledTime.local);
    const arrives = arr?.scheduledTime?.local ? iso(arr.scheduledTime.local) : "";
    const mins = arrives ? utcMin(arrives) - utcMin(departs) : 0;
    const code = f.airline?.iata || number.split(" ")[0];
    out.push({
      flights: [{
        airline: code, airline_name: f.airline?.name ?? null, operated_by: null, number,
        from, from_terminal: dep.terminal ?? null, to, to_terminal: arr?.terminal ?? null,
        departs, arrives: arrives || departs, duration: "", aircraft: f.aircraft?.model ?? null, cabin: "",
      }],
      stops: 0, via: [],
      total: mins > 0 ? `${Math.floor(mins / 60)}h ${String(mins % 60).padStart(2, "0")}m` : "",
      total_min: mins, baggage: "",
    });
  }
  out.sort((a, b) => a.flights[0].departs.localeCompare(b.flights[0].departs));
  return out;
}

async function adbSearch(from: string, to: string, depart: string, ret: string) {
  const wrap = (b: any) => ({ id: b.flights[0].number + b.flights[0].departs, bounds: [b] });
  const out1 = await adbBound(from, to, depart);
  let back: any[] = [];
  if (ret) { await sleep(1100); back = await adbBound(to, from, ret); }
  const legs = [out1.slice(0, 120).map(wrap)];
  if (ret) legs.push(back.slice(0, 120).map(wrap));
  return legs;
}

Deno.serve(async (req) => {
  const h = { ...cors(req.headers.get("origin")), "Content-Type": "application/json" };
  if (req.method === "OPTIONS") return new Response("ok", { headers: h });
  // quick readiness check used by the website to decide whether to show the "Show flights" button
  if (req.method === "GET") return new Response(JSON.stringify({ ready: !!(KEY || ADB_KEY || ADB_AM_KEY) }), { headers: { ...h, "Cache-Control": "max-age=300" } });
  if (req.method !== "POST") return new Response(JSON.stringify({ error: "POST only" }), { status: 405, headers: h });
  if (!KEY && !ADB_KEY && !ADB_AM_KEY) return new Response(JSON.stringify({ error: "not_configured" }), { status: 503, headers: h });

  let p: Record<string, unknown>;
  try { p = await req.json(); } catch { return new Response(JSON.stringify({ error: "bad_json" }), { status: 400, headers: h }); }

  const from = String(p.from ?? "").toUpperCase(), to = String(p.to ?? "").toUpperCase();
  const depart = String(p.depart ?? ""), ret = p.ret ? String(p.ret) : "";
  const adults = Math.min(9, Math.max(1, Number(p.adults) || 1));
  const children = Math.min(8, Math.max(0, Number(p.children) || 0));
  const infants = Math.min(adults, Math.max(0, Number(p.infants) || 0));
  const cabin = CABINS.includes(String(p.cabin)) ? String(p.cabin) : "ECONOMY";
  if (!CODE.test(from) || !CODE.test(to) || from === to || !DATE.test(depart) || (ret && (!DATE.test(ret) || ret < depart)) || adults + children > 9) {
    return new Response(JSON.stringify({ error: "invalid_input" }), { status: 400, headers: h });
  }

  if (!KEY) {
    try {
      const legs = await adbSearch(from, to, depart, ret);
      return new Response(JSON.stringify({ source: "timetable", legs }), { headers: { ...h, "Cache-Control": "no-store" } });
    } catch (e) {
      console.error("aerodatabox", String(e));
      const busy = String(e).includes("429");
      return new Response(JSON.stringify({ error: busy ? "busy" : "upstream", detail: String(e).slice(0, 200) }), { status: busy ? 429 : 502, headers: h });
    }
  }

  const q = new URLSearchParams({
    origins: ret ? `${from},${to}` : from,
    destinations: ret ? `${to},${from}` : to,
    dates: ret ? `${depart},${ret}` : depart,
    locale: "en-IN",
    flow: "NETWORK",
    adults: String(adults),
    children: String(children),
    infants: String(infants),
    travel_class: cabin,
    currency: "INR",
    number_of_results: "40",
    disable_deep_links: "TRUE",
  });
  if (p.nonstop === true) q.set("nonstop", "true");

  let data: any;
  try {
    const r = await fetch(`${GATEWAY}/api/v3/search/?${q}`, { headers: { "X-API-Key": KEY } });
    if (r.status === 429) return new Response(JSON.stringify({ error: "busy" }), { status: 429, headers: h });
    if (!r.ok) {
      console.error("amadeus", r.status, (await r.text()).slice(0, 500));
      return new Response(JSON.stringify({ error: "upstream", status: r.status }), { status: 502, headers: h });
    }
    data = await r.json();
  } catch (e) {
    console.error("fetch failed", e);
    return new Response(JSON.stringify({ error: "upstream" }), { status: 502, headers: h });
  }

  // Strip every price / link; keep schedule + baggage; de-duplicate identical flight combinations.
  const seen = new Set<string>();
  const options: unknown[] = [];
  for (const res of data?.results ?? []) {
    const bounds = (res.bounds ?? []).map((b: any) => {
      const fl = (b.flights ?? []).map((f: any) => ({
        airline: f.marketing_airline,
        operated_by: f.operating_airline && f.operating_airline !== f.marketing_airline ? f.operating_airline : null,
        number: `${f.marketing_airline} ${f.flight_number}`,
        from: f.origin?.airport, from_terminal: f.origin?.terminal ?? null,
        to: f.destination?.airport, to_terminal: f.destination?.terminal ?? null,
        departs: f.departs_at, arrives: f.arrives_at,
        duration: f.duration, aircraft: f.aircraft ?? null,
        cabin: f.booking_infos?.[0]?.travel_class ?? cabin,
      }));
      const first = fl[0], last = fl[fl.length - 1];
      const mins = first && last ? utcMin(last.arrives) - utcMin(first.departs) : 0;
      return {
        flights: fl,
        stops: Math.max(0, fl.length - 1),
        via: fl.slice(0, -1).map((x: any) => x.to),
        total: `${Math.floor(mins / 60)}h ${String(mins % 60).padStart(2, "0")}m`,
        total_min: mins,
        baggage: bagText(b.included_checked_bags),
      };
    });
    if (!bounds.length || bounds.some((b: any) => !b.flights.length)) continue;
    const key = bounds.map((b: any) => b.flights.map((f: any) => f.number + f.departs).join("+")).join("|");
    if (seen.has(key)) {
      continue;
    }
    seen.add(key);
    options.push({ id: key, bounds });
  }
  options.sort((a: any, b: any) =>
    a.bounds[0].flights[0].departs.localeCompare(b.bounds[0].flights[0].departs) || a.bounds[0].total_min - b.bounds[0].total_min);

  return new Response(JSON.stringify({ source: "amadeus", legs: [options.slice(0, 120)] }), {
    headers: { ...h, "Cache-Control": "no-store" },
  });
});
