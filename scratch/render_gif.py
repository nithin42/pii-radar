"""
Script to render an animated terminal GIF for pii-radar showing the complete end-to-end workflow:
1. Installation: pip install pii-radar
2. Scanning CSV: pii-radar scan data/customers.csv --fail-on-detect
3. Rich colored PII detection report table output.
"""

from PIL import Image, ImageDraw, ImageFont

def render_pii_radar_gif(output_gif_path="demo.gif"):
    # Dark theme colors (Catppuccin Mocha)
    BG_COLOR = (30, 30, 46)        # #1E1E2E
    HEADER_BG = (24, 24, 37)       # #181825
    TEXT_COLOR = (205, 214, 244)   # #CDD6F4
    GREEN = (166, 227, 161)        # #A6E3A1
    CYAN = (137, 220, 235)         # #89DCEB
    YELLOW = (249, 226, 175)       # #F9E2AF
    RED = (243, 139, 168)          # #F38BA8
    MUTED = (108, 112, 134)        # #6C7086

    WIDTH = 940
    HEIGHT = 580
    FONT_SIZE = 14

    try:
        font = ImageFont.truetype("consola.ttf", FONT_SIZE)
        font_bold = ImageFont.truetype("consolab.ttf", FONT_SIZE)
    except IOError:
        font = ImageFont.load_default()
        font_bold = font

    # Full End-to-End Installation + Audit script for pii-radar
    lines_script = [
        ("> pip install pii-radar", CYAN, True),
        ("Downloading pii_radar-0.5.0-py3-none-any.whl (28 kB)", MUTED, False),
        ("Successfully installed pii-radar-0.5.0 click-8.1.7 pandas-2.2.0 rich-13.7.0", GREEN, False),
        ("", TEXT_COLOR, False),
        ("> pii-radar scan data/customers.csv --fail-on-detect", CYAN, True),
        ("Scanning data/customers.csv for PII vulnerabilities (1,000 rows)...", YELLOW, False),
        ("Scanned 1,000 rows across 8 columns in 0.04s (25,000 rows/sec)", MUTED, False),
        ("", TEXT_COLOR, False),
        ("                      pii-radar Detection Summary                      ", CYAN, True),
        ("+------------------------------------------------------------------------+", MUTED, False),
        ("| PII Type        | Matches | Sample Value       | Column      | Risk    |", TEXT_COLOR, True),
        ("|-----------------+---------+--------------------+-------------+---------|", MUTED, False),
        ("| SSN             |   142   | ***-**-6789        | ssn         |  CRITICAL |", RED, True),
        ("|-----------------+---------+--------------------+-------------+---------|", MUTED, False),
        ("| CREDIT_CARD     |    98   | ************4321   | card_num    |  HIGH   |", RED, True),
        ("|-----------------+---------+--------------------+-------------+---------|", MUTED, False),
        ("| EMAIL           |   412   | jo***@example.com  | email       |  MEDIUM |", YELLOW, False),
        ("|-----------------+---------+--------------------+-------------+---------|", MUTED, False),
        ("| PHONE           |   305   | (555) ***-4321     | phone       |  MEDIUM |", YELLOW, False),
        ("|-----------------+---------+--------------------+-------------+---------|", MUTED, False),
        ("| IP_ADDRESS      |    45   | 192.168.***.***    | last_ip     |  LOW    |", GREEN, False),
        ("+------------------------------------------------------------------------+", MUTED, False),
        ("+---------------------------- Scan Summary -------------------------------+", MUTED, False),
        ("| File: data/customers.csv (Format: CSV, Size: 184 KB)                    |", TEXT_COLOR, False),
        ("| Total PII Instances Detected: 1,002 across 5 columns                    |", RED, True),
        ("| Security Gate Status: FAIL (--fail-on-detect triggered)                 |", RED, True),
        ("+-------------------------------------------------------------------------+", MUTED, False),
        ("", TEXT_COLOR, False),
        ("Exit code 1: Critical PII data leakage detected in data/customers.csv!", RED, True)
    ]

    frames = []

    # Progressive reveal frame generation
    for step in range(1, len(lines_script) + 1):
        img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
        draw = ImageDraw.Draw(img)

        # Draw Window Bar
        draw.rectangle([0, 0, WIDTH, 36], fill=HEADER_BG)
        draw.ellipse([15, 12, 27, 24], fill=(255, 95, 86))   # Red dot
        draw.ellipse([35, 12, 47, 24], fill=(255, 189, 46))  # Yellow dot
        draw.ellipse([55, 12, 67, 24], fill=(39, 201, 63))   # Green dot

        # Draw Window Title
        draw.text((WIDTH // 2 - 120, 10), "zsh — pii-radar scan (data governance)", font=font, fill=MUTED)

        # Draw terminal lines
        y = 50
        for i in range(step):
            text, color, is_bold = lines_script[i]
            f = font_bold if is_bold else font
            draw.text((20, y), text, font=f, fill=color)
            y += 16

        frames.append(img)

    # Add hold frames at the end
    last_frame = frames[-1]
    for _ in range(18):
        frames.append(last_frame)

    # Save animated GIF
    frames[0].save(
        output_gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=220,
        loop=0
    )
    print(f"pii-radar GIF successfully generated: {output_gif_path}")

if __name__ == "__main__":
    render_pii_radar_gif()
