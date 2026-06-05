import json, base64

P = json.load(open('/home/claude/pdp/photos.json'))
mapimg = P['map']
FONTCSS = open('/home/claude/pdp/fonts.css').read()
LEAFLET_CSS = open('/home/claude/pdp/node_modules/maplibre-gl/dist/maplibre-gl.css').read()
LEAFLET_JS  = open('/home/claude/pdp/node_modules/maplibre-gl/dist/maplibre-gl.js').read()

from PIL import Image as PILImage
from io import BytesIO

U = '/home/claude/trip_unpack/uploads/'
def enc(path):
    return 'data:image/png;base64,' + base64.b64encode(open(path, 'rb').read()).decode()
def enc_jpg(path, maxside=360, q=85):
    im = PILImage.open(path).convert('RGB')
    w, h = im.size; s = maxside / max(w, h)
    if s < 1: im = im.resize((int(w*s), int(h*s)), PILImage.LANCZOS)
    buf = BytesIO(); im.save(buf, 'JPEG', quality=q)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

relax = enc(U + 'Mask_Group-3.png')     # pool
golf  = enc(U + 'Mask_Group-3-1.png')   # golf (landscape)
canoe = enc(U + 'Mask_Group-3-2.png')   # unique
city  = enc(U + 'Mask_Group-3-3.png')   # popular
pack  = enc(U + 'Mask_Group-3-4.png')   # adventure
beach_img   = enc_jpg(U + 'c6c8ccc8f2de3e04c9569207cb2f8fbb.jpg')   # beach
foodie_img  = enc_jpg(U + '6079935af2ed381ec48507f835e2cd58.jpg')   # sushi / food
night_img   = enc_jpg(U + '139dae29f380f717fb99b9731c9854a2.jpg')   # bar scene
culture_img = enc_jpg(U + '9c06f18fb0360489e7992ef972b63680.jpg')   # museum
FACE_URI = 'data:image/png;base64,' + base64.b64encode(open('/home/claude/pdp/face.png','rb').read()).decode()

from airdata import AIR

def S(n, lat, lng, mins=None, r=None):
    d = {"n": n, "lat": lat, "lng": lng, "r": r or n}
    if mins is not None: d["mins"] = mins
    return d

# Destinations per vibe per transport mode.
# air = anywhere by flight (global) | car = drivable from SF | transit = rail-reachable from SF | walk = within San Francisco
VIBE_DATA = {
 "relax": {
   "air": AIR["relax"],
   "car":[S("Calistoga",38.58,-122.58,80,"Wine Country"),S("Carmel",36.55,-121.92,120),S("Big Sur",36.27,-121.81,160),S("Sonoma",38.29,-122.46,60,"Wine Country"),S("Lake Tahoe",39.10,-120.03,190)],
   "transit":[S("Santa Barbara",34.42,-119.70),S("San Luis Obispo",35.28,-120.66),S("Davis",38.54,-121.74),S("Truckee",39.33,-120.18),S("Martinez",38.02,-122.13)],
   "walk":[S("Golden Gate Park",37.769,-122.483),S("Dolores Park",37.759,-122.427),S("Lands End",37.788,-122.506),S("Tea Garden",37.770,-122.470),S("Baker Beach",37.793,-122.484)],
 },
 "popular": {
   "air": AIR["popular"],
   "car":[S("Los Angeles",34.05,-118.24,360),S("Las Vegas",36.17,-115.14,540),S("San Diego",32.72,-117.16,480),S("Portland",45.52,-122.68,600),S("Seattle",47.61,-122.33,750)],
   "transit":[S("Los Angeles",34.05,-118.24),S("Sacramento",38.58,-121.49),S("San Jose",37.34,-121.89),S("Portland",45.52,-122.68),S("Seattle",47.61,-122.33)],
   "walk":[S("Golden Gate Bridge",37.808,-122.475),S("Fisherman's Wharf",37.808,-122.417),S("Pier 39",37.809,-122.410),S("Union Square",37.788,-122.407),S("Coit Tower",37.802,-122.406)],
 },
 "unique": {
   "air": AIR["unique"],
   "car":[S("Yosemite",37.87,-119.54,210),S("Joshua Tree",33.87,-115.90,480),S("Death Valley",36.51,-116.93,480),S("Mendocino",39.31,-123.80,210),S("Lassen",40.49,-121.51,225)],
   "transit":[S("Truckee",39.33,-120.18),S("San Luis Obispo",35.28,-120.66),S("Dunsmuir",41.21,-122.27),S("Reno",39.53,-119.81),S("Klamath Falls",42.22,-121.78)],
   "walk":[S("Painted Ladies",37.776,-122.433),S("Lombard Street",37.802,-122.419),S("Sutro Baths",37.780,-122.514),S("Tiled Steps",37.756,-122.474),S("Sea Cliff",37.787,-122.492)],
 },
 "adventure": {
   "air": AIR["adventure"],
   "car":[S("Yosemite",37.87,-119.54,210),S("Lake Tahoe",39.10,-120.03,190),S("Mt Shasta",41.31,-122.31,240),S("Moab",38.57,-109.55,900),S("Zion",37.30,-113.03,660)],
   "transit":[S("Truckee",39.33,-120.18),S("Reno",39.53,-119.81),S("Dunsmuir",41.21,-122.27),S("Klamath Falls",42.22,-121.78),S("Denver",39.74,-104.99)],
   "walk":[S("Twin Peaks",37.751,-122.448),S("Lands End Trail",37.787,-122.506),S("Bernal Heights",37.743,-122.413),S("Mount Davidson",37.738,-122.454),S("Crissy Field",37.804,-122.465)],
 },
 "golf": {
   "air": AIR["golf"],
   "car":[S("Pebble Beach",36.57,-121.95,120,"Monterey Peninsula"),S("Bandon Dunes",43.18,-124.40,450),S("Torrey Pines",32.90,-117.25,480),S("Edgewood Tahoe",38.95,-119.94,195),S("Spyglass Hill",36.58,-121.96,120,"Monterey Peninsula")],
   "transit":[S("Pebble Beach",36.57,-121.95),S("Santa Barbara",34.42,-119.70),S("Torrey Pines",32.90,-117.25),S("Portland",45.52,-122.68),S("San Jose",37.34,-121.89)],
   "walk":[S("Presidio Golf",37.790,-122.464),S("Lincoln Park",37.783,-122.503),S("Golden Gate Park GC",37.767,-122.501),S("TPC Harding Park",37.722,-122.494),S("Gleneagles",37.713,-122.401)],
 },
 "beach": {
   "air": AIR["beach"],
   "car":[S("Santa Cruz",36.97,-122.03,75),S("Carmel Beach",36.55,-121.93,120),S("Santa Monica",34.01,-118.50,360),S("Pismo Beach",35.14,-120.64,210),S("Stinson Beach",37.90,-122.64,50)],
   "transit":[S("Santa Barbara",34.42,-119.70),S("San Diego",32.72,-117.16),S("Ventura",34.27,-119.29),S("San Clemente",33.43,-117.61),S("Carpinteria",34.40,-119.52)],
   "walk":[S("Ocean Beach",37.759,-122.511),S("Baker Beach",37.793,-122.484),S("China Beach",37.788,-122.491),S("Crissy Field",37.804,-122.465),S("Aquatic Park",37.807,-122.423)],
 },
 "foodie": {
   "air": AIR["foodie"],
   "car":[S("Napa",38.30,-122.29,75,"Wine Country"),S("Healdsburg",38.61,-122.87,80,"Wine Country"),S("Yountville",38.40,-122.36,75,"Wine Country"),S("Los Angeles",34.05,-118.24,360),S("Portland",45.52,-122.68,600)],
   "transit":[S("Los Angeles",34.05,-118.24),S("Sacramento",38.58,-121.49),S("San Jose",37.34,-121.89),S("Santa Barbara",34.42,-119.70),S("Portland",45.52,-122.68)],
   "walk":[S("Ferry Building",37.795,-122.393),S("Mission District",37.760,-122.414),S("Chinatown",37.794,-122.407),S("North Beach",37.800,-122.410),S("Hayes Valley",37.776,-122.424)],
 },
 "nightlife": {
   "air": AIR["nightlife"],
   "car":[S("Los Angeles",34.05,-118.24,360),S("Las Vegas",36.17,-115.14,540),S("San Diego",32.72,-117.16,480),S("Reno",39.53,-119.81,210),S("Portland",45.52,-122.68,600)],
   "transit":[S("Los Angeles",34.05,-118.24),S("San Diego",32.72,-117.16),S("Sacramento",38.58,-121.49),S("Reno",39.53,-119.81),S("Portland",45.52,-122.68)],
   "walk":[S("Mission",37.759,-122.419),S("North Beach",37.800,-122.410),S("SoMa",37.778,-122.405),S("Castro",37.762,-122.435),S("Polk Street",37.790,-122.420)],
 },
 "culture": {
   "air": AIR["culture"],
   "car":[S("Los Angeles",34.05,-118.24,360),S("Sacramento",38.58,-121.49,90),S("Monterey",36.60,-121.89,120),S("Portland",45.52,-122.68,600),S("Carmel",36.55,-121.92,120)],
   "transit":[S("Los Angeles",34.05,-118.24),S("Sacramento",38.58,-121.49),S("Santa Barbara",34.42,-119.70),S("Portland",45.52,-122.68),S("Seattle",47.61,-122.33)],
   "walk":[S("SFMOMA",37.786,-122.401),S("de Young",37.771,-122.469),S("Palace of Fine Arts",37.802,-122.448),S("Asian Art Museum",37.780,-122.416),S("Legion of Honor",37.785,-122.501)],
 },
}
VIBE_JSON = json.dumps(VIBE_DATA)

import re
def load_icon(path):
    s = open(path).read()
    s = s.replace('fill="#222222"', 'fill="currentColor"')
    s = re.sub(r'<svg width="16" height="16"', '<svg', s, count=1)
    return s.strip()
IC_AIR   = load_icon(U + 'ic_compact_maps_airport_16.svg')
IC_CAR   = load_icon(U + 'ic_compact_maps_car_rental_16.svg')
IC_TRAIN = load_icon(U + 'ic_compact_maps_subway_station_16.svg')
IC_WALK  = load_icon(U + 'ic_compact_person_walk_16.svg')
AIR_ICON_JSON = json.dumps(IC_AIR)

# Airbnb wordmark/bélo logo for the search bar (recoloured to brand red, sized via CSS).
LOGO_RAW = open('/home/claude/pdp/airbnb_logo.svg').read()
LOGO_RAW = LOGO_RAW.replace('#222222', '#FF385C').replace('width="40" height="40" ', '')
LOGO_RAW = re.sub(r'>\s+<', '><', LOGO_RAW)
LOGO_RAW = re.sub(r'\s+', ' ', LOGO_RAW).strip()
LOGO_JSON = json.dumps(LOGO_RAW)

# icon helper (white line icons for the image-less vibes)
ICONS = {
 'beach': '<path d="M4 17h16M6 21h12"/><circle cx="12" cy="8" r="3.4"/><path d="M12 2.5v1.5M12 12v1.5M17.5 8h-1.5M8 8H6.5M15.9 4.1l-1 1M9.1 11.9l-1 1M15.9 11.9l-1-1M9.1 4.1l-1-1"/>',
 'foodie': '<path d="M4 11h16a8 8 0 0 1-16 0z"/><path d="M9 3c0 1.2-1 1.2-1 2.4s1 1.2 1 2.4M14 3c0 1.2-1 1.2-1 2.4s1 1.2 1 2.4"/>',
 'nightlife': '<path d="M5 4h14l-7 8z"/><path d="M12 12v6"/><path d="M8 21h8"/>',
 'culture': '<path d="M3 21h18M5 21V10M9 21V10M15 21V10M19 21V10M3 10h18"/><path d="M12 3l8 6H4z"/>',
}

CATS = [
 dict(id='relax',     label='Relax',     kind='img',  src=relax, active=True),
 dict(id='popular',   label='Popular',   kind='img',  src=city),
 dict(id='unique',    label='Unique',    kind='img',  src=canoe),
 dict(id='adventure', label='Adventure', kind='img',  src=pack),
 dict(id='golf',      label='Golf',      kind='img',  src=golf),
 dict(id='beach',     label='Beach',     kind='img',  src=beach_img),
 dict(id='foodie',    label='Foodie',    kind='img',  src=foodie_img),
 dict(id='nightlife', label='Nightlife', kind='img',  src=night_img),
 dict(id='culture',   label='Culture',   kind='img',  src=culture_img),
]

def card_html(c):
    if c['kind'] == 'img':
        inner = f'<img src="{c["src"]}" alt="">'
    else:
        svg = (f'<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" '
               f'stroke-linecap="round" stroke-linejoin="round">{ICONS[c["icon"]]}</svg>')
        inner = f'<div class="grad" style="background:{c["grad"]}">{svg}</div>'
    active = ' active' if c.get('active') else ''
    return (f'<div class="cat{active}" data-id="{c["id"]}">'
            f'<div class="thumb-wrap"><div class="thumb">{inner}</div></div>'
            f'<div class="label">{c["label"]}</div></div>')

