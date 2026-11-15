# Generates the dual-readable products section + JSON-LD + llms.txt block from one data source.
import json, html, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
ORG = {"@id": "https://mitl.studio/#organization"}
CALL = "https://ro.am/keith"
E = html.escape

NETWORKS = [
  {"name": "Roofing Authority Network", "url": "https://www.roofingauthority.network/",
   "industry": "Commercial roofing",
   "desc": "The live broadcast network for commercial roofing, led by The Tie-In and The Service Side, run on the MiTL Studio system.",
   "status": "Live", "link_text": "Visit Roofing Authority Network"},
  {"name": "Let's Talk Supply Chain / SCAC", "url": "https://letstalksupplychain.com/",
   "industry": "Supply chain",
   "desc": "Let's Talk Supply Chain shows with Sarah Barnes-Humphrey, produced by MiTL Studio, including the weekly live show Thoughts and Coffee. The Supply Chain Authority Council (SCAC) is in development, with launch announced for January 2027.",
   "status": "Live · SCAC in development", "link_text": "Visit Let's Talk Supply Chain"},
]

def m(price, name, unit=None, desc=None):
    o = {"@type": "Offer", "name": name, "priceCurrency": "USD"}
    if unit:
        o["priceSpecification"] = {"@type": "UnitPriceSpecification", "price": price, "priceCurrency": "USD", "unitText": unit}
        o["price"] = price
    else:
        o["price"] = price
    if desc: o["description"] = desc
    return o
def quote(name, desc):
    return {"@type": "Offer", "name": name, "description": desc, "availability": "https://schema.org/InStock"}

