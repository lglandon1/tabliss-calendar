import datetime
import calendar
import holidays  # You'll need this in your requirements/action

def generate_css():
    # Setup Date
    now = datetime.datetime.now()
    year, month, day = now.year, now.month, now.day
    
    # Get Holidays for US (Change 'US' to your country code)
    uk_holidays = holidays.US(years=year)
    today_holiday = uk_holidays.get(datetime.date(year, month, day))
    
    # Generate Calendar Grid (Sunday start)
    cal_obj = calendar.TextCalendar(calendar.SUNDAY)
    cal_str = cal_obj.formatmonth(year, month)
    lines = cal_str.splitlines()
    
    # Format Content
    header = lines[0].strip().upper()
    days_header = " S  M  T  W  T  F  S"
    body = " \\A ".join(lines[2:])
    
    # Add Holiday Text if it exists
    footer = f"\\A\\A-- {today_holiday} --" if today_holiday else ""
    full_content = f"{header} \\A {days_header} \\A {body} {footer}"

    # Calculate Highlight Position
    # Sunday = 0, Saturday = 6
    first_day_weekday = (datetime.date(year, month, 1).weekday() + 1) % 7
    col = (day + first_day_weekday - 1) % 7
    row = (day + first_day_weekday - 1) // 7

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
