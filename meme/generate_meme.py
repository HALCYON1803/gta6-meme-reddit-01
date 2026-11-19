#!/usr/bin/env python3
"""Draw the gta6-meme-reddit-01 meme with PIL (no network, no fonts to install).

Joke (single panel, readable at 480 px): after waiting 13 years for GTA VI,
the download itself needs 13 more years. The make.fun ghost sits on the
download dialog, holding its magenta star coin, saying "worth it."

Layout (1024 x 1024):
  - Vice City sunset: purple -> magenta -> orange gradient, sun, skyline,
    palm silhouettes.
  - Top caption: INSTALLING GTA VI
  - Download dialog: 1% progress bar, TIME REMAINING: 13 YEARS
  - make.fun ghost mascot perched on the dialog (white body, thick black
    outline, black four-point sparkle eyes, round little hand, magenta coin
    with a white star) + speech bubble "worth it."
  - Bottom pill: make.fun + the line "where agents win real money"

Run: python3 meme/generate_meme.py  -> writes meme.png at the repo root.
"""

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "meme.png"

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, path=BOLD):
    return ImageFont.truetype(path, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def star4(cx, cy, r, fill):
    """Four-pointed sparkle (like the ghost's eyes): 8 polygon points."""
    k = 0.30
    pts = [
        (cx, cy - r),
        (cx + r * k, cy - r * k),
        (cx + r, cy),
        (cx + r * k, cy + r * k),
        (cx, cy + r),
        (cx - r * k, cy + r * k),
        (cx - r, cy),
        (cx - r * k, cy - r * k),
    ]
    return pts


def star5(cx, cy, r_out, r_in, fill):
    """Five-pointed star polygon."""
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        ang = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def draw_ghost(draw, cx, top, width, height):
    """make.fun ghost: white body, thick black outline, sparkle eyes,
    one round little hand holding a magenta coin with a white star.

    (cx, top) is the centre-top of the body; body is `width` wide and
    `height` tall including the wavy hem.
    """
    x0, x1 = cx - width / 2, cx + width / 2
    hem_y = top + height * 0.86

    def body_path(inset):
        # Bell shape: straight sides from the hem up to the dome's spring
        # line, an elliptical dome over the top, then three scallops back
        # along the hem from right to left. The hem's lowest points stay
        # `inset` inside the outline so the white body never pokes through
        # the black edge.
        bot_y = top + height - inset
        rx = width / 2 - inset
        ry = (hem_y - top - inset) / 2
        cy = top + inset + ry
        pts = [(x0 + inset, hem_y), (x0 + inset, cy)]
        steps = 40
        for i in range(steps + 1):
            ang = math.pi + i * math.pi / steps  # left -> over top -> right
            px = cx + rx * math.cos(ang)
            py = cy + ry * math.sin(ang)
            pts.append((px, py))
        pts.append((x1 - inset, hem_y))
        # Hem scallops, right to left: three bumps dipping to bot_y.
        n_bumps = 3
        seg = (x1 - inset - (x0 + inset)) / n_bumps
        for b in range(n_bumps):
            rx2 = x1 - inset - b * seg
            pts.append((rx2, hem_y))
            pts.append((rx2 - seg * 0.5, bot_y))
            pts.append((rx2 - seg, hem_y))
        return pts

    # Thick black outline: black body slightly larger, white body on top.
    draw.polygon(body_path(0), fill=(0, 0, 0))
    draw.polygon(body_path(9), fill=(255, 255, 255))

    # Eyes: two black four-pointed sparkles.
    eye_y = top + height * 0.38
    eye_dx = width * 0.20
    eye_r = width * 0.085
    for ex in (cx - eye_dx, cx + eye_dx):
        draw.polygon(star4(ex, eye_y, eye_r, (0, 0, 0)), fill=(0, 0, 0))

    # Round little hand + magenta coin with a white star, at the body's
    # right side, held up like the ghost is showing it off.
    hand_x, hand_y = cx + width * 0.52, top + height * 0.62
    # Short white arm from the body to the hand.
    draw.line(
        [(cx + width / 2 - 14, hand_y + 8), (hand_x - 8, hand_y + 4)],
        fill=(255, 255, 255),
        width=16,
    )
    draw.line(
        [(cx + width / 2 - 14, hand_y + 8), (hand_x - 8, hand_y + 4)],
        fill=(0, 0, 0),
        width=2,
    )
    draw.ellipse(
        [hand_x - 13, hand_y - 13, hand_x + 13, hand_y + 13],
        fill=(255, 255, 255),
        outline=(0, 0, 0),
        width=5,
    )
    coin_r = 38
    coin_cx, coin_cy = hand_x + 44, hand_y - 24
    draw.ellipse(
        [coin_cx - coin_r, coin_cy - coin_r, coin_cx + coin_r, coin_cy + coin_r],
        fill=(232, 0, 128),
        outline=(0, 0, 0),
        width=6,
    )
    draw.polygon(star5(coin_cx, coin_cy, 26, 11, (255, 255, 255)), fill=(255, 255, 255))
    return (coin_cx, coin_cy)


def main():
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # --- Sunset sky gradient: purple -> magenta -> orange -> warm yellow.
    stops = [
        (0.00, (38, 8, 74)),
        (0.30, (122, 16, 110)),
        (0.55, (216, 38, 110)),
        (0.75, (255, 110, 58)),
        (1.00, (255, 196, 107)),
    ]
    horizon = 760
    for y in range(horizon):
        t = y / horizon
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                col = lerp(c0, c1, (t - t0) / (t1 - t0))
                break
        else:
            col = stops[-1][1]
        draw.line([(0, y), (W, y)], fill=col)

    # Stars in the upper sky.
    rnd = random.Random(20261119)
    for _ in range(70):
        x = rnd.randint(10, W - 10)
        y = rnd.randint(10, 300)
        r = rnd.choice([1, 1, 2, 2, 3])
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255))

    # Sun, low over the skyline, up in the left sky so the card never hides it.
    draw.ellipse([180 - 145, 150, 180 + 145, 440], fill=(255, 214, 130))
    draw.ellipse([180 - 105, 190, 180 + 105, 400], fill=(255, 233, 168))

    # Skyline silhouette with lit windows.
    skyline = (28, 9, 51)
    buildings = [
        (0, 600, 120, 760), (95, 540, 190, 760), (175, 620, 260, 760),
        (250, 560, 340, 760), (330, 630, 420, 760), (410, 570, 500, 760),
        (490, 625, 580, 760), (570, 550, 660, 760), (650, 620, 740, 760),
        (730, 565, 820, 760), (810, 625, 900, 760), (890, 580, 1024, 760),
    ]
    for (x0, y0, x1, y1) in buildings:
        draw.rectangle([x0, y0, x1, y1], fill=skyline)
    for _ in range(90):
        bx = rnd.randint(0, len(buildings) - 1)
        x0, y0, x1, _ = buildings[bx]
        wx = rnd.randint(x0 + 8, x1 - 16)
        wy = rnd.randint(y0 + 12, 730)
        draw.rectangle([wx, wy, wx + 8, wy + 10], fill=(255, 214, 90))

    # Ground strip.
    draw.rectangle([0, 760, W, H], fill=(22, 7, 40))

    # No palm trees: the skyline, sun and gradient carry the Vice City
    # feel, and palm silhouettes read as stray curves at this scale.

    # --- Top caption.
    draw.text(
        (512, 70),
        "INSTALLING GTA VI",
        font=font(64),
        fill=(255, 255, 255),
        stroke_width=6,
        stroke_fill=(0, 0, 0),
        anchor="mm",
    )

    # --- Download dialog card.
    card = [110, 268, 914, 716]
    draw.rounded_rectangle(card, radius=36, fill=(16, 12, 44), outline=(255, 46, 136), width=6)
    draw.text(
        (512, 336),
        "GRAND THEFT AUTO VI  •  200 GB",
        font=font(38),
        fill=(255, 255, 255),
        anchor="mm",
    )
    # Progress track: a 2% sliver of magenta, the rest empty.
    track = [168, 420, 856, 478]
    draw.rounded_rectangle(track, radius=29, fill=(44, 33, 69))
    draw.rounded_rectangle([168, 420, 182, 478], radius=8, fill=(255, 46, 136))
    draw.text(
        (512, 560),
        "1%",
        font=font(104),
        fill=(255, 255, 255),
        stroke_width=4,
        stroke_fill=(0, 0, 0),
        anchor="mm",
    )
    draw.text(
        (512, 668),
        "TIME REMAINING: 13 YEARS",
        font=font(46),
        fill=(255, 210, 63),
        stroke_width=3,
        stroke_fill=(0, 0, 0),
        anchor="mm",
    )

    # --- Ghost mascot perched on the dialog's top edge, right side.
    ghost_cx, ghost_top = 810, 108
    draw_ghost(draw, ghost_cx, ghost_top, 185, 190)

    # Speech bubble: "worth it." (tail first, then the bubble over it).
    draw.polygon([(688, 196), (736, 228), (702, 210)], fill=(255, 255, 255))
    bubble = [542, 140, 708, 208]
    draw.rounded_rectangle(bubble, radius=26, fill=(255, 255, 255), outline=(0, 0, 0), width=5)
    draw.text((625, 174), "worth it.", font=font(32), fill=(0, 0, 0), anchor="mm")

    # --- Bottom: make.fun pill + the pitch line in the picture.
    draw.rounded_rectangle([250, 800, 774, 916], radius=58, fill=(232, 0, 128))
    draw.polygon(
        star5(306, 858, 24, 10, (255, 255, 255)), fill=(255, 255, 255)
    )
    draw.text(
        (565, 858),
        "make.fun",
        font=font(74),
        fill=(255, 255, 255),
        anchor="mm",
    )
    draw.text(
        (512, 968),
        "where agents win real money",
        font=font(36),
        fill=(255, 255, 255),
        stroke_width=2,
        stroke_fill=(0, 0, 0),
        anchor="mm",
    )

    img.save(OUT, "PNG")
    print(f"wrote {OUT} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
