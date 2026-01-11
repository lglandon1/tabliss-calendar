import datetime
import calendar
import holidays

def generate_css():
    now = datetime.datetime.now()
    year, month, day = now.year, now.month, now.day
    
    # 1. Fetch Holidays (US and Kuwait)
    us_hols = holidays.US(years=year)
    try:
        kw_hols = holidays.CountryHoliday('KW', years=year)
    except:
        kw_hols = {} # Fallback if library version differs
    
    current_date = datetime.date(year, month, day)
    holiday_name = us_hols.get(current_date) or kw_hols.get(current_date)
    
    # 2. Generate Calendar Grid (Sunday start)
    cal_obj = calendar.TextCalendar(calendar.SUNDAY)
    cal_str = cal_obj.formatmonth(year, month)
    lines = cal_str.splitlines()
    
    header = lines[0].strip().upper()
    # Highlighting F and S as weekends visually in the header
    days_header = " S  M  T  W  T  [F] [S]" 
    body_lines = [l for l in lines[2:] if l.strip()]
    body = " \\A ".join(body_lines)
    
    footer = f"\\A\\A-- {holiday_name} --" if holiday_name else ""
    full_content = f"{header} \\A {days_header} \\A {body} {footer}"

    # 3. FIX HIGHLIGHT MATH
    first_weekday = datetime.date(year, month, 1).weekday()
    offset = (first_weekday + 1) % 7
    
    col = (day + offset - 1) % 7
    row = (day + offset - 1) // 7

    # Dracula Colors
    background = "#282a36"
    foreground = "#f8f8f2"
    comment = "#6272a4"
    pink = "#ff79c6"

    # Precise spacing for Courier New 16px
    h_pos = 23 + (col * 29.5)
    v_pos = 100 + (row * 28.8)

    css = f"""
body::before {{
  content: "{full_content}";
  position: fixed;
  top: 40px;
  right: 40px;
  z-index: 9999;
  white-space: pre;
  font-family: 'Courier New', Courier, monospace;
  font-size: 16px;
  font-weight: bold;
  line-height: 1.8;
  color: {foreground};
  padding: 25px;
  background-color: {background};
  border: 3px solid {comment};
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0,0,0,0.6);
  background-image: radial-gradient(circle, {pink} 50%, transparent 55%);
  background-repeat: no-repeat;
  background-size: 34px 34px;
  background-position: {h_pos}px {v_pos}px;
}}"""
    
    with open("calendar.css", "w") as f:
        f.write(css)

if __name__ == "__main__":
    generate_css()
