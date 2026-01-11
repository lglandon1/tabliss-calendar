import datetime
import calendar
import holidays
import base64

def generate_css():
    now = datetime.datetime.now()
    year, month, day = now.year, now.month, now.day
    
    # --- CONFIGURATION ---
    # Colors (Dracula Theme)
    C_BG = "#282a36"       # Background
    C_FG = "#f8f8f2"       # Text
    C_PINK = "#ff79c6"     # Today Highlight
    C_PURPLE = "#bd93f9"   # Holiday Text/Shading
    C_CYAN_LOW = "rgba(139, 233, 253, 0.1)" # Weekend Shading
    C_BORDER = "#6272a4"   # Border color
    
    # --- HOLIDAY LOGIC (US + KUWAIT) ---
    us_hols = holidays.US(years=year)
    kw_hols = holidays.CountryHoliday('KW', years=year)
    
    # --- SVG GENERATION ---
    # Canvas Size
    width, height = 300, 340
    
    # Start SVG String
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']
    
    # 1. Main Card Background
    svg.append(f'<rect x="0" y="0" width="{width}" height="{height}" rx="15" fill="{C_BG}" stroke="{C_BORDER}" stroke-width="4"/>')
    
    # 2. Header (Month Year)
    header_text = datetime.date(year, month, 1).strftime("%B %Y").upper()
    svg.append(f'<text x="{width/2}" y="40" font-family="Courier New, monospace" font-size="20" font-weight="bold" fill="{C_FG}" text-anchor="middle" letter-spacing="2">{header_text}</text>')
    
    # 3. Days Header (S M T W T F S)
    days = ["S", "M", "T", "W", "T", "F", "S"]
    start_x, start_y = 30, 80
    col_width = 40
    row_height = 40
    
    for i, d in enumerate(days):
        x = start_x + (i * col_width)
        # Highlight Friday/Saturday in header slightly
        color = C_PURPLE if i in [5, 6] else C_FG 
        svg.append(f'<text x="{x}" y="{start_y}" font-family="Courier New, monospace" font-size="16" font-weight="bold" fill="{color}" text-anchor="middle">{d}</text>')
    
    # 4. Calendar Grid
    cal = calendar.Calendar(firstweekday=6) # Sunday start
    month_days = cal.monthdayscalendar(year, month)
    
    grid_start_y = 120
    
    for r_idx, week in enumerate(month_days):
        for c_idx, d in enumerate(week):
            if d == 0: continue # Empty day
            
            # Coordinates for this cell
            cx = start_x + (c_idx * col_width)
            cy = grid_start_y + (r_idx * row_height)
            
            # Check logic
            current_date = datetime.date(year, month, d)
            is_today = (d == day)
            is_weekend = (c_idx == 5 or c_idx == 6) # Friday (5) or Saturday (6)
            
            # Holiday Name Check
            h_name = us_hols.get(current_date) or kw_hols.get(current_date)
            
            # --- LAYERS ---
            
            # Layer A: Shading (Weekend or Holiday)
            if h_name or is_weekend:
                fill = C_PURPLE if h_name else C_CYAN_LOW
                opacity = "0.4" if h_name else "1"
                # Draw rect centered on the number
                svg.append(f'<rect x="{cx-18}" y="{cy-18}" width="36" height="30" rx="6" fill="{fill}" fill-opacity="{opacity}" />')

            # Layer B: TODAY Highlight (Pink Circle) - Draws ON TOP of shading
            if is_today:
                svg.append(f'<circle cx="{cx}" cy="{cy-5}" r="16" fill="{C_PINK}" />')
            
            # Layer C: The Number
            # If it's today, make text dark (so it pops on pink). Else white.
            text_color = "#282a36" if is_today else C_FG
            svg.append(f'<text x="{cx}" y="{cy}" font-family="Courier New, monospace" font-size="16" font-weight="bold" fill="{text_color}" text-anchor="middle">{d}</text>')

    # 5. Footer (Holiday Name)
    today_holiday = us_hols.get(datetime.date(year, month, day)) or kw_hols.get(datetime.date(year, month, day))
    if today_holiday:
        svg.append(f'<text x="{width/2}" y="{height-20}" font-family="Courier New, monospace" font-size="12" fill="{C_PURPLE}" text-anchor="middle">-- {today_holiday} --</text>')

    svg.append('</svg>')
    
    # --- OUTPUT ---
    svg_content = "".join(svg)
    # Encode to Base64 to embed directly in CSS
    b64_svg = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
    
    css = f"""
/* Generated SVG Calendar */
body::before {{
  content: "";
  display: block;
  position: fixed;
  top: 40px;
  right: 40px;
  width: {width}px;
  height: {height}px;
  z-index: 9999;
  background-image: url("data:image/svg+xml;base64,{b64_svg}");
  background-repeat: no-repeat;
  filter: drop-shadow(0 10px 20px rgba(0,0,0,0.5));
}}
"""
    
    with open("calendar.css", "w") as f:
        f.write(css)
    print("Success: SVG calendar generated.")

if __name__ == "__main__":
    generate_css()
