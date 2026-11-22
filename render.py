"""Draw the front page for 21 November 2026 as one 1024x1024 PNG.

Everything is drawn with Pillow from fixed text and fixed geometry: no
randomness, no clock, no network, no downloaded assets. Running this file
twice produces byte-identical output.
"""

import os

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024

PAPER = (247, 240, 220)
INK = (26, 26, 26)
RED = (176, 30, 36)
GREY = (112, 106, 94)
FAINT = (168, 160, 140)
SKY = (214, 230, 241)
SEA = (84, 106, 138)
SUN = (238, 196, 90)
TOWER = (58, 66, 84)
TOWER_LIT = (196, 176, 120)
SHIP = (40, 44, 56)

FONT_DIRS = (
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/noto",
)


def _find_font(names):
    """Return the first existing font file from the candidate names."""
    for folder in FONT_DIRS:
        for name in names:
            path = os.path.join(folder, name)
            if os.path.exists(path):
                return path
    return None


SERIF_BOLD = _find_font(["DejaVuSerif-Bold.ttf", "LiberationSerif-Bold.ttf"])
SERIF = _find_font(["DejaVuSerif.ttf", "LiberationSerif-Regular.ttf"])
SERIF_ITALIC = _find_font(
    ["DejaVuSerif-Italic.ttf", "LiberationSerif-Italic.ttf"]
)
SANS = _find_font(["DejaVuSans.ttf", "LiberationSans-Regular.ttf"])
SANS_BOLD = _find_font(["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"])


def _load(path, size):
    if path is None:
        return ImageFont.load_default()
    return ImageFont.truetype(path, size)


def serif_bold(size):
    return _load(SERIF_BOLD, size)


def serif(size):
    return _load(SERIF, size)


def serif_italic(size):
    return _load(SERIF_ITALIC, size)


def sans(size):
    return _load(SANS, size)


def sans_bold(size):
    return _load(SANS_BOLD, size)


