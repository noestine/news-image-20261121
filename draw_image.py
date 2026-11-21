#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261121.

Fresh drawing for Saturday 21 November 2026 world news, written in this
session. Uses Pillow and the system DejaVu fonts. Deterministic: no
timestamps, no randomness, fixed layout.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 24
GAP = 16

BG = (247, 243, 234)      # paper
NAVY = (14, 42, 71)       # header
GOLD = (212, 160, 60)
CARD = (255, 255, 255)
INK = (24, 28, 34)
MUTED = (96, 104, 116)
RED = (178, 34, 34)
RED_DARK = (139, 22, 22)
RED_SOFT = (248, 226, 224)
TEAL = (15, 118, 110)
BLUE = (30, 90, 168)
LINE = (214, 208, 196)
AMBER = (146, 96, 8)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
F_BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
F_REG = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
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


def draw_wrapped(draw, x, y, text, fnt, fill, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def card(draw, box, accent=None):
    draw.rounded_rectangle(box, radius=14, fill=CARD, outline=LINE, width=2)
    if accent:
        x0, y0, x1, y1 = box
        draw.rounded_rectangle([x0, y0, x0 + 10, y1], radius=5, fill=accent)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---------- header ----------
    d.rectangle([0, 0, W, 128], fill=NAVY)
    d.rectangle([0, 128, W, 134], fill=GOLD)
    d.text((MARGIN, 18), "SATURDAY, 21 NOVEMBER 2026",
           font=font(F_BOLD, 44), fill=(255, 255, 255))
    d.text((MARGIN, 82), "THE WORLD IN ONE DAY",
           font=font(F_BOLD, 25), fill=GOLD)
    d.text((W - MARGIN - 208, 86), "NEWS IN ONE IMAGE",
           font=font(F_REG, 20), fill=(170, 190, 210))

    # ---------- lead panel: missiles land in Poland ----------
    x0, x1 = MARGIN, W - MARGIN
    y0, y1 = 150, 540
    card(d, (x0, y0, x1, y1), accent=RED)
    px = x0 + 26
    d.text((px, y0 + 14), "MISSILES LAND IN POLAND",
           font=font(F_BOLD, 38), fill=RED_DARK)
    d.text((px, y0 + 62),
           "NATO on alert as the war spills onto allied soil",
           font=font(F_REG, 23), fill=MUTED)

    # left: impact map schematic (three crash sites, one per row)
    mx0, my0, mx1, my1 = px, y0 + 100, px + 430, y0 + 252
    d.rounded_rectangle([mx0, my0, mx1, my1], radius=10,
                        fill=(250, 244, 243), outline=(232, 200, 198), width=2)
    d.text((mx0 + 14, my0 + 10), "WHERE THEY CAME DOWN  —  SE POLAND",
           font=font(F_BOLD, 16), fill=MUTED)
    sites = [
        ("Kh-101 missile — Nowy Lipowiec", 46),
        ("2nd missile — Rudnik nad Sanem", 82),
        ("Jet-powered drone — Mołodycz", 118),
    ]
    for label, dy in sites:
        cy = my0 + dy
        for rr, col in ((13, (252, 214, 210)), (8, (240, 150, 140)),
                        (4, RED)):
            d.ellipse([mx0 + 28 - rr, cy - rr, mx0 + 28 + rr, cy + rr],
                      fill=col)
        d.text((mx0 + 50, cy - 10), label, font=font(F_BOLD, 17), fill=INK)
    d.text((mx0 + 14, my1 - 24),
           "All near the Ukraine border; Kh-101 ~50 km out",
           font=font(F_REG, 15), fill=MUTED)

    # right: the night's barrage in numbers (2x2 grid)
    rx = px + 460
    d.text((rx, y0 + 100), "THE NIGHT'S BARRAGE ON UKRAINE",
           font=font(F_BOLD, 19), fill=INK)
    grid = [
        ("400+", "drones fired", 0, 0),
        ("110", "missiles fired", 232, 0),
        ("8+", "killed in Ukraine", 0, 68),
        ("0", "hurt in Poland", 232, 68),
    ]
    for name, label, dx, dy in grid:
        d.text((rx + dx, y0 + 128 + dy), name, font=font(F_BOLD, 34), fill=RED)
        d.text((rx + dx, y0 + 170 + dy), label, font=font(F_REG, 17), fill=MUTED)

    # bottom of lead: quotes strip
    qy0, qy1 = y0 + 268, y1 - 16
    d.rounded_rectangle([px, qy0, x1 - 26, qy1], radius=10,
                        fill=(247, 243, 234), outline=LINE, width=2)
    draw_wrapped(d, px + 16, qy0 + 10,
                 "PM Donald Tusk: \"It does not look like an accident — "
                 "we are dealing with an intentional provocation.\" "
                 "Jets scrambled; NATO's Rutte calls it a \"grave "
                 "violation\" and visits Warsaw on Saturday.",
                 font(F_REG, 19), INK, x1 - 26 - px - 32, 25)

    # ---------- middle row: markets + Nvidia ----------
    my0, my1 = 556, 772
    mw = (W - 2 * MARGIN - GAP) // 2

    # Wall Street panel
    card(d, (x0, my0, x0 + mw, my1), accent=RED)
    tx = x0 + 26
    d.text((tx, my0 + 12), "WALL STREET JOINS THE ROUT",
           font=font(F_BOLD, 25), fill=RED_DARK)
    draw_wrapped(d, tx, my0 + 50,
                 "S&P 500 and Dow slide into correction as the AI "
                 "sell-off deepens: Nasdaq -5.3%, Nvidia -14%, "
                 "Dow down nearly 950 points.",
                 font(F_REG, 20), INK, mw - 52, 26)
    # mini descending chart
    cx0, cx1 = tx, x0 + mw - 26
    cy0, cy1 = my0 + 140, my0 + 196
    d.line([(cx0, cy1), (cx1, cy1)], fill=LINE, width=2)
    d.line([(cx0, cy0), (cx0, cy1)], fill=LINE, width=2)
    pts = [(0.00, 0.10), (0.15, 0.05), (0.30, 0.30), (0.45, 0.26),
           (0.60, 0.55), (0.75, 0.50), (0.88, 0.80), (1.00, 0.92)]
    xy = [(cx0 + fx * (cx1 - cx0), cy0 + fy * (cy1 - cy0)) for fx, fy in pts]
    poly = xy + [(cx1, cy1), (cx0, cy1)]
    d.polygon(poly, fill=RED_SOFT)
    d.line(xy, fill=RED, width=4, joint="curve")
    d.ellipse([xy[-1][0] - 7, xy[-1][1] - 7, xy[-1][0] + 7, xy[-1][1] + 7],
              fill=RED)

    # Nvidia probe panel
    cx = x0 + mw + GAP
    card(d, (cx, my0, x1, my1), accent=BLUE)
    tx2 = cx + 26
    d.text((tx2, my0 + 12), "SEC PROBES NVIDIA",
           font=font(F_BOLD, 25), fill=NAVY)
    draw_wrapped(d, tx2, my0 + 50,
                 "Reuters: the US Securities and Exchange Commission "
                 "is investigating Nvidia's accounting. Trump urges "
                 "the board to bring back ex-CEO Jensen Huang; "
                 "the board says it has no plans to.",
                 font(F_REG, 20), INK, mw - 52, 26)
    d.text((tx2, my1 - 34), "Chip giant at the centre of the AI rout",
           font=font(F_BOLD, 18), fill=MUTED)

    # ---------- bottom row: three small panels ----------
    by0, by1 = 788, 968
    bw3 = (W - 2 * MARGIN - 2 * GAP) // 3
    smalls = [
        ("DENMARK FOILS PLOT", NAVY,
         "Russian plot to kill rapper Kyivstoner foiled; 3 arrested "
         "in September. Denmark expels Russia's defence attache."),
        ("RIYADH INTERCEPTS 3 MISSILES", RED_DARK,
         "Saudi coalition shoots down 3 Houthi missiles over "
         "Riyadh and strikes Hodeidah, a day after the PIF "
         "Tower was hit."),
        ("YOUTUBE NEARS $3BN DEAL", TEAL,
         "In-principle deal with US school districts over "
         "addiction claims — the largest ever. Teen safeguards "
         "included."),
    ]
    for i, (title, color, body) in enumerate(smalls):
        sx0 = x0 + i * (bw3 + GAP)
        sx1 = sx0 + bw3
        card(d, (sx0, by0, sx1, by1), accent=color)
        stx = sx0 + 22
        draw_wrapped(d, stx, by0 + 12, title, font(F_BOLD, 20), color,
                     bw3 - 44, 25)
        draw_wrapped(d, stx, by0 + 66, body, font(F_REG, 17), INK,
                     bw3 - 44, 23)

    # ---------- footer ----------
    d.text((MARGIN, 982),
           "Also: COP31 runs into overtime — new draft due Saturday  |  "
           "Sources: AP, Reuters, Bloomberg",
           font=font(F_REG, 17), fill=MUTED)

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