GROUPS = [
 {"id": "get-your-own-show", "num": "01", "title": "Get your own show", "img": "show",
  "alt": "Keith Bilous, Jon Andersen and the MiTL AI cast on a rooftop together",
  "promise": "A show, a network or a cast of AI characters, produced for you.",
  "products": [
   {"key": "production", "name": "Live Show Production", "tag": "Done for you",
    "pitch": "Your own show, fully produced every week, without hiring a production team.",
    "best": "Brands that want their own show without hiring a production team.",
    "get": ["Production: 1 show, up to 4 episodes per month", "Production+: up to 3 shows, 12 episodes per month", "2 AI characters included", "Guest Engine booking and managed social channels"],
    "price": "Production: $3,000/mo; Production+: $4,997/mo", "price_short": "$3,000/mo · $4,997/mo",
    "start": "Book a call with Keith", "start_url": CALL, "url": "https://production.mitl.studio/", "link_text": "See production",
    "stype": "Live show production",
    "offers": [m("3000", "Production: 1 show, up to 4 episodes per month", "MONTH"), m("4997", "Production+: up to 3 shows, 12 episodes per month", "MONTH")]},
   {"key": "networks", "name": "Industry Networks", "tag": "Flagship",
    "pitch": "Your industry's own live network: shows, guests, an intelligence layer and sponsor seats.",
    "best": "An industry underserved by its own media.",
    "get": ["Show formats, hosts and an AI cast", "Live production, clips and distribution", "Guest, company and answer pages built for Google and AI search", "A sponsorship menu and the pages to sell it"],
    "price": "Custom scope", "price_short": "Custom scope",
    "start": "Talk about your industry", "start_url": CALL, "url": "https://mitl.studio/#case-study", "link_text": "Read the RAN case study",
    "stype": "Industry media network", "examples": True,
    "offers": [quote("Industry Network build", "Quote-based. Custom scope per industry; book a call.")]},
   {"key": "character", "name": "Character Engine", "tag": "AI cast",
    "pitch": "AI characters with memory, personality and a voice, built to represent your brand on air.",
    "best": "Brands that want an AI character to represent them on air.",
    "get": ["Memory, personality, voice and visual identity", "The same system behind the Mornings in the Lab cast"],
    "price": "From $997 to build, $47/mo to host", "price_short": "From $997 · $47/mo",
    "start": "Meet the characters", "start_url": "https://characterengine.live/", "url": "https://characterengine.live/", "link_text": "Meet the characters",
    "stype": "AI character creation and hosting", "avatars": True,
    "offers": [m("997", "AI character build (from)"), m("47", "AI character hosting", "MONTH")]},
  ]},
 {"id": "get-found", "num": "02", "title": "Get found", "img": "found",
  "alt": "Keith Bilous and Jon Andersen, MiTL Studio hosts, on a city rooftop",
  "promise": "Be the name Google ranks and AI assistants cite.",
  "products": [
   {"key": "seo", "name": "AI-Powered SEO & GEO", "tag": "Search + AI answers",
    "pitch": "Get found on Google and named in AI answers, on the same system we run for our own brands.",
    "best": "Businesses that want to rank on Google and be named in AI answers.",
    "get": ["Technical SEO and local search", "Structured data", "AI-answer (GEO) visibility"],
    "price": "Talk to us", "price_short": "Talk to us",
    "start": "Book a call with Keith", "start_url": CALL, "url": "https://mitl.studio/#seo", "link_text": "Talk to us about SEO",
    "stype": "Search engine optimization and generative engine optimization",
    "offers": [quote("AI-Powered SEO & GEO engagement", "Quote-based. Pricing set per engagement; book a call.")]},
   {"key": "authority", "name": "Authority Engine", "tag": "Platform",
    "pitch": "A branded authority hub, built so search and AI cite your people as the source.",
    "best": "An industry or community that wants its experts cited as the source.",
    "get": ["Expert profiles and curated contributions", "Live market signals", "Connected to MiTL live shows and ConversationOS"],
    "price": "Custom build · talk to us", "price_short": "Custom build",
    "start": "Book a call with Keith", "start_url": CALL, "url": "https://mitl.studio/#authority", "link_text": "Talk to us about Authority Engine",
    "stype": "Industry authority platform",
    "offers": [quote("Authority Engine build", "Quote-based. Custom build; book a call.")]},
   {"key": "guest", "name": "Guest Engine", "tag": "Authority",
    "pitch": "Get booked on live shows and produced into a month of content.",
    "best": "Experts and leaders who want to be booked as live-show guests.",
    "get": ["A produced live guest appearance", "An authority page built for Google and AI search", "Clips and distribution"],
    "price": "$497 per appearance · plans from $97/mo", "price_short": "$497 · from $97/mo",
    "start": "Get featured", "start_url": "https://guestengine.live/join/", "url": "https://guestengine.live/", "link_text": "Get featured",
    "stype": "Podcast and live show guest booking", "wide": True,
    "offers": [m("497", "Single guest appearance"), m("97", "Member plan", "MONTH"), m("297", "VIP plan", "MONTH")]},
  ]},
 {"id": "sell-with-video", "num": "03", "title": "Sell with video", "img": "video",
  "alt": "Keith Bilous and Jon Andersen with the MiTL cast in the studio lobby",
  "promise": "Let video walk buyers through the deal before the call.",
  "products": [
   {"key": "salesdesk", "name": "Sales Desk", "tag": "Sales video",
    "pitch": "Turn a proposal, product or complex service into a video sales experience.",
    "best": "Teams selling a proposal, product or complex service.",
    "get": ["A video sales experience with reporting on what buyers watch", "One-time: 3-minute $999, 5-minute $1,499, 10-minute $2,999", "Always-On: one Sales Desk per month, 12-month minimum"],
    "price": "One-time from $999 · Always-On $1,249/mo", "price_short": "From $999 · $1,249/mo",
    "start": "Explore Sales Desk", "start_url": "https://salesdesk.video/", "url": "https://salesdesk.video/", "link_text": "Explore Sales Desk",
    "stype": "Video sales experiences",
    "offers": [m("999", "One-time Sales Desk, 3-minute"), m("1499", "One-time Sales Desk, 5-minute"), m("2999", "One-time Sales Desk, 10-minute"), m("1249", "Sales Desk Always-On, one per month (12-month minimum)", "MONTH")]},
  ]},
]
ENGINE = {"key": "conversationos", "name": "ConversationOS", "tag": "The engine behind all of it",
  "pitch": "The AI engine that builds every episode: titles, scripts, thumbnails, guests and distribution.",
  "best": "Anyone who wants to try the engine behind every MiTL show.",
  "get": ["Titles, scripts and thumbnails", "Music, guests and social posts", "Distribution"],
  "price": "Start free", "price_short": "Free to start",
  "start": "Try ConversationOS", "start_url": "https://conversationos.live/", "url": "https://conversationos.live/", "link_text": "Try ConversationOS",
  "stype": "AI show production software",
  "offers": [m("0", "ConversationOS: start free")]}

