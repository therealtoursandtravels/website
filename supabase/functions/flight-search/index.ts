// Flight schedule search for www.therealtoursandtravels.com
// Calls the Amadeus Travel Builder flight search with the secret AMADEUS_API_KEY
// and returns ONLY schedule details (no fares, no deep links) so the customer can
// pick a flight and request a quote from The Real Tours and Travels.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const GATEWAY = Deno.env.get("AMADEUS_GATEWAY_URL") ?? "https://api.amadeus.com";
const KEY = Deno.env.get("AMADEUS_API_KEY") ?? "";
const ALLOWED = ["https://www.therealtoursandtravels.com", "https://therealtoursandtravels.com"];

function cors(origin: string | null) {
  const o = origin && (ALLOWED.includes(origin) || origin.startsWith("http://localhost")) ? origin : ALLOWED[0];
  return {
    "Access-Control-Allow-Origin": o,
    "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
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

Deno.serve(async (req) => {
  const h = { ...cors(req.headers.get("origin")), "Content-Type": "application/json" };
  if (req.method === "OPTIONS") return new Response("ok", { headers: h });
  if (req.method !== "POST") return new Response(JSON.stringify({ error: "POST only" }), { status: 405, headers: h });
  if (!KEY) return new Response(JSON.stringify({ error: "not_configured" }), { status: 503, headers: h });

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
      // keep the most generous baggage text seen for this combination
      continue;
    }
    seen.add(key);
    options.push({ id: key, bounds });
  }
  options.sort((a: any, b: any) =>
    a.bounds[0].flights[0].departs.localeCompare(b.bounds[0].flights[0].departs) || a.bounds[0].total_min - b.bounds[0].total_min);

  return new Response(JSON.stringify({ options: options.slice(0, 120), count: options.length }), {
    headers: { ...h, "Cache-Control": "no-store" },
  });
});