cards = '\n      '.join(card_html(c) for c in CATS)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Trip Creator</title>
<style>
  {LEAFLET_CSS}
  {FONTCSS}
  :root {{
    --bg:#AADAFF; --ink:#222222;
    --circle:#EEF8FF; --icon-grey:#8C8C8C; --accent:#4990EF;
    --cereal:"Airbnb Cereal",-apple-system,"SF Pro Display",system-ui,sans-serif;
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html,body {{ height:100%; }}
  body {{
    display:flex; align-items:center; justify-content:center; min-height:100vh;
    background:#dfe4ea;
    font-family:var(--cereal);
    font-weight:500;
    -webkit-font-smoothing:antialiased;
  }}
  .stage {{ transform-origin:center center; }}
  .screen {{
    position:relative; width:402px; height:874px; border-radius:40px;
    background-color:var(--bg);
    overflow:hidden; box-shadow:0 30px 80px rgba(0,0,0,.30);
  }}
  #map {{ position:absolute; inset:0; z-index:1; background:radial-gradient(circle at 50% 38%, #16213e 0%, #0a0f1f 62%, #06080f 100%); }}
  #loc-indicator {{ position:absolute; left:-100px; top:-100px; width:44px; height:44px; z-index:3; pointer-events:none; }}
  #loc-indicator .loc-dot {{
    position:absolute; inset:0; border-radius:50%; box-sizing:border-box;
    border:3px solid #222; background:center/cover no-repeat; background-image:url({FACE_URI});
    box-shadow:0 3px 9px rgba(0,0,0,.32); z-index:2;
  }}
  #loc-indicator .loc-ptr-wrap {{ position:absolute; inset:0; z-index:1; }}
  #loc-indicator .loc-ptr {{
    position:absolute; left:50%; top:-7px; transform:translateX(-50%);
    width:0; height:0; border-left:7px solid transparent; border-right:7px solid transparent;
    border-bottom:11px solid #222;
  }}
  /* globe-aware avatar pin (positioned + occluded by MapLibre) */
  .loc-pin {{ position:relative; width:44px; height:54px; cursor:pointer; }}
  .loc-pin .d {{
    position:absolute; top:0; left:0; width:44px; height:44px; box-sizing:border-box;
    border-radius:50%; border:3px solid #222; background:center/cover no-repeat;
    background-image:url({FACE_URI}); box-shadow:0 3px 9px rgba(0,0,0,.32);
  }}
  .loc-pin::after {{
    content:""; position:absolute; left:50%; bottom:0; transform:translateX(-50%);
    width:0; height:0; border-left:7px solid transparent; border-right:7px solid transparent;
    border-top:11px solid #222;
  }}
  .maplibregl-ctrl-attrib {{ font-size:9px; }}
  /* visited push pin (classic red) */
  .trippin {{ position:relative; width:22px; height:30px; cursor:default; }}
  .trippin .head {{
    position:absolute; left:50%; top:0; transform:translateX(-50%);
    width:16px; height:16px; border-radius:50%;
    background:radial-gradient(circle at 33% 30%, #ff8a82, #e2241a 48%, #a01109 100%);
    box-shadow:0 3px 6px rgba(0,0,0,.4), inset -2px -2px 3px rgba(0,0,0,.3), inset 2px 2px 3px rgba(255,255,255,.5);
  }}
  .trippin .head::after {{ content:""; position:absolute; left:24%; top:20%; width:5px; height:3.5px; border-radius:50%; background:rgba(255,255,255,.8); }}
  .trippin .pin {{
    position:absolute; left:50%; top:12px; width:2px; height:18px; transform:translateX(-50%) rotate(8deg); transform-origin:top center;
    background:linear-gradient(90deg,#888,#e2e2e6 45%,#9a9aa0);
  }}
  .trippin .sh {{ position:absolute; left:50%; top:29px; width:14px; height:4px; transform:translate(-44%,0) rotate(-8deg); background:radial-gradient(ellipse,rgba(0,0,0,.4),transparent 70%); }}
  /* airport pill */
  .airpin {{ transform:translateY(-50%); z-index:5; }}
  .airpin .box {{
    display:inline-flex; align-items:center; gap:7px; background:#2F80ED; color:#fff;
    font:600 12px/1 var(--cereal); padding:7px 11px 7px 7px; border-radius:11px;
    box-shadow:0 5px 14px rgba(47,128,237,.45), 0 1px 3px rgba(0,0,0,.3);
  }}
  .airpin .box svg {{ width:15px; height:15px; }}
  .airpin .box .code {{ background:rgba(255,255,255,.22); border-radius:5px; padding:2px 5px; font-size:10px; letter-spacing:.5px; }}
  .maplibregl-ctrl-attrib.maplibregl-compact {{ background:rgba(255,255,255,.6); }}
  .maplibregl-canvas, .maplibregl-canvas-container {{ outline:none; }}
  .mk {{ font-family:var(--cereal); cursor:pointer; }}
  /* .mk-pill = rail wrapper: slides horizontally so the bubble stays on-screen.
     .mk-pop  = the bubble itself (carries the pop-in animation).
     The tail counter-translates by --rail so it stays anchored on the map point. */
  .mk-pill {{
    display:inline-flex; position:relative;
    transform:translateX(var(--rail,0px));
  }}
  .mk-pop {{
    display:inline-flex; align-items:center; justify-content:center; position:relative;
    background:#fff; color:var(--ink); font:600 12px/1 var(--cereal);
    padding:6px 10px; border-radius:16px; white-space:nowrap; text-align:center;
    box-shadow:0 3px 10px rgba(0,0,0,.30); border:1px solid rgba(0,0,0,.06);
    transform-origin:50% 118%;
    animation:mkpop .44s cubic-bezier(.22,.9,.3,1.5) both;
  }}
  .mk-pop::after {{
    content:""; position:absolute; left:50%; bottom:-4px; width:8px; height:8px;
    background:#fff; transform:translateX(calc(-50% - var(--rail,0px))) rotate(45deg);
    border-right:1px solid rgba(0,0,0,.06); border-bottom:1px solid rgba(0,0,0,.06);
  }}
  @keyframes mkpop {{ 0%{{opacity:0; transform:scale(.15)}} 55%{{opacity:1}} 100%{{opacity:1; transform:scale(1)}} }}
  .mk-time {{ font-weight:400; color:#222; letter-spacing:.1px; }}
  .mk-fly {{
    display:inline-flex; align-items:center; justify-content:center;
    width:18px; height:18px; margin:0 6px 0 -3px; border-radius:50%;
    background:var(--accent); color:#fff; vertical-align:middle; flex:0 0 auto;
  }}
  .mk-fly svg {{ width:11px; height:11px; display:block; }}
  .mk-clusterwrap .mk-pop {{
    cursor:pointer;
    box-shadow:0 3px 10px rgba(0,0,0,.28), 5px 6px 0 -1px #fff, 6px 8px 11px -3px rgba(0,0,0,.22);
  }}

  /* Status bar */
  .status {{
    position:absolute; top:0; left:0; right:0; height:54px; z-index:5;
    display:flex; align-items:center; justify-content:space-between;
    padding:18px 32px 0; color:#0d0d0d; pointer-events:none;
  }}
  .status .time {{ font-size:17px; font-weight:500; letter-spacing:.2px; }}
  .status .glyphs {{ display:flex; align-items:center; gap:7px; }}

  /* Scrollable category strip */
  .cards-scroll {{
    position:absolute; top:58px; left:0; right:0; height:128px; z-index:4;
    display:flex; align-items:flex-start; gap:16px;
    padding:16px 20px 12px;
    overflow-x:auto; overflow-y:hidden;
    -webkit-overflow-scrolling:touch; scrollbar-width:none;
  }}
  .cards-scroll::-webkit-scrollbar {{ display:none; }}

  .cat {{ flex:0 0 auto; display:flex; flex-direction:column; align-items:center; cursor:pointer; }}
  .thumb-wrap {{ height:72px; display:flex; align-items:center; }}
  .thumb {{
    box-sizing:border-box; width:68px; height:68px;
    border:2px solid #fff; border-radius:16px; overflow:hidden;
    box-shadow:0 6px 14px rgba(0,0,0,.20), 0 1px 4px rgba(0,0,0,.12);
    transition:width .30s cubic-bezier(.34,1.1,.45,1), box-shadow .2s ease;
  }}
  .cat.active .thumb {{
    width:124px; height:68px;
    box-shadow:0 0 0 2px var(--ink), 0 7px 16px rgba(0,0,0,.26), 0 2px 5px rgba(0,0,0,.16);
  }}
  .thumb img, .thumb .grad {{ width:100%; height:100%; object-fit:cover; display:block; }}
  .thumb .grad {{ display:flex; align-items:center; justify-content:center; }}
  .thumb .grad svg {{ width:26px; height:26px; filter:drop-shadow(0 1px 2px rgba(0,0,0,.25)); }}
  .label {{
    margin-top:8px; font-size:12px; line-height:16px; font-weight:500; color:var(--ink);
    font-family:var(--cereal);
    -webkit-text-stroke:3px #fff; paint-order:stroke fill;
    white-space:nowrap; letter-spacing:.1px;
  }}

  /* Search pill */
  .pill {{
    position:absolute; left:24px; top:730px; width:354px; height:56px; border-radius:28px;
    background:#fff; display:flex; align-items:center; gap:6px; padding:0 8px; z-index:4;
    box-shadow:0 10px 28px rgba(0,0,0,.13), 0 2px 6px rgba(0,0,0,.06);
  }}
  .pill-side {{
    flex:0 0 auto; width:40px; height:40px; border-radius:12px; background:#ececec; border:0; padding:0;
    display:flex; align-items:center; justify-content:center; cursor:pointer;
  }}
  .pill-side:active {{ transform:scale(.94); }}
  #pillLeft {{ background:transparent; }}
  #pillRight {{ border-radius:50%; }}
  .pill-side svg {{ width:21px; height:21px; display:block; }}
  .pill-mid {{ flex:1 1 auto; min-width:0; display:flex; flex-direction:column; align-items:center; justify-content:center; }}
  .pill-t1 {{ font:600 16px/1.15 var(--cereal); color:var(--ink); white-space:nowrap; }}
  .pill-t2 {{ font:500 12px/1.2 var(--cereal); color:#717171; white-space:nowrap; margin-top:1px; }}

  /* Dock */
  .dock-btn {{
    position:absolute; top:802px; width:32px; height:32px; border-radius:50%;
    background:var(--circle); display:flex; align-items:center; justify-content:center;
    box-shadow:0 2px 6px rgba(0,0,0,.08); cursor:pointer; color:var(--icon-grey); z-index:4;
    transition:transform .12s ease, background .15s ease;
  }}
  .dock-btn:active {{ transform:scale(.9); }}
  .dock-btn.on {{ background:var(--accent); color:#fff; box-shadow:0 4px 10px rgba(73,144,239,.45); }}
  .d1 {{ left:119px; }} .d2 {{ left:163px; }} .d3 {{ left:207px; }} .d4 {{ left:251px; }}
  .dock-btn svg {{ width:18px; height:18px; }}

  /* once airport pins are on screen, drop the little flight glyph from the city pills */
  .screen.airports-visible .mk-fly {{ display:none; }}

  /* the search pill slides up to become the flight sheet's header */
  .pill {{ transition:top .52s cubic-bezier(.22,.9,.3,1.05); }}
  .pill.flight {{ z-index:8; }}

  /* flight destination endpoint on the map */
  .flightend {{ position:relative; width:16px; height:16px; }}
  .flightend .dot {{ position:absolute; inset:0; border-radius:50%; background:#111; border:3px solid #fff; box-shadow:0 2px 6px rgba(0,0,0,.35); }}
  .flightend .tag {{ position:absolute; bottom:21px; left:50%; transform:translateX(-50%); background:#111; color:#fff; font:600 11px/1 var(--cereal); padding:4px 7px; border-radius:7px; white-space:nowrap; box-shadow:0 3px 8px rgba(0,0,0,.3); }}

  /* flight half-sheet (rises from the bottom; the search pill docks at its top) */
  .flightsheet {{
    position:absolute; left:0; right:0; bottom:0; height:560px; z-index:6;
    background:#fff; border-radius:26px 26px 0 0;
    box-shadow:0 -14px 44px rgba(0,0,0,.20);
    transform:translateY(108%); transition:transform .52s cubic-bezier(.22,.9,.3,1.05);
    display:flex; flex-direction:column; padding:86px 14px 0;
  }}
  .flightsheet.up {{ transform:translateY(0); }}
  .fs-grip {{ position:absolute; top:11px; left:50%; transform:translateX(-50%); width:38px; height:5px; border-radius:3px; background:#e2e2e2; }}
  .fs-sub {{ font:600 13px/1.3 var(--cereal); color:#717171; padding:2px 8px 10px; display:flex; justify-content:space-between; }}
  .fs-sub .price-h {{ color:#222; }}
  .fs-list {{ flex:1 1 auto; overflow-y:auto; -webkit-overflow-scrolling:touch; padding:0 2px 18px; scrollbar-width:none; }}
  .fs-list::-webkit-scrollbar {{ display:none; }}
  .fs-row {{ display:flex; align-items:center; gap:11px; padding:13px 8px; border-bottom:1px solid #eee; }}
  .fs-badge {{ flex:0 0 auto; width:34px; height:34px; border-radius:9px; display:flex; align-items:center; justify-content:center; color:#fff; font:700 11px/1 var(--cereal); }}
  .fs-mid {{ flex:1 1 auto; min-width:0; }}
  .fs-times {{ font:600 15px/1.2 var(--cereal); color:#222; }}
  .fs-meta {{ font:500 12px/1.3 var(--cereal); color:#717171; margin-top:2px; }}
  .fs-right {{ flex:0 0 auto; text-align:right; }}
  .fs-price {{ font:700 15px/1 var(--cereal); color:#222; }}
  .fs-buy {{ margin-top:6px; border:0; background:var(--accent); color:#fff; font:600 12px/1 var(--cereal); padding:7px 12px; border-radius:9px; cursor:pointer; }}
  .fs-buy:active {{ transform:scale(.95); }}

  /* painterly arch overlay (drawn in screen space, recomputed each frame) */
  .arc-svg {{ position:absolute; inset:0; width:100%; height:100%; pointer-events:none; z-index:1; overflow:visible; }}
  .arc-shadow {{ fill:none; stroke:rgba(20,20,20,.22); stroke-width:5.5; stroke-linecap:round;
    stroke-dasharray:7 7; filter:blur(2px); transform:translateY(5px); }}
  .arc-line {{ fill:none; stroke:#141414; stroke-width:3.4; stroke-linecap:round; stroke-dasharray:7 7; }}
  .arc-time {{ position:absolute; left:0; top:0; z-index:4; pointer-events:none;
    display:inline-flex; align-items:center; gap:6px; background:#141414; color:#fff;
    font:700 13px/1 var(--cereal); padding:7px 12px; border-radius:16px; white-space:nowrap;
    box-shadow:0 5px 14px rgba(0,0,0,.3); }}
  .arc-time svg {{ width:13px; height:13px; }}
  /* layover waypoint on the dotted line */
  .viapin {{ display:flex; flex-direction:column; align-items:center; }}
  .viapin .vd {{ width:11px; height:11px; border-radius:50%; background:#141414; border:2.5px solid #fff; box-shadow:0 2px 5px rgba(0,0,0,.3); }}
  .viapin .vl {{ margin-top:3px; font:700 10px/1 var(--cereal); color:#141414; -webkit-text-stroke:3px #fff; paint-order:stroke fill; white-space:nowrap; }}

  /* airport price pills — red plane badge + city · price, icon sits on the airport point */
  .fa-pill {{ display:inline-flex; }}                       /* marker root — MapLibre owns its transform */
  .fa-pop {{
    display:inline-flex; align-items:center; gap:9px; background:#fff; color:#222;
    font:600 14px/1 var(--cereal); padding:7px 15px 7px 7px; border-radius:22px; white-space:nowrap; cursor:pointer;
    box-shadow:0 6px 18px rgba(0,0,0,.16), 0 1px 4px rgba(0,0,0,.10);
    transform-origin:0% 50%; animation:mkpop .4s cubic-bezier(.22,.9,.3,1.5) both;
  }}
  .fa-pop .fa-ico {{ flex:0 0 auto; width:30px; height:30px; border-radius:50%; background:#FF385C;
    display:flex; align-items:center; justify-content:center; }}
  .fa-pop .fa-ico svg {{ width:16px; height:16px; }}
  .fa-pop .fa-name {{ color:#222; font-weight:700; }}
  .fa-pop .fa-sep {{ color:#9b9b9b; font-weight:600; margin:0 -3px; }}
  .fa-pop .fa-price {{ color:#222; font-weight:600; }}
  .fa-pill.active .fa-pop {{ box-shadow:0 8px 22px rgba(0,0,0,.22), 0 0 0 2px var(--ink); }}
  .fs-row.sel {{ background:#f3f7ff; border-radius:12px; }}

  /* Airbnb-style stay price pills — only appear at street/neighbourhood zoom */
  .stay {{ pointer-events:none; }}                  /* purely visual; let the map pan underneath */
  .stay-pop {{
    display:inline-flex; align-items:center; background:#fff; color:#222;
    font:700 13px/1 var(--cereal); padding:7px 11px; border-radius:16px; white-space:nowrap;
    box-shadow:0 4px 12px rgba(0,0,0,.18), 0 1px 3px rgba(0,0,0,.12);
    animation:mkpop .35s cubic-bezier(.22,.9,.3,1.5) both;
  }}
</style>
</head>
<body>
  <div class="stage" id="stage">
  <div class="screen">

    <div id="map"></div>
    <div id="loc-indicator"><div class="loc-ptr-wrap"><div class="loc-ptr"></div></div><div class="loc-dot"></div></div>

    <div class="status">
      <span class="time">9:41</span>
      <span class="glyphs">
        <svg width="18" height="12" viewBox="0 0 18 12" fill="currentColor">
          <rect x="0" y="8" width="3" height="4" rx="1"/><rect x="5" y="5.5" width="3" height="6.5" rx="1"/>
          <rect x="10" y="3" width="3" height="9" rx="1"/><rect x="15" y="0" width="3" height="12" rx="1"/>
        </svg>
        <svg width="17" height="12" viewBox="0 0 17 12" fill="currentColor">
          <path d="M8.5 1C5.4 1 2.6 2.2.6 4.2c-.3.3-.3.8 0 1.1.3.3.8.3 1.1 0C3.4 3.6 5.8 2.6 8.5 2.6s5.1 1 6.8 2.7c.3.3.8.3 1.1 0 .3-.3.3-.8 0-1.1C14.4 2.2 11.6 1 8.5 1z"/>
          <path d="M8.5 5c-1.7 0-3.3.7-4.5 1.8-.3.3-.3.8 0 1.1.3.3.8.3 1.1 0 .9-.9 2.1-1.4 3.4-1.4s2.5.5 3.4 1.4c.3.3.8.3 1.1 0 .3-.3.3-.8 0-1.1C11.8 5.7 10.2 5 8.5 5z"/>
          <circle cx="8.5" cy="10.3" r="1.4"/>
        </svg>
        <svg width="27" height="13" viewBox="0 0 27 13" fill="none">
          <rect x="1" y="1" width="22" height="11" rx="3" stroke="currentColor" stroke-opacity="0.4"/>
          <rect x="2.5" y="2.5" width="19" height="8" rx="1.8" fill="currentColor"/>
          <path d="M25 4.5v4c.9-.4.9-3.6 0-4z" fill="currentColor" fill-opacity="0.5"/>
        </svg>
      </span>
    </div>

    <div class="cards-scroll" id="cards">
      {cards}
    </div>

    <div class="pill">
      <button class="pill-side" id="pillLeft" aria-label="menu"></button>
      <div class="pill-mid"><div class="pill-t1" id="pillT1">Where to?</div><div class="pill-t2" id="pillT2">Anywhere · Any week</div></div>
      <button class="pill-side" id="pillRight" aria-label="voice">
        <svg viewBox="0 -960 960 960" fill="#1f1f1f"><path d="M280-280v-400q0-17 11.5-28.5T320-720q17 0 28.5 11.5T360-680v400q0 17-11.5 28.5T320-240q-17 0-28.5-11.5T280-280Zm160 160v-720q0-17 11.5-28.5T480-880q17 0 28.5 11.5T520-840v720q0 17-11.5 28.5T480-80q-17 0-28.5-11.5T440-120ZM120-440v-80q0-17 11.5-28.5T160-560q17 0 28.5 11.5T200-520v80q0 17-11.5 28.5T160-400q-17 0-28.5-11.5T120-440Zm480 160v-400q0-17 11.5-28.5T640-720q17 0 28.5 11.5T680-680v400q0 17-11.5 28.5T640-240q-17 0-28.5-11.5T600-280Zm160-160v-80q0-17 11.5-28.5T800-560q17 0 28.5 11.5T840-520v80q0 17-11.5 28.5T800-400q-17 0-28.5-11.5T760-440Z"/></svg>
      </button>
    </div>

    <div class="dock-btn d1 on" data-mode="air">{IC_AIR}</div>
    <div class="dock-btn d2" data-mode="car">{IC_CAR}</div>
    <div class="dock-btn d3" data-mode="transit">{IC_TRAIN}</div>
    <div class="dock-btn d4" data-mode="walk">{IC_WALK}</div>

    <div class="flightsheet" id="flightsheet">
      <div class="fs-grip"></div>
      <div class="fs-sub" id="fsSub"></div>
      <div class="fs-list" id="fsList"></div>
    </div>

  </div>
  </div>

<script>{LEAFLET_JS}</script>
<script>
  // ---------- Live map (MapLibre GL — globe projection) ----------
  const SF = [-122.4194, 37.7749];   // [lng, lat]
  const SCREEN = document.querySelector('.screen');
  let flightMode = false, preFlight = null, flightInfo = {{}}, flightEndMarker = null;
  let flightDest = null, flightAirportMarkers = [], sheetTY = 0;
  let routeVia = null, viaMarker = null, curFlights = [], detent = 'expanded';
  const COLLAPSE_DY = 408;   // how far the flight sheet drops to its collapsed (map-revealing) detent
  const map = new maplibregl.Map({{
    container: 'map',
    style: {{
      version: 8,
      projection: {{ type: 'globe' }},
      sources: {{
        carto: {{
          type: 'raster', tileSize: 256,
          tiles: [
            'https://a.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}.png',
            'https://b.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}.png',
            'https://c.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}.png',
            'https://d.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}.png'
          ],
          attribution: '&copy; OpenStreetMap &copy; CARTO'
        }}
      }},
      layers: [
        {{ id: 'space', type: 'background', paint: {{ 'background-color': 'rgba(0,0,0,0)' }} }},
        {{ id: 'carto', type: 'raster', source: 'carto' }}
      ]
    }},
    center: [88, 8], zoom: 1.5, minZoom: 0.6, maxZoom: 18,
    attributionControl: true, dragRotate: false, pitchWithRotate: false, keyboard: false
  }});
  map.touchZoomRotate.disableRotation();

  const markerMap = new Map();   // id -> {{ m, lng, lat, far }}
  let currentSpots = [];
  let suppressLayout = false;   // hold destination markers during the intro's final zoom
  let introFlight = false;      // true while the opening flight is sweeping in
  const CAR_MAX = 540;          // ~9 hour drive: the default car boundary
  let carBaseZoom = 99;         // zoom the last car view framed to; below it we reveal farther cities
  const CLUSTER_PX = 80;        // pills closer than this on screen are candidates to merge
  const MAX_AIR = 22;           // most explore pins shown at once
  const GEO_MAX = 1.5;          // ...but only merge if they're also within this many degrees on the ground
  // Colloquial names for the metros/areas people actually use. A cluster whose centre falls
  // inside one of these is labelled with the area name (e.g. SF + Oakland + San Jose -> "Bay Area").
  const NAMED_REGIONS = [
    {{ name:'Bay Area',       lat:37.85, lng:-122.30, rad:0.95 }},
    {{ name:'Los Angeles',    lat:34.02, lng:-118.30, rad:1.00 }},
    {{ name:'San Diego',      lat:32.83, lng:-117.18, rad:0.60 }},
    {{ name:'Las Vegas',      lat:36.13, lng:-115.17, rad:0.55 }},
    {{ name:'Lake Tahoe',     lat:39.10, lng:-120.03, rad:0.55 }},
    {{ name:'New York City',  lat:40.71, lng:-73.95,  rad:0.85 }},
    {{ name:'Seattle',        lat:47.55, lng:-122.30, rad:0.65 }},
    {{ name:'Portland',       lat:45.52, lng:-122.66, rad:0.55 }},
    {{ name:'Phoenix',        lat:33.50, lng:-112.00, rad:0.85 }},
    {{ name:'Palm Springs',   lat:33.85, lng:-116.40, rad:0.70 }},
    {{ name:'Sedona',         lat:34.92, lng:-111.80, rad:0.55 }},
    {{ name:'Aspen',          lat:39.15, lng:-106.90, rad:0.75 }},
    {{ name:'Banff',          lat:51.45, lng:-116.10, rad:1.30 }},
    {{ name:'Whistler',       lat:50.15, lng:-122.95, rad:0.70 }},
    {{ name:'Los Cabos',      lat:23.05, lng:-109.80, rad:0.75 }},
    {{ name:'Riviera Maya',   lat:20.50, lng:-87.10,  rad:0.95 }},
    {{ name:'Puerto Vallarta',lat:20.75, lng:-105.40, rad:0.55 }},
    {{ name:'Maui',           lat:20.80, lng:-156.40, rad:0.65 }}
  ];
  function clusterLabel(pts) {{
    const clat = pts.reduce((a,s)=>a+s.lat,0)/pts.length, clng = pts.reduce((a,s)=>a+s.lng,0)/pts.length;
    for (const R of NAMED_REGIONS) if (angDist(clng, clat, R.lng, R.lat) < R.rad) return R.name;
    // fall back to the most prominent member (lowest rank) — usually the recognisable hub town
    let best = pts[0];
    for (const s of pts) if ((s.rank||99) < (best.rank||99)) best = s;
    return best.n;
  }}

  function clearMarkers() {{
    for (const o of markerMap.values()) o.m.remove();
    markerMap.clear();
  }}
  function fmtMin(m) {{
    const h = Math.floor(m/60), mm = m%60;
    if (h && mm) return h + ' hr ' + mm + ' min';
    if (h) return h + ' hr';
    return mm + ' min';
  }}
  // estimated flight time from SF (great-circle distance ÷ cruise speed + overhead)
  function flightMin(lng, lat) {{
    const km = angDist(SF[0], SF[1], lng, lat) * 111.32;
    return Math.max(20, Math.round(30 + km / 800 * 60));
  }}
  // explore (flights) mode: surface only the POIs relevant to the current zoom & viewport,
  // so the globe shows world icons, a continent shows its highlights, a metro shows local gems.
  function visibleAir() {{
    const z = map.getZoom(), c = map.getCenter();
    const el = map.getContainer(), W = el.clientWidth, H = el.clientHeight;
    const cand = [];
    for (const s of currentSpots) {{
      // Tier gate: world icons always; continental spots stay visible all the way down to
      // the globe (so panning/zooming out keeps a populated map); near/local spots still
      // reveal only once you zoom into a region.
      const mz = s.mz || 0;
      const gate = mz <= 0.01 ? 0 : (mz < 5.0 ? 1.2 : mz);
      if (z < gate - 0.01) continue;
      if (introFlight && mz > 0.5) continue;                   // during the intro sweep, world icons only
      if (!s.local && flightMin(s.lng, s.lat) < 60) continue;  // skip sub-1hr flights (not local spots)
      if (angDist(c.lng, c.lat, s.lng, s.lat) > 88) continue;  // far side of the globe
      const p = map.project([s.lng, s.lat]);
      if (p.x < -40 || p.x > W + 40 || p.y < -40 || p.y > H + 40) continue;   // off-screen
      cand.push(s);
    }}
    // Always keep the marquee world icons; fill the rest by tier then prominence.
    const world = cand.filter(s => (s.mz || 0) <= 0.01);
    const rest  = cand.filter(s => (s.mz || 0) > 0.01)
                      .sort((a, b) => (((b.mz||0) - (a.mz||0)) || ((a.rank||9) - (b.rank||9))));
    return world.concat(rest).slice(0, MAX_AIR);
  }}
  function buildGroups(spots) {{
    // Merge two pills only when they're BOTH crowded on screen AND genuinely close on the
    // ground — so far-apart places (e.g. Whistler & Banff) never collapse together just because
    // the globe shrank the distance. Each resulting group gets a real area name, not a count.
    const pr = spots.map(s => {{ const p = map.project([s.lng, s.lat]); return {{ s, x:p.x, y:p.y }}; }});
    const n = pr.length;
    const parent = pr.map((_, i) => i);
    const find = i => {{ while (parent[i] !== i) {{ parent[i] = parent[parent[i]]; i = parent[i]; }} return i; }};
    for (let i = 0; i < n; i++)
      for (let j = i+1; j < n; j++)
        if (Math.hypot(pr[i].x - pr[j].x, pr[i].y - pr[j].y) < CLUSTER_PX
            && angDist(pr[i].s.lng, pr[i].s.lat, pr[j].s.lng, pr[j].s.lat) < GEO_MAX)
          parent[find(i)] = find(j);
    const byRoot = {{}};
    for (let i = 0; i < n; i++) {{ const r = find(i); (byRoot[r] = byRoot[r] || []).push(pr[i].s); }}
    const out = [];
    for (const r in byRoot) {{
      const pts = byRoot[r];
      if (pts.length < 2) {{ out.push({{ id:'P:'+pts[0].n, type:'point', s:pts[0] }}); continue; }}
      const idkey = pts.map(p => p.n).sort().join('|');
      out.push({{ id:'C:'+idkey, type:'cluster', label: clusterLabel(pts), pts,
        lng: pts.reduce((a,s)=>a+s.lng,0)/pts.length,
        lat: pts.reduce((a,s)=>a+s.lat,0)/pts.length }});
    }}
    return out;
  }}
  function makePoint(s) {{
    const el = document.createElement('div'); el.className = 'mk';
    const t = s.local ? ''
            : (mode === 'car' && s.mins) ? '<span class="mk-time"> · ' + fmtMin(s.mins) + '</span>'
            : (mode === 'air') ? '<span class="mk-time"> · $' + bestPrice(s.n, s.lng, s.lat) + '</span>'
            : '';
    const fly = (mode === 'air' && !s.local) ? '<span class="mk-fly">' + AIR_ICON + '</span>' : '';
    el.innerHTML = '<span class="mk-pill"><span class="mk-pop">' + fly + s.n + t + '</span></span>';
    el.addEventListener('click', () => {{
      if (s.n === 'New York') {{ enterMetro(); return; }}
      viewStack.push({{ c: [map.getCenter().lng, map.getCenter().lat], z: map.getZoom() }});
      const z = Math.min(Math.max(map.getZoom() + 2.4, 7.6), 11.5);
      map.easeTo({{ center: [s.lng, s.lat], zoom: z, duration: 850, essential: true }});
    }});
    const m = new maplibregl.Marker({{ element: el, anchor: 'bottom', occludedOpacity: 0 }}).setLngLat([s.lng, s.lat]).addTo(map);
    return {{ m, lng: s.lng, lat: s.lat, far: (mode === 'car' && (s.mins||0) > CAR_MAX) }};
  }}
  function makeCluster(g) {{
    const el = document.createElement('div'); el.className = 'mk mk-clusterwrap';
    el.innerHTML = '<span class="mk-pill"><span class="mk-pop">' + g.label + '</span></span>';
    el.addEventListener('click', () => {{
      viewStack.push({{ c: [map.getCenter().lng, map.getCenter().lat], z: map.getZoom() }});
      const lngs = g.pts.map(s=>s.lng), lats = g.pts.map(s=>s.lat), p = 0.012;
      map.fitBounds([[Math.min(...lngs)-p, Math.min(...lats)-p], [Math.max(...lngs)+p, Math.max(...lats)+p]],
        {{ padding:{{ top:150, bottom:172, left:48, right:48 }}, maxZoom:15, duration:900 }});
    }});
    const m = new maplibregl.Marker({{ element: el, anchor: 'bottom', occludedOpacity: 0 }}).setLngLat([g.lng, g.lat]).addTo(map);
    return {{ m, lng: g.lng, lat: g.lat, far: false }};
  }}
  function refreshMarkers() {{
    const z = map.getZoom(), c = map.getCenter();
    for (const o of markerMap.values()) {{
      let hide = false;
      if (angDist(c.lng, c.lat, o.lng, o.lat) > 88) hide = true;        // far side of the globe
      if (o.far && z > carBaseZoom - 0.4) hide = true;                  // beyond ~9 hr, not zoomed out
      o.m.getElement().style.visibility = hide ? 'hidden' : 'visible';
    }}
  }}
  // recompute what should be shown and add/remove only the differences (unchanged pins don't flicker)
  function layout() {{
    if (flightMode) {{ clearMarkers(); return; }}
    if (!currentSpots.length) {{ clearMarkers(); return; }}
    const work = (mode === 'air') ? visibleAir() : currentSpots;
    const groups = buildGroups(work);
    const want = new Set(groups.map(g => g.id));
    for (const [id, o] of [...markerMap]) if (!want.has(id)) {{ o.m.remove(); markerMap.delete(id); }}
    for (const g of groups) if (!markerMap.has(g.id)) markerMap.set(g.id, g.type==='cluster' ? makeCluster(g) : makePoint(g.s));
    refreshMarkers();
    applyRails();
  }}

  // Edge rail: if a pill would be clipped by the phone edge, slide the bubble inward
  // while its pointer stays pinned to the map location. The pointer ends up at the
  // far-left or far-right of the pill so the full name is always readable.
  const RAIL_M = 6;        // keep this many px clear of each screen edge
  const TAIL_INSET = 14;   // pointer stays at least this far from the bubble's corners
  function applyRails() {{
    const W = map.getContainer().clientWidth;
    for (const o of markerMap.values()) {{
      const el = o.m.getElement();
      if (el.style.visibility === 'hidden') continue;
      const pill = el.querySelector('.mk-pill');
      const pop  = el.querySelector('.mk-pop');
      if (!pill || !pop) continue;
      const bw = pop.offsetWidth; if (!bw) continue;
      const px = map.project([o.lng, o.lat]).x;     // screen x of the map point (= bubble centre at rail 0)
      let off = 0;
      const leftOver  = RAIL_M - (px - bw/2);        // >0 when the left edge is clipped
      const rightOver = (px + bw/2) - (W - RAIL_M);  // >0 when the right edge is clipped
      if (leftOver > 0) off = leftOver;
      else if (rightOver > 0) off = -rightOver;
      const maxOff = Math.max(0, bw/2 - TAIL_INSET); // clamp so the pointer stays attached to the pill
      off = Math.max(-maxOff, Math.min(maxOff, off));
      pill.style.setProperty('--rail', off.toFixed(1) + 'px');
    }}
  }}

  // Keep airport pills from sitting on top of the city-name pills. Airports have no pointer,
  // so we nudge them vertically clear of every visible city/cluster pill (and each other);
  // if there's no free slot nearby, the airport hides. Recomputed on every move, so it keeps
  // re-tidying as you zoom and pan.
  function boxesOverlap(a, b) {{ return a.l < b.r && b.l < a.r && a.t < b.b && b.t < a.b; }}
  function declutterAirports() {{
    const cont = map.getContainer().getBoundingClientRect();
    const rel = r => ({{ l:r.left-cont.left, t:r.top-cont.top, r:r.right-cont.left, b:r.bottom-cont.top }});
    const placed = [];   // obstacles: every visible city/cluster bubble
    for (const o of markerMap.values()) {{
      const el = o.m.getElement();
      if (el.style.visibility === 'hidden') continue;
      const pop = el.querySelector('.mk-pop'); if (!pop) continue;
      placed.push(rel(pop.getBoundingClientRect()));
    }}
    for (const m of airportMarkers) {{
      const el = m.getElement();
      if (el.style.display === 'none') continue;          // out of range — leave hidden
      const box = el.querySelector('.box'); if (!box) continue;
      box.style.transform = '';                            // reset to measure the natural slot
      const base = rel(box.getBoundingClientRect());
      const bh = (base.b - base.t) + 6;
      let chosen = null;
      for (const dy of [0, -bh, bh, -2*bh, 2*bh, -3*bh]) {{
        const cand = {{ l:base.l, t:base.t+dy, r:base.r, b:base.b+dy }};
        if (!placed.some(p => boxesOverlap(cand, p))) {{ chosen = {{ dy, box:cand }}; break; }}
      }}
      if (chosen) {{
        box.style.transform = chosen.dy ? ('translateY(' + chosen.dy + 'px)') : '';
        el.style.visibility = 'visible';
        placed.push(chosen.box);
      }} else {{
        el.style.visibility = 'hidden';
      }}
    }}
  }}

  // ---- Airbnb-style stay price pills (metro / city / street zoom — never country or globe) ----
  // Listings sit on a QUANTIZED tile grid: the cell size halves every zoom level, so on-screen
  // density is roughly constant and only a few dozen cells are ever scanned per frame, at any zoom.
  // Prices/positions are deterministic per (zoomLevel, cell), so pills stay pinned while panning.
  const STAY_Z = 9.5;                 // metro level and tighter (matches the Brooklyn view); off at country/globe
  const STAY_BASE = 150;              // STEP = STAY_BASE / 2^floor(zoom) → a cell is ~constant screen size
  const stayMarkers = new Map();      // cell id -> marker (diffed so unchanged pills don't flicker)
  function srand(seed) {{
    let t = (seed >>> 0) + 0x6D2B79F5;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  }}
  function makeStay(lng, lat, price) {{
    const el = document.createElement('div'); el.className = 'stay';
    el.innerHTML = '<span class="stay-pop">$' + price.toLocaleString() + '</span>';
    return new maplibregl.Marker({{ element: el, anchor: 'center', occludedOpacity: 0 }}).setLngLat([lng, lat]).addTo(map);
  }}
  function refreshStays() {{
    const z = map.getZoom();
    if (flightMode || z < STAY_Z) {{
      if (stayMarkers.size) {{ for (const m of stayMarkers.values()) m.remove(); stayMarkers.clear(); }}
      return;
    }}
    const zq = Math.floor(z), STEP = STAY_BASE / Math.pow(2, zq);   // grid resolution locked per zoom level
    const b = map.getBounds(), W = map.getContainer().clientWidth, H = map.getContainer().clientHeight;
    const i0 = Math.floor(b.getWest()/STEP),  i1 = Math.ceil(b.getEast()/STEP);
    const j0 = Math.floor(b.getSouth()/STEP), j1 = Math.ceil(b.getNorth()/STEP);
    const keep = new Set(), placed = [], data = {{}};
    for (let i = i0; i <= i1 && keep.size < 22; i++) {{
      for (let j = j0; j <= j1 && keep.size < 22; j++) {{
        const seed = ((i * 73856093) ^ (j * 19349663) ^ (zq * 83492791)) >>> 0;
        if (srand(seed) > 0.55) continue;                          // ~55% of cells hold a listing
        const lng = (i + 0.18 + 0.64*srand(seed+1013)) * STEP;     // jitter inside the cell
        const lat = (j + 0.18 + 0.64*srand(seed+2027)) * STEP;
        const p = map.project([lng, lat]);
        if (p.x < 14 || p.x > W-14 || p.y < 64 || p.y > H-14) continue;   // on-screen, clear of the status bar
        if (placed.some(q => Math.hypot(q.x-p.x, q.y-p.y) < 58)) continue; // no overlapping pills
        placed.push(p);
        const id = 'S:' + zq + ':' + i + ':' + j;                  // id includes zoom level → clean re-resolve
        data[id] = {{ lng, lat, price: 1200 + Math.floor(srand(seed+3041) * 5300) }};
        keep.add(id);
      }}
    }}
    for (const [id, m] of [...stayMarkers]) if (!keep.has(id)) {{ m.remove(); stayMarkers.delete(id); }}
    for (const id of keep) if (!stayMarkers.has(id)) {{ const s = data[id]; stayMarkers.set(id, makeStay(s.lng, s.lat, s.price)); }}
  }}

  // ---- current-location avatar ----
  // On the globe (and when on-screen), it's a real MapLibre marker: correctly placed on the
  // sphere and automatically hidden when San Francisco rotates behind the globe.
  const locPinEl = document.createElement('div');
  locPinEl.className = 'loc-pin';
  locPinEl.innerHTML = '<div class="d"></div>';
  const locMarker = new maplibregl.Marker({{ element: locPinEl, anchor: 'bottom', occludedOpacity: 0 }}).setLngLat(SF).addTo(map);
  locPinEl.style.zIndex = '4';   // keep the avatar above the painterly arc

  // painterly arch overlay — lives inside the map container so HTML markers (z>=4) sit on top of it
  const PLANE_SVG = '<svg viewBox="3 3 18 19" fill="#fff"><path d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z"/></svg>';
  const CLOCK_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>';
  const arcSvg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  arcSvg.setAttribute('class', 'arc-svg'); arcSvg.style.display = 'none';
  const arcShadow = document.createElementNS('http://www.w3.org/2000/svg', 'path'); arcShadow.setAttribute('class', 'arc-shadow');
  const arcLine = document.createElementNS('http://www.w3.org/2000/svg', 'path'); arcLine.setAttribute('class', 'arc-line');
  arcSvg.appendChild(arcShadow); arcSvg.appendChild(arcLine);
  map.getContainer().appendChild(arcSvg);
  const arcTime = document.createElement('div'); arcTime.className = 'arc-time'; arcTime.style.display = 'none';
  map.getContainer().appendChild(arcTime);
  function setArcTimeText(s) {{ arcTime.innerHTML = CLOCK_SVG + '<span>' + s + '</span>'; }}
  // control point that lifts a segment into an upward arch
  function archCtrl(a, b) {{
    const dx = b.x-a.x, dy = b.y-a.y, len = Math.hypot(dx, dy) || 1;
    let nx = -dy/len, ny = dx/len; if (ny > 0) {{ nx = -nx; ny = -ny; }}
    const lift = Math.max(34, Math.min(len*0.26, 210));
    return {{ x:(a.x+b.x)/2 + nx*lift, y:(a.y+b.y)/2 + ny*lift }};
  }}
  function bez(a, c, b, t) {{ const u=1-t; return {{ x:u*u*a.x+2*u*t*c.x+t*t*b.x, y:u*u*a.y+2*u*t*c.y+t*t*b.y }}; }}
  const fpt = p => p.x.toFixed(1) + ',' + p.y.toFixed(1);
  function drawArc() {{
    if (!flightMode || !flightDest) {{ arcSvg.style.display = 'none'; arcTime.style.display = 'none'; return; }}
    arcSvg.style.display = ''; arcTime.style.display = '';
    const p0 = map.project(SF), pE = map.project([flightDest.lng, flightDest.lat]);
    let d, mid;
    if (routeVia) {{
      const pv = map.project([routeVia.lng, routeVia.lat]);
      const c1 = archCtrl(p0, pv), c2 = archCtrl(pv, pE);
      d = 'M' + fpt(p0) + ' Q' + fpt(c1) + ' ' + fpt(pv) + ' Q' + fpt(c2) + ' ' + fpt(pE);
      mid = bez(p0, c1, pv, 0.5);                       // time pill on the first leg
    }} else {{
      const c = archCtrl(p0, pE);
      d = 'M' + fpt(p0) + ' Q' + fpt(c) + ' ' + fpt(pE);
      mid = bez(p0, c, pE, 0.5);
    }}
    arcLine.setAttribute('d', d); arcShadow.setAttribute('d', d);
    arcTime.style.transform = 'translate(' + mid.x.toFixed(1) + 'px,' + mid.y.toFixed(1) + 'px) translate(-50%,-50%)';
  }}
  // tap the avatar to fly back to the starting (post-intro) view
  locPinEl.addEventListener('click', (ev) => {{
    ev.stopPropagation(); metro = false; viewStack = [];
    map.easeTo({{ center: SF, zoom: 3.0, offset: [0, 32], duration: 1200, easing: t => 1 - Math.pow(1 - t, 3), essential: true }});
  }});

  // visited trips — classic red push pins that stay on the map
  [['London',51.51,-0.13],['Paris',48.86,2.35],['Milan',45.46,9.19]].forEach(([n,lat,lng]) => {{
    const e = document.createElement('div'); e.className = 'trippin'; e.title = n;
    e.innerHTML = '<div class="sh"></div><div class="pin"></div><div class="head"></div>';
    new maplibregl.Marker({{ element: e, anchor: 'bottom', occludedOpacity: 0 }}).setLngLat([lng, lat]).addTo(map);
  }});

  // metro airports — blue pills, shown when zoomed into a city
  const airportMarkers = [];
  let derivedAir = null;              // synthetic "nearest airport" for destinations with no curated one
  const AIRPIN_SVG = '<svg viewBox="3 3 18 19" fill="#fff"><path d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z"/></svg>';
  function airpinEl(code) {{
    const e = document.createElement('div'); e.className = 'airpin';
    e.innerHTML = '<div class="box">' + AIRPIN_SVG + '<span class="code">' + code + '</span></div>';
    return e;
  }}
  // Build a plausible 3-letter code from a place name, e.g. "Mendocino" -> "MEN", "Sea Ranch" -> "SEA".
  function deriveCode(name) {{
    const L = (name || '').toUpperCase().replace(/[^A-Z]/g, '');
    return L.length >= 3 ? L.slice(0, 3) : (L + 'XXX').slice(0, 3);
  }}
  const AIRPORTS = [
    ['SFO',37.621,-122.379],['LAX',33.942,-118.408],['SAN',32.733,-117.190],['PSP',33.829,-116.507],
    ['JFK',40.641,-73.778],['LGA',40.777,-73.872],['EWR',40.689,-74.174],['ORD',41.978,-87.905],
    ['LAS',36.084,-115.154],['PHX',33.434,-112.012],['FLG',35.138,-111.671],['MIA',25.795,-80.287],
    ['SEA',47.450,-122.309],['DEN',39.856,-104.673],['BOS',42.366,-71.020],['ATL',33.640,-84.427],
    ['MSY',29.993,-90.258],['PDX',45.589,-122.595],['ASE',39.223,-106.869],['EGE',39.643,-106.918],
    ['RNO',39.499,-119.768],['OGG',20.899,-156.430],['HNL',21.318,-157.922],
    ['BZN',45.777,-111.153],['JAC',43.607,-110.738],['WYS',44.688,-111.118],['IDA',43.515,-112.071],['COD',44.520,-109.024],['SLC',40.788,-111.978],['SMF',38.695,-121.591],
    ['YVR',49.195,-123.182],['YYC',51.114,-114.020],['YYZ',43.677,-79.624],['YUL',45.470,-73.741],
    ['CUN',21.037,-86.877],['SJD',23.152,-109.721],['PVR',20.680,-105.254],['MEX',19.436,-99.072],
    ['CDG',49.010,2.548],['LHR',51.470,-0.454],['FCO',41.800,12.239],['BCN',41.297,2.083],
    ['AMS',52.309,4.764],['MXP',45.630,8.728],['IST',41.262,28.742],['ATH',37.937,23.945],['LIS',38.774,-9.134],
    ['HND',35.553,139.781],['NRT',35.772,140.392],['BKK',13.690,100.750],['SIN',1.364,103.991],
    ['HKG',22.308,113.918],['ICN',37.460,126.441],['DPS',-8.748,115.167],
    ['SYD',-33.946,151.177],['AKL',-37.008,174.792],['MEL',-37.669,144.841],['NAN',-17.755,177.443]
  ];
  AIRPORTS.forEach(([code,lat,lng]) => {{
    const e = airpinEl(code);
    const m = new maplibregl.Marker({{ element: e, anchor: 'center', occludedOpacity: 0 }}).setLngLat([lng, lat]).addTo(map);
    e.addEventListener('click', () => openFlight(code, lng, lat));
    e.style.display = 'none'; airportMarkers.push(m);
  }});
  function refreshAirports() {{
    if (flightMode) {{
      for (const m of airportMarkers) m.getElement().style.display = 'none';
      if (derivedAir) {{ derivedAir.remove(); derivedAir = null; }}
      SCREEN.classList.remove('airports-visible'); return;
    }}
    const z = map.getZoom(), c = map.getCenter();
    const near = z >= 6.2;
    const R = Math.PI / 180;
    let anyAir = false;
    for (const m of airportMarkers) {{
      const ll = m.getLngLat();
      const d = Math.acos(Math.min(1, Math.sin(c.lat*R)*Math.sin(ll.lat*R) + Math.cos(c.lat*R)*Math.cos(ll.lat*R)*Math.cos((ll.lng-c.lng)*R))) / R;
      const show = near && d < 3.5;
      m.getElement().style.display = show ? '' : 'none';
      if (show) anyAir = true;
    }}
    // Fallback: zoomed into a place with no curated airport in range → derive a nearest airport on the
    // fly, anchored to the destination itself (nearest explore spot, else nearest town, else a stable
    // rounded point) so EVERY destination always has at least one tappable airport.
    if (near && !anyAir) {{
      let anchor = null, bd = 1e9;
      for (const s of currentSpots) {{ const d = angDist(c.lng, c.lat, s.lng, s.lat); if (d < bd) {{ bd = d; anchor = s; }} }}
      let name, blat, blng;
      if (anchor && bd < 1.6) {{ name = anchor.n; blat = anchor.lat; blng = anchor.lng; }}
      else {{ const t = nearestTown({{ lng:c.lng, lat:c.lat }});
        if (t) {{ name = t.n; blat = t.lat; blng = t.lng; }}
        else {{ name = 'This area'; blat = Math.round(c.lat*2)/2; blng = Math.round(c.lng*2)/2; }} }}  // stable under panning
      const alat = blat + 0.045, alng = blng + 0.05;            // airport sits just outside the place
      const code = deriveCode(name);
      const id = code + '@' + alat.toFixed(2) + ',' + alng.toFixed(2);
      if (!derivedAir || derivedAir._id !== id) {{                // only rebuild when the target actually changes
        if (derivedAir) derivedAir.remove();
        const e = airpinEl(code);
        e.addEventListener('click', () => openFlight(code, alng, alat));
        derivedAir = new maplibregl.Marker({{ element: e, anchor: 'center', occludedOpacity: 0 }}).setLngLat([alng, alat]).addTo(map);
        derivedAir._id = id;
      }}
      anyAir = true;
    }} else if (derivedAir) {{ derivedAir.remove(); derivedAir = null; }}
    SCREEN.classList.toggle('airports-visible', anyAir);   // hides the city-pill flight glyphs while pins are up
  }}

  // When zoomed in (flat) and SF is off-screen, swap to an edge indicator that points home.
  const locEl = document.getElementById('loc-indicator');
  const locPtr = locEl.querySelector('.loc-ptr-wrap');
  const LR = 22, RECT = {{ l:30, t:214, r:372, b:700 }};
  function angDist(lo1, la1, lo2, la2) {{   // great-circle angle in degrees
    const r = Math.PI/180; la1 *= r; la2 *= r;
    const c = Math.sin(la1)*Math.sin(la2) + Math.cos(la1)*Math.cos(la2)*Math.cos((lo2-lo1)*r);
    return Math.acos(Math.max(-1, Math.min(1, c)))/r;
  }}
  function updateLoc() {{
    const z = map.getZoom();
    const p = map.project(SF);
    if (z < 4.5) {{
      // globe view: marker rides the sphere; hide it when SF is on the far side
      locEl.style.display = 'none';
      const c = map.getCenter();
      const behind = angDist(c.lng, c.lat, SF[0], SF[1]) > 90;
      locPinEl.style.display = behind ? 'none' : '';
      return;
    }}
    const inRect = p.x >= RECT.l && p.x <= RECT.r && p.y >= RECT.t && p.y <= RECT.b;
    if (!inRect) {{
      // flat + off-screen → edge indicator pointing back toward SF
      locPinEl.style.display = 'none';
      locEl.style.display = 'block';
      const cx0 = (RECT.l+RECT.r)/2, cy0 = (RECT.t+RECT.b)/2;
      let dx = p.x-cx0, dy = p.y-cy0, t = 1;
      if (dx > 0) t = Math.min(t, (RECT.r-cx0)/dx);
      if (dx < 0) t = Math.min(t, (RECT.l-cx0)/dx);
      if (dy > 0) t = Math.min(t, (RECT.b-cy0)/dy);
      if (dy < 0) t = Math.min(t, (RECT.t-cy0)/dy);
      const cx = cx0+dx*t, cy = cy0+dy*t;
      const theta = Math.atan2(p.y-cy, p.x-cx);
      locEl.style.left = (cx-LR)+'px';
      locEl.style.top  = (cy-LR)+'px';
      locPtr.style.transform = 'rotate(' + (theta*180/Math.PI + 90) + 'deg)';
    }} else {{
      // flat + on-screen → MapLibre marker at SF
      locPinEl.style.display = '';
      locEl.style.display = 'none';
    }}
  }}
  map.on('move', () => {{ if (!suppressLayout) layout(); updateLoc(); updateContext(); refreshAirports(); applyRails(); declutterAirports(); updateSearchBar(); drawArc(); refreshStays(); }});

  const VIBES = {VIBE_JSON};
  const AIR_ICON = {AIR_ICON_JSON};

  // Only real, curated places are shown — nothing is synthesized.
  function airSpots(vibe) {{ return VIBES[vibe].air; }}
  let mode = 'air';        // matches the highlighted dock button
  let activeVibe = null;

  function render(instant) {{
    if (!activeVibe || !VIBES[activeVibe]) return;
    currentSpots = (mode === 'air') ? airSpots(activeVibe) : (VIBES[activeVibe][mode] || []);
    // explore (flights) is zoom/locale-driven: keep the current camera and just re-pick the
    // POIs that belong to this view. The incremental layout swaps the old vibe's pins for the new.
    if (mode === 'air') {{ layout(); return; }}
    clearMarkers();
    if (!currentSpots.length) return;
    const isCar = mode === 'car';

    // car mode frames the ~9 hr radius (near cities + the SF origin); other modes fit everything
    let pts;
    if (isCar) {{
      const near = currentSpots.filter(s => (s.mins||0) <= CAR_MAX);
      pts = (near.length ? near : currentSpots).map(s => [s.lng, s.lat]);
      pts.push(SF);
    }} else {{
      pts = currentSpots.map(s => [s.lng, s.lat]);
    }}
    const b = [
      [Math.min(...pts.map(p=>p[0])), Math.min(...pts.map(p=>p[1]))],
      [Math.max(...pts.map(p=>p[0])), Math.max(...pts.map(p=>p[1]))]
    ];
    const pad = {{ top:150, bottom:176, left:46, right:46 }};
    if (isCar) {{
      const cam = map.cameraForBounds(b, {{ padding: pad, maxZoom: 12 }});
      carBaseZoom = cam ? cam.zoom : 7;
    }}
    map.fitBounds(b, {{ padding: pad, maxZoom: isCar ? 12 : 14.5, duration: instant ? 0 : 1300 }});
    layout();
  }}

  // ---------- Category strip (global vibes ↔ context-aware local vibes) ----------
  const wrap = document.getElementById('cards');
  const GLOBAL_CARDS_HTML = wrap.innerHTML;     // the photo cards, captured for restore
  let globalVibe = 'relax', localType = null, localVibe = null;
  let viewStack = [];   // remembers prior zoom views so Back can return to them
  let metro = false;    // true while inside a metropolitan (borough) view
  const NYC_BOROUGHS = [
    {{n:'Manhattan',lat:40.78,lng:-73.97,mz:0,rank:1,r:'Manhattan',local:true}},
    {{n:'Brooklyn',lat:40.65,lng:-73.95,mz:0,rank:2,r:'Brooklyn',local:true}},
    {{n:'Queens',lat:40.73,lng:-73.79,mz:0,rank:3,r:'Queens',local:true}},
    {{n:'The Bronx',lat:40.84,lng:-73.87,mz:0,rank:4,r:'Bronx',local:true}},
    {{n:'Staten Island',lat:40.58,lng:-74.15,mz:0,rank:5,r:'StatenIsland',local:true}}
  ];
  function enterMetro() {{
    metro = true;
    viewStack.push({{ c: [map.getCenter().lng, map.getCenter().lat], z: map.getZoom() }});
    currentSpots = NYC_BOROUGHS; clearMarkers();
    map.easeTo({{ center: [-73.96, 40.71], zoom: 9.2, duration: 1000, easing: t => 1 - Math.pow(1 - t, 3), essential: true }});
    map.once('moveend', () => layout());
  }}

  const LOCAL_Z = 5.4;
  const ICONP = {{
    ski:'M3 20h7l4-9 4 9h3M8 20l3-7', bar:'M5 4h14l-7 8zM12 12v6M8 21h8',
    town:'M4 21h16M6 21V8l5-3 5 3v13M9 21v-4h4v4', star:'M12 3l2.5 5.5 5.5.6-4 4 1 5.4L12 21l-4.5-2.5 1-5.4-4-4 5.5-.6z',
    view:'M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12zM12 9a3 3 0 100 6 3 3 0 000-6z',
    trail:'M6 21c4-2 2-6 5-8s5 1 7-3M5 21h.01', food:'M4 11h16a8 8 0 0 1-16 0zM9 3c0 1.2-1 1.2-1 2.4M14 3c0 1.2-1 1.2-1 2.4',
    beach:'M4 18h16M6 18a8 8 0 0114 0M12 5v1', wave:'M2 14c2-2 4-2 6 0s4 2 6 0 4-2 6 0M2 18c2-2 4-2 6 0s4 2 6 0 4-2 6 0',
    sun:'M12 5V3M12 21v-2M5 12H3M21 12h-2M6 6L5 5M19 19l-1-1M6 18l-1 1M19 5l-1 1M12 8a4 4 0 100 8 4 4 0 000-8z',
    spa:'M12 21c-4-3-7-6-7-10a4 4 0 018 0 4 4 0 018 0c0 4-3 7-9 10z', gem:'M12 3l8 6-8 12L4 9z'
  }};
  const G = {{ a:'linear-gradient(135deg,#5b8def,#3a6fd8)', b:'linear-gradient(135deg,#f2a65a,#e07a3f)',
    c:'linear-gradient(135deg,#56c596,#2fa777)', d:'linear-gradient(135deg,#b07cf0,#8a52d8)',
    e:'linear-gradient(135deg,#f06595,#d6457a)', f:'linear-gradient(135deg,#4dc4d9,#2a9fb8)' }};
  const LOCAL_VIBES = {{
    ski:[
      {{id:'skiio',label:'Ski-in Ski-out',icon:'ski',grad:G.a,sat:['Base Lodge','Gondola Plaza','Slopeside Inn','Chairlift 7','Village Run']}},
      {{id:'apres',label:'Après-Ski',icon:'bar',grad:G.b,sat:['Lodge Bar','Fondue House','Hot Tub Deck','Brewpub','Fire Pit Lounge']}},
      {{id:'village',label:'Close to Village',icon:'town',grad:G.c,sat:['Village Stroll','Main Plaza','Market Square','The Promenade','Clock Tower']}},
      {{id:'views',label:'Mountain Views',icon:'view',grad:G.f,sat:['Summit Deck','Glacier Lookout','Ridge Vista','Peak Café','Alpine Overlook']}},
      {{id:'easy',label:'Easy Runs',icon:'trail',grad:G.d,sat:['Bunny Hill','Green Run','Magic Carpet','Ski School','Family Slope']}}],
    beach:[
      {{id:'beachfront',label:'Beachfront',icon:'beach',grad:G.f,sat:['Beach Club','Boardwalk','The Pier','Shore Cabanas','Sandbar']}},
      {{id:'snorkel',label:'Snorkel Spots',icon:'wave',grad:G.c,sat:['Coral Reef','Hidden Cove','Blue Lagoon','Marine Park','Tide Pools']}},
      {{id:'sunset',label:'Sunset Bars',icon:'sun',grad:G.b,sat:['Sunset Deck','Tiki Bar','Cliff Lounge','Rooftop Bar','Beach Fire']}},
      {{id:'townb',label:'Close to Town',icon:'town',grad:G.a,sat:['Old Town','The Marina','Main Street','Market','Harbor Walk']}},
      {{id:'familyb',label:'Family Beaches',icon:'star',grad:G.e,sat:['Calm Bay','Kids Cove','The Shallows','Picnic Beach','Lifeguard Beach']}}],
    city:[
      {{id:'downtown',label:'Close to Downtown',icon:'town',grad:G.a,sat:['City Center','Main Square','Grand Avenue','Riverside','Old Quarter']}},
      {{id:'fav',label:'Most Favorite',icon:'star',grad:G.b,sat:['The Landmark','Icon Plaza','Famous Bridge','Top Sight','Grand Gallery']}},
      {{id:'hidden',label:'Hidden Gems',icon:'gem',grad:G.d,sat:['Backstreet Café','Secret Courtyard','Local Bar','Tucked Bistro','Quiet Garden']}},
      {{id:'food',label:'Foodie Picks',icon:'food',grad:G.c,sat:['Food Market','Bistro Row','Night Market','Bakery Lane','Wine Bar']}},
      {{id:'night',label:'Nightlife',icon:'bar',grad:G.e,sat:['Club District','Live Music','Rooftop Bar','Jazz Cellar','Late Lounge']}}],
    desert:[
      {{id:'scenic',label:'Scenic Drives',icon:'view',grad:G.b,sat:['Canyon Drive','Red Rock Loop','Vista Point','Desert Overlook','Sunset Road']}},
      {{id:'wellness',label:'Wellness & Spa',icon:'spa',grad:G.c,sat:['Hot Springs','Spa Retreat','Yoga Mesa','Healing Center','Day Spa']}},
      {{id:'stars',label:'Stargazing',icon:'star',grad:G.d,sat:['Dark Sky Park','Star Mesa','Night Overlook','Observatory','Desert Camp']}},
      {{id:'trail',label:'Trailheads',icon:'trail',grad:G.f,sat:['Trailhead','Slot Canyon','Rim Trail','Summit Path','Oasis Walk']}},
      {{id:'favd',label:'Most Favorite',icon:'gem',grad:G.a,sat:['Famous Rock','Top Vista','Icon Trail','Best Sunset','Landmark']}}],
    default:[
      {{id:'fav',label:'Most Favorite',icon:'star',grad:G.b,sat:['Top Sight','The Landmark','Best Spot','Local Icon','Must See']}},
      {{id:'downtown',label:'Close to Downtown',icon:'town',grad:G.a,sat:['Downtown','City Center','Main Street','Old Town','Central Plaza']}},
      {{id:'hidden',label:'Hidden Gems',icon:'gem',grad:G.d,sat:['Backstreet','Local Favorite','Tucked Away','Secret Spot','Quiet Corner']}},
      {{id:'top',label:'Top Rated',icon:'star',grad:G.c,sat:['Five Star','Award Winner','Top Pick','Acclaimed','Best Reviewed']}},
      {{id:'family',label:'Family Friendly',icon:'view',grad:G.e,sat:['Family Park','Kids Zone','Easy Walk','Picnic Area','Playground']}}]
  }};
  const TOWNS = [
    ['Whistler',50.12,-122.95,'ski'],['Aspen',39.19,-106.82,'ski'],['Banff',51.18,-115.57,'ski'],['Vail',39.64,-106.37,'ski'],['Lake Tahoe',39.10,-120.03,'ski'],['Queenstown',-45.03,168.66,'ski'],['Chamonix',45.92,6.87,'ski'],
    ['Maui',20.79,-156.33,'beach'],['Cancún',21.16,-86.85,'beach'],['Tulum',20.21,-87.46,'beach'],['Cabo San Lucas',22.89,-109.91,'beach'],['Puerto Vallarta',20.65,-105.22,'beach'],['Bali',-8.41,115.19,'beach'],['Phuket',7.88,98.39,'beach'],['Bora Bora',-16.5,-151.74,'beach'],['Maldives',3.2,73.0,'beach'],['Waikiki',21.28,-157.84,'beach'],
    ['Paris',48.86,2.35,'city'],['Tokyo',35.68,139.69,'city'],['New York',40.71,-74.0,'city'],['London',51.51,-0.13,'city'],['Rome',41.9,12.5,'city'],['Barcelona',41.39,2.17,'city'],['San Francisco',37.77,-122.42,'city'],['Mexico City',19.43,-99.13,'city'],['Bangkok',13.75,100.5,'city'],['Las Vegas',36.17,-115.14,'city'],
    ['Sedona',34.87,-111.76,'desert'],['Palm Springs',33.83,-116.55,'desert'],['Joshua Tree',33.87,-115.90,'desert'],['Moab',38.57,-109.55,'desert'],['Grand Canyon',36.1,-112.11,'desert']
  ];
  function nearestTown(c) {{
    let best = null, bd = 1e9;
    for (const t of TOWNS) {{ const d = angDist(c.lng, c.lat, t[2], t[1]); if (d < bd) {{ bd = d; best = {{ n:t[0], lat:t[1], lng:t[2], type:t[3], d }}; }} }}
    return (best && best.d < 2.2) ? best : null;
  }}
  function localCardHtml(v, active) {{
    return '<div class="cat' + (active ? ' active' : '') + '" data-id="' + v.id + '">'
      + '<div class="thumb-wrap"><div class="thumb"><div class="grad" style="background:' + v.grad + '">'
      + '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="' + ICONP[v.icon] + '"/></svg>'
      + '</div></div></div><div class="label">' + v.label + '</div></div>';
  }}
  function centerCard(c) {{ setTimeout(() => {{ const left = c.offsetLeft - (wrap.clientWidth - c.offsetWidth) / 2; wrap.scrollTo({{ left: Math.max(0, left), behavior:'smooth' }}); }}, 60); }}
  function bindCards() {{
    wrap.querySelectorAll('.cat').forEach(c => {{
      c.addEventListener('click', () => {{
        const cur = wrap.querySelector('.cat.active');
        if (cur !== c) {{ cur && cur.classList.remove('active'); c.classList.add('active'); centerCard(c); }}
        if (localType) {{ localVibe = c.dataset.id; currentSpots = airSpots(activeVibe); clearMarkers(); layout(); }}
        else {{ globalVibe = activeVibe = c.dataset.id; render(); }}
      }});
    }});
  }}
  function showGlobalCards() {{
    wrap.innerHTML = GLOBAL_CARDS_HTML;
    wrap.querySelectorAll('.cat').forEach(c => c.classList.toggle('active', c.dataset.id === globalVibe));
    wrap.scrollTo({{ left:0 }}); bindCards();
  }}
  function showLocalCards(type) {{
    const set = LOCAL_VIBES[type] || LOCAL_VIBES.default;
    localVibe = set[0].id;
    wrap.innerHTML = set.map((v, i) => localCardHtml(v, i === 0)).join('');
    wrap.scrollTo({{ left:0 }}); bindCards();
  }}
  // swap the strip to fit where you are: local vibes when zoomed into a place, global vibes otherwise
  function updateContext() {{
    if (flightMode) return;
    if (mode !== 'air') {{ if (localType) {{ localType = null; showGlobalCards(); }} metro = false; updateSearchBar(); return; }}
    const z = map.getZoom();
    if (z >= LOCAL_Z) {{
      const t = nearestTown(map.getCenter()), type = t ? t.type : 'default';
      if (localType !== type) {{ localType = type; showLocalCards(type); if (!metro) {{ currentSpots = airSpots(activeVibe); clearMarkers(); layout(); }} }}
      updateSearchBar();
    }} else if (localType) {{
      localType = null; metro = false; showGlobalCards();
      activeVibe = globalVibe; currentSpots = airSpots(globalVibe); clearMarkers(); layout();
      updateSearchBar();
    }}
  }}
  bindCards();

  // ---------- search bar (logo/back + two-line title + voice) ----------
  // Placeholder brand mark — drop your own logo SVG here in place of LOGO_SVG.
  const LOGO_SVG = {LOGO_JSON};
  const BACK_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="#1f1f1f" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg>';
  const pillLeft = document.getElementById('pillLeft');
  const pillT1 = document.getElementById('pillT1');
  const pillT2 = document.getElementById('pillT2');
  function updateSearchBar() {{
    if (flightMode) {{
      pillLeft.dataset.act = 'flightback';
      pillLeft.innerHTML = BACK_SVG;
      pillT1.textContent = flightInfo.t1 || '';
      pillT2.textContent = flightInfo.t2 || '';
      return;
    }}
    const drilled = viewStack.length > 0 || (mode === 'air' && localType);
    const want = drilled ? 'back' : 'logo';
    if (pillLeft.dataset.act !== want) {{
      pillLeft.dataset.act = want;
      pillLeft.innerHTML = drilled ? BACK_SVG : LOGO_SVG;
    }}
    if (mode === 'air' && localType) {{
      const t = nearestTown(map.getCenter());
      pillT1.textContent = (t ? t.n : 'This') + ' area';
      pillT2.textContent = 'a week in October';
    }} else {{
      pillT1.textContent = 'Where to?';
      pillT2.textContent = 'Anywhere · Any week';
    }}
  }}
  function goBack() {{
    if (viewStack.length) {{
      const v = viewStack.pop();
      map.easeTo({{ center: v.c, zoom: v.z, offset: [0, 32], duration: 800, easing: t => 1 - Math.pow(1 - t, 3), essential: true }});
    }} else {{
      map.easeTo({{ center: SF, zoom: 3.0, offset: [0, 32], duration: 800, easing: t => 1 - Math.pow(1 - t, 3), essential: true }});
    }}
  }}
  pillLeft.addEventListener('click', () => {{
    if (pillLeft.dataset.act === 'flightback') closeFlight();
    else if (pillLeft.dataset.act === 'back') goBack();
  }});

  // ---------- flight mode (tap an airport → arc + buyable flights half-sheet) ----------
  // The arch itself is drawn in screen space by drawArc() (defined near the avatar) so it
  // reads as a lifted, painterly arc at every zoom. Below: pricing, the sheet, alternates.
  function pad2(n) {{ return (n<10?'0':'') + n; }}
  function fmtClock(mins) {{ let h=Math.floor(mins/60)%24, m=mins%60; const ap=h<12?'AM':'PM'; let hh=h%12; if(!hh)hh=12; return hh+':'+pad2(m)+' '+ap; }}
  function fmtDurShort(mins) {{ const h=Math.floor(mins/60), m=mins%60; return (h?h+'h':'') + (h&&m?' ':'') + (m?m+'m':(h?'':'0m')); }}
  // pick a sensible connecting hub between SF and the destination for layover flights
  const HUBS = [['DEN',39.856,-104.673],['LAX',33.942,-118.408],['PHX',33.434,-112.012],['LAS',36.084,-115.154],['SEA',47.450,-122.309],['ORD',41.978,-87.905],['ATL',33.640,-84.427]];
  function pickVia(destCode, dLng, dLat) {{
    let best = null, bd = 1e9;
    for (const [c,la,lo] of HUBS) {{
      if (c === destCode) continue;
      const detour = angDist(SF[0], SF[1], lo, la) + angDist(lo, la, dLng, dLat);
      if (detour < bd && detour > angDist(SF[0],SF[1],dLng,dLat) + 0.25) {{ bd = detour; best = {{ code:c, lng:lo, lat:la }}; }}
    }}
    return best;
  }}
  function mockFlights(code, lng, lat) {{
    const fmins = flightMin(lng, lat);
    const base = Math.round(70 + fmins*0.9);
    const lines = [['AS','Alaska','#01426a'],['UA','United','#1414aa'],['DL','Delta','#9b1b30'],['B6','JetBlue','#1c3f94'],['WN','Southwest','#2e4bb6']];
    const deps = [375, 580, 785, 980, 1190], stops = [0,0,1,0,1];
    const via = pickVia(code, lng, lat);
    return deps.map((dep,i) => {{
      const extra = stops[i] ? 95 : 0, total = fmins + extra;
      return {{ a:lines[i%lines.length], dep:fmtClock(dep), arr:fmtClock(dep+total),
        durMins: total, dur: fmtMin(total), stop: stops[i] ? '1 stop' : 'Nonstop',
        via: stops[i] ? via : null, price: base + i*23 + (stops[i]?-35:18) }};
    }});
  }}
  function bestPrice(code, lng, lat) {{ return Math.min(...mockFlights(code, lng, lat).map(f => f.price)); }}
  function renderFlights(code, lng, lat) {{
    curFlights = mockFlights(code, lng, lat);
    const durs = curFlights.map(f => f.durMins);
    setArcTimeText(fmtDurShort(Math.min(...durs)) + ' – ' + fmtDurShort(Math.max(...durs)));
    document.getElementById('fsSub').innerHTML =
      '<span>Departing today · 1 adult</span><span class="price-h">from $' + Math.min(...curFlights.map(f=>f.price)) + '</span>';
    document.getElementById('fsList').innerHTML = curFlights.map((f,i) =>
      '<div class="fs-row" data-i="' + i + '">'
      + '<div class="fs-badge" style="background:' + f.a[2] + '">' + f.a[0] + '</div>'
      + '<div class="fs-mid"><div class="fs-times">' + f.dep + ' – ' + f.arr + '</div>'
      + '<div class="fs-meta">' + f.a[1] + ' · ' + f.stop + (f.via ? ' via ' + f.via.code : '') + ' · ' + f.dur + '</div></div>'
      + '<div class="fs-right"><div class="fs-price">$' + f.price + '</div><button class="fs-buy">Select</button></div>'
      + '</div>').join('');
  }}
  // tapping a flight row previews its routing — layovers bend the dotted line through the hub
  document.getElementById('fsList').addEventListener('click', e => {{
    const row = e.target.closest('.fs-row'); if (!row) return;
    const f = curFlights[+row.dataset.i]; if (!f) return;
    document.querySelectorAll('.fs-row.sel').forEach(r => r.classList.remove('sel'));
    row.classList.add('sel');
    setRoute(f.via);
    setArcTimeText(fmtDurShort(f.durMins));
    frameFlight(700);                                          // bring the layover hub into frame too
    if (detent === 'collapsed') map.once('moveend', showAlternates);
  }});
  function setRoute(via) {{
    routeVia = via || null;
    if (viaMarker) {{ viaMarker.remove(); viaMarker = null; }}
    if (routeVia) {{
      const el = document.createElement('div'); el.className = 'viapin';
      el.innerHTML = '<div class="vd"></div><div class="vl">' + routeVia.code + '</div>';
      viaMarker = new maplibregl.Marker({{ element: el, anchor: 'top', occludedOpacity: 0 }}).setLngLat([routeVia.lng, routeVia.lat]).addTo(map);
      el.style.zIndex = '4';
    }}
    drawArc();
  }}

  // ---- the flight half-sheet (the search pill is its draggable header) ----
  const fsheet = document.getElementById('flightsheet');
  const fpill  = document.querySelector('.pill');
  const PILL_TOP = 316;
  function setSheet(ty) {{
    sheetTY = Math.max(0, Math.min(COLLAPSE_DY, ty));
    fsheet.style.transform = 'translateY(' + sheetTY + 'px)';
    fpill.style.top = (PILL_TOP + sheetTY) + 'px';
  }}
  // The flight view always keeps the two ends in frame — the avatar (SF) and the destination
  // airport (plus the layover hub when there is one). Only the bottom padding changes between
  // detents, so collapsing just reveals more map instead of jumping to a new place.
  function curBottom() {{ return detent === 'collapsed' ? 188 : 566; }}
  function frameFlight(dur) {{
    if (!flightDest) return;
    const pts = [SF, [flightDest.lng, flightDest.lat]];
    if (routeVia) pts.push([routeVia.lng, routeVia.lat]);
    const lngs = pts.map(p=>p[0]), lats = pts.map(p=>p[1]);
    map.fitBounds([[Math.min(...lngs), Math.min(...lats)], [Math.max(...lngs), Math.max(...lats)]],
      {{ padding:{{ top:118, bottom:curBottom(), left:70, right:96 }}, maxZoom:7,
         duration:dur, easing:t => 1 - Math.pow(1 - t, 3), essential:true }});
  }}
  function expandSheet() {{ detent = 'expanded'; setSheet(0); clearAlternates(); frameFlight(820); }}
  function collapseSheet() {{ detent = 'collapsed'; setSheet(COLLAPSE_DY); frameFlight(820); map.once('moveend', showAlternates); }}
  // drag the search-bar header up/down to move between the two detents
  let dragY=null, dragTY=0, dragMoved=0;
  fpill.addEventListener('pointerdown', e => {{
    if (!flightMode) return;
    if (e.target.closest('#pillLeft') || e.target.closest('#pillRight')) return;
    dragY = e.clientY; dragTY = sheetTY; dragMoved = 0;
    fsheet.style.transition = 'none'; fpill.style.transition = 'none';
    try {{ fpill.setPointerCapture(e.pointerId); }} catch (_) {{}}
  }});
  fpill.addEventListener('pointermove', e => {{
    if (dragY == null) return;
    const dy = e.clientY - dragY; dragMoved = Math.max(dragMoved, Math.abs(dy));
    setSheet(dragTY + dy);
  }});
  fpill.addEventListener('pointerup', e => {{
    if (dragY == null) return; dragY = null;
    fsheet.style.transition = ''; fpill.style.transition = '';
    if (dragMoved < 6) {{ (sheetTY > 4 ? expandSheet() : collapseSheet()); }}     // tap toggles
    else {{ (sheetTY > COLLAPSE_DY/2 ? collapseSheet() : expandSheet()); }}        // drag snaps
  }});

  // ---- nearby-airport price pills (shown when the sheet is pulled down) ----
  function clearAlternates() {{ flightAirportMarkers.forEach(m => m.remove()); flightAirportMarkers = []; }}
  const AIRPORT_CITY = {{ SFO:'San Francisco', LAX:'Los Angeles', SAN:'San Diego', PSP:'Palm Springs', JFK:'New York', LGA:'LaGuardia', EWR:'Newark', ORD:'Chicago', LAS:'Las Vegas', PHX:'Phoenix', FLG:'Flagstaff', MIA:'Miami', SEA:'Seattle', DEN:'Denver', BOS:'Boston', ATL:'Atlanta', MSY:'New Orleans', PDX:'Portland', ASE:'Aspen', EGE:'Vail', RNO:'Reno', OGG:'Maui', HNL:'Honolulu', YVR:'Vancouver', YYC:'Calgary', YYZ:'Toronto', YUL:'Montréal', CUN:'Cancún', SJD:'Los Cabos', PVR:'Puerto Vallarta', MEX:'Mexico City', CDG:'Paris', LHR:'London', FCO:'Rome', BCN:'Barcelona', AMS:'Amsterdam', MXP:'Milan', IST:'Istanbul', ATH:'Athens', LIS:'Lisbon', HND:'Tokyo', NRT:'Tokyo', BKK:'Bangkok', SIN:'Singapore', HKG:'Hong Kong', ICN:'Seoul', DPS:'Bali', SYD:'Sydney', AKL:'Auckland', MEL:'Melbourne', NAN:'Fiji' }};
  function airName(code, lng, lat) {{ if (AIRPORT_CITY[code]) return AIRPORT_CITY[code]; const t = nearestTown({{ lng, lat }}); return t ? t.n : code; }}
  function pricePillEl(code, lng, lat, active) {{
    const el = document.createElement('div'); el.className = 'fa-pill' + (active ? ' active' : '');
    el.innerHTML = '<span class="fa-pop"><span class="fa-ico">' + PLANE_SVG + '</span><span class="fa-name">' + airName(code,lng,lat)
      + '</span><span class="fa-sep">·</span><span class="fa-price">$' + bestPrice(code, lng, lat) + '</span></span>';
    return el;
  }}
  function showAlternates() {{
    clearAlternates();
    if (!flightDest || detent !== 'collapsed') return;
    const W = map.getContainer().clientWidth, H = map.getContainer().clientHeight;
    const placed = [ map.project(SF), map.project([flightDest.lng, flightDest.lat]) ];   // don't crowd the two ends
    for (const [code,lat,lng] of AIRPORTS) {{
      if (code === flightDest.code) continue;
      const p = map.project([lng, lat]);
      if (p.x < 40 || p.x > W - 40 || p.y < 64 || p.y > H - 168) continue;               // on-screen, above the sheet
      if (placed.some(q => Math.hypot(q.x - p.x, q.y - p.y) < 104)) continue;            // keep pills from overlapping
      placed.push(p);
      const el = pricePillEl(code, lng, lat, false);
      el.addEventListener('click', ev => {{ ev.stopPropagation(); retarget(code, lng, lat); }});
      const m = new maplibregl.Marker({{ element: el, anchor: 'left', occludedOpacity: 0 }}).setLngLat([lng, lat]).addTo(map);
      el.style.zIndex = '5'; flightAirportMarkers.push(m);
      if (flightAirportMarkers.length >= 6) break;
    }}
  }}

  // ---- set / switch destination ----
  function setDest(code, lng, lat) {{
    flightDest = {{ code, lng, lat }};
    const city = airName(code, lng, lat);
    flightInfo = {{ t1: 'San Francisco → ' + city, t2: 'SFO–' + code + ' · from $' + bestPrice(code, lng, lat) }};
    setRoute(null);                                                            // new destination starts as a direct arch
    if (flightEndMarker) flightEndMarker.remove();
    const el = pricePillEl(code, lng, lat, true);                              // destination = the active price pill
    flightEndMarker = new maplibregl.Marker({{ element: el, anchor:'left', occludedOpacity:0 }}).setLngLat([lng,lat]).addTo(map);
    flightEndMarker.getElement().style.zIndex = '6';
    renderFlights(code, lng, lat); updateSearchBar(); drawArc();
  }}
  function retarget(code, lng, lat) {{ setDest(code, lng, lat); frameFlight(800); if (detent === 'collapsed') map.once('moveend', showAlternates); }}

  function openFlight(code, lng, lat) {{
    if (flightMode) return;
    flightMode = true; userTouched = true; introFlight = false;
    preFlight = {{ c:[map.getCenter().lng, map.getCenter().lat], z: map.getZoom() }};
    clearMarkers();
    for (const m of airportMarkers) m.getElement().style.display = 'none';
    SCREEN.classList.remove('airports-visible');
    SCREEN.querySelector('.cards-scroll').style.display = 'none';
    document.querySelectorAll('.dock-btn').forEach(d => d.style.display = 'none');
    fpill.classList.add('flight');
    detent = 'expanded'; setSheet(0);
    setDest(code, lng, lat);
    frameFlight(1100);
  }}
  function closeFlight() {{
    if (!flightMode) return;
    flightMode = false; flightDest = null; sheetTY = 0; detent = 'expanded';
    clearAlternates(); setRoute(null);
    arcSvg.style.display = 'none'; arcTime.style.display = 'none';
    if (flightEndMarker) {{ flightEndMarker.remove(); flightEndMarker = null; }}
    fsheet.style.transform = 'translateY(108%)';
    fpill.style.top = '730px'; setTimeout(() => fpill.classList.remove('flight'), 540);
    SCREEN.querySelector('.cards-scroll').style.display = '';
    document.querySelectorAll('.dock-btn').forEach(d => d.style.display = '');
    updateSearchBar();
    if (preFlight) map.easeTo({{ center: preFlight.c, zoom: preFlight.z, duration: 900, essential:true }});
    preFlight = null;
  }}
  updateSearchBar();

  document.querySelectorAll('.dock-btn').forEach(b => {{
    b.addEventListener('click', () => {{
      document.querySelectorAll('.dock-btn').forEach(x => x.classList.remove('on'));
      b.classList.add('on');
      mode = b.dataset.mode;
      viewStack = []; metro = false;     // switching modes returns to the top level
      if (mode === 'air') {{
        // flights re-frames to the wider country view (US / lower Canada / upper Mexico)
        currentSpots = airSpots(activeVibe);
        clearMarkers();
        map.easeTo({{ center: SF, zoom: 3.0, offset: [0, 32], duration: 1100,
          easing: t => 1 - Math.pow(1 - t, 3), essential: true }});
      }} else {{
        render();
      }}
    }});
  }});

  // ---------- cinematic intro ----------
  let userTouched = false;
  function stopIntro() {{ userTouched = true; introFlight = false; suppressLayout = false; }}
  ['pointerdown','wheel','touchstart'].forEach(ev =>
    document.addEventListener(ev, stopIntro, {{ capture:true }}));

  // relaxing spots across Canada / USA / Mexico pop into existence one after another
  function introPopIn() {{
    clearMarkers();
    const groups = buildGroups(visibleAir());
    groups.forEach((g, i) => {{
      const o = g.type === 'cluster' ? makeCluster(g) : makePoint(g.s);
      const pop = o.m.getElement().querySelector('.mk-pop');
      if (pop) pop.style.animationDelay = (i * 95) + 'ms';
      markerMap.set(g.id, o);
    }});
    refreshMarkers();
    applyRails();
  }}

  const FAR = [88, 8];   // start on the far side of the world (S. Asia / Indian Ocean)
  let started = false;
  function start() {{
    if (started) return; started = true;
    map.resize();
    const relaxCard = document.querySelector('.cat[data-id="relax"]');
    if (relaxCard) relaxCard.classList.add('active');
    activeVibe = 'relax';
    map.jumpTo({{ center: FAR, zoom: 1.5 }});
    render(true);            // load relax spots; world icons read as call-outs as we travel
    updateLoc();
    if (userTouched) return;

    // One fluid motion: a speedy eastward sweep across the Pacific that eases slower as the
    // avatar comes to the middle, the zoom blending in toward the end to stop on North America —
    // US, lower Canada and upper Mexico. No seam between the travel and the zoom.
    introFlight = true;
    const LNG0 = FAR[0], LNG1 = SF[0] + 360;   // 88° -> 238° (=122°W): the Pacific route
    const LAT0 = FAR[1], LAT1 = SF[1];
    const Z0 = 1.5, Z1 = 3.0, DUR = 3200;
    const smooth = x => x*x*(3 - 2*x);          // smoothstep, C1-continuous (no velocity jumps)
    let t0 = 0;
    function fly(ts) {{
      if (userTouched) return;
      if (!t0) t0 = ts;
      const p = Math.min(1, (ts - t0) / DUR);
      const e = 1 - Math.pow(1 - p, 3);                       // ease-out sweep: fast, then slowing
      const zp = smooth(Math.min(1, Math.max(0, (p - 0.40) / 0.60)));  // zoom holds, then blends in
      map.easeTo({{
        center: [LNG0 + (LNG1 - LNG0) * e, LAT0 + (LAT1 - LAT0) * e],
        zoom: Z0 + (Z1 - Z0) * zp,
        offset: [0, 32 * zp],                                 // avatar settles to centre as it lands
        duration: 0
      }});
      if (p < 1) requestAnimationFrame(fly);
      else {{ introFlight = false; if (!userTouched) introPopIn(); }}   // relaxing spots pop in, one by one
    }}
    requestAnimationFrame(fly);
  }}
  map.on('load', start);
  setTimeout(start, 400);
</script>
</body>
</html>"""

open('/mnt/user-data/outputs/trip-creator-mobile.html', 'w').write(html)
print('written', len(html), 'bytes,', len(CATS), 'categories')

# ---- iPhone full-screen build: installs to the Home Screen as a standalone app ----
# A fixed 402-wide viewport lets the browser scale the whole UI to the device width while
# keeping touch coordinates in the same 402-space the layout (and MapLibre) expect — so it's
# crisp and gestures land correctly, with no JS scaling hacks.
META = (
  '<meta name="viewport" content="width=402, viewport-fit=cover, user-scalable=no, maximum-scale=1">\n'
  '<meta name="apple-mobile-web-app-capable" content="yes">\n'
  '<meta name="mobile-web-app-capable" content="yes">\n'
  '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'
  '<meta name="apple-mobile-web-app-title" content="Trips">\n'
  '<meta name="theme-color" content="#AADAFF">'
)
IOS_CSS = (
  '<style id="ios-fullscreen">\n'
  '  html,body{ height:100%; margin:0; overflow:hidden; background:#000; overscroll-behavior:none; }\n'
  '  *{ -webkit-tap-highlight-color:transparent; -webkit-touch-callout:none; -webkit-user-select:none; user-select:none; }\n'
  '  body{ align-items:flex-start; }\n'
  '  .stage{ transform:none !important; }\n'
  '  .screen{ border-radius:0 !important; box-shadow:none !important; }\n'
  '  .status{ display:none !important; }\n'
  '</style>\n'
)
device = html.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">', META)
device = device.replace('</head>', IOS_CSS + '</head>')
open('/mnt/user-data/outputs/trip-creator-iphone.html', 'w').write(device)
print('written iphone build', len(device), 'bytes')
