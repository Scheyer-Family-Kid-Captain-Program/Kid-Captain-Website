import calendar
import json
from datetime import date
from flask import Flask, render_template_string, request

app = Flask(__name__)
app.secret_key = "sfkcp-secret"

# ── DATA ──────────────────────────────────────────────────────────────────────

events = [
    {"id": 1, "title": "Hospital Playroom Session", "date": "2026-05-04",
     "time": "10:00 AM", "location": "Duke Children's Hospital – Playroom",
     "description": "Volunteer-led craft and play session for pediatric patients.", "spots": 6, "signups": []},
    {"id": 2, "title": "Cameron Indoor Field Day", "date": "2026-05-17",
     "time": "2:00 PM", "location": "Cameron Indoor Stadium",
     "description": "Basketball shoot-around and outdoor activities for kids and families.", "spots": 20, "signups": []},
    {"id": 3, "title": "Duke Athletics Hospital Visit", "date": "2026-05-23",
     "time": "11:00 AM", "location": "Duke Children's Hospital",
     "description": "Duke student athletes visit hospital floors to spend time with patients.", "spots": 10, "signups": []},
    {"id": 4, "title": "Kid Captain Orientation", "date": "2026-05-30",
     "time": "9:00 AM", "location": "Cameron Indoor Stadium",
     "description": "Orientation for newly selected Kid Captains and their families ahead of the season.", "spots": 15, "signups": []},
]

partners = [
    {"name": "Duke Athletics",             "type": "University Athletics", "icon": "🏟️",
     "focus": "Duke student athletes across all sports participate in hospital visits and community events",
     "contact": "goduke.com"},
    {"name": "K-Ville",                    "type": "Duke Tradition",       "icon": "⛺",
     "focus": "Cameron Crazies tenting community supporting Kid Captains at Duke Basketball home games",
     "contact": "duke.edu/kville"},
    {"name": "Durham Partnership for Service", "type": "Community Service", "icon": "🌱",
     "focus": "Connecting Durham volunteers and organizations to meaningful service opportunities",
     "contact": "durhampartnership.org"},
    {"name": "Doers for Good",            "type": "Local Nonprofit",    "icon": "🤝",
     "focus": "Youth development and community service across Durham",       "contact": "doersforgood.org"},
    {"name": "Emily K Center",             "type": "Youth Development",  "icon": "📚",
     "focus": "Academic support and leadership for Durham youth",             "contact": "emilykcenter.org"},
    {"name": "Boys & Girls Club of Durham","type": "Youth Organization", "icon": "🏀",
     "focus": "After-school programming and mentorship for Durham kids",      "contact": "bgcdurham.org"},
    {"name": "Durham YMCA",                "type": "Community Center",   "icon": "🏃",
     "focus": "Recreation, health, and youth programming across Durham",      "contact": "durhamymca.org"},
]

donations = []
contacts   = []

# ── STATIC CSS ────────────────────────────────────────────────────────────────
HTML_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Scheyer Family Kid Captain Program</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*,*::before,*::after { box-sizing:border-box; margin:0; padding:0 }
:root {
  --blue:#003087; --navy:#001347; --royal:#0f44c0;
  --gold:#C8AA6E; --gold-dk:#9e7e3c;
  --bg:#f4f5f9; --surface:#fff; --border:#dde3f0;
  --text:#0c1020; --muted:#5a6278;
  --sh:0 2px 14px rgba(0,40,130,.09);
  --sh-lg:0 8px 36px rgba(0,40,130,.15);
  --r:13px;
}
html { scroll-behavior:smooth }
body { font-family:'Inter',Arial,sans-serif; background:var(--bg); color:var(--text); min-height:100vh }

