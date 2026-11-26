#!/usr/bin/env python3
"""Draw the LinkedIn banner (1584x396) in the profile's style, light and dark.

python3 scripts/linkedin_banner.py  ->  linkedin/banner-{light,dark}.svg
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


if __name__ == "__main__":
    for mode, t in bp.THEMES.items():
        banner(t, mode)
