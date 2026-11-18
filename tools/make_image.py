#!/usr/bin/env python3
"""Build entry.png for the make.fun news-image-20261118 bounty.

One 1024x1024 infographic summarising world news of Wednesday
18 November 2026. Deterministic: same input, same bytes every run
(PNG output of Pillow with fixed parameters).

Run:  python3 tools/make_image.py   (writes repo/entry.png)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")

# ---- palette ----
BG = (13, 22, 38)          # deep navy
BG2 = (18, 30, 52)         # slightly lighter navy (header band)
CARD = (24, 38, 62)        # card fill
CARD_EDGE = (52, 72, 104)  # card border
WHITE = (245, 247, 250)
MUTED = (196, 205, 218)    # summary text
GOLD = (212, 175, 55)
GOLD_DARK = (20, 16, 4)
RED = (226, 74, 74)
GREY = (150, 163, 180)

CAT_COLORS = {
    "DIPLOMACY": (212, 175, 55),    # gold
    "WAR": (226, 74, 74),           # red
    "MIDDLE EAST": (240, 140, 60),  # orange
    "TECH": (72, 180, 230),         # cyan-blue
    "UK / EUROPE": (178, 132, 235),# purple
    "TRADE": (88, 200, 120),        # green
    "ASIA": (64, 200, 190),         # teal
    "WEATHER": (120, 170, 245),     # light blue
}

NEWS = [
    ("DIPLOMACY", "Trump lands in Manila for Quad summit",
     "US President Donald Trump arrives in the Philippines for the first Quad "
     "meeting in two years, before meeting Xi Jinping."),
    ("WAR", "Ukraine damages Crimea Bridge; Russia hits Kyiv bridges",
     "A Ukrainian strike damages the Kerch Bridge roadway; Russia retaliates "
     "against two key bridges in Kyiv."),
    ("MIDDLE EAST", "Iran drones US radar site in Bahrain",
     "Iran fires drones at a US radar facility at Sheikh Isa Air Base, "
     "Bahrain; Kuwait intercepts drones."),
    ("TECH", "Nvidia rules out Huang return; Q3 revenue up 103%",
     "Nvidia's board will not consider Huang's return after his 12 Nov "
     "resignation; third-quarter revenue rises 103% year on year."),
    ("UK / EUROPE", "UK sanctions Israeli settlement firms",
     "London freezes assets and bans directors of eight settlement "
     "construction firms in the West Bank."),
    ("TRADE", "Canada\u2013China extend trade deal ahead of APEC",
     "PM Mark Carney meets Xi Jinping; the two countries extend their "
     "trade deal."),
    ("ASIA", "US presses UN body over Taiwan flight rules; China hits back",
     "A dispute at the UN agency over Taiwan flight rules."),
    ("WEATHER", "Cyclone Akvan strengthens in Bay of Bengal",
     "Cyclone Akvan heads for severe cyclonic storm status; warnings issued."),
]

SPORT = "MS Dhoni retires from the IPL, becomes Chennai Super Kings mentor"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap text, truncate with ellipsis if it exceeds max_lines."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    while lines and draw.textlength(lines[-1] + "\u2026", font=fnt) > max_w:
        lines[-1] = lines[-1].rsplit(" ", 1)[0] if " " in lines[-1] else lines[-1][:-1]
    lines[-1] = lines[-1] + "\u2026"
    return lines


def rounded(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # subtle vertical gradient band behind header
    for y in range(0, 158):
        t = y / 158.0
        r = int(BG2[0] + (BG[0] - BG2[0]) * t)
        g = int(BG2[1] + (BG[1] - BG2[1]) * t)
        b = int(BG2[2] + (BG[2] - BG2[2]) * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))

    # ---------- header ----------
    mx = 32
    d.rectangle([(0, 0), (W, 5)], fill=GOLD)
    f_title = font(F_BOLD, 60)
    f_date = font(F_BOLD, 27)
    f_kicker = font(F_BOLD, 17)
    d.text((mx, 24), "THE WORLD", font=f_title, fill=WHITE)
    # gold underline accent under title
    d.rectangle([(mx, 96), (mx + 300, 100)], fill=GOLD)
    d.text((mx, 110), "WEDNESDAY  18  NOVEMBER  2026", font=f_date, fill=GOLD)
    # right-side tag
    tag = "ONE-DAY WORLD NEWS"
    tw = d.textlength(tag, font=f_kicker)
    d.text((W - mx - tw, 30), tag, font=f_kicker, fill=GREY)
    d.text((W - mx - d.textlength("8 STORIES  \u00b7  18 NOV 2026", font=f_kicker), 56),
           "8 STORIES  \u00b7  18 NOV 2026", font=f_kicker, fill=GREY)
    d.line([(mx, 152), (W - mx, 152)], fill=CARD_EDGE, width=2)

    # ---------- news grid: 2 cols x 4 rows ----------
    grid_top, grid_bottom = 168, 912
    gap = 12
    cols, rows = 2, 4
    cw = (W - 2 * mx - (cols - 1) * gap) // cols
    ch = (grid_bottom - grid_top - (rows - 1) * gap) // rows

    f_num = font(F_BOLD, 20)
    f_cat = font(F_BOLD, 15)
    f_head = font(F_BOLD, 22)
    f_sum = font(F_REG, 16)

    for i, (cat, head, summ) in enumerate(NEWS):
        r, c = divmod(i, cols)
        x0 = mx + c * (cw + gap)
        y0 = grid_top + r * (ch + gap)
        x1, y1 = x0 + cw, y0 + ch
        color = CAT_COLORS[cat]

        rounded(d, [x0, y0, x1, y1], 14, fill=CARD, outline=CARD_EDGE, width=1)
        # left accent bar
        d.rounded_rectangle([x0, y0, x0 + 7, y1], radius=3, fill=color)

        pad = 18
        tx = x0 + pad + 6
        tw_text = cw - pad * 2 - 6

        # number circle + category pill
        cy = y0 + 14
        d.ellipse([tx, cy, tx + 32, cy + 32], fill=color)
        num = str(i + 1)
        nw = d.textlength(num, font=f_num)
        d.text((tx + (32 - nw) / 2, cy + 4), num, font=f_num, fill=(12, 16, 28))
        pill_x = tx + 42
        pill_w = d.textlength(cat, font=f_cat) + 20
        rounded(d, [pill_x, cy + 2, pill_x + pill_w, cy + 30], 14, fill=color)
        d.text((pill_x + 10, cy + 7), cat, font=f_cat, fill=(12, 16, 28))

        # headline (up to 3 lines)
        head_lines = wrap(d, head, f_head, tw_text)
        if len(head_lines) > 3:
            head_lines = fit_lines(d, head, f_head, tw_text, 3)
        hy = y0 + 56
        for ln in head_lines:
            d.text((tx, hy), ln, font=f_head, fill=WHITE)
            hy += 27

        # summary (3 lines, or 2 if headline took 3)
        max_sum = 3 if len(head_lines) <= 2 else 2
        sum_lines = fit_lines(d, summ, f_sum, tw_text, max_sum)
        sy = hy + 6
        for ln in sum_lines:
            d.text((tx, sy), ln, font=f_sum, fill=MUTED)
            sy += 21

    # ---------- footer ----------
    fy = 928
    # sports strip
    f_sport = font(F_BOLD, 18)
    sport_text = "SPORT  \u00b7  " + SPORT
    rounded(d, [mx, fy, W - mx, fy + 36], 10, fill=GOLD)
    d.text((mx + 16, fy + 7), sport_text, font=f_sport, fill=GOLD_DARK)

    # sources + tagline
    f_src = font(F_REG, 15)
    d.text((mx, fy + 48), "Sources: AP  \u00b7  Reuters  \u00b7  BBC  \u00b7  The Guardian",
           font=f_src, fill=GREY)
    tag2 = "One-image summary of 18 Nov 2026 world news"
    d.text((W - mx - d.textlength(tag2, font=f_src), fy + 48), tag2,
           font=f_src, fill=GREY)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
