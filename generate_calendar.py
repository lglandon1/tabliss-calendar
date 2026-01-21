#!/usr/bin/env python3
"""Generate a Dracula-themed SVG calendar (current + next month) as base64-encoded CSS for Tabliss."""

import datetime
import calendar
import base64
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Set

@dataclass(frozen=True)
class CalendarConfig:
    """All configurable style and layout settings."""

    # Dimensions
    width: int = 300
    single_calendar_height: int = 340
    gap_between_calendars: int = 60          # Clear space between the two cards
    card_padding: int = 10                   # Inset for each calendar's background
    card_border_radius: int = 12

    # Colors
    bg_outer: str = "#282a36"                # Very subtle outer if needed
    bg_card: str = "#2e3440"                 # Slightly lighter/darker for contrast
    border_card: str = "#4c566a"             # Softer border for cards
    fg: str = "#f8f8f2"
    pink: str = "#ff79c6"                    # Today + Kuwait holidays
    purple: str = "#bd93f9"                  # US holidays & weekend headers
    cyan_low: str = "rgba(139, 233, 253, 0.12)"
    payday_star: str = "#f1fa8c"

    # Visual tuning
    col_width: int = 40
    row_height: int = 40
    grid_start_x: int = 30
    cell_size: int = 36
    today_radius: int = 16
    today_circle_dy: int = -2
    text_dy: int = 5
    holiday_opacity: str = "0.45"
    weekend_opacity: str = "1.0"
    fade_opacity: float = 0.62
    hover_opacity: float = 1.0

    # Layout behavior
    first_weekday: int = 6
    weekend_columns: set[int] = frozenset({5, 6})  # Friday=5, Saturday=6


DEFAULT_CONFIG = CalendarConfig()


