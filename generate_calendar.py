import datetime
import calendar

# --- CONFIGURATION ---
# Add your custom holidays here (Month, Day)
HOLIDAYS = {
    (1, 1): "New Year's Day",
    (1, 19): "MLK Day",
    (2, 14): "Valentine's",
    # Add more...
}

now = datetime.datetime.now()
year, month, day = now.year, now.month, now.day

# Generate the calendar string
cal_obj = calendar.TextCalendar(calendar.SUNDAY)
cal_str = cal_obj.formatmonth(year, month)
lines = cal_str.splitlines()

# Title and Header
header = lines[0].strip().upper()
days_header = " S  M  T  W  T  F  S"
body_lines = lines[2:]

# Format rows with \A for CSS line breaks
content = f"{header} \\A {days_header}"
for line in body_lines:
    content += f" \\A {line}"

# Calculate Highlight Position
# (Base coordinates: 23px horizontal, 98px vertical for first row)
first_day_weekday = datetime.date(year, month, 1).weekday() 
# Adjusting for Sunday start: (weekday + 1) % 7
col = (datetime.date(year, month, day).weekday() + 1) % 7
row = (day + (datetime.date(year, month, 1).weekday() + 1) % 7 - 1) // 7

h_pos = 23 + (col * 29)
v_pos = 98 + (row * 29)

# Build the CSS
css_content = f"""
body::before {{
  content: "{content}";
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
}}
"""

with open("calendar.css", "w") as f:
    f.write(css_content)
