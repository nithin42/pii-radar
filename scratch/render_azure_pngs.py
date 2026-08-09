"""
Script to generate 2 pixel-perfect, official Microsoft Azure architecture PNG diagrams:
1. azure_blob_pii_flow.png (Flow 1: Azure Blob Storage PII Redaction)
2. azure_eventhub_pii_flow.png (Flow 2: Real-Time Event Hubs PII Redaction)
"""

import os
from PIL import Image, ImageDraw, ImageFont

def draw_azure_logo(draw, x, y):
    # Azure 'A' shape
    # Left triangle
    draw.polygon([(x+18, y), (x, y+34), (x+11, y+34), (x+18, y+19), (x+29, y+34), (x+40, y+34)], fill=(0, 120, 212))
    # Right cyan accent
    draw.polygon([(x+23, y+23), (x+13, y+34), (x+38, y+34)], fill=(80, 230, 255))

def draw_ms_logo(draw, x, y):
    # Microsoft 4 square logo
    draw.rectangle([x, y, x+12, y+12], fill=(242, 80, 34))
    draw.rectangle([x+15, y, x+27, y+12], fill=(127, 186, 0))
    draw.rectangle([x, y+15, x+12, y+27], fill=(0, 164, 239))
    draw.rectangle([x+15, y+15, x+27, y+27], fill=(255, 185, 0))

def draw_circle_badge(draw, cx, cy, radius, number_str, font, bg_color=(16, 124, 65)):
    draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius], fill=bg_color)
    # Draw number centered
    draw.text((cx-5, cy-9), str(number_str), fill=(255, 255, 255), font=font)

