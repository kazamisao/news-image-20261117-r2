#!/usr/bin/env python3
"""Renderer for the news-image-20261117 round-2 entry.

Draws a one-page illustrated broadsheet of the world news of Tuesday,
17 November 2026 at three times final size and downscales it to a
1024x1024 PNG named news.png beside this file. Pure Pillow, no network,
deterministic: the same bytes on every run.

Layout: a navy masthead with the date in large serif; a wide hero panel
on the Kerch Bridge strike; six illustrated story panels (Hormuz,
Zaporizhzhia, Gaza aid call, COP31, US measles, Trump in Manila); and an
"Also today" strip carrying five more stories.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

SS = 3                      # supersample factor
W = 1024 * SS               # canvas edge in device pixels
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news.png")

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (13, 34, 64)
CREAM = (244, 236, 217)
PAPER = (247, 242, 230)
RED = (200, 16, 46)
WHITE = (255, 255, 255)
INK = (20, 24, 32)
SUB = (206, 218, 236)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, max_w, start, tracking=0):
    """Largest font (stepping down from start) whose text fits max_w."""
    size = start
    while size > 20:
        f = font(path, size)
        if draw.textlength(text, font=f) + tracking * max(0, len(text) - 1) <= max_w:
            return f, size
        size -= 4
    return font(path, 20), 20


def tracked(draw, cx, y, text, f, fill, tracking):
    """Draw letter-spaced text centred on cx; returns nothing."""
    total = draw.textlength(text, font=f) + tracking * max(0, len(text) - 1)
    x = cx - total / 2
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + tracking


def wrap(draw, text, f, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def gradient(w, h, top, bottom):
    col = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        col.putpixel((0, y), tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return col.resize((w, h))


# ---------------------------------------------------------------- scenes
# Each painter receives a Draw bound to a transparent layer and a box
# (x0, y0, x1, y1); the caller clips the layer to the box, so paint may
# safely overshoot the edges.

def paint_bridge(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    deck = y0 + int(h * 0.52)
    water = y0 + int(h * 0.66)
    d.rectangle([x0, water, x1, y1], fill=(23, 58, 94))
    for i in range(7):
        yy = water + int(h * 0.05) + i * int(h * 0.045)
        d.line([x0 + (i % 3) * 60, yy, x1 - (i % 2) * 90, yy], fill=(52, 96, 138), width=5)
    # intact arch, left
    d.arc([x0 + int(w * 0.10), deck - int(h * 0.46), x0 + int(w * 0.52), deck + int(h * 0.20)],
          180, 360, fill=(196, 206, 219), width=16)
    # broken arch, right: rising stub only
    bx = x0 + int(w * 0.60)
    d.arc([bx, deck - int(h * 0.44), bx + int(w * 0.34), deck + int(h * 0.20)],
          180, 285, fill=(196, 206, 219), width=16)
    # fallen span in the water, with a ripple
    fx, fy = x0 + int(w * 0.66), deck + int(h * 0.16)
    d.polygon([(fx, fy), (fx + int(w * 0.16), fy + int(h * 0.05)),
               (fx + int(w * 0.13), fy + int(h * 0.13)), (fx - int(w * 0.02), fy + int(h * 0.07))],
              fill=(120, 130, 145))
    d.ellipse([fx + int(w * 0.03), fy + int(h * 0.13), fx + int(w * 0.17), fy + int(h * 0.19)],
              outline=(160, 190, 215), width=5)
    # deck with a gap at the break, dashed centre line, pillars
    d.rectangle([x0, deck, x0 + int(w * 0.615), deck + int(h * 0.055)], fill=(88, 98, 112))
    d.rectangle([x0 + int(w * 0.70), deck, x1, deck + int(h * 0.055)], fill=(88, 98, 112))
    for xx in range(int(x0 + 20), int(x1 - 20), 64):
        if x0 + int(w * 0.60) < xx < x0 + int(w * 0.71):
            continue
        d.line([xx, deck + int(h * 0.027), xx + 34, deck + int(h * 0.027)], fill=(230, 230, 220), width=5)
    for px in (0.16, 0.38, 0.80, 0.93):
        d.rectangle([x0 + int(w * px), deck + int(h * 0.05),
                     x0 + int(w * px) + 26, water + int(h * 0.05)], fill=(70, 80, 95))
    # fire where the strike landed, smoke climbing away
    cx, cy = x0 + int(w * 0.665), deck - int(h * 0.02)
    for rf, c in [(0.095, (255, 122, 26)), (0.066, (255, 176, 32)), (0.040, (255, 226, 120))]:
        r = int(h * rf)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    for dxf, dyf, rf in [(0.010, -0.15, 0.085), (0.028, -0.24, 0.12),
                         (0.010, -0.34, 0.155), (0.037, -0.42, 0.13)]:
        dx, dy, r = int(w * dxf), int(h * dyf), int(h * rf)
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=(74, 72, 78))
    # a drone overhead
    dx_, dy_ = x0 + int(w * 0.30), y0 + int(h * 0.16)
    d.ellipse([dx_ - 16, dy_ - 10, dx_ + 16, dy_ + 10], fill=(24, 26, 30))
    for sx, sy in [(-52, -26), (52, -26), (-52, 26), (52, 26)]:
        d.ellipse([dx_ + sx - 15, dy_ + sy - 6, dx_ + sx + 15, dy_ + sy + 6], fill=(24, 26, 30))
        d.line([dx_, dy_, dx_ + sx, dy_ + sy], fill=(24, 26, 30), width=6)
    # low sun
    d.ellipse([x1 - int(w * 0.13), y0 + int(h * 0.10),
               x1 - int(w * 0.055), y0 + int(h * 0.10) + int(w * 0.075)], fill=(250, 205, 110))


def paint_tanker(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    sea = y0 + int(h * 0.72)
    d.rectangle([x0, sea, x1, y1], fill=(18, 52, 88))
    hull = y0 + int(h * 0.52)
    d.polygon([(x0 + int(w * 0.06), hull), (x0 + int(w * 0.94), hull),
               (x0 + int(w * 0.86), sea + 8), (x0 + int(w * 0.16), sea + 8)], fill=(38, 42, 50))
    d.rectangle([x0 + int(w * 0.10), hull - int(h * 0.10), x0 + int(w * 0.62), hull], fill=(150, 52, 40))
    d.rectangle([x0 + int(w * 0.70), hull - int(h * 0.30), x0 + int(w * 0.84), hull], fill=(210, 214, 220))
    for i in range(3):
        d.rectangle([x0 + int(w * 0.725) + i * int(w * 0.04), hull - int(h * 0.24),
                     x0 + int(w * 0.745) + i * int(w * 0.04), hull - int(h * 0.17)], fill=(30, 60, 90))
    cx, cy = x0 + int(w * 0.36), hull - int(h * 0.08)
    for rf, c in [(0.16, (255, 110, 20)), (0.115, (255, 168, 28)), (0.068, (255, 224, 130))]:
        r = int(h * rf)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    for dxf, dyf, rf in [(0.018, -0.22, 0.105), (0.058, -0.35, 0.15), (0.022, -0.49, 0.19)]:
        dx, dy, r = int(w * dxf), int(h * dyf), int(h * rf)
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=(60, 58, 64))
    # the mine that did it, bobbing off the bow
    mx, my = x0 + int(w * 0.90), sea + int(h * 0.12)
    d.ellipse([mx - 30, my - 30, mx + 30, my + 30], fill=(16, 18, 22))
    for a in range(0, 360, 45):
        rad = math.radians(a)
        ex, ey = mx + int(44 * math.cos(rad)), my + int(44 * math.sin(rad))
        d.line([mx, my, ex, ey], fill=(16, 18, 22), width=8)
        d.ellipse([ex - 8, ey - 8, ex + 8, ey + 8], fill=(16, 18, 22))


def paint_city(d, box):
    """A skyline at night with a blast blooming over its centre."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    base = y0 + int(h * 0.94)
    shades = [(70, 78, 95), (56, 64, 82), (84, 92, 108)]
    bx, i = x0 + int(w * 0.05), 0
    while bx < x1 - int(w * 0.10):
        bw = int(w * (0.10 + (i % 3) * 0.025))
        bh = int(h * (0.34 + ((i * 37) % 30) / 100.0))
        d.rectangle([bx, base - bh, bx + bw, base], fill=shades[i % 3])
        for wy in range(base - bh + 16, base - 18, 34):
            for wx in range(bx + 12, bx + bw - 14, 30):
                if (wx * 7 + wy * 13) % 5:
                    d.rectangle([wx, wy, wx + 13, wy + 16], fill=(250, 214, 120))
        bx += bw + int(w * 0.02)
        i += 1
    cx, cy = x0 + int(w * 0.52), y0 + int(h * 0.40)
    for rf, c in [(0.30, (255, 116, 22)), (0.21, (255, 172, 30)), (0.12, (255, 230, 140))]:
        r = int(h * rf)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    for dxf, dyf, rf in [(0.010, -0.20, 0.11), (0.066, -0.30, 0.15), (0.008, -0.40, 0.185)]:
        dx, dy, r = int(w * dxf), int(h * dyf), int(h * rf)
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=(66, 62, 66))


