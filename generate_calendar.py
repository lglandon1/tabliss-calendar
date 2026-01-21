import datetime
import calendar
import base64

# Optional: try to import holidays library
try:
    import holidays
    HOLIDAYS_AVAILABLE = True
except ImportError:
    HOLIDAYS_AVAILABLE = False
    print("Warning: 'holidays' library not found. Holiday highlighting will be disabled.")


def generate_css():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day

    # ── CONFIGURATION ────────────────────────────────────────────────────────
    # Dimensions
    WIDTH = 300
    HEIGHT = 340
    COL_WIDTH = 40
    ROW_HEIGHT = 40
    GRID_START_X = 30
    GRID_START_Y = 120

    # Colors (Dracula theme)
    C_BG = "#282a36"
    C_FG = "#f8f8f2"
    C_PINK = "#ff79c6"              # Today highlight
    C_PURPLE = "#bd93f9"            # Holiday text / shading
    C_CYAN_LOW = "rgba(139, 233, 253, 0.12)"  # Weekend background
    C_BORDER = "#6272a4"
    C_OTHER_MONTH = "rgba(248, 248, 242, 0.35)"  # Optional faded days from prev/next month

    # Visual settings
    CELL_SIZE = 36
    TODAY_RADIUS = 16
    BG_OPACITY_HOLIDAY = "0.45"
    BG_OPACITY_WEEKEND = "1.0"
    FADE_OPACITY = 0.62          # Base calendar visibility
    HOVER_OPACITY = 1.0

    FIRST_WEEKDAY = 6            # 6 = Sunday (keeps standard layout: S M T W T F S)

    # ── HOLIDAY DATA (US + Kuwait) ───────────────────────────────────────────
    us_hols = kw_hols = None
    if HOLIDAYS_AVAILABLE:
        us_hols = holidays.US(years=year)
        # Kuwait holidays supported in recent versions of the library
        try:
            kw_hols = holidays.KW(years=[year, year + 1, year + 2])
        except (AttributeError, NotImplementedError):
            kw_hols = None
            print("Note: Kuwait holidays not available in this version of the library.")

    # ── SVG CONSTRUCTION ─────────────────────────────────────────────────────
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}">']

    # 1. Card background
    svg.append(
        f'<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" rx="15" '
        f'fill="{C_BG}" stroke="{C_BORDER}" stroke-width="4"/>'
    )

    # 2. Header: Month Year
    header_text = datetime.date(year, month, 1).strftime("%B %Y").upper()
    svg.append(
        f'<text x="{WIDTH/2}" y="40" font-family="Courier New, monospace" '
        f'font-size="20" font-weight="bold" fill="{C_FG}" text-anchor="middle" '
        f'letter-spacing="2">{header_text}</text>'
    )

    # 3. Weekday labels (S M T W T F S) — highlight Fri/Sat in purple per README intent
    weekdays = ["S", "M", "T", "W", "T", "F", "S"]
    for i, wd in enumerate(weekdays):
        x = GRID_START_X + (i * COL_WIDTH)
        color = C_PURPLE if i in (5, 6) else C_FG  # Friday (5), Saturday (6)
        svg.append(
            f'<text x="{x}" y="80" font-family="Courier New, monospace" '
            f'font-size="16" font-weight="bold" fill="{color}" text-anchor="middle">{wd}</text>'
        )

    # 4. Calendar days
    cal = calendar.Calendar(firstweekday=FIRST_WEEKDAY)
    month_days = cal.monthdayscalendar(year, month)

    for row_idx, week in enumerate(month_days):
        for col_idx, day_num in enumerate(week):
            if day_num == 0:
                continue

            cx = GRID_START_X + (col_idx * COL_WIDTH)
            cy = GRID_START_Y + (row_idx * ROW_HEIGHT)

            date = datetime.date(year, month, day_num)
            is_today = (day_num == day)
            # Kuwait weekend: Friday (col 5) and Saturday (col 6)
            is_weekend = (col_idx in (5, 6))
            holiday_name = None

            if HOLIDAYS_AVAILABLE:
                holiday_name = us_hols.get(date)
                if not holiday_name and kw_hols:
                    holiday_name = kw_hols.get(date)

            # Background for weekend or holiday
            if holiday_name or is_weekend:
                fill = C_PURPLE if holiday_name else C_CYAN_LOW
                opacity = BG_OPACITY_HOLIDAY if holiday_name else BG_OPACITY_WEEKEND
                svg.append(
                    f'<rect x="{cx - CELL_SIZE/2}" y="{cy - CELL_SIZE/2 + 2}" '
                    f'width="{CELL_SIZE}" height="{CELL_SIZE - 4}" rx="6" '
                    f'fill="{fill}" fill-opacity="{opacity}"/>'
                )

            # Today circle
            if is_today:
                svg.append(
                    f'<circle cx="{cx}" cy="{cy - 4}" r="{TODAY_RADIUS}" fill="{C_PINK}"/>'
                )

            # Day number text
            text_color = "#000000" if is_today else C_FG
            svg.append(
                f'<text x="{cx}" y="{cy + 6}" font-family="Courier New, monospace" '
                f'font-size="16" font-weight="bold" fill="{text_color}" text-anchor="middle">'
                f'{day_num}</text>'
            )

    # 5. Optional: show today’s holiday name at bottom
    today_date = datetime.date(year, month, day)
    today_holiday = None
    if HOLIDAYS_AVAILABLE:
        today_holiday = us_hols.get(today_date) or (kw_hols.get(today_date) if kw_hols else None)

    if today_holiday:
        svg.append(
            f'<text x="{WIDTH/2}" y="{HEIGHT - 20}" font-family="Courier New, monospace" '
            f'font-size="12" fill="{C_PURPLE}" text-anchor="middle">-- {today_holiday} --</text>'
        )
    elif HOLIDAYS_AVAILABLE is False:
        svg.append(
            f'<text x="{WIDTH/2}" y="{HEIGHT - 20}" font-family="Courier New, monospace" '
            f'font-size="11" fill="#6272a4" text-anchor="middle">(holidays library not installed)</text>'
        )

    svg.append('</svg>')
    svg_content = "".join(svg)

    # ── BASE64 ENCODING ──────────────────────────────────────────────────────
    b64_svg = base64.b64encode(svg_content.encode("utf-8")).decode("utf-8")

    # ── CSS (faded + hover effect) ───────────────────────────────────────────
    css_content = f"""\
/* Faded SVG Calendar with Hover Brighten */
body::before {{
  content: "";
  display: block;
  position: fixed;
  top: 40px;
  right: 40px;
  width: {WIDTH}px;
  height: {HEIGHT}px;
  z-index: 9999;
  background-image: url("data:image/svg+xml;base64,{b64_svg}");
  background-repeat: no-repeat;
  background-position: center;
  filter: drop-shadow(0 10px 20px rgba(0,0,0,0.5));
  opacity: {FADE_OPACITY};
  transition: opacity 0.4s ease;
}}

body::before:hover {{
  opacity: {HOVER_OPACITY};
}}
"""

    with open("calendar.css", "w", encoding="utf-8") as f:
        f.write(css_content)

    print("Success: Faded SVG calendar CSS file generated.")


if __name__ == "__main__":
    generate_css()
