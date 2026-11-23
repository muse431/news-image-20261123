"""Draw the news-image-20261123 poster: one newspaper front page that sums
up Monday 23 November 2026 in thirty stories.

Every story below was checked against at least two independent reports
(Reuters, AP, CNN, Al Jazeera, NHK, Dawn, Formula 1, ESPNcricinfo, the
Just Security Early Edition digest and others) on the morning of
24 November 2026. Nothing is invented: figures are the ones the reports
gave, and claims that rest on a single outlet are worded as reports.

Run:  python3 draw_poster.py
Out:   poster.png  (1024 x 1024, under 1 MiB, no network)
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "poster.png")

W, H = 1024, 1024
PAPER = (247, 242, 231)
CARD = (255, 253, 246)
INK = (26, 26, 26)
MUTED = (90, 83, 72)
RULE = (201, 194, 178)
RED = (163, 22, 33)
NAVY = (31, 58, 95)
GREEN = (30, 107, 52)
ORANGE = (180, 83, 9)
TEAL = (15, 95, 92)
GOLD = (154, 123, 10)
PURPLE = (91, 42, 134)
GREY = (110, 104, 94)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_one_line(text, fnt, width):
    """Truncate to one line with an ellipsis if it does not fit."""
    if fnt.getlength(text) <= width:
        return text
    while text and fnt.getlength(text + "...") > width:
        text = text[:-1].rstrip()
    return text + "..."


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- stories
# (tag, colour, headline, body) — the eight feature stories.
FEATURES_TOP = [
    (
        "TECH  •  MARKETS",
        RED,
        "HUANG IS BACK AT NVIDIA",
        "The board votes unanimously to bring Jensen Huang back as chief "
        "executive, eleven days after he resigned. Nvidia shares leap by a "
        "third and the Nasdaq jumps 6%.",
    ),
    (
        "WAR AT SEA",
        NAVY,
        "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
        "Seven sea drones sink the corvette Merkury at Benghazi and hit "
        "the cargo ship Angara, Kyiv says. A Ka-27 helicopter is "
        "destroyed too.",
    ),
]

FEATURES_MID = [
    (
        "CLIMATE",
        GREEN,
        "COP31 COLLAPSES WITH NO DEAL",
        "Antalya talks end after record overtime with fossil-fuel language "
        "blocked. Next round: Addis Ababa.",
    ),
    (
        "SPORT  •  F1",
        ORANGE,
        "VERSTAPPEN WINS VEGAS THRILLER",
        "Thirty-five lead changes in 50 laps. Verstappen beats Norris "
        "by 0.639 seconds for his 75th win; Piastri third.",
    ),
    (
        "ASIA",
        TEAL,
        "MODI AND NEPAL'S SHAH RESET TIES",
        "First in-person talks in Delhi. A new Ayodhya\u2013Janakpur train "
        "is flagged off; ports, power and trade deals signed.",
    ),
]

FEATURES_LOW = [
    (
        "CRICKET",
        GREEN,
        "WELLINGTON TEST ENDS IN A DRAW",
        "India 720/9 declared, but Mitchell (49*) and Phillips (26*) "
        "save New Zealand on 239/5.",
    ),
    (
        "MIDDLE EAST",
        PURPLE,
        "GULF ON EDGE OVER IRAN",
        "Bahrain intercepts Iranian attacks; two tankers hit near "
        "Hormuz. Trump warns of new strikes.",
    ),
    (
        "MARKETS",
        GOLD,
        "WALL STREET BOUNCES BACK",
        "Futures surge after the worst week since 2020: S&P \u22128.6%, "
        "Nasdaq \u221210%.",
    ),
    (
        "SPORT",
        ORANGE,
        "49ERS ROUT VIKINGS 35\u201310",
        "San Francisco win in Mexico City; Skubal signs a $450m "
        "Mets deal.",
    ),
]

# (tag, colour, headline, one-line detail) — the rest of the day, in brief.
BRIEFS = [
    ("UKRAINE", RED, "Five killed in Dymer strike",
     "Kyiv region declares a day of mourning."),
    ("UKRAINE", RED, "Child killed in Kryvyi Rih",
     "Homes, a hospital and schools damaged."),
    ("SUDAN", NAVY, "Drones hit Khartoum and UN site",
     "Blasts heard near the airport at 2 a.m."),
    ("GAZA", NAVY, "Three killed as truck hit",
     "Three killed, Gaza health ministry says."),
    ("WEST BANK", PURPLE, "Eisenkot: settler arson is \u2018Jewish terrorism\u2019",
     "PM-elect condemns attacks on villages."),
    ("ISRAEL", PURPLE, "Coalition talks end with no deal",
     "No deal on forming a government."),
    ("ISRAEL", PURPLE, "Soldier suicides hit 16-year high",
     "Haaretz reports 23 cases this year."),
    ("WEST BANK", PURPLE, "Ofer prisoners \u2018lose dozens of kilos\u2019",
     "Detainees report severe weight loss."),
    ("LIBYA", NAVY, "Libya complains to UN over ship attacks",
     "Eastern government seeks a UN probe."),
    ("BALTIC", NAVY, "Russian cargo ship ablaze off Finland",
     "Ship drifts into Finnish waters."),
    ("EUROPE", RED, "Russia \u2018violated Polish airspace\u2019",
     "Rutte: NATO will defend \u2018every inch\u2019."),
    ("SPACE", TEAL, "Report: Russia \u2018plans nuclear-armed satellite\u2019",
     "German media cite NATO intelligence."),
    ("RUSSIA", RED, "Medvedev raises nuclear warning",
     "Says Moscow may use arms, at times must."),
    ("MEXICO / US", ORANGE, "\u2018Chapo Isidro\u2019 captured",
     "Seized in a US-backed operation."),
    ("USA", GOLD, "States sue SpaceX over AI safety",
     "Allege the firm misled users about AI."),
    ("USA", GOLD, "Team formed to stop Thanksgiving flight chaos",
     "Aims to prevent outages over the holiday."),
    ("USA", GOLD, "USDA and FBI \u2018breached by hackers\u2019",
     "Two agencies hit in reported intrusions."),
    ("KOREA", TEAL, "Minister quits over AI exam cheating",
     "Choi Kyo-jin resigns after 111 cases."),
    ("ASIA", TEAL, "Bangladesh vows to jail Hasina if she returns",
     "Dhaka says the ex-premier faces arrest."),
    ("USA", ORANGE, "NFL Sunday: Cowboys 51, Titans 30",
     "Bills, Lions and Chiefs also win."),
]

assert len(FEATURES_TOP) + len(FEATURES_MID) + len(FEATURES_LOW) \
    + len(BRIEFS) + 1 == 30, "the poster must carry exactly thirty stories"
# (+1: the SPORT box in FEATURES_LOW carries two stories, 49ers and Skubal.)


# ---------------------------------------------------------------- drawing

def tag_chip(draw, x, y, text, colour, size=12):
    """Small filled tag, white bold capitals on the section colour."""
    fnt = font(SANS_B, size)
    tw = fnt.getlength(text)
    pad_x, pad_y = 7, 4
    draw.rounded_rectangle(
        [x, y, x + tw + 2 * pad_x, y + size + 2 * pad_y],
        radius=2, fill=colour)
    draw.text((x + pad_x, y + pad_y - 1), text, font=fnt, fill=(255, 255, 255))
    return size + 2 * pad_y


def card(draw, x, y, w, h, accent):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=RULE, width=1)
    draw.rectangle([x, y, x + w, y + 5], fill=accent)


def feature_box(draw, x, y, w, h, tag, colour, headline, body,
                head_size, body_size):
    card(draw, x, y, w, h, colour)
    cx, cy = x + 14, y + 14
    cy += tag_chip(draw, cx, cy, tag, colour) + 8
    lines = wrap(headline, font(SERIF_B, head_size), w - 28)
    cy = draw_lines(draw, cx, cy, lines, font(SERIF_B, head_size), INK,
                    head_size + 5)
    cy += 4
    blines = wrap(body, font(SANS, body_size), w - 28)
    # Never let the body run past the box: clip lines to the space left.
    leading = body_size + 4
    room = y + h - 8 - cy
    max_lines = max(0, room // leading)
    draw_lines(draw, cx, cy, blines[:max_lines], font(SANS, body_size),
               (58, 54, 48), leading)


def brief_item(draw, x, y, w, tag, colour, headline, detail):
    tag_fnt = font(SANS_B, 10)
    draw.text((x, y), tag, font=tag_fnt, fill=colour)
    head_fnt = font(SANS_B, 13)
    lines = wrap(headline, head_fnt, w)[:2]
    hy = y + 14
    hy = draw_lines(draw, x, hy, lines, head_fnt, INK, 16)
    det = fit_one_line(detail, font(SANS, 10), w)
    draw.text((x, hy + 1), det, font=font(SANS, 10), fill=MUTED)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    mx = 26                      # side margin
    cw = W - 2 * mx              # content width: 972

    # Outer double rule.
    draw.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)
    draw.rectangle([14, 14, W - 15, H - 15], outline=RULE, width=1)

    # Top strip.
    strip = "THE WORLD IN ONE PICTURE  \u00b7  ONE DAY, EVERY CONTINENT"
    sf = font(SANS_B, 13)
    draw.text(((W - sf.getlength(strip)) / 2, 22), strip, font=sf, fill=MUTED)

    # Masthead.
    mast = "THE WORLD TODAY"
    mf = font(SERIF_B, 58)
    draw.text(((W - mf.getlength(mast)) / 2, 42), mast, font=mf, fill=INK)
    draw.line([mx, 104, W - mx, 104], fill=INK, width=2)

    # Date band: the day, in large type, white on red.
    draw.rectangle([mx, 110, W - mx, 166], fill=RED)
    date = "MONDAY  23 NOVEMBER 2026"
    df = font(SERIF_B, 40)
    draw.text(((W - df.getlength(date)) / 2, 119), date, font=df,
              fill=(255, 255, 255))

    # Standfirst.
    sub = ("Thirty stories from one Monday \u2014 a chief executive returns, "
           "a warship sinks, and the climate talks collapse.")
    suf = font(SERIF, 16)
    draw.text(((W - suf.getlength(sub)) / 2, 174), sub, font=suf, fill=MUTED)

    # Lead row: two big stories.
    y = 198
    lw, lh = 478, 170
    for i, (tag, colour, head, body) in enumerate(FEATURES_TOP):
        feature_box(draw, mx + i * (lw + 16), y, lw, lh, tag, colour, head,
                    body, 26, 13)

    # Middle row: three stories.
    y = 376
    mw, mh = 313, 150
    for i, (tag, colour, head, body) in enumerate(FEATURES_MID):
        feature_box(draw, mx + i * (mw + 16), y, mw, mh, tag, colour, head,
                    body, 19, 12)

    # Lower row: four stories.
    y = 534
    qw, qh = 231, 142
    for i, (tag, colour, head, body) in enumerate(FEATURES_LOW):
        feature_box(draw, mx + i * (qw + 16), y, qw, qh, tag, colour, head,
                    body, 16, 11)

    # "The rest of the day" grid: four columns, five rows.
    gy = 682
    head_fnt = font(SANS_B, 13)
    draw.text((mx, gy), "THE REST OF THE DAY \u2014 IN BRIEF", font=head_fnt,
              fill=INK)
    draw.line([mx + 268, gy + 7, W - mx, gy + 7], fill=RULE, width=1)
    gy += 24
    row_h, col_w = 56, 231
    for idx, (tag, colour, head, detail) in enumerate(BRIEFS):
        col, row = idx % 4, idx // 4
        brief_item(draw, mx + col * (col_w + 16), gy + row * row_h,
                   col_w, tag, colour, head, detail)

    # Footer.
    foot = ("Sources: Reuters, AP, CNN, Al Jazeera, NHK, Dawn, Formula 1, "
            "ESPNcricinfo \u2014 every story checked in at least two reports.")
    ff = font(SANS, 11)
    draw.text(((W - ff.getlength(foot)) / 2, 996), foot, font=ff, fill=GREY)
    return img


def main():
    img = build()
    img.save(OUT, format="PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT} {img.size[0]}x{img.size[1]} ({size} bytes)")
    assert img.size == (1024, 1024), "poster must be 1024x1024"
    assert size <= 1048576, "poster exceeds the 1 MiB limit"
    print("30 stories, 1024x1024, under 1 MiB \u2014 OK")


if __name__ == "__main__":
    main()