def paint_aid(d, box):
    """An aid truck at a crossing barrier, a parachute drop beside it."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    ground = y0 + int(h * 0.80)
    d.rectangle([x0, ground, x1, y1], fill=(146, 116, 74))
    tx, ty = x0 + int(w * 0.10), ground - int(h * 0.34)
    d.rectangle([tx, ty, tx + int(w * 0.52), ground - int(h * 0.06)], fill=(238, 240, 244))
    d.rectangle([tx + int(w * 0.52), ty + int(h * 0.10), tx + int(w * 0.68), ground - int(h * 0.06)], fill=RED)
    d.rectangle([tx + int(w * 0.55), ty + int(h * 0.15), tx + int(w * 0.645), ty + int(h * 0.30)],
                fill=(170, 220, 240))
    ccx, ccy = tx + int(w * 0.26), ty + int(h * 0.15)
    d.rectangle([ccx - 13, ccy - 40, ccx + 13, ccy + 40], fill=RED)
    d.rectangle([ccx - 40, ccy - 13, ccx + 40, ccy + 13], fill=RED)
    for wx in (tx + int(w * 0.10), tx + int(w * 0.55)):
        d.ellipse([wx, ground - int(h * 0.13), wx + int(w * 0.11), ground - int(h * 0.02)], fill=(24, 26, 30))
    px, py = x0 + int(w * 0.80), y0 + int(h * 0.14)
    d.pieslice([px - 78, py - 44, px + 78, py + 44], 180, 360, fill=(250, 176, 32))
    d.line([px - 72, py, px - 16, py + 92], fill=(240, 240, 240), width=5)
    d.line([px + 72, py, px + 16, py + 92], fill=(240, 240, 240), width=5)
    d.rectangle([px - 24, py + 88, px + 24, py + 128], fill=(168, 120, 66))
    d.rectangle([x0 + int(w * 0.03), ground - int(h * 0.52), x0 + int(w * 0.055), ground], fill=(90, 90, 96))
    d.rectangle([x0 + int(w * 0.03), ground - int(h * 0.52), x0 + int(w * 0.30), ground - int(h * 0.46)],
                fill=(250, 250, 250))
    for i in range(4):
        sx = x0 + int(w * 0.05) + i * int(w * 0.065)
        d.line([sx, ground - int(h * 0.52), sx + int(w * 0.03), ground - int(h * 0.46)], fill=RED, width=9)


def paint_globe(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy, r = x0 + w // 2, y0 + int(h * 0.46), int(min(w, h) * 0.34)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(38, 110, 168))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(190, 225, 250), width=5)
    for pts in [[(-0.62, -0.42), (-0.30, -0.55), (-0.22, -0.28), (-0.38, -0.10), (-0.60, -0.16)],
                [(-0.34, 0.10), (-0.16, 0.06), (-0.20, 0.34), (-0.30, 0.48), (-0.38, 0.26)],
                [(0.02, -0.52), (0.22, -0.44), (0.16, -0.24), (0.0, -0.30)],
                [(0.06, -0.10), (0.20, -0.06), (0.24, 0.22), (0.12, 0.34), (0.02, 0.14)],
                [(0.36, -0.46), (0.66, -0.38), (0.60, -0.14), (0.40, -0.20)],
                [(0.48, 0.16), (0.68, 0.22), (0.62, 0.40), (0.46, 0.34)]]:
        d.polygon([(cx + int(px * r), cy + int(py * r)) for px, py in pts], fill=(74, 168, 92))
    lx, ly = cx + int(r * 0.62), cy + int(r * 0.60)
    d.ellipse([lx - 62, ly - 62, lx + 62, ly + 62], fill=(34, 150, 70))
    d.polygon([(lx - 26, ly + 30), (lx + 4, ly - 34), (lx + 34, ly - 6), (lx + 12, ly + 26)],
              fill=(210, 245, 200))
    d.line([lx - 26, ly + 30, lx + 30, ly - 28], fill=(20, 100, 50), width=6)


def paint_virus(d, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    color = (232, 64, 52)
    for fx, fy, r in [(0.26, 0.34, 62), (0.55, 0.55, 84), (0.80, 0.28, 52),
                      (0.72, 0.74, 40), (0.38, 0.78, 34)]:
        cx, cy = x0 + int(w * fx), y0 + int(h * fy)
        for a in range(0, 360, 36):
            rad = math.radians(a)
            ex, ey = cx + int((r + 20) * math.cos(rad)), cy + int((r + 20) * math.sin(rad))
            d.line([cx, cy, ex, ey], fill=color, width=9)
            d.ellipse([ex - 10, ey - 10, ex + 10, ey + 10], fill=color)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
        d.ellipse([cx - int(r * 0.4), cy - int(r * 0.4), cx + int(r * 0.1), cy + int(r * 0.1)],
                  fill=(255, 170, 150))


def paint_manila(d, box):
    """Skyline, three flags and a jet on approach."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    base = y0 + int(h * 0.96)
    bx, i = x0 + int(w * 0.04), 0
    while bx < x1 - int(w * 0.06):
        bw = int(w * 0.09)
        bh = int(h * (0.24 + ((i * 29) % 20) / 100.0))
        d.rectangle([bx, base - bh, bx + bw, base], fill=(88, 104, 128))
        bx += bw + int(w * 0.025)
        i += 1
    cx, cy = x0 + int(w * 0.52), y0 + int(h * 0.34)
    d.polygon([(cx + 190, cy), (cx + 60, cy - 26), (cx - 40, cy - 78), (cx - 90, cy - 78),
               (cx - 70, cy - 24), (cx - 170, cy - 30), (cx - 200, cy - 6), (cx - 200, cy + 14),
               (cx - 150, cy + 16), (cx - 60, cy + 52), (cx, cy + 26)], fill=(240, 244, 248))
    d.ellipse([cx - 205, cy - 12, cx - 168, cy + 20], fill=RED)
    for i, col in enumerate([(178, 34, 52), (250, 250, 250), (36, 84, 160)]):
        fx, fy = x0 + int(w * (0.10 + i * 0.13)), y0 + int(h * 0.10)
        d.line([fx, fy, fx, fy + int(h * 0.34)], fill=(230, 230, 230), width=7)
        d.rectangle([fx, fy, fx + int(w * 0.10), fy + int(h * 0.11)], fill=col)


