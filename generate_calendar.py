import datetime
import calendar
import holidays

def generate_css():
    now = datetime.datetime.now()
    year, month, day = now.year, now.month, now.day
    
    # 1. Fetch Holidays for both US and Kuwait
    us_hols = holidays.US(years=year)
    kw_hols = holidays.KW(years=year) # Kuwait Country Code
    
    # Check if today is a holiday in either country
    current_date = datetime.date(year, month, day)
    holiday_name = us_hols.get(current_date) or kw_hols.get(current_date)
    
    # 2. Generate Calendar Grid (Sunday start)
    cal_obj = calendar.TextCalendar(calendar.SUNDAY)
    cal_str = cal_obj.formatmonth(year, month)
    lines = cal_str.splitlines()
    
    header = lines[0].strip().upper()
    days_header = " S  M  T  W  T  F  S"
    body_lines = [l for l in lines[2:] if l.strip()]
    body = " \\A ".join(body_lines)
    
    footer = f"\\A\\A-- {holiday_name} --" if holiday_name else ""
    full_content = f"{header} \\A {days_header} \\A {body} {footer}"

    # 3. FIX HIGHLIGHT MATH
    # Find weekday of the 1st (Monday=0, Sunday=6)
    first_weekday = datetime.date(year, month, 1).weekday()
    # Convert to Sunday=0 for our grid
    offset = (first_weekday + 1) % 7
    
    # Calculate grid position
    col = (day + offset - 1) % 7
    row = (day + offset - 1) // 7

    # Dracula Colors
    background = "#282a36"
    current_line = "#44475a"
    foreground = "#f8f8f2"
    comment = "#6272a4"
    pink = "#ff79c6"

    # Coordinates: 25px padding + slightly adjusted spacing
    h_pos = 24 + (col * 29.3)
    v_pos = 100 + (row * 28.8)

    css = f"""
body::before {{
  content: "{full_content}";
  position: fixed;
  top: 40px;
  right: 40px;
  z-index: 999;
  white-space: pre;
  font-family: "Courier New", Courier, monospace;
  font-size: 16px;
  font-weight: bold;
  line-height: 1.8;
  color: {foreground};
  padding: 25px;
  background: {background};
  border: 2px solid {comment};
  border-radius: 12px;
  text-align: center;
  box-shadow: 10px 10px 20px rgba(0,0,0,0.5);

  /* Dracula Highlight */
  background-image: radial-gradient(circle, {pink} 55%, transparent 60%);
  background-repeat: no-repeat;
  background-size: 32px 32px;
  background-position: {h_pos}px {v_pos}px;
}}"""
    
    with open("calendar.css", "w") as f:
        f.write(css)

if __name__ == "__main__":
    generate_css()
