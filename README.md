# :calendar: Automated Dracula SVG Calendar for Tabliss

An automated, smart calendar widget designed specifically for the [Tabliss](https://tabliss.io/) browser extension. This project uses Python and GitHub Actions to generate a daily-updated, Dracula-themed SVG calendar featuring a dual-month view.



## :rocket: New in this Version

* **Dual-Month View**: Displays both the current month and the upcoming month as distinct, vertically stacked cards.
* **Payday Tracking**: Includes a specialized `paydays_2026` dictionary that marks paydays with a yellow star (★).
* **Enhanced Layout**: Built with a clean background card system, border radii, and improved spacing logic.
* **Object-Oriented Config**: All visual parameters (colors, dimensions, opacity) are now managed via a `CalendarConfig` dataclass for easier tweaking.

## :art: Features

* **Dracula Theme**: Features the official Dracula color palette (Pink for today, Purple for holidays, Cyan for weekends).
* **Smart Highlighting**: 
    * **Pink**: Today's date and Kuwait-specific holidays.
    * **Purple**: US holidays and weekend headers.
    * **Yellow Star**: Paydays.
* **Kuwait-Specific Logic**: Configured to recognize **Friday and Saturday** as weekends.
* **Zero-Maintenance**: GitHub Actions runs the script daily at midnight to ensure the "Today" highlight is always accurate.

---

## 🛠️ Installation

### 1. Repository Setup
1.  Ensure `generate_calendar.py` is in your root directory.
2.  Ensure your workflow file is located at `.github/workflows/daily.yml`.

### 2. GitHub Actions Permissions
To allow the script to save the generated `calendar.css` back to your repository:
1.  Go to **Settings** > **Actions** > **General**.
2.  Under **Workflow permissions**, select **Read and write permissions**.
3.  Click **Save**.

### 3. Tabliss Configuration
1.  Open **Tabliss Settings**.
2.  Add a **Custom CSS** widget.
3.  Paste the following line (replace with your actual username/repo):
    ```css
    @import url('[https://lglandon1.github.io/tabliss-calendar/calendar.css](https://lglandon1.github.io/tabliss-calendar/calendar.css)');
    ```
    *Note: Use `.../calendar.css?v=1` to force a refresh if the browser caches the old version.*

---

## :gear: Customization

The script now uses a `CalendarConfig` dataclass. You can modify these values directly in `generate_calendar.py`:

| Variable | Default | Description |
| :--- | :--- | :--- |
| `width` | `300` | Width of the calendar widget. |
| `gap_between_calendars` | `60` | Vertical space between the two month cards. |
| `bg_card` | `#2e3440` | Background color of the individual month cards. |
| `payday_star` | `#f1fa8c` | Color of the payday star (Dracula Yellow). |
| `fade_opacity` | `0.62` | The idle transparency of the widget. |
| `weekend_columns` | `{5, 6}` | Set to `{5, 6}` for Fri/Sat or `{6, 0}` for Sat/Sun. |

---

## :lion: Brave Browser Troubleshooting

If your settings (including the CSS snippet) disappear when you restart Brave:
1.  **Disable "Clear on Exit"**: Go to `brave://settings/cookies` and ensure "Clear cookies and site data when you close all windows" is **OFF**.
2.  **Disable Shields**: Click the Lion icon in the address bar on your Tabliss page and toggle Shields **OFF**.
3.  **Persist Settings**: In Tabliss Settings (General), toggle **Persist Settings** to **ON**.

## :ledger: License
MIT License - Feel free to use and modify for your own dashboard!
