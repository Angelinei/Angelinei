#!/usr/bin/env python3
"""Draw every image of the GitHub profile README into assets/.

Static pieces (hero, badges, cards) are always redrawn. Live pieces
(stats card, contribution graph) use the GitHub GraphQL API when a token
is available in GH_TOKEN / GITHUB_TOKEN; without one, placeholders are drawn.

Run locally:   python3 scripts/build_profile.py
In CI:         see .github/workflows/profile.yml (runs every night)
"""
from __future__ import annotations

import datetime as dt
import base64
import json
import re
import textwrap
import xml.etree.ElementTree as ET
import os
import urllib.request
from html import escape
from pathlib import Path

LOGIN = os.environ.get("PROFILE_LOGIN", "Angelinei")
YT_HANDLE = "skillxgames"
YT_URL = f"https://www.youtube.com/@{YT_HANDLE}"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"

THEMES = {
    "light": {
        "bg": "#FFF8EF", "panel": "#FFFFFF", "ink": "#1B1433", "muted": "#6B6386",
        "line": "#EADFF5", "pink": "#E8368F", "mint": "#0FA37F", "violet": "#6C3CE0",
        "yellow": "#F2B705", "grid": "#F1E6DA",
        "heat": ["#EFE7F7", "#D7C2F4", "#B08BEE", "#8655E4", "#5B2BC9"],
    },
    "dark": {
        "bg": "#120E24", "panel": "#1B1533", "ink": "#F6F1FF", "muted": "#A79FC4",
        "line": "#2E2650", "pink": "#FF4FA3", "mint": "#3BE8B0", "violet": "#9C7BFF",
        "yellow": "#FFD23F", "grid": "#1D1736",
        "heat": ["#221B3D", "#3D2D78", "#6343B8", "#8F6BF0", "#C4AEFF"],
    },
}

def mascot(x, y, height):
    """Embed assets/mascot.png (GitHub won't load external images from an SVG)."""
    src = ROOT / "assets" / "mascot.png"
    data = base64.b64encode(src.read_bytes()).decode()
    width = round(height * 341 / 440)
    return (
        f'<ellipse cx="{x + width / 2:.0f}" cy="{y + height - 4}" rx="{width * 0.36:.0f}" ry="8" fill="#000" opacity="0.12"/>'
        f'<image x="{x}" y="{y}" width="{width}" height="{height}" href="data:image/png;base64,{data}"/>'
    )


def svg(w: int, h: int, body: str, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">'
        f"<title>{escape(title)}</title>{body}</svg>\n"
    )


def write(name: str, content: str) -> None:
    (OUT / name).write_text(content, encoding="utf-8")


def text(x, y, s, size, fill, family=SANS, weight=400, anchor="start", extra=""):
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{escape(s)}</text>'
    )


def dot_grid(w, h, color, step=24):
    return (
        f'<defs><pattern id="g" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
        f'<rect width="3" height="3" fill="{color}"/></pattern></defs>'
        f'<rect width="{w}" height="{h}" fill="url(#g)"/>'
    )


def frame(w, h, t, r=18):
    return (
        f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}" fill="{t["bg"]}" '
        f'stroke="{t["line"]}" stroke-width="2"/>'
    )