ALL = [p for g in GROUPS for p in g["products"]] + [ENGINE]
AV = ["sterling-james", "preston-vale", "sophia-grant", "maya-reyes", "frankie", "tommy"]

def facts(p):
    li = "".join(f"<li>{E(x)}</li>" for x in p["get"])
    return f"""<dl class="facts">
          <div><dt>Best for</dt><dd>{E(p['best'])}</dd></div>
          <div><dt>You get</dt><dd><ul>{li}</ul></dd></div>
          <div class="pr"><dt>Price</dt><dd>{E(p['price'])}</dd></div>
          <div><dt>How to start</dt><dd><a href="{p['start_url']}">{E(p['start'])}</a></dd></div>
        </dl>"""

def examples_html():
    out = []
    for n in NETWORKS:
        out.append(f"""<li class="ex">
            <span class="ex-ind">{E(n['industry'])}</span>
            <h5>{E(n['name'])}</h5>
            <p>{E(n['desc'])}</p>
            <span class="ex-status">{E(n['status'])}</span>
            <a href="{n['url']}">{E(n['link_text'])} →</a>
          </li>""")
    return '<div class="examples"><h4>Networks we run</h4><ul>' + "".join(out) + "</ul></div>"

def card(p):
    extra = ""
    if p.get("avatars"):
        extra = '<div class="avatars" aria-hidden="true">' + "".join(
            f'<img src="/assets/cast/{a}.webp" width="48" height="48" loading="lazy" alt="">' for a in AV) + "</div>"
    if p.get("examples"):
        extra = examples_html()
    wide = " wide" if (p.get("examples") or p.get("wide")) else ""
    return f"""<article class="pcard reveal{wide}" id="{p['key']}" aria-labelledby="{p['key']}-h">
        <div class="pcard-top"><span class="tag">{E(p['tag'])}</span><span class="pill">{E(p['price_short'])}</span></div>
        <h4 id="{p['key']}-h">{E(p['name'])}</h4>
        <p class="pitch">{E(p['pitch'])}</p>
        {extra}
        {facts(p)}
        <a class="more" href="{p['url']}">{E(p['link_text'])} →</a>
      </article>"""

def group(g):
    cards = "\n      ".join(card(p) for p in g["products"])
    return f"""<section class="og reveal" id="{g['id']}" aria-labelledby="{g['id']}-h">
    <div class="og-media">
      <picture><source srcset="/assets/proto/{g['img']}.webp" type="image/webp"><img src="/assets/proto/{g['img']}.jpg" loading="lazy" decoding="async" alt="{E(g['alt'])}"></picture>
      <div class="og-cap"><span class="num">{g['num']}</span><h3 id="{g['id']}-h">{E(g['title'])}</h3><p>{E(g['promise'])}</p></div>
    </div>
    <div class="og-cards n{len(g['products'])}">
      {cards}
    </div>
  </section>"""

