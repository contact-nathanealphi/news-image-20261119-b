"""Render the front-page image for the 19 November 2026 news entry.

Variant B: bold modern, photo-led. One large self-drawn illustration
(three leaders at a summit table, Shenzhen skyline, globe), a huge
headline, five solid-colour story cards, an ALSO TODAY strip.

Original drawing only: every shape and letter is drawn here with Pillow
primitives. No photos, no copied artwork, no network, no randomness, no
timestamps, so re-running this script produces the same PNG bytes.

Usage: python3 tools/render.py   (from anywhere; paths are script-relative)
Output: assets/entry.png, 1024x1024, under 1 MiB.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "entry.png"

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"
REGULAR = FONT_DIR / "DejaVuSans.ttf"

W, H = 1024, 1024
NAVY = (20, 38, 64)
NAVY_DARK = (12, 24, 40)
SKY = (30, 58, 92)
GOLD = (232, 163, 61)
YELLOW = (255, 205, 60)
RED = (179, 38, 30)
TEAL = (14, 107, 107)
BLUE = (31, 95, 168)
AMBER = (154, 107, 0)
WHITE = (255, 255, 255)
PAPER = (250, 248, 242)
INK = (18, 18, 18)
GRAY = (96, 96, 96)
WOOD = (122, 46, 29)
WOOD_TOP = (150, 62, 38)


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    if not path.exists():
        raise SystemExit(f"missing font file: {path}")
    return ImageFont.truetype(str(path), size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont,
         max_width: int) -> list[str]:
    """Greedy word wrap measured with the real font; never splits a word."""
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(draw: ImageDraw.ImageDraw, x: int, y: int, text: str,
               fnt: ImageFont.FreeTypeFont, max_width: int,
               fill: tuple[int, int, int], line_gap: int = 4,
               max_lines: int = 3) -> int:
    """Draw wrapped text; return the y just below the last line."""
    lines = wrap(draw, text, fnt, max_width)[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


# ---------------- icons (52x52 box, drawn with primitives) ----------------

def icon_bridge(d, x, y, c):
    d.line([(x + 2, y + 38), (x + 22, y + 38)], fill=c, width=4)
    d.line([(x + 30, y + 38), (x + 50, y + 38)], fill=c, width=4)
    d.arc([x + 2, y + 8, x + 50, y + 56], start=180, end=360, fill=c, width=4)
    d.line([(x + 26, y + 38), (x + 26, y + 48)], fill=c, width=3)
    d.line([(x + 12, y + 38), (x + 12, y + 30)], fill=c, width=3)
    d.line([(x + 40, y + 38), (x + 40, y + 30)], fill=c, width=3)


def icon_chip(d, x, y, c):
    d.rectangle([x + 10, y + 10, x + 42, y + 42], outline=c, width=4)
    d.rectangle([x + 20, y + 20, x + 32, y + 32], outline=c, width=3)
    for t in (16, 26, 36):
        d.line([(x + t, y + 2), (x + t, y + 10)], fill=c, width=3)
        d.line([(x + t, y + 42), (x + t, y + 50)], fill=c, width=3)
        d.line([(x + 2, y + t), (x + 10, y + t)], fill=c, width=3)
        d.line([(x + 42, y + t), (x + 50, y + t)], fill=c, width=3)


def icon_rain(d, x, y, c):
    d.ellipse([x + 8, y + 6, x + 30, y + 26], fill=c)
    d.ellipse([x + 22, y + 6, x + 44, y + 26], fill=c)
    d.rectangle([x + 8, y + 18, x + 44, y + 26], fill=c)
    for dx in (12, 24, 36):
        d.line([(x + dx, y + 32), (x + dx - 3, y + 46)], fill=c, width=3)


def icon_burst(d, x, y, c):
    cx, cy = x + 26, y + 26
    for dx, dy in [(0, -22), (16, -16), (22, 0), (16, 16),
                   (0, 22), (-16, 16), (-22, 0), (-16, -16)]:
        d.line([(cx, cy), (cx + dx, cy + dy)], fill=c, width=4)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=c)


def icon_ballot(d, x, y, c):
    d.rectangle([x + 8, y + 20, x + 44, y + 46], outline=c, width=4)
    d.line([(x + 20, y + 20), (x + 32, y + 20)], fill=PAPER, width=4)
    d.rectangle([x + 20, y + 4, x + 32, y + 20], outline=c, width=3)
    d.line([(x + 14, y + 33), (x + 21, y + 40)], fill=c, width=3)
    d.line([(x + 21, y + 40), (x + 38, y + 26)], fill=c, width=3)


# ---------------- hero illustration ----------------

def hero(d: ImageDraw.ImageDraw) -> None:
    """Three leaders at a summit table, Shenzhen skyline, globe. y 64-380."""
    # Sky
    d.rectangle([0, 64, W, 380], fill=NAVY)
    d.rectangle([0, 64, W, 200], fill=NAVY_DARK)
    # Stars (fixed positions)
    for sx, sy in [(70, 90), (150, 130), (330, 84), (430, 140), (520, 96),
                   (640, 120), (740, 84), (950, 110), (990, 160), (250, 160)]:
        d.ellipse([sx, sy, sx + 4, sy + 4], fill=WHITE)
    # Globe, top right (kept clear of the third figure's head)
    gx, gy, gr = 890, 150, 80
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=TEAL)
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=WHITE, width=4)
    d.ellipse([gx - 38, gy - gr, gx + 38, gy + gr], outline=(90, 180, 180),
              width=3)
    d.line([(gx - gr, gy), (gx + gr, gy)], fill=(90, 180, 180), width=3)
    d.ellipse([gx - 58, gy - 52, gx - 6, gy - 8], fill=(64, 160, 160))
    d.ellipse([gx + 4, gy + 6, gx + 52, gy + 54], fill=(64, 160, 160))
    d.ellipse([gx + 18, gy - 62, gx + 56, gy - 26], fill=(64, 160, 160))
    # Shenzhen skyline silhouettes (fixed heights, lit windows)
    # Horizon glow band first, so towers occlude it in gaps
    d.rectangle([0, 318, W, 334], fill=GOLD)
    towers = [(0, 300), (70, 250), (140, 282), (210, 232), (285, 268),
              (360, 240), (430, 290), (500, 258), (575, 296), (650, 246),
              (720, 286), (790, 262), (880, 300), (950, 268)]
    for tx, top in towers:
        d.rectangle([tx, top, tx + 62, 380], fill=(8, 16, 28))
        for wy in range(top + 14, 372, 22):
            for wx in (tx + 12, tx + 30, tx + 48):
                if (wx + wy) % 44 < 22:
                    d.rectangle([wx, wy, wx + 6, wy + 8], fill=GOLD)
    # Table
    d.polygon([(40, 334), (984, 334), (1024, 380), (0, 380)], fill=WOOD)
    d.polygon([(40, 334), (984, 334), (1000, 352), (24, 352)], fill=WOOD_TOP)
    # Three leaders: head + shoulders, distinct colours
    figures = [(268, RED, "TRUMP"), (512, GOLD, "XI"), (756, TEAL, "PUTIN")]
    f_plate = font(BOLD, 15)
    for fx, colour, name in figures:
        d.ellipse([fx - 34, 218, fx + 34, 286], fill=colour)
        d.ellipse([fx - 34, 218, fx + 34, 286], outline=WHITE, width=3)
        d.polygon([(fx - 62, 334), (fx + 62, 334), (fx + 44, 282),
                   (fx - 44, 282)], fill=colour)
        d.polygon([(fx - 62, 334), (fx + 62, 334), (fx + 44, 282),
                   (fx - 44, 282)], outline=WHITE, width=2)
        pw = d.textlength(name, font=f_plate) + 18
        d.rectangle([fx - pw / 2, 348, fx + pw / 2, 372], fill=WHITE)
        d.text((fx - d.textlength(name, font=f_plate) / 2, 352), name,
               font=f_plate, fill=NAVY)


def story_card(d: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int,
               kicker: str, colour: tuple[int, int, int], head: str,
               summ: str, icon) -> None:
    """One solid story card: white body, colour top band + left bar, icon."""
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=colour, width=3)
    d.rectangle([x, y, x + w, y + 34], fill=colour)
    f_kick = font(BOLD, 17)
    d.text((x + 14, y + 7), kicker, font=f_kick, fill=WHITE)
    icon(d, x + w - 62, y + 40, colour)
    f_head = font(BOLD, 20)
    y2 = text_block(d, x + 14, y + 44, head, f_head, w - 88, INK,
                    line_gap=1, max_lines=2)
    f_sum = font(REGULAR, 17)
    text_block(d, x + 14, y2 + 4, summ, f_sum, w - 28, GRAY, line_gap=1,
               max_lines=2)


def main() -> None:
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_title = font(BOLD, 40)
    f_date = font(BOLD, 22)
    f_kick = font(BOLD, 20)
    f_headline = font(BOLD, 62)
    f_sub = font(REGULAR, 21)
    f_also = font(BOLD, 20)
    f_item = font(REGULAR, 17)
    f_foot = font(REGULAR, 15)

    # Top band: masthead + unmissable date chip
    d.rectangle([0, 0, W, 64], fill=NAVY)
    d.text((28, 11), "THE WORLD TODAY", font=f_title, fill=WHITE)
    date = "THURSDAY 19 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date) + 28
    d.rounded_rectangle([W - 28 - dw, 12, W - 28, 52], radius=8, fill=YELLOW)
    d.text((W - 28 - dw + 14, 18), date, font=f_date, fill=NAVY)

    # Hero illustration
    hero(d)

    # Headline block
    d.text((28, 392), "SHENZHEN SUMMIT  \u2014  APEC SIDELINES", font=f_kick,
           fill=RED)
    d.text((28, 416), "THREE LEADERS, ONE TABLE", font=f_headline, fill=NAVY)
    text_block(d, 28, 492,
               "Trump, Xi and Putin hold their first three-way summit in "
               "Shenzhen. Nuclear arms, Ukraine and the Iran conflict are on "
               "the agenda.",
               f_sub, W - 56, INK, line_gap=3, max_lines=2)

    # Story cards, row 1 (3 cards)
    y1, h1 = 556, 152
    cards1 = [
        (28, 316, "UKRAINE WAR", NAVY, "Kerch Bridge struck a third time",
         "Ukraine hit the bridge to Crimea again.", icon_bridge),
        (356, 316, "TECHNOLOGY", TEAL, "Anthropic debuts on Nasdaq as ANT",
         "Record $81.3bn IPO priced at $83 a share.", icon_chip),
        (684, 316, "GAZA FLOODS", BLUE, "Four nations urge Gaza aid access",
         "Heavy rain displaced 46,000+ households.", icon_rain),
    ]
    for cx, cw, kick, colour, head, summ, icon in cards1:
        story_card(d, cx, y1, cw, h1, kick, colour, head, summ, icon)

    # Story cards, row 2 (2 wide cards)
    y2, h2 = 720, 152
    cards2 = [
        (28, 472, "GULF STRIKES", RED, "Iran fires at US bases; US strikes Qeshm",
         "A tanker was also struck in the Strait of Hormuz.", icon_burst),
        (524, 472, "ISRAEL POLITICS", AMBER, "Herzog asks Eisenkot to form a government",
         "Bypassing Netanyahu; Kahana elected Knesset speaker with 66 votes.",
         icon_ballot),
    ]
    for cx, cw, kick, colour, head, summ, icon in cards2:
        story_card(d, cx, y2, cw, h2, kick, colour, head, summ, icon)

    # ALSO TODAY strip
    d.rectangle([0, 884, W, 968], fill=NAVY)
    d.text((28, 894), "ALSO TODAY", font=f_also, fill=YELLOW)
    items = [
        "ICJ to rule on Myanmar genocide case",
        "EU governments approve Indonesia trade deal",
        "Voyager 1 believed to reach light-day milestone",
        "IAEA: North Korea expanded enrichment at Yongbyon",
    ]
    # two rows of two items
    d.text((28, 922), "\u2022  " + items[0], font=f_item, fill=WHITE)
    d.text((524, 922), "\u2022  " + items[1], font=f_item, fill=WHITE)
    d.text((28, 944), "\u2022  " + items[2], font=f_item, fill=WHITE)
    d.text((524, 944), "\u2022  " + items[3], font=f_item, fill=WHITE)

    # Footer
    foot = "DRAWN FROM REPORTS PUBLISHED 19 NOVEMBER 2026"
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, 984), foot,
           font=f_foot, fill=GRAY)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