def create_flow_1_png(output_path="azure_blob_pii_flow.png"):
    W, H = 1200, 675
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("segoeuib.ttf", 32)
        font_header = ImageFont.truetype("segoeui.ttf", 22)
        font_bold = ImageFont.truetype("segoeuib.ttf", 16)
        font_regular = ImageFont.truetype("segoeui.ttf", 14)
        font_small = ImageFont.truetype("segoeui.ttf", 12)
        font_badge = ImageFont.truetype("segoeuib.ttf", 15)
    except IOError:
        font_title = font_header = font_bold = font_regular = font_small = font_badge = ImageFont.load_default()

    # Title
    draw.text((50, 45), "Flow 1: Azure Blob Storage PII Redaction", fill=(0, 0, 0), font=font_title)

    # Azure Dashed Outer Boundary Box
    # Using a series of small rectangles for dashed effect
    dash_color = (0, 120, 212)
    bx, by, bw, bh = 250, 130, 900, 450
    
    # Draw dashed rectangle
    for x in range(bx, bx+bw, 12):
        draw.line([(x, by), (min(x+6, bx+bw), by)], fill=dash_color, width=2)
        draw.line([(x, by+bh), (min(x+6, bx+bw), by+bh)], fill=dash_color, width=2)
    for y in range(by, by+bh, 12):
        draw.line([(bx, y), (bx, min(y+6, by+bh))], fill=dash_color, width=2)
        draw.line([(bx+bw, y), (bx+bw, min(y+6, by+bh))], fill=dash_color, width=2)

    # Azure Header inside Box
    draw_azure_logo(draw, 275, 150)
    draw.text((325, 155), "Azure", fill=(0, 120, 212), font=font_header)

    # Step 1: Applications (Left)
    draw_circle_badge(draw, 170, 260, 15, "1", font_badge)
    draw.text((140, 290), "Upload\nCSV files", fill=(51, 51, 51), font=font_regular)

    # App Icon (Stacked files)
    draw.rectangle([70, 340, 120, 400], fill=(255, 255, 255), outline=(85, 85, 85), width=2)
    draw.rectangle([80, 330, 130, 390], fill=(255, 255, 255), outline=(85, 85, 85), width=2)
    draw.rectangle([90, 320, 140, 380], fill=(255, 255, 255), outline=(51, 51, 51), width=2)
    draw.line([(100, 335), (130, 335)], fill=(51, 51, 51), width=2)
    draw.line([(100, 348), (130, 348)], fill=(51, 51, 51), width=2)
    draw.line([(100, 361), (120, 361)], fill=(51, 51, 51), width=2)
    draw.text((115, 410), "Applications", fill=(34, 34, 34), font=font_bold, anchor="ms")

    # Arrow 1 -> Blob Storage
    draw.line([(175, 350), (285, 350)], fill=(51, 51, 51), width=2)
    draw.polygon([(285, 345), (295, 350), (285, 355)], fill=(51, 51, 51))

    # Step 2: Azure Blob Storage
    draw.rounded_rectangle([295, 320, 365, 375], fill=(0, 120, 212), radius=6)
    draw.rectangle([299, 324, 327, 345], fill=(113, 175, 229))
    draw.rectangle([333, 324, 361, 345], fill=(113, 175, 229))
    draw.rectangle([299, 349, 327, 370], fill=(113, 175, 229))
    draw.rectangle([333, 349, 361, 370], fill=(255, 255, 255))
    draw.text((330, 400), "Azure Blob\nStorage", fill=(34, 34, 34), font=font_bold, anchor="ms", align="center")

    # Arrow Blob -> Event Grid
    draw.line([(375, 350), (465, 350)], fill=(51, 51, 51), width=2)
    draw.polygon([(465, 345), (475, 350), (465, 355)], fill=(51, 51, 51))

    # Badge 2
    draw_circle_badge(draw, 420, 260, 15, "2", font_badge)

    # Event Grid Node
    draw.rounded_rectangle([475, 320, 540, 385], fill=(0, 120, 212), radius=8)
    draw.ellipse([497, 342, 517, 362], fill=(255, 255, 255))
    draw.ellipse([482, 327, 492, 337], fill=(255, 255, 255))
    draw.ellipse([522, 327, 532, 337], fill=(255, 255, 255))
    draw.ellipse([482, 367, 492, 377], fill=(255, 255, 255))
    draw.ellipse([522, 367, 532, 377], fill=(255, 255, 255))
    draw.text((507, 410), "Event Grid", fill=(34, 34, 34), font=font_bold, anchor="ms")

    # Arrow Event Grid -> pii-radar
    draw.line([(545, 350), (625, 350)], fill=(51, 51, 51), width=2)
    draw.polygon([(625, 345), (635, 350), (625, 355)], fill=(51, 51, 51))

    # Step 3: pii-radar Container Box
    draw.rectangle([635, 240, 905, 470], fill=(242, 242, 242), outline=(204, 204, 204), width=1)
    
    # pii-radar logo inside
    draw.text((700, 260), "pii-radar", fill=(51, 51, 51), font=font_header)
    draw.ellipse([670, 265, 680, 275], fill=(0, 120, 212))
    draw.ellipse([682, 257, 692, 267], fill=(0, 120, 212))
    draw.ellipse([682, 273, 692, 283], fill=(0, 120, 212))
    draw.ellipse([694, 265, 704, 275], fill=(0, 120, 212))

    # App Service Hexagon
    hex_pts = [(770, 310), (805, 330), (805, 370), (770, 390), (735, 370), (735, 330)]
    draw.polygon(hex_pts, fill=(0, 120, 212))
    draw.text((770, 340), "<...>", fill=(255, 255, 255), font=font_header, anchor="mm")

    draw.text((770, 415), "AzureBlobStreamRedactor", fill=(51, 51, 51), font=font_regular, anchor="ms")

    # Step Badge 3 inside pii-radar box
    draw_circle_badge(draw, 770, 440, 14, "3", font_badge)

    # Step Badge 3 Label below (CORRECTED FROM 4 TO 3!)
    draw_circle_badge(draw, 490, 475, 15, "3", font_badge)
    draw.text((515, 465), "Performs Luhn algorithm\nand PII regex redaction", fill=(34, 34, 34), font=font_regular)

    # Arrow pii-radar -> Output Branch
    draw.line([(905, 350), (970, 350)], fill=(51, 51, 51), width=2)
    draw.line([(970, 265), (970, 435)], fill=(51, 51, 51), width=2)

    draw.line([(970, 265), (1005, 265)], fill=(51, 51, 51), width=2)
    draw.polygon([(1005, 260), (1015, 265), (1005, 270)], fill=(51, 51, 51))

    draw.line([(970, 435), (1005, 435)], fill=(51, 51, 51), width=2)
    draw.polygon([(1005, 430), (1015, 435), (1005, 440)], fill=(51, 51, 51))

    # Step Badge 4 (Top Output)
    draw_circle_badge(draw, 775, 175, 15, "4", font_badge)
    draw.text((775, 200), "Save sanitized\nCSV data", fill=(34, 34, 34), font=font_regular, anchor="ms", align="center")

    # Badge 4 on branch
    draw_circle_badge(draw, 970, 350, 14, "4", font_badge)

    # Dest 1: Azure Blob Storage
    hex1 = [(1045, 230), (1075, 247), (1075, 282), (1045, 299), (1015, 282), (1015, 247)]
    draw.polygon(hex1, fill=(0, 120, 212))
    draw.rounded_rectangle([1033, 248, 1057, 280], fill=(255, 255, 255), radius=2)
    draw.text((1045, 264), "CSV", fill=(0, 120, 212), font=font_small, anchor="mm")
    draw.text((1045, 320), "Azure Blob\nStorage", fill=(34, 34, 34), font=font_bold, anchor="ms", align="center")

    # Dest 2: Azure Synapse
    hex2 = [(1045, 400), (1075, 417), (1075, 452), (1045, 469), (1015, 452), (1015, 417)]
    draw.polygon(hex2, fill=(0, 120, 212))
    draw.ellipse([1031, 420, 1059, 448], outline=(255, 255, 255), width=3)
    draw.text((1045, 490), "Azure Synapse", fill=(34, 34, 34), font=font_bold, anchor="ms")

    # Footer Microsoft Logo
    draw_ms_logo(draw, 45, 620)
    draw.text((80, 623), "Microsoft Azure", fill=(94, 94, 94), font=font_header)

    img.save(output_path, "PNG")
    print(f"Generated Flow 1 PNG: {output_path}")