# ---------------------------------------------------------------- hero
def hero(t, mode):
    title = "Bonjour, I'm Angéline. Building learning products where EdTech meets AI."
    w, h = 1200, 380
    b = [frame(w, h, t, 24), dot_grid(w, h, t["grid"])]
    b.append(f'<rect x="60" y="64" width="150" height="34" rx="6" fill="{t["pink"]}"/>')
    b.append(text(135, 87, "▶ PRESS START", 15, "#FFFFFF", MONO, 700, "middle"))
    b.append(text(60, 170, "Bonjour, I'm Angéline.", 62, t["ink"], SANS, 800))
    b.append(text(60, 222, "When EdTech meets AI.", 30, t["violet"], SANS, 700))
    b.append(text(60, 270, "Founder of Skillxtube & Skillxgames · learning designer · AI product builder", 19, t["muted"]))
    # score bar
    b.append(f'<rect x="60" y="300" width="560" height="10" rx="5" fill="{t["line"]}"/>')
    b.append(f'<rect x="60" y="300" width="400" height="10" rx="5" fill="{t["mint"]}"/>')
    b.append(text(60, 340, "LVL 99 · LEARNING MODE: ON", 14, t["muted"], MONO, 700, extra='letter-spacing="2"'))
    b.append(mascot(880, 26, 330))
    for i, (x, y) in enumerate([(836, 120), (1120, 70), (1140, 280)]):
        c = [t["yellow"], t["pink"], t["violet"]][i]
        b.append(f'<rect x="{x}" y="{y}" width="12" height="12" fill="{c}"/>')
    write(f"hero-{mode}.svg", svg(w, h, "".join(b), title))

    # phone version
    w, h = 600, 520
    b = [frame(w, h, t, 22), dot_grid(w, h, t["grid"])]
    b.append(mascot(234, 24, 180))
    b.append(f'<rect x="40" y="226" width="150" height="34" rx="6" fill="{t["pink"]}"/>')
    b.append(text(115, 249, "▶ PRESS START", 15, "#FFFFFF", MONO, 700, "middle"))
    b.append(text(40, 320, "Bonjour,", 52, t["ink"], SANS, 800))
    b.append(text(40, 378, "I'm Angéline.", 52, t["ink"], SANS, 800))
    b.append(text(40, 422, "When EdTech meets AI.", 28, t["violet"], SANS, 700))
    b.append(text(40, 466, "Skillxtube · Skillxgames · learning design", 19, t["muted"]))
    write(f"hero-{mode}-mobile.svg", svg(w, h, "".join(b), title))


# ---------------------------------------------------------------- badges
BADGES = [
    ("website", "◆", "angelinepoitout.com"),
    ("linkedin", "in", "LinkedIn"),
    ("skillxtube", "★", "Skillxtube"),
    ("skillxgames", "◉", "Skillxgames"),
    ("youtube", "▶", "YouTube @skillxgames"),
]