# ------------------------------------------------------------- composition

def masthead(d):
    d.rectangle([0, 0, W, 400], fill=NAVY)
    f_k, _ = fit(d, "THE WORLD IN ONE DAY", BOLD, W * 0.8, 62, tracking=16)
    tracked(d, W // 2, 58, "THE WORLD IN ONE DAY", f_k, (168, 188, 220), 16)
    f_d, _ = fit(d, "TUESDAY, 17 NOVEMBER 2026", SERIF, W - 120, 208)
    tw = d.textlength("TUESDAY, 17 NOVEMBER 2026", font=f_d)
    d.text(((W - tw) / 2, 148), "TUESDAY, 17 NOVEMBER 2026", font=f_d, fill=WHITE)
    d.rectangle([0, 400, W, 414], fill=RED)


def clipped_scene(img, painter, box):
    """Paint a scene on its own layer and paste only what lands in box."""
    layer = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    painter(ImageDraw.Draw(layer), box)
    crop = layer.crop(box)
    img.paste(crop, (box[0], box[1]), crop)


def panel(img, d, box, painter, sky, headline, sub):
    x0, y0, x1, y1 = box
    band = int((y1 - y0) * 0.40)
    img.paste(gradient(x1 - x0, (y1 - y0) - band, sky[0], sky[1]), (x0, y0))
    clipped_scene(img, painter, (x0, y0, x1, y1 - band))
    by = y1 - band
    d.rectangle([x0, by, x1, y1], fill=NAVY)
    f_h, hs = fit(d, headline, BOLD, (x1 - x0) - 56, 60)
    yy = by + 26
    for ln in wrap(d, headline, f_h, (x1 - x0) - 56)[:2]:
        d.text((x0 + 28, yy), ln, font=f_h, fill=WHITE)
        yy += int(hs * 1.14)
    f_s = font(REG, 45)
    for ln in wrap(d, sub, f_s, (x1 - x0) - 56)[:2]:
        d.text((x0 + 28, yy + 4), ln, font=f_s, fill=SUB)
        yy += int(45 * 1.28)


def ticker(d, y0, items):
    h = W - y0 - 66
    d.rectangle([54, y0, W - 54, y0 + h], fill=PAPER)
    d.rectangle([54, y0, 78, y0 + h], fill=RED)
    d.text((108, y0 + 22), "ALSO TODAY", font=font(BOLD, 52), fill=RED)
    f = font(REG, 49)
    yy = y0 + 92
    for ln in wrap(d, "   •   ".join(items), f, W - 240)[:3]:
        d.text((108, yy), ln, font=f, fill=INK)
        yy += 64


def build():
    img = Image.new("RGB", (W, W), CREAM)
    d = ImageDraw.Draw(img)
    masthead(d)
    m = 54
    # hero: the Kerch Bridge
    hy0, hy1 = 440, 1290
    img.paste(gradient(W - 2 * m, hy1 - hy0 - 250, (40, 54, 98), (236, 130, 64)), (m, hy0))
    clipped_scene(img, paint_bridge, (m, hy0, W - m, hy1 - 250))
    d.rectangle([m, hy1 - 250, W - m, hy1], fill=NAVY)
    f_h, _ = fit(d, "UKRAINE CUTS THE KERCH BRIDGE", BOLD, W - 2 * m - 60, 104)
    d.text((m + 30, hy1 - 226), "UKRAINE CUTS THE KERCH BRIDGE", font=f_h, fill=WHITE)
    f_s = font(REG, 54)
    d.text((m + 30, hy1 - 118), "A span falls into the strait on a second night of strikes;",
           font=f_s, fill=SUB)
    d.text((m + 30, hy1 - 56), "Russia answers by hitting bridges in Kyiv.", font=f_s, fill=SUB)
    # six panels in two rows of three
    rows = [
        [(paint_tanker, ((26, 44, 84), (214, 116, 58)), "TANKERS ABLAZE IN HORMUZ",
          "A fourth tanker hits a mine in 24 hours; Iran seizes a U.S. drone."),
         (paint_city, ((30, 40, 70), (120, 96, 110)), "40 KILLED IN ZAPORIZHZHIA",
          "A Russian strike levels homes; an aid centre is hit too, killing 26."),
         (paint_aid, ((70, 120, 160), (214, 178, 120)), "WEST TO GAZA: OPEN THE GATES",
          "Britain, Australia, Canada and Italy urge Israel to let aid flood in.")],
        [(paint_globe, ((24, 70, 110), (90, 160, 130)), "COP31 DRAFT: END FOSSIL ERA FASTER",
          "Antalya text seeks $120bn a year in climate aid by 2035."),
         (paint_virus, ((90, 30, 44), (150, 52, 52)), "U.S. LOSES MEASLES-FREE STATUS",
          "5,400 cases and 10 deaths — the worst toll in three decades."),
         (paint_manila, ((52, 84, 130), (196, 170, 130)), "TRUMP LANDS IN MANILA",
          "ASEAN and Quad open his Asia tour; Shenzhen summit set Thursday.")],
    ]
    y = hy1 + 26
    rh = 668
    cw = (W - 2 * m - 2 * 24) // 3
    for row in rows:
        for i, (painter, sky, head, sub) in enumerate(row):
            x = m + i * (cw + 24)
            panel(img, d, (x, y, x + cw, y + rh), painter, sky, head, sub)
        y += rh + 24
    ticker(d, y + 2, [
        "JAPAN — jets scramble as Russian aircraft enter its airspace",
        "TRUMP — shrugs off six days of U.S. tech, bank and airline outages  •  NVIDIA — first post-Huang earnings",
        "KEMEROVO — military plane crash kills all 19 aboard",
        "FRANCE — 146,000 march on living costs",
        "EBOLA — DR Congo toll passes 5,500 dead",
    ])
    return img.resize((1024, 1024), Image.LANCZOS)


if __name__ == "__main__":
    build().save(OUT)
    print("wrote", OUT)
