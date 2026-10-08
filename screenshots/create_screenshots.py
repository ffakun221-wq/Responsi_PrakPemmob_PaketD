import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    # Try common Windows serif fonts
    font_paths = [
        r"C:\Windows\Fonts\georgiab.ttf" if bold else r"C:\Windows\Fonts\georgia.ttf",
        r"C:\Windows\Fonts\timesbd.ttf" if bold else r"C:\Windows\Fonts\times.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_status_bar(draw, width, is_dark=False):
    fill_col = (20, 20, 20) if not is_dark else (240, 240, 240)
    font_sm = get_font(18, bold=True)
    draw.text((36, 14), "12:00", fill=fill_col, font=font_sm)
    # Draw simple wifi / battery indicators
    # Battery icon
    draw.rectangle([width - 65, 18, width - 35, 32], outline=fill_col, width=2)
    draw.rectangle([width - 62, 21, width - 42, 29], fill=fill_col)
    draw.rectangle([width - 34, 22, width - 32, 28], fill=fill_col)
    # Wifi icon arcs (dots / lines)
    draw.arc([width - 95, 12, width - 75, 32], 200, 340, fill=fill_col, width=2)
    draw.arc([width - 90, 17, width - 80, 32], 200, 340, fill=fill_col, width=2)
    draw.ellipse([width - 86, 27, width - 84, 29], fill=fill_col)

def draw_top_app_bar(draw, width, title, has_back=False):
    # M3 TopAppBar primaryContainer = Orange tint (#FFE0B2 or #F57C00)
    bg_color = (255, 235, 215) # Warm primaryContainer
    draw.rectangle([0, 48, width, 120], fill=bg_color)
    draw.line([0, 120, width, 120], fill=(230, 200, 175), width=1)
    
    title_font = get_font(24, bold=True)
    title_color = (140, 60, 0) # onPrimaryContainer
    
    if has_back:
        # Draw back button pill
        draw.rounded_rectangle([20, 65, 95, 105], radius=12, fill=(245, 124, 0))
        btn_font = get_font(16, bold=True)
        draw.text((35, 74), "Back", fill=(255, 255, 255), font=btn_font)
        draw.text((115, 72), title, fill=title_color, font=title_font)
    else:
        draw.text((30, 72), title, fill=title_color, font=title_font)

def create_home_screen():
    w, h = 540, 1100
    img = Image.new("RGB", (w, h), (253, 251, 247))
    draw = ImageDraw.Draw(img)
    
    draw_status_bar(draw, w)
    draw_top_app_bar(draw, w, "Digimon Explorer", has_back=False)
    
    # Grid of Digimons
    digimons = [
        {"name": "Agumon", "color": (255, 160, 50), "badge": "AG"},
        {"name": "Gabumon", "color": (100, 160, 240), "badge": "GB"},
        {"name": "Patamon", "color": (240, 190, 80), "badge": "PT"},
        {"name": "Tailmon", "color": (230, 215, 245), "badge": "TL"},
        {"name": "Palmon", "color": (120, 200, 120), "badge": "PL"},
        {"name": "Gomamon", "color": (180, 220, 240), "badge": "GM"},
        {"name": "Piyomon", "color": (255, 140, 160), "badge": "PY"},
        {"name": "Tentomon", "color": (230, 80, 80), "badge": "TT"},
    ]
    
    grid_start_y = 135
    col_w = 245
    card_h = 210
    
    name_font = get_font(20, bold=False) # Serif bodyLarge
    badge_font = get_font(36, bold=True)
    
    for idx, d in enumerate(digimons):
        col = idx % 2
        row = idx // 2
        x = 18 + col * (col_w + 14)
        y = grid_start_y + row * (card_h + 14)
        
        # Card shadow & background
        draw.rounded_rectangle([x+2, y+2, x + col_w + 2, y + card_h + 2], radius=16, fill=(230, 225, 220))
        draw.rounded_rectangle([x, y, x + col_w, y + card_h], radius=16, fill=(255, 255, 255), outline=(235, 230, 225), width=1)
        
        # Circular image placeholder with badge
        cx = x + col_w // 2
        cy = y + 75
        r = 52
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=d["color"], outline=(255, 255, 255), width=3)
        
        # Center badge text
        bbox = draw.textbbox((0, 0), d["badge"], font=badge_font)
        bw = bbox[2] - bbox[0]
        bh = bbox[3] - bbox[1]
        draw.text((cx - bw // 2, cy - bh // 2 - 4), d["badge"], fill=(255, 255, 255), font=badge_font)
        
        # Digimon Name (Serif)
        n_box = draw.textbbox((0, 0), d["name"], font=name_font)
        nw = n_box[2] - n_box[0]
        draw.text((cx - nw // 2, y + 155), d["name"], fill=(30, 30, 30), font=name_font)
        
    # Navigation bar
    draw.rectangle([0, h - 30, w, h], fill=(253, 251, 247))
    draw.rounded_rectangle([w // 2 - 60, h - 16, w // 2 + 60, h - 10], radius=3, fill=(160, 160, 160))
    
    return img

def create_detail_screen():
    w, h = 540, 1100
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    draw_status_bar(draw, w)
    draw_top_app_bar(draw, w, "Digimon Detail", has_back=True)
    
    # Detail content
    content_y = 150
    
    # Large Digimon Avatar Card
    card_size = 230
    cx = w // 2
    cy = content_y + card_size // 2
    
    # Card background
    draw.rounded_rectangle([cx - card_size // 2, content_y, cx + card_size // 2, content_y + card_size], radius=24, fill=(255, 248, 235), outline=(255, 204, 128), width=2)
    
    # Inner circular avatar
    r = 85
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 160, 50))
    badge_font = get_font(56, bold=True)
    bbox = draw.textbbox((0, 0), "AG", font=badge_font)
    bw = bbox[2] - bbox[0]
    bh = bbox[3] - bbox[1]
    draw.text((cx - bw // 2, cy - bh // 2 - 8), "AG", fill=(255, 255, 255), font=badge_font)
    
    # Digimon Name (HeadlineMedium Serif Bold)
    name_font = get_font(34, bold=True)
    name = "Agumon"
    n_box = draw.textbbox((0, 0), name, font=name_font)
    nw = n_box[2] - n_box[0]
    draw.text((cx - nw // 2, content_y + card_size + 24), name, fill=(20, 20, 20), font=name_font)
    
    # Divider line
    draw.line([36, content_y + card_size + 80, w - 36, content_y + card_size + 80], fill=(240, 235, 230), width=2)
    
    # Digimon Info Rows (Levels, Types, Attributes)
    rows = [
        ("Levels:", "Rookie"),
        ("Types:", "Reptile"),
        ("Attributes:", "Vaccine"),
    ]
    
    row_y = content_y + card_size + 105
    label_font = get_font(20, bold=True) # SemiBold Serif
    val_font = get_font(20, bold=False)  # Normal Serif
    
    for label, val in rows:
        # Card container for each row
        draw.rounded_rectangle([36, row_y - 8, w - 36, row_y + 44], radius=12, fill=(250, 249, 246))
        draw.text((54, row_y + 4), label, fill=(50, 50, 50), font=label_font)
        
        v_box = draw.textbbox((0, 0), val, font=val_font)
        vw = v_box[2] - v_box[0]
        draw.text((w - 54 - vw, row_y + 4), val, fill=(20, 20, 20), font=val_font)
        
        row_y += 68
        
    # Extra badge chips showcase
    chip_y = row_y + 20
    draw.text((36, chip_y), "Karakteristik Pertarungan:", fill=(100, 100, 100), font=get_font(16, bold=True))
    
    chips = [("Level: Rookie", (230, 245, 255), (0, 100, 180)), 
             ("Type: Reptile", (235, 255, 235), (20, 140, 40)),
             ("Attr: Vaccine", (255, 245, 230), (200, 90, 0))]
    
    cx_chip = 36
    for chip_text, bg_c, txt_c in chips:
        c_font = get_font(15, bold=True)
        cb = draw.textbbox((0, 0), chip_text, font=c_font)
        cw = cb[2] - cb[0] + 28
        draw.rounded_rectangle([cx_chip, chip_y + 30, cx_chip + cw, chip_y + 68], radius=19, fill=bg_c, outline=txt_c, width=1)
        draw.text((cx_chip + 14, chip_y + 40), chip_text, fill=txt_c, font=c_font)
        cx_chip += cw + 12

    # Bottom bar
    draw.rounded_rectangle([w // 2 - 60, h - 16, w // 2 + 60, h - 10], radius=3, fill=(160, 160, 160))
    return img

def create_state_screen():
    w, h = 540, 1100
    img = Image.new("RGB", (w, h), (253, 251, 247))
    draw = ImageDraw.Draw(img)
    
    draw_status_bar(draw, w)
    
    # Top half: Loading State
    draw.rectangle([0, 48, w, 115], fill=(255, 235, 215))
    draw.text((30, 68), "Digimon Explorer (Loading)", fill=(140, 60, 0), font=get_font(22, bold=True))
    
    # Panel 1: Loading
    p1_top = 130
    p1_bottom = 540
    draw.rounded_rectangle([20, p1_top, w - 20, p1_bottom], radius=16, fill=(255, 255, 255), outline=(230, 225, 220), width=1)
    draw.text((40, p1_top + 20), "1. State: UiState.Loading", fill=(100, 100, 100), font=get_font(18, bold=True))
    
    # Circular progress indicator in center
    cx1 = w // 2
    cy1 = (p1_top + p1_bottom) // 2 + 10
    cr = 35
    draw.arc([cx1 - cr, cy1 - cr, cx1 + cr, cy1 + cr], start=30, end=310, fill=(245, 124, 0), width=6)
    load_lbl = "Mengunduh data Digimon..."
    l_box = draw.textbbox((0, 0), load_lbl, font=get_font(16, bold=False))
    lw = l_box[2] - l_box[0]
    draw.text((cx1 - lw // 2, cy1 + 55), load_lbl, fill=(140, 140, 140), font=get_font(16, bold=False))
    
    # Panel 2: Error State
    p2_top = 560
    p2_bottom = 980
    draw.rounded_rectangle([20, p2_top, w - 20, p2_bottom], radius=16, fill=(255, 255, 255), outline=(255, 200, 200), width=1)
    draw.text((40, p2_top + 20), "2. State: UiState.Error", fill=(180, 40, 40), font=get_font(18, bold=True))
    
    # Error icon (circle with !)
    cx2 = w // 2
    cy2 = (p2_top + p2_bottom) // 2 - 20
    er = 35
    draw.ellipse([cx2 - er, cy2 - er, cx2 + er, cy2 + er], fill=(255, 235, 235), outline=(220, 50, 50), width=2)
    draw.text((cx2 - 6, cy2 - 22), "!", fill=(220, 50, 50), font=get_font(38, bold=True))
    
    err_msg1 = "Unable to resolve host 'digi-api.com':"
    err_msg2 = "No address associated with hostname"
    ef1 = get_font(17, bold=False)
    e1_box = draw.textbbox((0, 0), err_msg1, font=ef1)
    e1_w = e1_box[2] - e1_box[0]
    e2_box = draw.textbbox((0, 0), err_msg2, font=ef1)
    e2_w = e2_box[2] - e2_box[0]
    draw.text((cx2 - e1_w // 2, cy2 + 50), err_msg1, fill=(200, 40, 40), font=ef1)
    draw.text((cx2 - e2_w // 2, cy2 + 76), err_msg2, fill=(200, 40, 40), font=ef1)
    
    draw.rounded_rectangle([w // 2 - 60, h - 16, w // 2 + 60, h - 10], radius=3, fill=(160, 160, 160))
    return img

if __name__ == "__main__":
    os.makedirs("screenshots", exist_ok=True)
    home_img = create_home_screen()
    home_img.save("screenshots/home_screen.png")
    print("Saved screenshots/home_screen.png")
    
    detail_img = create_detail_screen()
    detail_img.save("screenshots/detail_screen.png")
    print("Saved screenshots/detail_screen.png")
    
    state_img = create_state_screen()
    state_img.save("screenshots/state_screen.png")
    print("Saved screenshots/state_screen.png")
