#!/usr/bin/env python3
"""Render the ATLAS v6 poster: 'THE FULL DAY' — Sunday 22 November 2026.

One-page newspaper poster, 1024x1024, drawn from scratch with Pillow.
Every story and number comes from the verified pool in stories-v3.md /
stories-daybreak.md (Reuters / AP / BBC / AFP / UKMTO / wires, 22 Nov 2026).
Deterministic: same bytes on every run.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (250, 247, 240)
INK = (20, 24, 29)
RED = (179, 39, 30)
TEAL = (14, 90, 90)
GOLD = (176, 132, 44)
GREY = (96, 100, 104)
CARD = (255, 254, 250)
LINE = (205, 198, 186)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SERIF = FD + "DejaVuSerif.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, size, max_w, min_size=12):
    """Shrink font until text fits max_w; return (font, size)."""
    s = size
    while s > min_size:
        f = font(path, s)
        if draw.textlength(text, font=f) <= max_w:
            return f, s
        s -= 1
    return font(path, min_size), min_size


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, fnt, fill=INK, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


# ---------- tiny flat scenes (geometric, no text inside) ----------

def scene_hormuz(d, box):
    x0, y0, x1, y1 = box
    # sky bands
    for i in range(6):
        c = (214 - i * 6, 148 - i * 7, 96 - i * 5)
        d.rectangle([x0, y0 + i * 9, x1, y0 + (i + 1) * 9], fill=c)
    sea_y = y0 + 54
    d.rectangle([x0, sea_y, x1, y1], fill=(38, 84, 106))
    for i in range(4):
        yy = sea_y + 14 + i * 16
        d.line([x0 + 14, yy, x1 - 30, yy], fill=(70, 122, 142), width=2)
    # dashed route
    for xx in range(x0 + 20, x1 - 20, 26):
        d.line([xx, sea_y + 44, xx + 12, sea_y + 44], fill=(240, 220, 160), width=3)

    def tanker(cx, cy, s, hull=(24, 28, 34)):
        d.polygon([(cx - 52 * s, cy), (cx + 52 * s, cy), (cx + 38 * s, cy + 13 * s),
                   (cx - 40 * s, cy + 13 * s)], fill=hull)
        d.rectangle([cx - 46 * s, cy - 8 * s, cx + 44 * s, cy], fill=hull)
        d.rectangle([cx + 22 * s, cy - 22 * s, cx + 38 * s, cy - 8 * s], fill=(60, 66, 74))
        for k in range(3):
            d.rectangle([cx - 34 * s + k * 24 * s, cy - 14 * s,
                         cx - 18 * s + k * 24 * s, cy - 8 * s], fill=(96, 104, 112))

    tanker(x0 + 150, sea_y + 26, 1.0)
    tanker(x0 + 430, sea_y + 52, 0.8, hull=(34, 38, 44))
    # fire + smoke on the far tanker
    fx, fy = x0 + 430, sea_y + 30
    d.polygon([(fx - 13, fy), (fx, fy - 34), (fx + 13, fy)], fill=(232, 116, 32))
    d.polygon([(fx - 6, fy), (fx + 2, fy - 20), (fx + 9, fy)], fill=(246, 178, 60))
    for dx, dy, r, g in ((24, -34, 9, 150), (36, -44, 12, 170), (50, -52, 15, 195)):
        d.ellipse([fx + dx - r, fy + dy - r, fx + dx + r, fy + dy + r],
                  fill=(g, g, g))


def scene_skyline_fire(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(52, 44, 48))
    for i, (bx, bh) in enumerate(((8, 34), (52, 48), (98, 28), (140, 42), (186, 30))):
        d.rectangle([x0 + bx, y1 - bh, x0 + bx + 34, y1], fill=(28, 26, 30))
    d.polygon([(x0 + 66, y1 - 48), (x0 + 76, y0 + 8), (x0 + 86, y1 - 48)], fill=(232, 116, 32))
    d.polygon([(x0 + 70, y1 - 48), (x0 + 77, y0 + 22), (x0 + 83, y1 - 48)], fill=(246, 178, 60))
    d.polygon([(x0 + 150, y1 - 42), (x0 + 158, y0 + 18), (x0 + 166, y1 - 42)], fill=(232, 116, 32))


def icon_chart(d, box, color):
    x0, y0, x1, y1 = box
    pts = [(x0 + 4, y0 + 6), (x0 + 26, y0 + 12), (x0 + 44, y0 + 10),
           (x0 + 62, y0 + 24), (x0 + 84, y1 - 6)]
    d.line(pts, fill=color, width=4, joint="curve")
    d.polygon([(x0 + 84, y1 - 6), (x0 + 72, y1 - 8), (x0 + 82, y1 - 18)], fill=color)


def icon_stars(d, box, color):
    x0, y0, x1, y1 = box
    import math
    cx, cy, r = (x0 + x1) // 2, (y0 + y1) // 2, 15
    for k in range(8):
        a = 2 * math.pi * k / 8
        px, py = cx + r * math.cos(a), cy + r * math.sin(a)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=color)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=color)


def icon_flag(d, box, color):
    x0, y0, x1, y1 = box
    for r in range(3):
        for c in range(4):
            fill = color if (r + c) % 2 == 0 else (240, 238, 232)
            d.rectangle([x0 + 8 + c * 11, y0 + 6 + r * 11, x0 + 19 + c * 11,
                         y0 + 17 + r * 11], fill=fill)


def icon_ball(d, box, color):
    x0, y0, x1, y1 = box
    cx, cy, r = (x0 + x1) // 2, (y0 + y1) // 2, 17
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=160, fill=color, width=3)
    d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=340, fill=color, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=color, width=3)


def icon_cross(d, box, color):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([cx - 6, cy - 17, cx + 6, cy + 17], fill=color)
    d.rectangle([cx - 17, cy - 6, cx + 17, cy + 6], fill=color)
    d.rectangle([x0 + 6, y1 - 12, x1 - 6, y1 - 4], outline=color, width=3)


def icon_jet(d, box, color):
    x0, y0, x1, y1 = box
    cy = (y0 + y1) // 2
    d.polygon([(x0 + 8, cy), (x0 + 58, cy - 6), (x0 + 88, cy), (x0 + 58, cy + 6)],
              fill=color)
    d.polygon([(x0 + 40, cy), (x0 + 54, cy - 16), (x0 + 62, cy)], fill=color)
    d.polygon([(x0 + 40, cy), (x0 + 54, cy + 16), (x0 + 62, cy)], fill=color)


def icon_virus(d, box, color):
    import math
    x0, y0, x1, y1 = box
    cx, cy, r = (x0 + x1) // 2, (y0 + y1) // 2, 12
    for k in range(8):
        a = 2 * math.pi * k / 8
        ex, ey = cx + 19 * math.cos(a), cy + 19 * math.sin(a)
        d.line([cx, cy, ex, ey], fill=color, width=3)
        d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=color)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)


def icon_hands(d, box, color):
    x0, y0, x1, y1 = box
    d.polygon([(x0 + 10, y0 + 26), (x0 + 40, y0 + 10), (x0 + 52, y0 + 22),
               (x0 + 24, y0 + 34)], fill=color)
    d.polygon([(x1 - 10, y1 - 26), (x1 - 40, y1 - 10), (x1 - 52, y1 - 22),
               (x1 - 24, y1 - 34)], fill=color)
    d.ellipse([x0 + 40, y0 + 14, x0 + 54, y0 + 28], outline=(250, 247, 240), width=3)


# ---------- layout ----------

def chip(d, x, y, s, fill=RED, fg=(255, 255, 255), size=17):
    f = font(SANS_B, size)
    w = d.textlength(s, font=f) + 22
    d.rounded_rectangle([x, y, x + w, y + size + 13], radius=6, fill=fill)
    text(d, (x + 11, y + 5), s, f, fill=fg)
    return w


def card(d, box, region, region_color, headline, chip_text, icon):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=CARD, outline=LINE, width=1)
    d.rectangle([x0, y0, x1, y0 + 42], fill=region_color)
    text(d, (x0 + 12, y0 + 12), region, font(SANS_B, 14), fill=(255, 255, 255))
    icon(d, (x1 - 104, y0 + 2, x1 - 8, y0 + 40), (255, 255, 255))
    f, _ = fit(d, headline, SERIF_B, 23, x1 - x0 - 24, min_size=18)
    lines = wrap(d, headline, f, x1 - x0 - 24)
    yy = y0 + 54
    for ln in lines[:2]:
        text(d, (x0 + 12, yy), ln, f)
        yy += 27
    csize = 16
    while csize > 11 and 24 + d.textlength(chip_text, font=font(SANS_B, csize)) > (x1 - x0) - 20:
        csize -= 1
    cf = font(SANS_B, csize)
    d.rounded_rectangle([x0 + 12, y1 - 34, x0 + 24 + d.textlength(chip_text, font=cf),
                         y1 - 8], radius=5, fill=INK)
    text(d, (x0 + 18, y1 - 30), chip_text, cf, fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead: black band, white title, red rule
    d.rectangle([0, 0, W, 96], fill=INK)
    text(d, (28, 18), "THE FULL DAY", font(SERIF_B, 56), fill=(255, 255, 255))
    text(d, (996, 16), "SUNDAY", font(SANS_B, 25), fill=(255, 255, 255), anchor="ra")
    text(d, (996, 50), "22 NOVEMBER 2026", font(SANS_B, 25), fill=(246, 178, 60),
         anchor="ra")
    d.rectangle([0, 96, W, 103], fill=RED)
    text(d, (28, 112), "16 STORIES · 7 REGIONS · ONE PAGE", font(SANS_B, 17), fill=INK)
    text(d, (996, 112), "EVERY STORY FROM SUNDAY'S WIRES", font(SANS_B, 17),
         fill=GREY, anchor="ra")

    # hero (left)
    hx0, hy0, hx1, hy1 = 20, 142, 628, 478
    d.rectangle([hx0, hy0, hx1, hy1], fill=CARD, outline=LINE, width=1)
    d.rectangle([hx0, hy0, hx1, hy0 + 30], fill=RED)
    text(d, (hx0 + 12, hy0 + 7), "MIDDLE EAST — THE BIG STORY", font(SANS_B, 15),
         fill=(255, 255, 255))
    scene_hormuz(d, (hx0 + 8, hy0 + 38, hx1 - 8, hy0 + 168))
    hf, _ = fit(d, "TANKERS HIT IN THE STRAIT OF HORMUZ", SERIF_B, 38, hx1 - hx0 - 28)
    for i, ln in enumerate(wrap(d, "TANKERS HIT IN THE STRAIT OF HORMUZ", hf,
                                hx1 - hx0 - 28)):
        text(d, (hx0 + 14, hy0 + 182 + i * 44), ln, hf)
    deck = ("Iran's third strike in five days hits Bahrain; at least 3 tankers "
            "are struck in the strait, and US jets hit Qeshm island.")
    df = font(SANS, 15)
    for i, ln in enumerate(wrap(d, deck, df, hx1 - hx0 - 28)[:2]):
        text(d, (hx0 + 14, hy0 + 256 + i * 21), ln, df, fill=(52, 56, 60))
    chip(d, hx0 + 14, hy1 - 40, "3 TANKERS HIT", fill=RED, size=18)
    text(d, (hx1 - 14, hy1 - 34), "AP · REUTERS · UKMTO", font(SANS_B, 14),
         fill=GREY, anchor="ra")

    # right rail: COP31 second lead
    rx0, rx1 = 644, 1004
    d.rectangle([rx0, 142, rx1, 316], fill=(233, 240, 238), outline=LINE, width=1)
    d.rectangle([rx0, 142, rx1, 172], fill=TEAL)
    text(d, (rx0 + 12, 149), "GLOBAL — CLIMATE", font(SANS_B, 15), fill=(255, 255, 255))
    cf2, _ = fit(d, "COP31 TALKS COLLAPSE — NO DEAL", SERIF_B, 27, rx1 - rx0 - 24)
    for i, ln in enumerate(wrap(d, "COP31 TALKS COLLAPSE — NO DEAL", cf2,
                                rx1 - rx0 - 24)[:2]):
        text(d, (rx0 + 12, 182 + i * 32), ln, cf2)
    text(d, (rx0 + 12, 222), "The longest summit ever ends with", font(SANS, 15),
         fill=(52, 56, 60))
    text(d, (rx0 + 12, 242), "nothing adopted.", font(SANS, 15), fill=(52, 56, 60))
    chip(d, rx0 + 12, 272, "0 FOSSIL-FUEL MENTIONS", fill=TEAL, size=14)

    # right rail: Serang factory fire
    d.rectangle([rx0, 328, rx1, 478], fill=CARD, outline=LINE, width=1)
    scene_skyline_fire(d, (rx0 + 8, 336, rx1 - 8, 390))
    sf, _ = fit(d, "SERANG FACTORY FIRE", SERIF_B, 27, rx1 - rx0 - 24)
    text(d, (rx0 + 12, 396), "SERANG FACTORY FIRE", sf)
    text(d, (rx0 + 12, 430), "3 dead confirmed at the Milkita plant.", font(SANS, 14),
         fill=(52, 56, 60))
    chip(d, rx0 + 12, 450, "39 MISSING", fill=RED, size=13)

    # grid 4x2
    cards = [
        ("ASIA-PACIFIC", TEAL, "TAIWAN STOCKS PLUNGE", "7,641 PTS IN A WEEK", icon_chart),
        ("EUROPE", (44, 84, 150), "BRITAIN OPENS TO EU YOUTH", "100,000 A YEAR", icon_stars),
        ("N. AMERICA", (120, 62, 140), "VERSTAPPEN WINS IN VEGAS", "34 LEAD CHANGES", icon_flag),
        ("N. AMERICA", (120, 62, 140), "WEMBANYAMA SCORES 50", "SPURS WIN 114–91", icon_ball),
        ("MIDDLE EAST", RED, "AID WORKERS KILLED IN GAZA", "3 KILLED", icon_cross),
        ("MIDDLE EAST", RED, "70+ RAIDS HIT YEMEN", "8 AREAS STRUCK", icon_jet),
        ("AFRICA", (150, 96, 20), "EBOLA TOLL PASSES 5,700", "DR CONGO OUTBREAK", icon_virus),
        ("ASIA-PACIFIC", TEAL, "EU–INDONESIA TRADE DEAL", "10 YRS OF TALKS", icon_hands),
    ]
    gx, gy, cw, chh, gap = 20, 492, 237, 146, 12
    for i, (region, color, head, chp, icon) in enumerate(cards):
        cx = gx + (i % 4) * (cw + gap)
        cy = gy + (i // 4) * (chh + gap)
        card(d, (cx, cy, cx + cw, cy + chh), region, color, head, chp, icon)

    # ALSO TODAY black band
    by0 = 806
    d.rectangle([20, by0, 1004, by0 + 88], fill=INK)
    text(d, (36, by0 + 8), "ALSO TODAY", font(SANS_B, 16), fill=(246, 178, 60))
    rows = [
        "PUGH SWIMS THE STRAIT — 15 KM IN 3 DAYS   ·   TOKYO: PILOTLESS AIR TAXI CARRIES FIRST RIDERS",
        "MADRID: BANK TAX TO EXPAND FOR HOUSING   ·   USA: TEEN GAMER HELPS FBI RESCUE GIRL",
        "BRAZIL: TOWN DIGS OUT AFTER DEADLY STORM",
    ]
    for j, row in enumerate(rows):
        f2, _ = fit(d, row, SANS_B, 15, 952, min_size=12)
        text(d, (36, by0 + 31 + j * 19), row, f2, fill=(255, 255, 255))

    # DATE CHECK
    dy0 = 902
    d.rectangle([20, dy0, 1004, dy0 + 56], outline=RED, width=2)
    text(d, (36, dy0 + 7), "DATE CHECK — NOT SUNDAY'S NEWS, SO LEFT OUT:", font(SANS_B, 15),
         fill=RED)
    text(d, (36, dy0 + 30),
         "Shenzhen summit was Thu 19 Nov  ·  'El Chapo Isidro' arrest was Fri 20 Nov",
         font(SANS, 15), fill=INK)

    # footer
    text(d, (20, 966), "WIRE-CHECKED · 22 NOV 2026", font(SANS_B, 14), fill=INK)
    text(d, (20, 989),
         "Regions: Middle East 3 · Asia-Pacific 4 · N. America 3 · Europe 2 · Global 2 · Africa 1 · Latin America 1",
         font(SANS, 13), fill=GREY)
    text(d, (1004, 966), "REUTERS · AP · BBC · AFP · UKMTO · WIRES", font(SANS_B, 14),
         fill=GREY, anchor="ra")

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