def table():
    rows = []
    for p in ALL:
        name = E(p["name"])
        if p.get("examples"):
            name += '<small>Examples: ' + " · ".join(E(n["name"]) for n in NETWORKS) + "</small>"
        rows.append(f'<tr><th scope="row" data-label="Product"><a href="{p["url"]}">{name}</a></th><td data-label="Best for">{E(p["best"])}</td><td data-label="Price">{E(p["price"])}</td><td data-label="Start"><a href="{p["start_url"]}">{E(p["start"])}</a></td></tr>')
    return f"""<div class="glance reveal" id="at-a-glance">
    <table>
      <caption><h3>At a glance</h3><span>Every MiTL Studio product, who it's for, what it costs and how to start. Prices in USD.</span></caption>
      <thead><tr><th scope="col">Product</th><th scope="col">Best for</th><th scope="col">Price</th><th scope="col">Start</th></tr></thead>
      <tbody>
      {chr(10).join('      '+r for r in rows).strip()}
      </tbody>
    </table>
  </div>"""

def jsonld():
    items = []
    for i, p in enumerate(ALL, 1):
        offers = []
        for o in p["offers"]:
            o = dict(o); o["url"] = p["start_url"] if "price" not in o else p["url"]
            o.setdefault("seller", ORG)
            offers.append(o)
        desc = p["pitch"] + " Best for: " + p["best"] + " Price: " + p["price"] + "."
        if p.get("examples"):
            desc += " Examples: " + "; ".join(n["name"] + " (" + n["industry"].lower() + ")" for n in NETWORKS) + "."
        svc = {"@type": "Service", "@id": f"https://mitl.studio/#{p['key']}", "name": p["name"], "serviceType": p["stype"],
               "description": desc, "url": p["url"], "provider": ORG, "offers": offers}
        items.append({"@type": "ListItem", "position": i, "item": svc})
    ex = []
    for i, n in enumerate(NETWORKS, 1):
        if n["name"].startswith("Let's"):
            org = {"@type": "Organization", "name": "Let's Talk Supply Chain", "url": n["url"],
                   "description": "Let's Talk Supply Chain shows with Sarah Barnes-Humphrey, produced by MiTL Studio, including the weekly live show Thoughts and Coffee.",
                   "subOrganization": {"@type": "Organization", "name": "Supply Chain Authority Council", "alternateName": "SCAC",
                       "description": "A Let's Talk Supply Chain initiative in development; launch announced for January 2027."}}
        else:
            org = {"@type": "Organization", "@id": "https://www.roofingauthority.network/#organization", "name": n["name"], "url": n["url"], "description": n["desc"]}
        ex.append({"@type": "ListItem", "position": i, "item": org})
    data = {"@context": "https://schema.org", "@graph": [
        {"@type": "ItemList", "@id": "https://mitl.studio/#products-list", "name": "MiTL Studio products and services",
         "description": "Grouped by outcome: get your own show, get found, sell with video, plus the ConversationOS engine. Prices in USD; quote-based offers carry no price.",
         "numberOfItems": len(items), "itemListOrder": "https://schema.org/ItemListUnordered", "itemListElement": items},
        {"@type": "ItemList", "@id": "https://mitl.studio/#industry-network-examples", "name": "Industry Networks examples",
         "numberOfItems": len(ex), "itemListElement": ex}]}
    return json.dumps(data, indent=1, ensure_ascii=False)

