#!/usr/bin/env python3
"""Draw the LinkedIn banner (1584x396) in the profile's style, light and dark.

python3 scripts/linkedin_banner.py  ->  linkedin/banner-*.svg, linkedin/featured-*.svg
Then export to PNG (see linkedin/README.md).
The left ~460px stay calm: LinkedIn puts the profile photo there.
"""
import build_profile as bp

W, H = 1584, 396


def banner(t, mode):
    b = [f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>', bp.dot_grid(W, H, t["grid"], 26)]
    x = 520
    b.append(f'<rect x="{x}" y="70" width="150" height="34" rx="6" fill="{t["pink"]}"/>')
    b.append(bp.text(x + 75, 93, "▶ PRESS START", 15, "#FFFFFF", bp.MONO, 700, "middle"))
    b.append(bp.text(x, 170, "When EdTech meets AI.", 56, t["ink"], bp.SANS, 800))
    b.append(bp.text(x, 218, "Founder of Skillxtube & Skillxgames", 28, t["violet"], bp.SANS, 700))
    b.append(bp.text(x, 258, "Learning designer · AI product builder · small games for sharp minds", 20, t["muted"]))
    b.append(f'<rect x="{x}" y="290" width="520" height="10" rx="5" fill="{t["line"]}"/>')
    b.append(f'<rect x="{x}" y="290" width="370" height="10" rx="5" fill="{t["mint"]}"/>')
    b.append(bp.text(x, 330, "skillxtube.com · skillxgames.com · angelinepoitout.com", 15, t["muted"], bp.MONO, 700, extra='letter-spacing="1"'))
    for (sx, sy), c in zip([(1250, 80), (1520, 60), (1500, 320), (1230, 300)],
                           [t["yellow"], t["pink"], t["violet"], t["mint"]]):
        b.append(f'<rect x="{sx}" y="{sy}" width="14" height="14" fill="{c}"/>')
    b.append(bp.mascot(1290, 30, 340))
    out = bp.ROOT / "linkedin" / f"banner-{mode}.svg"
    out.write_text(bp.svg(W, H, "".join(b), "LinkedIn banner"), encoding="utf-8")


# ---------------------------------------------------------------- featured cards
FW, FH = 1200, 627  # LinkedIn "Featured" thumbnail ratio (1.91:1)
FEATURED = [
    ("skillxgames", "pink", "Skillxgames", "Retro arcade edutainment",
     ["299 small games for sharp minds", "A community, a feed, records for everything",
      "Adopt a pixel dragon, keep it alive by learning"], "skillxgames.com"),
    ("skillxtube", "violet", "Skillxtube", "AI-powered learning ecosystem",
     ["Turns online content into structured learning paths", "Built for the international EdTech market",
      "LLMs + agents + solid instructional design"], "skillxtube.com"),
    ("consulting", "mint", "Learning Design", "Freelance consulting",
     ["Instructional design & curriculum development", "Assessment strategy & learning experiences",
      "EdTech & AI product consulting"], "angelinepoitout.com"),
]


def featured(t, mode):
    for slug, acc, name, tag, bullets, url in FEATURED:
        a = t[acc]
        b = [f'<rect width="{FW}" height="{FH}" fill="{t["bg"]}"/>', bp.dot_grid(FW, FH, t["grid"], 26)]
        b.append(f'<rect x="0" y="0" width="{FW}" height="14" fill="{a}"/>')
        x = 70
        b.append(f'<rect x="{x}" y="80" width="150" height="34" rx="6" fill="{a}"/>')
        b.append(bp.text(x + 75, 103, "▶ PRESS START", 15, "#FFFFFF", bp.MONO, 700, "middle"))
        b.append(bp.text(x, 205, name, 76, t["ink"], bp.SANS, 800))
        b.append(bp.text(x, 258, tag, 32, a, bp.SANS, 700))
        for i, s in enumerate(bullets):
            y = 330 + i * 50
            b.append(f'<rect x="{x}" y="{y - 16}" width="14" height="14" fill="{a}"/>')
            b.append(bp.text(x + 30, y - 2, s, 25, t["ink"]))
        b.append(bp.text(x, 545, url + "  →", 22, t["muted"], bp.MONO, 700, extra='letter-spacing="1"'))
        b.append(bp.mascot(880, 200, 360))
        out = bp.ROOT / "linkedin" / f"featured-{slug}-{mode}.svg"
        out.write_text(bp.svg(FW, FH, "".join(b), f"{name}: {tag}"), encoding="utf-8")


if __name__ == "__main__":
    for mode, t in bp.THEMES.items():
        banner(t, mode)
        featured(t, mode)
