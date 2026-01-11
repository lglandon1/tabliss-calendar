import datetime
import calendar
import holidays

def generate_css():
    now = datetime.datetime.now()
    year, month, day = now.year, now.month, now.day
    
    # Get Holidays
    us_holidays = holidays.US(years=year)
    today_holiday = us_holidays.get(datetime.date(year, month, day))
    
    # Generate Grid
    cal_obj = calendar.TextCalendar(calendar.SUNDAY)
    cal_str = cal_obj.formatmonth(year, month)
    lines = cal_str.splitlines()
    
    header = lines[0].strip().upper()
    days_header = " S  M  T  W  T  F  S"
    # Filter out empty lines and format for CSS
    body_lines = [l for l in lines[2:] if l.strip()]
    body = " \\A ".join(body_lines)
    
    footer = f"\\A\\A-- {today_holiday} --" if today_holiday else ""
    full_content = f"{header} \\A {days_header} \\A {body} {footer}"

    # Calculate Grid Positioning
    # Sunday is 6 in datetime.weekday(), so (wd + 1) % 7 makes Sun=0
    first_day_of_month = datetime.date(year, month, 1)
    start_col = (first_day_of_month.weekday() + 1) % 7
    
    col = (day + start_col - 1) % 7
    row = (day + start_col - 1) // 7

    # Horizontal: 23px is left edge, 29px per column
    # Vertical: 98px is first row of numbers, 29px per row
    h_pos = 23 + (col * 29)
    v_pos = 98 + (row * 29)

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
  line-height: 1.8;
  color: #fff;
  padding: 25px;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  text-align: center;
  background-image: radial-gradient(circle, rgba(255, 255, 255, 0.3) 50%, transparent 55%);
  background-repeat: no-repeat;
  background-size: 35px 35px;
  background-position: {h_pos}px {v_pos}px;
}}"""
    
    with open("calendar.css", "w") as f:
        f.write(css)

if __name__ == "__main__":
    generate_css()