def section():
    eng = ENGINE
    groups = "\n  ".join(group(g) for g in GROUPS)
    return f"""<section id="products" class="dual" aria-labelledby="products-h">
<div class="wrap">
  <header class="dual-head reveal">
    <div class="eyebrow">What we build</div>
    <h2 id="products-h">One studio. Everything behind the camera.</h2>
    <p class="sub">Pick the outcome you need. Every product runs on the same engine, ConversationOS.</p>
    <nav class="jump" aria-label="Outcomes"><a href="#get-your-own-show">01 Get your own show</a><a href="#get-found">02 Get found</a><a href="#sell-with-video">03 Sell with video</a><a href="#at-a-glance">At a glance</a></nav>
  </header>

  {groups}

  <aside class="engine reveal" id="{eng['key']}" aria-labelledby="{eng['key']}-h">
    <div class="engine-copy">
      <span class="tag"><i class="dot" aria-hidden="true"></i>{E(eng['tag'])}</span>
      <h3 id="{eng['key']}-h">{E(eng['name'])}</h3>
      <p class="pitch">{E(eng['pitch'])}</p>
    </div>
    {facts(eng)}
    <a class="btn" href="{eng['url']}">{E(eng['link_text'])}</a>
  </aside>

  {table()}
</div>
<script type="application/ld+json">
{jsonld()}
</script>
</section>"""

def llms_block():
    L = ["## Products at a glance (USD; mirrors the JSON-LD ItemList on https://mitl.studio/#products)"]
    for g in GROUPS + [{"title": "The engine behind all of it", "products": [ENGINE]}]:
        L.append(f"### {g['title']}")
        for p in g["products"]:
            L.append(f"- {p['name']} ({p['url']})")
            L.append(f"  - Best for: {p['best']}")
            L.append(f"  - You get: {'; '.join(p['get'])}")
            L.append(f"  - Price: {p['price']}" + ("" if any('price' in o for o in p['offers']) else " (quote-based, no list price)"))
            L.append(f"  - How to start: {p['start']}: {p['start_url']}")
            if p.get("examples"):
                for n in NETWORKS:
                    L.append(f"  - Example: {n['name']} ({n['industry']}): {n['desc']} {n['url']}")
    return "\n".join(L) + "\n"

if __name__ == "__main__":
    idx = ROOT / "index.html"; s = idx.read_text()
    start = s.index('<section id="products"')
    brands = s.index('    <div class="group-label">Our own brands')
    end = s.index("</section>", brands) + len("</section>")
    brands_html = s[brands:s.rindex("</div>", brands, end)]  # brand label + grid
    brands_html = brands_html[:brands_html.rindex("</div>")+6] if False else brands_html
    new = section() + '\n\n<section id="brands" class="brands">\n  <div class="wrap">\n' + brands_html.rstrip() + "\n  </div>\n</section>"
    s = s[:start] + new + s[end:]
    css = (ROOT / "_proto" / "proto.css").read_text(); js = (ROOT / "_proto" / "proto.js").read_text()
    s = s.replace("</style>\n</head>", css + "\n</style>\n<script>document.documentElement.classList.add('js')</script>\n</head>", 1)
    s = s.replace("</body>", "<script>\n" + js + "\n</script>\n</body>", 1)
    idx.write_text(s)
    (ROOT / "_proto" / "products.jsonld").write_text(jsonld())
    ll = (ROOT / "llms.txt").read_text()
    ll = ll.replace("- [Roofing Authority Network](https://www.roofingauthority.network/): The live broadcast network for commercial roofing (The Tie-In, The Service Side).",
      "- [Roofing Authority Network](https://www.roofingauthority.network/): The live broadcast network for commercial roofing (The Tie-In, The Service Side).\n- [Let's Talk Supply Chain](https://letstalksupplychain.com/): Supply chain shows with Sarah Barnes-Humphrey, produced by MiTL Studio. The Supply Chain Authority Council (SCAC) is in development (launch announced for January 2027).")
    ll = ll.replace("- [Industry Networks](https://www.roofingauthority.network/)", "- [Industry Networks](https://mitl.studio/#networks)")
    ll = ll.replace("Flagship: Roofing Authority Network. Custom scope.", "Examples: Roofing Authority Network (commercial roofing); Let's Talk Supply Chain / SCAC (supply chain). Custom scope.")
    ll = ll.replace("## Networks and shows", llms_block() + "\n## Networks and shows", 1)
    (ROOT / "llms.txt").write_text(ll)
    print("ok")