def badges(t, mode):
    accents = [t["violet"], t["pink"], t["mint"], t["yellow"], "#FF0033"]
    for (slug, icon, label), acc in zip(BADGES, accents):
        w = 64 + int(len(label) * 9.6)
        h = 44
        b = [f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="22" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="2"/>']
        b.append(f'<circle cx="23" cy="22" r="14" fill="{acc}"/>')
        b.append(text(23, 27, icon, 13, "#FFFFFF" if acc != t["yellow"] else "#1B1433", SANS, 800, "middle"))
        b.append(text(46, 28, label, 16, t["ink"], SANS, 600))
        write(f"badge-{slug}-{mode}.svg", svg(w, h, "".join(b), label))


# ---------------------------------------------------------------- section labels
SECTIONS = {
    "building": "WHAT I'M BUILDING",
    "background": "BACKGROUND",
    "toolkit": "TOOLKIT",
    "activity": "PLAYER ACTIVITY",
    "videos": "LATEST VIDEOS",
}


def labels(t, mode):
    for slug, label in SECTIONS.items():
        w, h = 1200, 60
        b = [f'<rect x="0" y="22" width="14" height="14" fill="{t["pink"]}"/>']
        b.append(text(30, 37, label, 20, t["ink"], MONO, 800, extra='letter-spacing="4"'))
        lx = 30 + len(label) * 16.5 + 24
        b.append(f'<rect x="{lx:.0f}" y="28" width="{1200 - lx:.0f}" height="2" fill="{t["line"]}"/>')
        write(f"section-{slug}-{mode}.svg", svg(w, h, "".join(b), label))


# ---------------------------------------------------------------- whoami
def whoami(t, mode):
    lines = [
        ("$", "whoami", t["mint"]),
        (" ", "Angéline Poitout: founder, learning designer, AI product builder.", t["ink"]),
        (" ", "I turn online content into structured learning, and learning into games.", t["ink"]),
        ("$", "cat now.txt", t["mint"]),
        (" ", "→ Shipping Skillxgames: 299 small games for sharp minds.", t["ink"]),
        (" ", "→ Growing Skillxtube: AI-powered learning paths for the international EdTech market.", t["ink"]),
        ("$", "echo $MOTTO", t["mint"]),
        (" ", "Small games, sharp minds. Learning should feel like play.", t["pink"]),
    ]
    w, h = 1200, 90 + len(lines) * 34
    b = [f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="2"/>']
    for i, c in enumerate([t["pink"], t["yellow"], t["mint"]]):
        b.append(f'<circle cx="{34 + i * 24}" cy="32" r="7" fill="{c}"/>')
    b.append(text(w / 2, 37, "angeline@skillx: ~", 14, t["muted"], MONO, 600, "middle"))
    for i, (p, s, c) in enumerate(lines):
        y = 88 + i * 34
        b.append(text(34, y, p, 17, t["violet"], MONO, 700))
        b.append(text(58, y, s, 17, c, MONO, 700 if p == "$" else 400))
    write(f"whoami-{mode}.svg", svg(w, h, "".join(b), "whoami: Angéline Poitout, founder of Skillxtube and Skillxgames"))


# ---------------------------------------------------------------- project cards
PROJECTS = [
    ("skillxgames", "Skillxgames", "Retro arcade edutainment", [
        "299 small games for sharp minds",
        "A community, a feed, records for everything",
        "Adopt a pixel dragon, keep it alive by learning",
    ], ["299 GAMES", "ARCADE", "LIVE"], "pink"),
    ("skillxtube", "Skillxtube", "AI-powered learning ecosystem", [
        "Turns online content into learning paths",
        "Built for the international EdTech market",
        "LLMs + agents + solid instructional design",
    ], ["AI", "EDTECH", "LIVE"], "violet"),
]


def projects(t, mode):
    for slug, name, tag, bullets, chips, acc in PROJECTS:
        a = t[acc]
        w, h = 590, 330
        b = [f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="2"/>']
        b.append(f'<rect x="34" y="1" width="{w-68}" height="8" rx="4" fill="{a}"/>')
        b.append(text(34, 72, name, 36, t["ink"], SANS, 800))
        b.append(text(34, 104, tag, 18, a, SANS, 700))
        for i, s in enumerate(bullets):
            y = 152 + i * 36
            b.append(f'<rect x="34" y="{y - 12}" width="10" height="10" fill="{a}"/>')
            b.append(text(56, y - 2, s, 17, t["ink"]))
        x = 34
        for c in chips:
            cw = 26 + len(c) * 9
            b.append(f'<rect x="{x}" y="268" width="{cw}" height="30" rx="15" fill="none" stroke="{a}" stroke-width="2"/>')
            b.append(text(x + cw / 2, 288, c, 13, a, MONO, 700, "middle"))
            x += cw + 10
        b.append(text(w - 34, 288, "VISIT →", 14, t["muted"], MONO, 700, "end"))
        write(f"card-{slug}-{mode}.svg", svg(w, h, "".join(b), f"{name}: {tag}"))


# ---------------------------------------------------------------- background
BACKGROUND = [
    ("Founder & AI Product Builder", "Skillxtube", "AI-powered learning products for the international EdTech market."),
    ("Learning Consultant / Instructional Designer", "Freelance", "Learning design, curriculum development, assessment, EdTech consulting."),
    ("Digital Product & Communication", "EdTech · startups · institutions", "Digital products, content, marketing and project management."),
]


def background(t, mode):
    w, h = 1200, 60 + len(BACKGROUND) * 100
    b = [f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="2"/>']
    b.append(f'<rect x="52" y="50" width="4" height="{h - 100}" fill="{t["line"]}"/>')
    for i, (role, where, desc) in enumerate(BACKGROUND):
        y = 70 + i * 100
        c = [t["pink"], t["violet"], t["mint"]][i]
        b.append(f'<rect x="44" y="{y - 12}" width="20" height="20" fill="{c}"/>')
        b.append(text(90, y + 4, role, 22, t["ink"], SANS, 700))
        b.append(text(90, y + 34, where.upper(), 13, c, MONO, 700, extra='letter-spacing="2"'))
        b.append(text(90, y + 60, desc, 17, t["muted"]))
    write(f"background-{mode}.svg", svg(w, h, "".join(b), "Background"))


# ---------------------------------------------------------------- toolkit
TOOLS = ["Python", "JavaScript", "TypeScript", "React", "Next.js", "FastAPI",
         "Supabase", "APIs", "LLMs", "AI Agents", "Automation", "Learning Design"]


def toolkit(t, mode):
    w = 1200
    accents = [t["pink"], t["violet"], t["mint"], t["yellow"]]
    x, y, chips = 0, 0, []
    for i, tool in enumerate(TOOLS):
        cw = 44 + len(tool) * 10.5
        if x + cw > w:
            x, y = 0, y + 58
        a = accents[i % 4]
        chips.append(f'<rect x="{x + 1:.0f}" y="{y + 1}" width="{cw:.0f}" height="44" rx="10" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="2"/>')
        chips.append(f'<rect x="{x + 16:.0f}" y="{y + 17}" width="10" height="10" fill="{a}"/>')
        chips.append(text(x + 36, y + 28, tool, 16, t["ink"], MONO, 700))
        x += cw + 12
    write(f"toolkit-{mode}.svg", svg(w, y + 48, "".join(chips), "Toolkit: " + ", ".join(TOOLS)))


# ---------------------------------------------------------------- live data
def fetch_stats():
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        return None
    q = """query($login:String!){user(login:$login){
      followers{totalCount}
      repositories(ownerAffiliations:OWNER,privacy:PUBLIC,first:100){totalCount nodes{stargazerCount}}
      contributionsCollection{contributionCalendar{totalContributions
        weeks{contributionDays{date contributionCount}}}}}}"""
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": q, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if data.get("errors"):
        raise SystemExit(f"GraphQL error: {data['errors']}")
    u = data["data"]["user"]
    cal = u["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    return {
        "total": cal["totalContributions"],
        "days": days,
        "repos": u["repositories"]["totalCount"],
        "stars": sum(n["stargazerCount"] for n in u["repositories"]["nodes"]),
        "followers": u["followers"]["totalCount"],
    }


def streaks(days):
    counts = [d["contributionCount"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    cur, i = 0, len(counts) - 1
    if i >= 0 and counts[i] == 0:  # today not done yet: don't break the streak
        i -= 1
    while i >= 0 and counts[i]:
        cur, i = cur + 1, i - 1
    return cur, longest


def stats_card(t, mode, s):
    if s:
        cur, longest = streaks(s["days"])
        items = [(f'{s["total"]:,}', "CONTRIBUTIONS", "last 12 months"),
                 (f"{cur}", "DAY STREAK", f"best: {longest} days"),
                 (f'{s["repos"]}', "PUBLIC REPOS", f'{s["followers"]} followers'),
                 (f'{s["stars"]}', "STARS EARNED", "across my repos")]
        title = (f'{s["total"]} contributions in the last year, {cur}-day current streak, '
                 f'{longest}-day longest streak, {s["repos"]} public repos, {s["stars"]} stars')
    else:
        items = [("—", "CONTRIBUTIONS", "last 12 months"), ("—", "DAY STREAK", "best: —"),
                 ("—", "PUBLIC REPOS", "— followers"), ("—", "STARS EARNED", "across my repos")]
        title = "GitHub stats (refreshed nightly)"
    w, h = 1200, 190
    b = [f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="2"/>']
    accents = [t["pink"], t["mint"], t["violet"], t["yellow"]]
    cw = (w - 40) / 4
    for i, ((big, lab, sub), a) in enumerate(zip(items, accents)):
        x = 20 + i * cw
        if i:
            b.append(f'<rect x="{x:.0f}" y="40" width="2" height="110" fill="{t["line"]}"/>')
        cx = x + cw / 2
        b.append(text(cx, 92, big, 46, t["ink"], SANS, 800, "middle"))
        b.append(f'<rect x="{cx - 20:.0f}" y="106" width="40" height="5" fill="{a}"/>')
        b.append(text(cx, 136, lab, 14, a, MONO, 800, "middle", 'letter-spacing="2"'))
        b.append(text(cx, 160, sub, 14, t["muted"], SANS, 400, "middle"))
    write(f"stats-{mode}.svg", svg(w, h, "".join(b), title))


def heatmap(t, mode, s):
    w, h = 1200, 252
    cell, gap, x0, y0 = 17, 4, 58, 80
    b = [f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="2"/>']
    if s:
        days = s["days"]
        title = f'{s["total"]} contributions in the last year'
        b.append(text(30, 36, f'{s["total"]:,} contributions in the last year', 15, t["ink"], MONO, 700))
    else:
        today = dt.date.today()
        days = [{"date": (today - dt.timedelta(days=370 - i)).isoformat(), "contributionCount": 0} for i in range(371)]
        title = "Contribution graph (refreshed nightly)"
        b.append(text(30, 36, "Contribution graph · refreshed every night", 15, t["ink"], MONO, 700))
    days = days[-371:]
    first = dt.date.fromisoformat(days[0]["date"])
    offset = (first.weekday() + 1) % 7  # GitHub weeks start on Sunday
    mx = max([d["contributionCount"] for d in days] + [1])
    last_month = None
    for i, d in enumerate(days):
        k = i + offset
        col, row = k // 7, k % 7
        if col > 52:
            continue
        c = d["contributionCount"]
        lvl = 0 if c == 0 else min(4, 1 + int(3 * c / mx))
        x, y = x0 + col * (cell + gap), y0 + row * (cell + gap)
        b.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{t["heat"][lvl]}"/>')
        date = dt.date.fromisoformat(d["date"])
        if row == 0 and date.month != last_month and 1 < col < 51:
            last_month = date.month
            b.append(text(x, y0 - 10, date.strftime("%b").upper(), 11, t["muted"], MONO, 700))
    for r, lab in [(1, "MON"), (3, "WED"), (5, "FRI")]:
        b.append(text(x0 - 10, y0 + r * (cell + gap) + 13, lab, 11, t["muted"], MONO, 700, "end"))
    lx = w - 30 - 5 * (cell + gap) - 40
    b.append(text(lx - 10, 36, "LESS", 11, t["muted"], MONO, 700, "end"))
    for i, c in enumerate(t["heat"]):
        b.append(f'<rect x="{lx + i * (cell + gap)}" y="23" width="{cell}" height="{cell}" rx="3" fill="{c}"/>')
    b.append(text(lx + 5 * (cell + gap) + 4, 36, "MORE", 11, t["muted"], MONO, 700))
    write(f"activity-{mode}.svg", svg(w, h, "".join(b), title))


# ---------------------------------------------------------------- YouTube
VIDEO_CACHE = OUT / "videos.json"
UA = {"User-Agent": "Mozilla/5.0 (profile-readme bot)", "Accept-Language": "en"}


def get(url, timeout=30):
    req = urllib.request.Request(url, headers={**UA, "Cookie": "CONSENT=YES+1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def fetch_videos(n=3):
    """Latest uploads from the channel's public RSS feed, thumbnails inlined."""
    cid = os.environ.get("YT_CHANNEL_ID")
    if not cid:
        page = get(YT_URL).decode("utf-8", "replace")
        m = (re.search(r'"externalId":"(UC[\w-]{22})"', page)
             or re.search(r'channel_id=(UC[\w-]{22})', page)
             or re.search(r'"channelId":"(UC[\w-]{22})"', page))
        if not m:
            raise RuntimeError("channel id not found on " + YT_URL)
        cid = m.group(1)
    feed = ET.fromstring(get(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"))
    ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
    videos = []
    for e in feed.findall("a:entry", ns):
        vid = e.findtext("yt:videoId", namespaces=ns)
        link = e.find("a:link", ns).get("href", f"https://www.youtube.com/watch?v={vid}")
        if "/shorts/" in link:
            continue  # keep the long-form videos for the cards
        thumb = base64.b64encode(get(f"https://i.ytimg.com/vi/{vid}/mqdefault.jpg")).decode()
        videos.append({"id": vid, "title": e.findtext("a:title", namespaces=ns),
                       "date": e.findtext("a:published", namespaces=ns)[:10],
                       "url": link, "thumb": thumb})
        if len(videos) == n:
            break
    return videos


def load_videos():
    try:
        videos = fetch_videos()
        VIDEO_CACHE.write_text(json.dumps(videos), encoding="utf-8")
        return videos
    except Exception as e:  # YouTube hiccup: keep the last good set
        print(f"videos fetch failed ({e}); using cache")
        if VIDEO_CACHE.exists():
            return json.loads(VIDEO_CACHE.read_text(encoding="utf-8"))
        return []


def video_card(t, mode, i, v):
    w, h, pad = 380, 340, 16
    tw, th = w - 2 * pad, round((w - 2 * pad) * 9 / 16)
    accent = [t["pink"], t["violet"], t["mint"]][i % 3]
    b = [f'<defs><clipPath id="c"><rect x="{pad}" y="{pad}" width="{tw}" height="{th}" rx="12"/></clipPath></defs>',
         f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="{t["panel"]}" stroke="{t["line"]}" stroke-width="2"/>']
    if v:
        b.append(f'<image x="{pad}" y="{pad}" width="{tw}" height="{th}" preserveAspectRatio="xMidYMid slice" '
                 f'clip-path="url(#c)" href="data:image/jpeg;base64,{v["thumb"]}"/>')
        title = v["title"]
        meta = dt.date.fromisoformat(v["date"]).strftime("%d %b %Y").upper() + " · YOUTUBE"
    else:
        b.append(f'<rect x="{pad}" y="{pad}" width="{tw}" height="{th}" rx="12" fill="{t["bg"]}"/>')
        b.append(dot_grid(w, h, t["grid"]).replace('<rect width="380" height="340"',
                 f'<rect x="{pad}" y="{pad}" width="{tw}" height="{th}" clip-path="url(#c)"'))
        title = "New videos loading… subscribe to @skillxgames"
        meta = "YOUTUBE"
    # pixel play button
    px, py = pad + tw - 58, pad + th - 52
    b.append(f'<rect x="{px}" y="{py}" width="44" height="38" rx="8" fill="{accent}"/>')
    b.append(f'<path d="M{px+17} {py+10} L{px+30} {py+19} L{px+17} {py+28} Z" fill="#FFFFFF"/>')
    lines = textwrap.wrap(title, 30)[:2]
    if len(textwrap.wrap(title, 30)) > 2:
        lines[1] = lines[1][:28].rstrip() + "…"
    for k, line in enumerate(lines):
        b.append(text(pad + 4, pad + th + 38 + k * 26, line, 19, t["ink"], SANS, 700))
    b.append(f'<rect x="{pad + 4}" y="{h - 40}" width="10" height="10" fill="{accent}"/>')
    b.append(text(pad + 22, h - 31, meta, 12, t["muted"], MONO, 700, extra='letter-spacing="1"'))
    write(f"video-{i + 1}-{mode}.svg", svg(w, h, "".join(b), title))


def readme_videos(videos):
    """Rewrite the README block between the videos markers."""
    readme = ROOT / "README.md"
    if not readme.exists():
        return
    items = videos or [None]
    cells = []
    for i, v in enumerate(items):
        href = v["url"] if v else YT_URL
        alt = escape(v["title"] if v else "YouTube @skillxgames", quote=True)
        cells.append(
            f'<a href="{href}"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/video-{i + 1}-dark.svg">'
            f'<img src="assets/video-{i + 1}-light.svg" width="32%" alt="{alt}"></picture></a>')
    block = "<!-- videos:start -->\n<p align=\"center\">\n" + "\n".join(cells) + "\n</p>\n<!-- videos:end -->"
    s = readme.read_text(encoding="utf-8")
    s = re.sub(r"<!-- videos:start -->.*?<!-- videos:end -->", lambda _: block, s, flags=re.S)
    readme.write_text(s, encoding="utf-8")


def main():
    OUT.mkdir(exist_ok=True)
    try:
        stats = fetch_stats()
    except Exception as e:  # keep the previous images rather than failing the run
        if os.environ.get("CI"):
            raise
        print(f"stats fetch failed ({e}); drawing placeholders")
        stats = None
    videos = load_videos()
    for mode, t in THEMES.items():
        hero(t, mode)
        badges(t, mode)
        labels(t, mode)
        whoami(t, mode)
        projects(t, mode)
        background(t, mode)
        toolkit(t, mode)
        stats_card(t, mode, stats)
        heatmap(t, mode, stats)
        for i, v in enumerate(videos or [None]):
            video_card(t, mode, i, v)
    readme_videos(videos)
    print("live stats:" if stats else "no token: placeholders drawn", stats and stats["total"])


if __name__ == "__main__":
    main()