def wrap(draw, text, font, max_width):
    """Split text into lines that fit max_width, word by word."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=font) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def centred(draw, y, text, font, fill, centre_x=512):
    width = draw.textlength(text, font=font)
    draw.text((centre_x - width / 2, y), text, font=font, fill=fill)
    return y + font.size


def paragraph(draw, x, y, max_width, text, font, fill, leading):
    for line in wrap(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def rule(draw, y, width=2, colour=INK):
    draw.line([(40, y), (984, y)], fill=colour, width=width)


def masthead(draw):
    centred(draw, 24, "AN AI-DRAWN FRONT PAGE", sans(13), GREY)
    centred(draw, 46, "THE WORLD IN ONE IMAGE", serif_bold(60), INK)
    draw.rectangle([40, 122, 984, 168], fill=RED)
    centred(
        draw, 133,
        "SATURDAY  ·  21 NOVEMBER 2026",
        sans_bold(25), (255, 255, 255),
    )
    rule(draw, 180)
    rule(draw, 184)


def gulf_scene(draw, left, top, right, bottom):
    """Bahrain skyline on the Gulf: sun, clouds, towers, sea, ship, waves."""
    draw.rectangle([left, top, right, bottom], fill=SKY, outline=INK, width=2)
    # Sun with a soft halo, low over the far shore.
    draw.ellipse([right - 76, top + 10, right - 6, top + 80], fill=SUN)
    draw.ellipse(
        [right - 68, top + 18, right - 14, top + 72], fill=(244, 212, 120)
    )
    # Thin clouds drifting over the sky.
    for cx, cy, cw in (
        (left + 18, top + 22, 64),
        (left + 120, top + 44, 84),
        (left + 230, top + 18, 56),
    ):
        draw.ellipse([cx, cy, cx + cw, cy + 12], fill=(255, 255, 255))
        draw.ellipse(
            [cx + 12, cy - 6, cx + cw - 10, cy + 8], fill=(255, 255, 255)
        )
    # Skyline: towers of different heights along the far shore, each with
    # lit windows and a distinct roofline.
    base = bottom - 58
    towers = [
        (left + 12, base - 62, 30, TOWER, "flat"),
        (left + 48, base - 84, 28, TOWER, "point"),
        (left + 82, base - 52, 34, TOWER_LIT, "dome"),
        (left + 122, base - 76, 26, TOWER, "flat"),
        (left + 154, base - 92, 30, TOWER, "spire"),
        (left + 190, base - 66, 32, TOWER_LIT, "flat"),
        (left + 228, base - 86, 28, TOWER, "point"),
        (left + 262, base - 54, 30, TOWER, "dome"),
        (left + 298, base - 72, 26, TOWER, "flat"),
        (left + 330, base - 46, 28, TOWER_LIT, "flat"),
    ]
    for x, y, w, colour, roof in towers:
        draw.rectangle([x, y, x + w, base], fill=colour)
        if roof == "point":
            draw.polygon(
                [(x, y), (x + w // 2, y - 14), (x + w, y)], fill=colour
            )
        elif roof == "dome":
            draw.pieslice([x, y - 12, x + w, y + 12], 180, 360, fill=colour)
        elif roof == "spire":
            draw.polygon(
                [(x + 4, y), (x + w // 2, y - 26), (x + w - 4, y)],
                fill=colour,
            )
            draw.line(
                [(x + w // 2, y - 26), (x + w // 2, y - 34)],
                fill=colour, width=3,
            )
            draw.ellipse(
                [x + w // 2 - 3, y - 38, x + w // 2 + 3, y - 32], fill=SUN
            )
        # Lit windows in two columns down the face of each tower.
        for wy in range(y + 10, base - 8, 16):
            for wx in (x + 6, x + w - 10):
                draw.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 240, 180))
    # Sea, with wave lines breaking across it.
    draw.rectangle([left, base, right, bottom], fill=SEA)
    for i, wy in enumerate((base + 8, base + 16, base + 40, base + 48)):
        x0 = left + 12 + (i % 2) * 40
        draw.line([(x0, wy), (x0 + 70, wy)], fill=(255, 255, 255), width=2)
        draw.line(
            [(x0 + 110, wy + 3), (x0 + 170, wy + 3)],
            fill=(255, 255, 255), width=2,
        )
    # A naval ship crossing the Gulf, mast and funnel above the hull.
    hull_x = left + 96
    hull_y = base + 20
    draw.polygon(
        [(hull_x, hull_y), (hull_x + 150, hull_y),
         (hull_x + 132, hull_y + 18), (hull_x + 18, hull_y + 18)],
        fill=SHIP,
    )
    draw.rectangle([hull_x + 58, hull_y - 16, hull_x + 96, hull_y], fill=SHIP)
    draw.line(
        [(hull_x + 77, hull_y - 30), (hull_x + 77, hull_y - 16)],
        fill=SHIP, width=3,
    )
    draw.rectangle([hull_x + 104, hull_y - 14, hull_x + 118, hull_y], fill=SHIP)
    # Small red flag flying from the mast.
    draw.polygon(
        [(hull_x + 77, hull_y - 30), (hull_x + 92, hull_y - 26),
         (hull_x + 77, hull_y - 22)],
        fill=RED,
    )
    # Foam wake trailing behind the ship.
    for i, wy in enumerate((hull_y + 24, hull_y + 30, hull_y + 36)):
        draw.line(
            [(left + 16 + i * 10, wy), (left + 88 - i * 6, wy)],
            fill=(255, 255, 255), width=2,
        )
    # A small patrol boat near the far shore.
    boat_x = left + 268
    boat_y = base + 6
    draw.polygon(
        [(boat_x, boat_y), (boat_x + 44, boat_y),
         (boat_x + 36, boat_y + 8), (boat_x + 8, boat_y + 8)],
        fill=SHIP,
    )
    draw.rectangle([boat_x + 14, boat_y - 8, boat_x + 26, boat_y], fill=SHIP)


def lead(draw):
    draw.text((40, 198), "GULF CRISIS  ·  BAHRAIN", font=sans_bold(16), fill=RED)
    y = 224
    y = paragraph(
        draw, 40, y, 545,
        "Iran strikes US bases in Bahrain",
        serif_bold(41), INK, 50,
    )
    y += 6
    paragraph(
        draw, 40, y, 545,
        "Iran's Revolutionary Guards said they hit two US military "
        "positions in Bahrain, at al-Riffa and Awali. Bahrain said a "
        "civilian industrial facility was hit and caught fire; no "
        "injuries were reported.",
        sans(18), INK, 24,
    )
    gulf_scene(draw, 612, 198, 984, 392)
    paragraph(
        draw, 612, 398, 372,
        "Bahrain's skyline on the Gulf; shipping through the Strait of "
        "Hormuz is at risk.",
        serif_italic(14), GREY, 19,
    )
    rule(draw, 448)


def card(draw, x, y, width, kicker, headline, body):
    draw.text((x, y), kicker, font=sans_bold(15), fill=RED)
    y += 24
    y = paragraph(draw, x, y, width, headline, serif_bold(21), INK, 26)
    y += 4
    paragraph(draw, x, y, width, body, sans(15), INK, 19)


def grid(draw):
    columns = [40, 363, 686]
    width = 298
    cards = [
        (
            "UKRAINE  ·  KRYVYI RIH",
            "Russian missile hits Zelensky's hometown",
            "A ballistic missile hits the centre: 2 killed, one a boy "
            "of 7, about 60 wounded. Two missiles and a suspected drone "
            "came down in Poland the day before.",
        ),
        (
            "MARKETS  ·  AI",
            "AI sell-off drags markets into correction",
            "The S&P 500 falls 3.7% on Friday, the Dow enters correction "
            "and the Nasdaq erases its 2026 gains. The Nikkei drops "
            "5.06%, the Hang Seng 3.79%.",
        ),
        (
            "MEXICO  ·  CARTEL",
            "Mexico captures FBI most-wanted cartel boss",
            "Special forces seize Fausto Isidro Meza Flores, 'El Chapo "
            "Isidro', in Guasave, Sinaloa. Gunfights and blockades "
            "follow: at least 11 dead, 8 detained.",
        ),
        (
            "CLIMATE  ·  COP31",
            "COP31 runs past deadline over fossil fuels",
            "The UN climate summit in Antalya runs into overtime without "
            "a deal. Nearly 200 countries disagree on fossil fuels, "
            "finance and targets.",
        ),
        (
            "EUROPE  ·  BRUSSELS",
            "UK and EU sign three post-Brexit deals",
            "In Brussels: British food exports, emissions trading and a "
            "youth experience scheme. PM Andy Burnham signs; rejoining "
            "the EU is on the table, says the foreign secretary.",
        ),
        (
            "SCIENCE  ·  MATHS",
            "AI-assisted Riemann proof claimed",
            "Anthropic mathematician Levent Alpöge says he used Claude "
            "to prove the Riemann hypothesis in six weeks. Two groups "
            "have verified his claim; wider checks will take time.",
        ),
    ]
    rows = [462, 650]
    for index, (kicker, headline, body) in enumerate(cards):
        row = index // 3
        col = index % 3
        card(draw, columns[col], rows[row], width, kicker, headline, body)
    for sep_x in (350, 673):
        draw.line([(sep_x, 462), (sep_x, 830)], fill=FAINT, width=1)
    rule(draw, 842)


def also_today(draw):
    draw.text((40, 854), "ALSO TODAY", font=sans_bold(17), fill=RED)
    briefs = [
        "Israeli strike kills three in Gaza food vehicle",
        "Saudi defences intercept three Houthi missiles",
        "Drones hit Russian cargo ship Sparta II",
        "France protests draw 82,500 nationwide",
        "Bolsonaro taken to ICU in Brasilia",
        "EU–Indonesia sign trade deal: 98.5% tariffs cut",
    ]
    left_x = 40
    right_x = 540
    y = 882
    for row in range(3):
        for col_x, text in ((left_x, briefs[row * 2]), (right_x, briefs[row * 2 + 1])):
            draw.ellipse([col_x, y + 5, col_x + 9, y + 14], fill=RED)
            draw.text((col_x + 18, y), text, font=sans(15), fill=INK)
        y += 26
    rule(draw, 956)
    centred(
        draw, 966,
        "Sources: One Turn · Reuters · NYT · Telegraph",
        sans(13), GREY,
    )
    centred(
        draw, 986,
        "Built 22 Nov 2026, covering news reported on 21 Nov 2026",
        sans(13), GREY,
    )


def render_image():
    image = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(image)
    masthead(draw)
    lead(draw)
    grid(draw)
    also_today(draw)
    return image


def main():
    image = render_image()
    image.save("entry.png", format="PNG")


if __name__ == "__main__":
    main()