/* ── HEADER ── */
.header {
  background:linear-gradient(108deg,var(--navy) 0%,var(--blue) 52%,#0a3db8 100%);
  border-bottom:3px solid var(--gold);
  position:sticky; top:0; z-index:200;
  box-shadow:0 2px 18px rgba(0,20,100,.28);
}
.header-inner {
  max-width:1140px; margin:0 auto; padding:0 24px;
  display:flex; align-items:center; justify-content:space-between; gap:16px; min-height:70px;
}
.brand { display:flex; align-items:center; gap:14px; text-decoration:none }
.brand-logos { display:flex; align-items:center; gap:8px }
.brand-text { color:#fff }
.brand-name { font-family:'Oswald',sans-serif; font-size:1.05rem; font-weight:600; letter-spacing:.02em; line-height:1.2 }
.brand-sub  { font-size:.67rem; opacity:.68; letter-spacing:.1em; text-transform:uppercase; margin-top:2px }
nav { display:flex; gap:2px; flex-wrap:wrap }
nav a {
  color:rgba(255,255,255,.82); text-decoration:none;
  padding:7px 12px; border-radius:7px;
  font-size:.78rem; font-weight:600; letter-spacing:.055em; text-transform:uppercase;
  transition:all .17s;
}
nav a:hover, nav a.active { background:var(--gold); color:var(--navy) }

/* ── PAGE ── */
.page { max-width:1140px; margin:0 auto; padding:0 24px 90px }

/* ── HERO ── */
.hero {
  display:flex; align-items:center; gap:48px;
  background:linear-gradient(115deg,var(--navy) 0%,var(--blue) 60%,#1040b8 100%);
  border-radius:0 0 32px 32px; padding:64px 56px 72px;
  color:#fff; margin-bottom:0;
  border-bottom:5px solid var(--gold); box-shadow:var(--sh-lg);
  position:relative; overflow:hidden;
}
.hero::before {
  content:''; position:absolute; right:-120px; top:-120px;
  width:420px; height:420px; border-radius:50%;
  background:rgba(255,255,255,.04); pointer-events:none;
}
.hero-text { flex:1; min-width:0; position:relative }
.hero-eyebrow {
  font-size:.75rem; font-weight:600; letter-spacing:.18em; text-transform:uppercase;
  color:var(--gold); margin-bottom:14px;
}
.hero h1 {
  font-family:'Oswald',sans-serif; font-size:3rem; font-weight:700;
  line-height:1.08; margin-bottom:16px;
}
.hero-tagline {
  font-size:1.08rem; opacity:.88; line-height:1.65; max-width:500px; margin-bottom:32px;
  font-style:italic;
}
.hero-btns { display:flex; gap:12px; flex-wrap:wrap }
.hero-logo {
  flex-shrink:0; width:200px; height:200px;
  border-radius:50%; overflow:hidden;
  box-shadow:0 0 0 6px rgba(200,170,110,.35), 0 12px 40px rgba(0,0,0,.35);
  position:relative;
}
.hero-logo img { width:100%; height:100%; object-fit:cover }
@media(max-width:720px) { .hero { flex-direction:column; padding:44px 28px 52px; text-align:center } .hero-logo { width:150px; height:150px } }

/* ── ABOUT BAND ── */
.about-band {
  background:#fff; border-bottom:1px solid var(--border);
  padding:64px 0;
}
.about-inner {
  max-width:1140px; margin:0 auto; padding:0 24px;
  display:grid; grid-template-columns:1fr 1fr; gap:56px; align-items:center;
}
@media(max-width:700px) { .about-inner { grid-template-columns:1fr; gap:32px } }
.about-inner h2 {
  font-family:'Oswald',sans-serif; font-size:2rem; font-weight:700;
  color:var(--blue); margin-bottom:16px;
  border-left:5px solid var(--gold); padding-left:14px;
}
.about-inner p { color:var(--muted); line-height:1.75; font-size:.97rem; margin-bottom:14px }
.about-inner p:last-child { margin-bottom:0 }
.about-highlights { list-style:none; margin-top:10px }
.about-highlights li {
  display:flex; align-items:flex-start; gap:12px;
  color:var(--text); font-size:.93rem; margin-bottom:13px; line-height:1.5;
}
.about-highlights li .dot {
  width:10px; height:10px; border-radius:50%; background:var(--gold);
  margin-top:5px; flex-shrink:0;
}

/* ── PAGE CONTENT ── */
.page-content { padding-top:40px }

/* ── STATS ── */
.stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(138px,1fr)); gap:14px; margin-bottom:36px }
.stat-card {
  background:var(--blue); color:#fff; border-radius:var(--r);
  padding:22px 18px; border-bottom:4px solid var(--gold); box-shadow:var(--sh);
}
.stat-card .n { font-family:'Oswald',sans-serif; font-size:2.2rem; font-weight:700 }
.stat-card .l { font-size:.69rem; opacity:.74; letter-spacing:.09em; text-transform:uppercase; margin-top:3px }

/* ── SECTION HEADING ── */
.sh-label {
  font-family:'Oswald',sans-serif; font-size:1.28rem; font-weight:700; color:var(--blue);
  border-left:5px solid var(--gold); padding-left:12px; margin-bottom:18px;
}

/* ── CARDS ── */
.card {
  background:var(--surface); border:1px solid var(--border);
  border-radius:var(--r); padding:22px 24px; margin-bottom:14px;
  box-shadow:var(--sh); transition:box-shadow .2s, transform .2s;
}
.card:hover { box-shadow:var(--sh-lg); transform:translateY(-2px) }
.card h3 { font-family:'Oswald',sans-serif; color:var(--blue); font-size:1.1rem; font-weight:600; margin-bottom:5px }
.meta  { color:var(--muted); font-size:.83rem; margin-bottom:9px }
.badge {
  display:inline-block; background:var(--blue); color:#fff;
  border-radius:4px; padding:2px 9px; font-size:.73rem;
  font-weight:600; letter-spacing:.04em; margin-bottom:8px;
}

/* ── BUTTONS ── */
.btn {
  display:inline-block; background:var(--blue); color:#fff;
  border:none; padding:11px 24px; border-radius:8px; cursor:pointer;
  font-size:.88rem; font-weight:600; font-family:'Inter',sans-serif;
  letter-spacing:.03em; text-decoration:none; transition:background .18s, transform .15s;
}
.btn:hover { background:var(--navy); transform:translateY(-1px) }
.btn-gold { background:var(--gold); color:var(--navy) }
.btn-gold:hover { background:var(--gold-dk); color:#fff }
.btn-wht { background:rgba(255,255,255,.15); color:#fff; border:2px solid rgba(255,255,255,.6) }
.btn-wht:hover { background:rgba(255,255,255,.25) }
.btn-outline { background:transparent; color:var(--blue); border:2px solid var(--blue) }
.btn-outline:hover { background:var(--blue); color:#fff }
.btn-sm { padding:6px 14px; font-size:.8rem }

/* ── FORMS ── */
label { font-weight:600; font-size:.83rem; color:var(--blue); display:block; margin-bottom:4px }
input,select,textarea {
  width:100%; padding:10px 13px; margin-bottom:14px;
  border:1.5px solid var(--border); border-radius:8px;
  font-size:.93rem; font-family:'Inter',sans-serif;
  background:#fff; transition:border-color .18s, box-shadow .18s;
}
input:focus,select:focus,textarea:focus {
  outline:none; border-color:var(--blue); box-shadow:0 0 0 3px rgba(0,48,135,.11);
}
.form-row { display:grid; grid-template-columns:1fr 1fr; gap:22px }
@media(max-width:580px) { .form-row { grid-template-columns:1fr } }

/* ── ALERTS ── */
.alert { border-radius:9px; padding:13px 18px; margin-bottom:20px; font-size:.91rem }
.a-ok  { background:#e8f5e9; border:1.5px solid #a5d6a7; color:#1b5e20 }
.a-err { background:#ffebee; border:1.5px solid #ef9a9a; color:#b71c1c }

/* ── CALENDAR ── */
.cal-wrap { border-radius:var(--r); overflow:hidden; box-shadow:var(--sh-lg); margin-bottom:32px }
.cal-nav {
  display:flex; align-items:center; justify-content:space-between;
  background:var(--blue); color:#fff; padding:15px 22px;
}
.cal-nav a { color:var(--gold); text-decoration:none; font-size:1.35rem; font-weight:700; padding:0 6px; transition:color .15s }
.cal-nav a:hover { color:#fff }
.cal-month { font-family:'Oswald',sans-serif; font-size:1.15rem; font-weight:600; letter-spacing:.06em }
.cal-table { width:100%; border-collapse:collapse; background:#fff }
.cal-table thead th {
  background:var(--navy); color:var(--gold); padding:9px 0; text-align:center;
  font-family:'Oswald',sans-serif; font-size:.7rem; letter-spacing:.13em; text-transform:uppercase;
}
.cal-table td {
  border:1px solid var(--border); vertical-align:top;
  min-height:104px; padding:7px 8px 9px;
  cursor:pointer; transition:background .14s; width:calc(100% / 7);
}
.cal-table td:hover { background:#eef2ff }
.cal-table td.empty { background:#f4f5f9; cursor:default }
.cal-table td.empty:hover { background:#f4f5f9 }
.cal-table td.has-ev { background:#f6f8ff }
.day-num {
  font-weight:600; font-size:.88rem; color:var(--blue); margin-bottom:5px;
  width:28px; height:28px; display:flex; align-items:center; justify-content:center; border-radius:50%;
}
.cal-table td.today .day-num { background:var(--gold); color:var(--navy); font-weight:700 }
.ev-pill {
  display:block; background:var(--blue); color:#fff;
  border-radius:4px; padding:2px 6px; font-size:.69rem; font-weight:600;
  margin-bottom:3px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; pointer-events:none;
}
.cal-table td.has-ev:hover .ev-pill { background:var(--gold); color:var(--navy) }

/* ── DAY MODAL ── */
.overlay {
  display:none; position:fixed; inset:0; z-index:300;
  background:rgba(0,14,60,.52); backdrop-filter:blur(4px);
  align-items:flex-end; justify-content:center;
}
.overlay.open { display:flex }
.day-modal {
  background:#fff; border-radius:20px 20px 0 0;
  width:100%; max-width:640px; max-height:84vh; overflow-y:auto;
  padding:28px 30px 48px; animation:slideUp .27s cubic-bezier(.18,.82,.28,1);
}
@keyframes slideUp { from { transform:translateY(90px); opacity:0 } to { transform:translateY(0); opacity:1 } }
.modal-hd {
  display:flex; align-items:center; justify-content:space-between;
  border-bottom:3px solid var(--gold); padding-bottom:12px; margin-bottom:20px;
}
.modal-date { font-family:'Oswald',sans-serif; font-size:1.22rem; font-weight:700; color:var(--blue) }
.modal-x {
  background:none; border:none; font-size:1.35rem; cursor:pointer;
  color:var(--muted); padding:4px 8px; border-radius:7px; transition:all .15s; line-height:1;
}
.modal-x:hover { color:var(--blue); background:#eef2ff }
.modal-ev {
  border:1.5px solid var(--border); border-radius:11px; padding:16px 18px;
  margin-bottom:12px; border-left:5px solid var(--blue); transition:box-shadow .15s;
}
.modal-ev:hover { box-shadow:var(--sh) }
.modal-ev h4 { font-family:'Oswald',sans-serif; color:var(--blue); font-size:1rem; margin-bottom:4px }
.no-ev { color:var(--muted); text-align:center; padding:38px 0; font-size:.93rem }

/* ── PARTNER GRID ── */
.p-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(224px,1fr)); gap:16px }
.p-card {
  background:var(--surface); border:1px solid var(--border); border-radius:var(--r);
  padding:26px 20px; border-top:5px solid var(--blue);
  box-shadow:var(--sh); transition:box-shadow .2s, transform .2s;
}
.p-card:hover { box-shadow:var(--sh-lg); transform:translateY(-2px) }
.p-card .icon { font-size:2.1rem; margin-bottom:10px }
.p-card h3 { font-family:'Oswald',sans-serif; color:var(--blue); font-size:1rem; font-weight:600; margin-bottom:5px }
.p-card p  { font-size:.83rem; color:var(--muted); margin-bottom:9px; line-height:1.5 }
.p-card .site { font-size:.77rem; color:var(--royal) }

/* ── DONATION TIERS ── */
.tier-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(172px,1fr)); gap:14px; margin-bottom:22px }
.tier {
  border:2px solid var(--border); border-radius:var(--r); padding:22px 14px;
  text-align:center; cursor:pointer; background:var(--surface); transition:all .2s;
}
.tier:hover,.tier.sel { border-color:var(--blue); background:#eef2ff; box-shadow:0 0 0 3px rgba(0,48,135,.10) }
.tier.featured { border-color:var(--gold); background:#fffdf4 }
.tier.featured:hover,.tier.featured.sel { box-shadow:0 0 0 3px rgba(200,170,110,.22) }
.tier .amt  { font-family:'Oswald',sans-serif; font-size:1.9rem; font-weight:700; color:var(--blue) }
.tier .perks { font-size:.77rem; color:var(--muted); margin-top:7px; line-height:1.45 }
.full-tag { color:#aaa; font-style:italic; font-size:.83rem }

/* ── PHOTO GALLERY ── */
.gallery-band {
  background:var(--navy); padding:56px 0 60px; border-bottom:4px solid var(--gold);
}
.gallery-inner {
  max-width:1140px; margin:0 auto; padding:0 24px;
}
.gallery-inner .sh-label {
  color:var(--gold); border-left-color:var(--gold); margin-bottom:24px;
}
.gallery-scroll {
  display:flex; gap:16px; overflow-x:auto; padding-bottom:8px;
  scrollbar-width:thin; scrollbar-color:var(--gold) rgba(255,255,255,.1);
}
.gallery-scroll::-webkit-scrollbar { height:5px }
.gallery-scroll::-webkit-scrollbar-track { background:rgba(255,255,255,.08); border-radius:4px }
.gallery-scroll::-webkit-scrollbar-thumb { background:var(--gold); border-radius:4px }
.g-item {
  flex:0 0 280px; border-radius:14px; overflow:hidden; position:relative;
  box-shadow:0 6px 28px rgba(0,0,0,.45);
}
.g-item img { width:100%; height:220px; object-fit:cover; display:block; transition:transform .35s }
.g-item:hover img { transform:scale(1.04) }
.g-caption {
  position:absolute; bottom:0; left:0; right:0;
  background:linear-gradient(transparent,rgba(0,19,71,.88));
  color:#fff; font-size:.78rem; font-weight:500; padding:22px 12px 12px;
  line-height:1.4;
}

/* ── CONTACT INFO BOX ── */
.contact-info {
  background:var(--blue); color:#fff; border-radius:var(--r);
  padding:32px 28px; border-bottom:4px solid var(--gold);
}
.contact-info h3 { font-family:'Oswald',sans-serif; font-size:1.25rem; font-weight:700; margin-bottom:18px }
.contact-row { display:flex; align-items:flex-start; gap:12px; margin-bottom:16px; font-size:.92rem; line-height:1.5 }
.contact-row .ci-icon { font-size:1.2rem; flex-shrink:0; margin-top:1px }
</style>
</head>
<body>
"""

HTML_FOOTER = "</div></body></html>"

# ── HEADER  (nav slots injected via .format()) ────────────────────────────────
_HEADER_TPL = """
<header class="header">
  <div class="header-inner">
    <a href="/" class="brand">
      <div class="brand-logos">
        <img src="/static/duke_logp.png" alt="Duke" style="height:46px;width:auto;border-radius:5px">
        <img src="/static/sheyer.avif"   alt="SFKCP" style="height:46px;width:auto;border-radius:50%">
      </div>
      <div class="brand-text">
        <div class="brand-name">Scheyer Family Kid Captain Program</div>
        <div class="brand-sub">Duke Athletics &middot; Durham Community</div>
      </div>
    </a>
    <nav>
      <a href="/"          {home}>Home</a>
      <a href="/events"    {events}>Calendar</a>
      <a href="/partners"  {partners}>Partners</a>
      <a href="/volunteer" {volunteer}>Volunteer</a>
      <a href="/donate"    {donate}>Donate</a>
      <a href="/contact"   {contact}>Contact</a>
    </nav>
  </div>
</header>
<div class="page">
"""

def make_nav(active=""):
    slots = {k: "" for k in ["home","events","partners","volunteer","donate","contact"]}
    if active in slots:
        slots[active] = 'class="active"'
    return _HEADER_TPL.format(**slots)


# ── CALENDAR MODAL JS  (__EVENTS_JSON__ replaced at request time) ─────────────
_MODAL_JS = """
<div class="overlay" id="day-modal" onclick="if(event.target===this)closeDay()">
  <div class="day-modal">
    <div class="modal-hd">
      <span class="modal-date" id="modal-title"></span>
      <button class="modal-x" onclick="closeDay()">&#10005;</button>
    </div>
    <div id="modal-body"></div>
  </div>
</div>
<script>
var SFKCP = __EVENTS_JSON__;
var byDate = {};
for (var i = 0; i < SFKCP.length; i++) {
  var e = SFKCP[i];
  if (!byDate[e.date]) byDate[e.date] = [];
  byDate[e.date].push(e);
}
function openDay(ds) {
  var evs = byDate[ds] || [];
  var d = new Date(ds + 'T12:00:00');
  document.getElementById('modal-title').textContent =
    d.toLocaleDateString('en-US', {weekday:'long', month:'long', day:'numeric', year:'numeric'});
  var html = '';
  if (evs.length === 0) {
    html = '<p class="no-ev">No events scheduled for this day.</p>';
  } else {
    for (var j = 0; j < evs.length; j++) {
      var ev = evs[j];
      var btn = ev.spots_left > 0
        ? '<a href="/signup/' + ev.id + '" class="btn btn-sm">Sign Up (' + ev.spots_left + ' left)</a>'
        : '<span class="full-tag">Event full</span>';
      html += '<div class="modal-ev"><h4>' + ev.title + '</h4>'
        + '<div class="meta">&#9201; ' + ev.time + ' &bull; &#128205; ' + ev.location + '</div>'
        + '<p style="font-size:.83rem;color:#5a6278;margin:7px 0 12px;">' + ev.description + '</p>'
        + btn + '</div>';
    }
  }
  document.getElementById('modal-body').innerHTML = html;
  document.getElementById('day-modal').classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeDay() {
  document.getElementById('day-modal').classList.remove('open');
  document.body.style.overflow = '';
}
</script>
"""

def make_modal_js():
    ev_list = [{"id": e["id"], "title": e["title"], "date": e["date"],
                "time": e["time"], "location": e["location"],
                "description": e["description"],
                "spots_left": e["spots"] - len(e["signups"])} for e in events]
    return _MODAL_JS.replace("__EVENTS_JSON__", json.dumps(ev_list))


# ── CALENDAR GRID ─────────────────────────────────────────────────────────────
def build_calendar(year, month):
    cal = calendar.Calendar(firstweekday=6)
    weeks = cal.monthdayscalendar(year, month)
    today = date.today()
    by_day = {}
    for e in events:
        d = date.fromisoformat(e["date"])
        if d.year == year and d.month == month:
            by_day.setdefault(d.day, []).append(e)

    pm = month - 1 if month > 1 else 12
    py = year  if month > 1 else year - 1
    nm = month + 1 if month < 12 else 1
    ny = year  if month < 12 else year + 1

    html = (f'<div class="cal-wrap">'
            f'<div class="cal-nav">'
            f'<a href="/events?y={py}&m={pm}">&#8592;</a>'
            f'<span class="cal-month">{date(year,month,1).strftime("%B %Y")}</span>'
            f'<a href="/events?y={ny}&m={nm}">&#8594;</a>'
            f'</div>'
            f'<table class="cal-table"><thead><tr>'
            f'<th>Sun</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th>'
            f'</tr></thead><tbody>')

    for week in weeks:
        html += "<tr>"
        for day in week:
            if day == 0:
                html += '<td class="empty"></td>'
            else:
                day_evs = by_day.get(day, [])
                is_today = (today == date(year, month, day))
                ds  = f"{year}-{month:02d}-{day:02d}"
                cls = ("today " if is_today else "") + ("has-ev" if day_evs else "")
                pills = "".join(
                    f'<span class="ev-pill">{e["title"][:20]}{"…" if len(e["title"])>20 else ""}</span>'
                    for e in day_evs)
                html += f'<td class="{cls.strip()}" onclick="openDay(\'{ds}\')">'
                html += f'<div class="day-num">{day}</div>{pills}</td>'
        html += "</tr>"

    html += "</tbody></table></div>"
    return html


# ── ROUTES ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    total_signups = sum(len(e["signups"]) for e in events)
    total_raised  = sum(d["amount"] for d in donations)

    # Hero + About live OUTSIDE .page so they can span full width
    pre_page = f"""
    <div class="hero">
      <div class="hero-text">
        <div class="hero-eyebrow">Duke Athletics &nbsp;&bull;&nbsp; Duke Children&rsquo;s Hospital</div>
        <h1>Scheyer Family<br>Kid Captain</h1>
        <p class="hero-tagline">&ldquo;Honoring the courage of the kids who inspire us all.&rdquo;</p>
        <div class="hero-btns">
          <a href="/events"   class="btn btn-gold">View Calendar</a>
          <a href="/donate"   class="btn btn-wht">Donate</a>
          <a href="/contact"  class="btn btn-wht">Contact Us</a>
        </div>
      </div>
      <div class="hero-logo">
        <img src="/static/sheyer.avif" alt="Scheyer Kid Captain Logo">
      </div>
    </div>

    <div class="about-band">
      <div class="about-inner">
        <div>
          <h2>About the Program</h2>
          <p>
            The Scheyer Family Kid Captain Program connects Duke Basketball with the incredible children
            at Duke Children&rsquo;s Hospital. Each season, select pediatric patients are honored as
            Kid Captains&nbsp;&mdash; brought to Cameron Indoor Stadium to be celebrated in front of
            thousands of Blue Devil fans.
          </p>
          <p>
            Beyond game day, we work to expand programming, grow community partnerships across Durham,
            and make every child in the hospital feel seen and supported.
          </p>
        </div>
        <div>
          <ul class="about-highlights">
            <li><span class="dot"></span>Kid Captains honored at Duke Basketball home games</li>
            <li><span class="dot"></span>Hospital visits from Duke student athletes across all sports</li>
            <li><span class="dot"></span>Weekly playroom sessions and activity programming</li>
            <li><span class="dot"></span>Partnership with Durham youth organizations</li>
            <li><span class="dot"></span>Summer camp and community field day events</li>
            <li><span class="dot"></span>Family engagement and long-term community connection</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="gallery-band">
      <div class="gallery-inner">
        <div class="sh-label">Kid Captain Moments</div>
        <div class="gallery-scroll">
          <div class="g-item">
            <img src="/static/skff2.jpeg" alt="Kid Captain with basketball">
            <div class="g-caption">A Kid Captain receives a signed basketball at Cameron Indoor</div>
          </div>
          <div class="g-item">
            <img src="/static/sfkk3.jpeg" alt="Kid Captain with Duke mascot">
            <div class="g-caption">Kid Captain celebrates on court with the Blue Devil mascot and cheerleaders</div>
          </div>
          <div class="g-item">
            <img src="/static/skff4.jpeg" alt="Kid Captain high-fiving Cameron Crazies">
            <div class="g-caption">High-fives from the Cameron Crazies — a moment kids never forget</div>
          </div>
          <div class="g-item">
            <img src="/static/skff5.webp" alt="Signed Duke basketball">
            <div class="g-caption">&ldquo;To Samantha — Dream Big! Go Duke!&rdquo; &mdash; Coach Scheyer</div>
          </div>
          <div class="g-item">
            <img src="/static/skff1.avif" alt="Kid Captain at Cameron">
            <div class="g-caption">Every game, a child is honored as our Kid Captain at Cameron Indoor Stadium</div>
          </div>
        </div>
      </div>
    </div>
    """

    content = f"""
    <div class="page-content">
      <div style="margin-bottom:36px;margin-top:36px">
        <div class="stats">
          <div class="stat-card"><div class="n">{len(events)}</div><div class="l">Upcoming Events</div></div>
          <div class="stat-card"><div class="n">{total_signups}</div><div class="l">Sign-Ups</div></div>
          <div class="stat-card"><div class="n">{len(partners)}</div><div class="l">Durham Partners</div></div>
          <div class="stat-card"><div class="n">${total_raised:,.0f}</div><div class="l">Raised</div></div>
        </div>
      </div>

      <div class="sh-label">Get Involved</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:14px;margin-bottom:0">
        <div class="card" style="border-top:4px solid var(--blue)">
          <h3>Event Calendar</h3>
          <p style="color:var(--muted);font-size:.88rem;margin:7px 0 14px;line-height:1.5">Browse and sign up for upcoming events. Click any date to see what&rsquo;s on.</p>
          <a href="/events" class="btn">Open Calendar</a>
        </div>
        <div class="card" style="border-top:4px solid var(--blue)">
          <h3>Durham Partners</h3>
          <p style="color:var(--muted);font-size:.88rem;margin:7px 0 14px;line-height:1.5">Meet the Durham community organizations we work with to reach more kids.</p>
          <a href="/partners" class="btn">View Partners</a>
        </div>
        <div class="card" style="border-top:4px solid var(--blue)">
          <h3>Volunteer</h3>
          <p style="color:var(--muted);font-size:.88rem;margin:7px 0 14px;line-height:1.5">Join our network of Duke students and Durham community volunteers.</p>
          <a href="/volunteer" class="btn">Sign Up</a>
        </div>
        <div class="card" style="border-top:4px solid var(--gold)">
          <h3>Donate</h3>
          <p style="color:var(--muted);font-size:.88rem;margin:7px 0 14px;line-height:1.5">Your support helps bring more kids to Cameron and funds hospital programming.</p>
          <a href="/donate" class="btn btn-gold">Give Now</a>
        </div>
      </div>
    </div>
    """

    # Hero and About live before the page wrapper; we close .page after content
    header_html = make_nav("home")
    # header ends with <div class="page"> — close it after content
    return render_template_string(
        HTML_HEAD + header_html + pre_page + content + HTML_FOOTER
    )


@app.route("/events")
def events_page():
    today = date.today()
    year  = int(request.args.get("y", today.year))
    month = int(request.args.get("m", today.month))

    cal_html   = build_calendar(year, month)
    modal_html = make_modal_js()

    list_html = ""
    for e in events:
        spots_left = e["spots"] - len(e["signups"])
        action = (f'<a href="/signup/{e["id"]}" class="btn">Sign Up ({spots_left} left)</a>'
                  if spots_left > 0 else '<span class="full-tag">Event full</span>')
        list_html += f"""
        <div class="card">
          <h3>{e["title"]}</h3>
          <div class="meta">&#128197; {e["date"]} &nbsp; &#9201; {e["time"]} &nbsp; &#128205; {e["location"]}</div>
          <p style="font-size:.88rem;color:var(--muted);margin-bottom:13px;line-height:1.55">{e["description"]}</p>
          {action}
        </div>"""

    content = f"""
    <div class="page-content">
      <div class="sh-label" style="margin-top:32px">Event Calendar</div>
      <p style="color:var(--muted);font-size:.88rem;margin-bottom:16px">Click any date to see events. Blue cells have scheduled events.</p>
      {cal_html}
      <div class="sh-label" style="margin-top:32px">Upcoming Events</div>
      {list_html}
      {modal_html}
    </div>
    """
    return render_template_string(HTML_HEAD + make_nav("events") + content + HTML_FOOTER)


@app.route("/signup/<int:event_id>", methods=["GET", "POST"])
def signup(event_id):
    event = next((e for e in events if e["id"] == event_id), None)
    if not event:
        return "Event not found", 404

    alert = ""
    if request.method == "POST":
        name  = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        role  = request.form.get("role", "").strip()
        if name and email:
            spots_left = event["spots"] - len(event["signups"])
            if spots_left > 0:
                event["signups"].append({"name": name, "email": email, "role": role})
                alert = f'<div class="alert a-ok">You&rsquo;re signed up for <strong>{event["title"]}</strong>! Confirmation would go to {email}.</div>'
            else:
                alert = '<div class="alert a-err">Sorry, this event is now full.</div>'

    content = f"""
    <div class="page-content">
      {alert}
      <div class="sh-label" style="margin-top:32px">Sign Up: {event["title"]}</div>
      <div class="card meta" style="margin-bottom:18px;border-left:5px solid var(--gold)">
        &#128197; {event["date"]} &nbsp; &#9201; {event["time"]} &nbsp; &#128205; {event["location"]}
      </div>
      <div class="card">
        <form method="POST">
          <div class="form-row">
            <div>
              <label>Full Name</label>
              <input name="name" required placeholder="Jane Smith">
              <label>Email</label>
              <input name="email" type="email" required placeholder="jane@duke.edu">
            </div>
            <div>
              <label>Role</label>
              <select name="role">
                <option>Volunteer</option>
                <option>Attendee / Family</option>
                <option>Duke Athlete</option>
                <option>Durham Community Partner</option>
              </select>
            </div>
          </div>
          <button class="btn" type="submit">Confirm Sign-Up</button>
        </form>
      </div>
      <a href="/events" style="color:var(--blue);font-weight:600;text-decoration:none">&#8592; Back to Calendar</a>
    </div>
    """
    return render_template_string(HTML_HEAD + make_nav("events") + content + HTML_FOOTER)


@app.route("/partners")
def partners_page():
    cards = "".join(f"""
    <div class="p-card">
      <div class="icon">{p["icon"]}</div>
      <h3>{p["name"]}</h3>
      <span class="badge">{p["type"]}</span>
      <p>{p["focus"]}</p>
      <div class="site">{p["contact"]}</div>
    </div>""" for p in partners)

    content = f"""
    <div class="page-content">
      <div class="sh-label" style="margin-top:32px">Durham Community Partners</div>
      <p style="color:var(--muted);margin-bottom:22px;font-size:.93rem;line-height:1.6">
        These organizations help us expand the Kid Captain program beyond the hospital and into the broader Durham community.
      </p>
      <div class="p-grid" style="margin-bottom:28px">{cards}</div>
      <div class="card" style="border-top:5px solid var(--gold)">
        <h3>Partner With Us</h3>
        <p style="color:var(--muted);font-size:.88rem;margin:8px 0 16px;line-height:1.55">
          Is your Durham organization interested in collaborating? We&rsquo;re looking for partners in youth development, recreation, and community health.
        </p>
        <a href="/contact" class="btn">Get In Touch</a>
      </div>
    </div>
    """
    return render_template_string(HTML_HEAD + make_nav("partners") + content + HTML_FOOTER)


@app.route("/volunteer", methods=["GET", "POST"])
def volunteer():
    alert = ""
    if request.method == "POST":
        name  = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        if name and email:
            alert = f'<div class="alert a-ok">Thanks, <strong>{name}</strong>! We&rsquo;ll reach out to {email} about volunteer opportunities and training sessions.</div>'

    content = f"""
    <div class="page-content">
      {alert}
      <div class="sh-label" style="margin-top:32px">Volunteer &amp; Partner Sign-Up</div>
      <p style="color:var(--muted);margin-bottom:22px;font-size:.93rem;line-height:1.6">
        Volunteers complete a 2-hour training (offered each semester) to work with patients at Duke Children&rsquo;s Hospital.
      </p>
      <div class="form-row" style="margin-bottom:0">
        <div class="card">
          <form method="POST">
            <label>Full Name</label>
            <input name="name" required placeholder="Jane Smith">
            <label>Email</label>
            <input name="email" type="email" required placeholder="jane@example.com">
            <label>Organization <span style="font-weight:400;color:var(--muted)">(optional)</span></label>
            <input name="org" placeholder="Duke, Boys &amp; Girls Club, YMCA&hellip;">
            <label>I&rsquo;m interested in&hellip;</label>
            <select name="interest">
              <option>Hospital volunteering (playroom, visits)</option>
              <option>Event support (field day, community events)</option>
              <option>Durham community partnership</option>
              <option>Fundraising / donations</option>
            </select>
            <button class="btn" type="submit">Submit Interest</button>
          </form>
        </div>
        <div>
          <div class="card" style="border-top:5px solid var(--gold);margin-bottom:14px">
            <h3>Training Schedule</h3>
            <p style="color:var(--muted);font-size:.87rem;margin-top:7px;line-height:1.55">
              2-hour orientation sessions run each semester (summer, fall, winter). Trained volunteers join Monday playroom sessions and special events.
            </p>
          </div>
          <div class="card" style="border-top:5px solid var(--blue)">
            <h3>Requirements</h3>
            <ul style="color:var(--muted);font-size:.87rem;padding-left:18px;margin-top:7px;line-height:2">
              <li>Current flu shot</li>
              <li>Completed 2-hr volunteer training</li>
              <li>Duke affiliation <em>or</em> partner organization</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    """
    return render_template_string(HTML_HEAD + make_nav("volunteer") + content + HTML_FOOTER)


@app.route("/donate", methods=["GET", "POST"])
def donate():
    alert = ""
    if request.method == "POST":
        name   = request.form.get("name", "").strip()
        email  = request.form.get("email", "").strip()
        amount = request.form.get("amount", "").strip()
        note   = request.form.get("note", "").strip()
        try:
            amt = float(amount)
            if name and email and amt > 0:
                donations.append({"name": name, "email": email, "amount": amt, "note": note})
                alert = f'<div class="alert a-ok">Thank you, <strong>{name}</strong>! Your pledge of <strong>${amt:,.2f}</strong> helps bring more kids to Cameron. We&rsquo;ll be in touch at {email}.</div>'
            else:
                alert = '<div class="alert a-err">Please fill in all fields with a valid amount.</div>'
        except ValueError:
            alert = '<div class="alert a-err">Please enter a valid donation amount.</div>'

    total_raised = sum(d["amount"] for d in donations)
    num_donors   = len(donations)

    tier_js = """<script>
function setAmt(v,el) {
  document.getElementById('amt').value = v;
  document.querySelectorAll('.tier').forEach(function(t) { t.classList.remove('sel'); });
  el.classList.add('sel');
}
</script>"""

    content = f"""
    <div class="page-content">
      {alert}
      <div class="sh-label" style="margin-top:32px">Support the Kid Captain Program</div>
      <p style="color:var(--muted);margin-bottom:24px;font-size:.93rem;line-height:1.6">
        Your donation brings more children to Cameron Indoor, funds hospital visits, and grows programming across Durham.
      </p>
      <div class="stats" style="margin-bottom:28px">
        <div class="stat-card"><div class="n">${total_raised:,.0f}</div><div class="l">Total Raised</div></div>
        <div class="stat-card"><div class="n">{num_donors}</div><div class="l">Donors</div></div>
      </div>
      <div class="sh-label" style="font-size:1.05rem">Choose an Amount</div>
      <div class="tier-grid">
        <div class="tier" onclick="setAmt(25,this)"><div class="amt">$25</div><div class="perks">Craft supplies for one playroom session</div></div>
        <div class="tier" onclick="setAmt(100,this)"><div class="amt">$100</div><div class="perks">Game-day tickets for one Kid Captain family</div></div>
        <div class="tier featured" onclick="setAmt(500,this)"><div class="amt">$500</div><div class="perks">&#11088; Sponsor a full hospital visit event</div></div>
        <div class="tier" onclick="setAmt(1000,this)"><div class="amt">$1,000</div><div class="perks">Fund a semester of playroom sessions</div></div>
      </div>
      <div class="card">
        <form method="POST">
          <div class="form-row">
            <div>
              <label>Full Name</label>
              <input name="name" required placeholder="Jane Smith">
              <label>Email</label>
              <input name="email" type="email" required placeholder="jane@example.com">
            </div>
            <div>
              <label>Donation Amount ($)</label>
              <input id="amt" name="amount" type="number" min="1" step="any" required placeholder="500">
              <label>Dedication / Note <span style="font-weight:400;color:var(--muted)">(optional)</span></label>
              <input name="note" placeholder="In honor of&hellip;">
            </div>
          </div>
          <button class="btn btn-gold" type="submit" style="padding:11px 30px;font-size:.95rem">Pledge Donation</button>
        </form>
      </div>
      {tier_js}
    </div>
    """
    return render_template_string(HTML_HEAD + make_nav("donate") + content + HTML_FOOTER)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    alert = ""
    if request.method == "POST":
        first = request.form.get("first", "").strip()
        last  = request.form.get("last",  "").strip()
        email = request.form.get("email", "").strip()
        if first and last and email:
            contacts.append({k: request.form.get(k, "").strip()
                             for k in ["first","last","email","phone","title","message"]})
            alert = f'<div class="alert a-ok">Thanks, <strong>{first}</strong>! We&rsquo;ve received your message and will be in touch at {email} soon.</div>'
        else:
            alert = '<div class="alert a-err">Please fill in your name and email.</div>'

    content = f"""
    <div class="page-content">
      {alert}
      <div class="sh-label" style="margin-top:32px">Contact Us</div>
      <p style="color:var(--muted);margin-bottom:24px;font-size:.93rem;line-height:1.6">
        Have a question about the program, want to get involved, or interested in partnering with us?
        We&rsquo;d love to hear from you.
      </p>

      <div class="form-row" style="align-items:start">
        <div class="card">
          <form method="POST">
            <div class="form-row" style="margin-bottom:0">
              <div>
                <label>First Name</label>
                <input name="first" required placeholder="Jane">
              </div>
              <div>
                <label>Last Name</label>
                <input name="last" required placeholder="Smith">
              </div>
            </div>
            <div class="form-row" style="margin-bottom:0">
              <div>
                <label>Email</label>
                <input name="email" type="email" required placeholder="jane@example.com">
              </div>
              <div>
                <label>Phone <span style="font-weight:400;color:var(--muted)">(optional)</span></label>
                <input name="phone" type="tel" placeholder="(919) 555-0100">
              </div>
            </div>
            <label>Title / Organization <span style="font-weight:400;color:var(--muted)">(optional)</span></label>
            <input name="title" placeholder="Student, Parent, Partner Organization&hellip;">
            <label>Message</label>
            <textarea name="message" rows="5" placeholder="How can we help?" style="resize:vertical"></textarea>
            <button class="btn" type="submit">Send Message</button>
          </form>
        </div>

        <div>
          <div class="contact-info" style="margin-bottom:14px">
            <h3>Get In Touch</h3>
            <div class="contact-row">
              <span class="ci-icon">&#9993;</span>
              <span>scheyerkidcaptain@gmail.com</span>
            </div>
            <div class="contact-row">
              <span class="ci-icon">&#128205;</span>
              <span>Duke Children&rsquo;s Hospital<br>Durham, North Carolina</span>
            </div>
            <div class="contact-row">
              <span class="ci-icon">&#128197;</span>
              <span>Volunteer trainings held each semester.<br>New volunteers always welcome.</span>
            </div>
          </div>
          <div class="card" style="border-top:5px solid var(--gold)">
            <h3>Quick Links</h3>
            <div style="display:flex;flex-direction:column;gap:8px;margin-top:10px">
              <a href="/volunteer" class="btn btn-outline" style="text-align:center">Volunteer Sign-Up</a>
              <a href="/donate"    class="btn btn-gold"    style="text-align:center">Donate</a>
            </div>
          </div>
        </div>
      </div>
    </div>
    """
    return render_template_string(HTML_HEAD + make_nav("contact") + content + HTML_FOOTER)


if __name__ == "__main__":
    app.run(debug=True)