def create_flow_2_png(output_path="azure_eventhub_pii_flow.png"):
    W, H = 1200, 675
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("segoeuib.ttf", 32)
        font_header = ImageFont.truetype("segoeui.ttf", 22)
        font_bold = ImageFont.truetype("segoeuib.ttf", 16)
        font_regular = ImageFont.truetype("segoeui.ttf", 14)
        font_small = ImageFont.truetype("segoeui.ttf", 12)
        font_badge = ImageFont.truetype("segoeuib.ttf", 15)
    except IOError:
        font_title = font_header = font_bold = font_regular = font_small = font_badge = ImageFont.load_default()

    # Title
    draw.text((50, 45), "Flow 2: Real-Time Event Hubs PII Redaction", fill=(0, 0, 0), font=font_title)

    # Azure Dashed Outer Boundary Box
    dash_color = (0, 120, 212)
    bx, by, bw, bh = 250, 130, 900, 450
    
    for x in range(bx, bx+bw, 12):
        draw.line([(x, by), (min(x+6, bx+bw), by)], fill=dash_color, width=2)
        draw.line([(x, by+bh), (min(x+6, bx+bw), by+bh)], fill=dash_color, width=2)
    for y in range(by, by+bh, 12):
        draw.line([(bx, y), (bx, min(y+6, by+bh))], fill=dash_color, width=2)
        draw.line([(bx+bw, y), (bx+bw, min(y+6, by+bh))], fill=dash_color, width=2)

    # Azure Header inside Box
    draw_azure_logo(draw, 275, 150)
    draw.text((325, 155), "Azure", fill=(0, 120, 212), font=font_header)

    # Step 1: Client Devices & Microservices (Left)
    draw_circle_badge(draw, 170, 260, 15, "1", font_badge)
    draw.text((140, 290), "Send HTTP\nTelemetry", fill=(51, 51, 51), font=font_regular)

    # Devices Icons
    draw.rectangle([70, 330, 100, 385], fill=(255, 255, 255), outline=(51, 51, 51), width=2)
    draw.rectangle([75, 338, 95, 374], fill=(241, 245, 249))
    
    draw.rectangle([115, 320, 175, 362], fill=(255, 255, 255), outline=(51, 51, 51), width=2)
    draw.rectangle([120, 325, 170, 355], fill=(241, 245, 249))
    draw.text((115, 410), "Client Devices &\nMicroservices", fill=(34, 34, 34), font=font_bold, anchor="ms", align="center")

    # Arrow 1 -> Event Hubs
    draw.line([(175, 350), (285, 350)], fill=(51, 51, 51), width=2)
    draw.polygon([(285, 345), (295, 350), (285, 355)], fill=(51, 51, 51))

    # Step 2: Azure Event Hubs
    draw_circle_badge(draw, 420, 260, 15, "2", font_badge)

    draw.rounded_rectangle([295, 320, 365, 375], fill=(0, 120, 212), radius=6)
    draw.rounded_rectangle([303, 330, 357, 338], fill=(255, 255, 255), radius=2)
    draw.rounded_rectangle([303, 343, 357, 351], fill=(255, 255, 255), radius=2)
    draw.rounded_rectangle([303, 356, 357, 364], fill=(255, 255, 255), radius=2)
    draw.text((330, 400), "Azure Event\nHubs", fill=(34, 34, 34), font=font_bold, anchor="ms", align="center")

    # Arrow Event Hubs -> pii-radar
    draw.line([(375, 350), (625, 350)], fill=(51, 51, 51), width=2)
    draw.polygon([(625, 345), (635, 350), (625, 355)], fill=(51, 51, 51))

    # Step 3: pii-radar Container Box
    draw.rectangle([635, 240, 905, 470], fill=(242, 242, 242), outline=(204, 204, 204), width=1)
    
    draw.text((700, 260), "pii-radar", fill=(51, 51, 51), font=font_header)
    draw.ellipse([670, 265, 680, 275], fill=(0, 120, 212))
    draw.ellipse([682, 257, 692, 267], fill=(0, 120, 212))
    draw.ellipse([682, 273, 692, 283], fill=(0, 120, 212))
    draw.ellipse([694, 265, 704, 275], fill=(0, 120, 212))

    # App Service Hexagon
    hex_pts = [(770, 310), (805, 330), (805, 370), (770, 390), (735, 370), (735, 330)]
    draw.polygon(hex_pts, fill=(16, 124, 65))
    draw.text((770, 340), "<...>", fill=(255, 255, 255), font=font_header, anchor="mm")

    draw.text((770, 415), "AzureEventHubHandler", fill=(51, 51, 51), font=font_regular, anchor="ms")

    # Step Badge 3 inside box
    draw_circle_badge(draw, 770, 440, 14, "3", font_badge)

    # Step Badge 3 Label below (CORRECTED FROM 4 TO 3!)
    draw_circle_badge(draw, 490, 475, 15, "3", font_badge)
    draw.text((515, 465), "Masks SSN & Credit Cards\nin real-time stream batches", fill=(34, 34, 34), font=font_regular)

    # Arrow pii-radar -> Output Branch
    draw.line([(905, 350), (970, 350)], fill=(51, 51, 51), width=2)
    draw.line([(970, 265), (970, 435)], fill=(51, 51, 51), width=2)

    draw.line([(970, 265), (1005, 265)], fill=(51, 51, 51), width=2)
    draw.polygon([(1005, 260), (1015, 265), (1005, 270)], fill=(51, 51, 51))

    draw.line([(970, 435), (1005, 435)], fill=(51, 51, 51), width=2)
    draw.polygon([(1005, 430), (1015, 435), (1005, 440)], fill=(51, 51, 51))

    # Step Badge 4 (Top Output)
    draw_circle_badge(draw, 775, 175, 15, "4", font_badge)
    draw.text((775, 200), "Forward clean\ntelemetry stream", fill=(34, 34, 34), font=font_regular, anchor="ms", align="center")

    # Badge 4 on branch
    draw_circle_badge(draw, 970, 350, 14, "4", font_badge)

    # Dest 1: Azure Stream Analytics
    hex1 = [(1045, 230), (1075, 247), (1075, 282), (1045, 299), (1015, 282), (1015, 247)]
    draw.polygon(hex1, fill=(0, 120, 212))
    draw.ellipse([1033, 248, 1057, 280], outline=(255, 255, 255), width=2)
    draw.text((1045, 320), "Azure Stream\nAnalytics", fill=(34, 34, 34), font=font_bold, anchor="ms", align="center")

    # Dest 2: Azure Databricks
    hex2 = [(1045, 400), (1075, 417), (1075, 452), (1045, 469), (1015, 452), (1015, 417)]
    draw.polygon(hex2, fill=(255, 54, 33))
    draw.text((1045, 490), "Azure Databricks", fill=(34, 34, 34), font=font_bold, anchor="ms")

    # Footer Microsoft Logo
    draw_ms_logo(draw, 45, 620)
    draw.text((80, 623), "Microsoft Azure", fill=(94, 94, 94), font=font_header)

    img.save(output_path, "PNG")
    print(f"Generated Flow 2 PNG: {output_path}")

if __name__ == "__main__":
    create_flow_1_png()
    create_flow_2_png()