def generate_calendar_css(
    year: Optional[int] = None,
    month: Optional[int] = None,
    config: CalendarConfig = DEFAULT_CONFIG,
    output_path: str | Path = "calendar.css",
) -> None:
    """Generate CSS file with base64-encoded SVG (two visually separate calendars)."""
    now = datetime.datetime.now()
    year = year or now.year
    month = month or now.month

    # Paydays for 2026
    paydays_2026: dict[int, Set[int]] = {
        2: {13, 27}, 3: {13, 27}, 4: {10, 24}, 5: {8, 22}, 6: {5, 18},
        7: {2, 17, 31}, 8: {14, 28}, 9: {11, 18}, 10: {9, 23},
        11: {6, 20}, 12: {4, 18, 31},
    }

    # ── HOLIDAY DATA ─────────────────────────────────────────────────────────
    try:
        import holidays
        holidays_available = True
        us_hols = holidays.US(years=year)
        kw_hols = None
        try:
            kw_hols = holidays.KW(years=[year, year + 1, year + 2])
        except (AttributeError, NotImplementedError):
            warnings.warn("Kuwait holidays not supported in this version.", ImportWarning)
    except ImportError:
        holidays_available = False
        us_hols = kw_hols = None
        warnings.warn("'holidays' library not installed.", ImportWarning)

    total_height = (config.single_calendar_height * 2) + config.gap_between_calendars

    svg_lines: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{config.width}" height="{total_height}">'
    ]

    def add_calendar(
        base_y: int,
        m: int,
        yr: int,
        is_current: bool = False,
        title_y_offset: int = 40,
        weekdays_y_offset: int = 80,
        grid_y_offset: int = 120,
    ):
        # Individual card background
        card_y = base_y
        card_height = config.single_calendar_height
        svg_lines.append(
            f'<rect x="{config.card_padding}" y="{card_y}" '
            f'width="{config.width - 2 * config.card_padding}" height="{card_height}" '
            f'rx="{config.card_border_radius}" fill="{config.bg_card}" '
            f'stroke="{config.border_card}" stroke-width="2"/>'
        )

        header_y = card_y + title_y_offset
        weekdays_y = card_y + weekdays_y_offset
        grid_start_y = card_y + grid_y_offset

        # Header
        header_text = datetime.date(yr, m, 1).strftime("%B %Y").upper()
        svg_lines.append(
            f'<text x="{config.width / 2}" y="{header_y}" font-family="Courier New, monospace" '
            f'font-size="20" font-weight="bold" fill="{config.fg}" text-anchor="middle" '
            f'letter-spacing="2">{header_text}</text>'
        )

        # Weekday headers
        weekdays = ["S", "M", "T", "W", "T", "F", "S"]
        for i, wd in enumerate(weekdays):
            x = config.grid_start_x
            cx = x + (i * config.col_width)
            color = config.purple if i in config.weekend_columns else config.fg
            svg_lines.append(
                f'<text x="{cx}" y="{weekdays_y}" font-family="Courier New, monospace" '
                f'font-size="16" font-weight="bold" fill="{color}" text-anchor="middle">{wd}</text>'
            )

        # Grid
        cal = calendar.Calendar(firstweekday=config.first_weekday)
        month_days = cal.monthdayscalendar(yr, m)
        today_day = now.day if is_current and yr == now.year and m == now.month else None

        for row_idx, week in enumerate(month_days):
            for col_idx, day_num in enumerate(week):
                if day_num == 0:
                    continue

                cx = config.grid_start_x + (col_idx * config.col_width)
                cy = grid_start_y + (row_idx * config.row_height)

                is_today = (day_num == today_day)
                is_weekend = col_idx in config.weekend_columns
                is_payday = day_num in paydays_2026.get(m, set())

                holiday_name = None
                holiday_country = None
                if holidays_available:
                    date = datetime.date(yr, m, day_num)
                    if kw_hols and date in kw_hols:
                        holiday_name = kw_hols.get(date)
                        holiday_country = "KW"
                    elif us_hols and date in us_hols:
                        holiday_name = us_hols.get(date)
                        holiday_country = "US"

                # Background rect
                if holiday_name or is_weekend:
                    fill = config.pink if holiday_country == "KW" else config.purple if holiday_name else config.cyan_low
                    opacity = config.holiday_opacity if holiday_name else config.weekend_opacity
                    svg_lines.append(
                        f'<rect x="{cx - config.cell_size / 2}" y="{cy - config.cell_size / 2 + 2}" '
                        f'width="{config.cell_size}" height="{config.cell_size - 4}" rx="6" '
                        f'fill="{fill}" fill-opacity="{opacity}"/>'
                    )

                # Today circle
                if is_today:
                    svg_lines.append(
                        f'<circle cx="{cx}" cy="{cy + config.today_circle_dy}" '
                        f'r="{config.today_radius}" fill="{config.pink}"/>'
                    )

                # Day number
                text_color = "#000000" if is_today else config.fg
                svg_lines.append(
                    f'<text x="{cx}" y="{cy + config.text_dy}" font-family="Courier New, monospace" '
                    f'font-size="16" font-weight="bold" fill="{text_color}" text-anchor="middle">{day_num}</text>'
                )

                # Payday star
                if is_payday:
                    star_x = cx + 12
                    star_y = cy + config.text_dy - 2
                    svg_lines.append(
                        f'<text x="{star_x}" y="{star_y}" font-family="Courier New, monospace" '
                        f'font-size="14" fill="{config.payday_star}" text-anchor="middle">★</text>'
                    )

    # First calendar (current month)
    add_calendar(base_y=0, m=month, yr=year, is_current=True)

    # Second calendar (next month)
    next_month = month + 1
    next_year = year
    if next_month > 12:
        next_month = 1
        next_year += 1

    add_calendar(base_y=config.single_calendar_height + config.gap_between_calendars,
                 m=next_month, yr=next_year)

    # Today's holiday note (bottom of first calendar only)
    if holidays_available and now.month == month and now.year == year:
        today_date = datetime.date(year, month, now.day)
        today_holiday = kw_hols.get(today_date) if kw_hols and today_date in kw_hols else \
                        us_hols.get(today_date) if us_hols and today_date in us_hols else None
        if today_holiday:
            note_y = config.single_calendar_height - 20
            svg_lines.append(
                f'<text x="{config.width / 2}" y="{note_y}" '
                f'font-family="Courier New, monospace" font-size="12" fill="{config.purple}" '
                f'text-anchor="middle">-- {today_holiday} --</text>'
            )

    svg_lines.append("</svg>")
    svg_content = "".join(svg_lines)

    b64_svg = base64.b64encode(svg_content.encode("utf-8")).decode("utf-8")

    css_content = f"""\
/* Faded SVG Calendar - Two Separate Cards */
body::before {{
  content: "";
  display: block;
  position: fixed;
  top: 40px;
  right: 40px;
  width: {config.width}px;
  height: {total_height}px;
  z-index: 9999;
  background-image: url("data:image/svg+xml;base64,{b64_svg}");
  background-repeat: no-repeat;
  background-position: center;
  filter: drop-shadow(0 10px 20px rgba(0,0,0,0.5));
  opacity: {config.fade_opacity};
  transition: opacity 0.4s ease;
}}

body::before:hover {{
  opacity: {config.hover_opacity};
}}
"""

    output_path = Path(output_path)
    try:
        output_path.write_text(css_content, encoding="utf-8")
        print(f"Success: Calendar CSS written to {output_path}")
    except OSError as e:
        warnings.warn(f"Failed to write CSS file: {e}", RuntimeWarning)
        raise


if __name__ == "__main__":
    generate_calendar_css()
