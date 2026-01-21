# 📅 Automated Dracula SVG Calendar for Tabliss

An automated, smart calendar widget designed specifically for the [Tabliss](https://tabliss.io/) browser extension. This project uses Python and GitHub Actions to generate a daily-updated, Dracula-themed SVG calendar that highlights holidays (US & Kuwait) and weekends.

## 🚀 Features

* **Smart Layout**: Uses SVG generation to ensure pixel-perfect alignment between dates and highlights.
* **Dracula Theme**: Features the official Dracula color palette (Pink for today, Purple for holidays, Cyan for weekends).
* **Dual-Country Holidays**: Automatically fetches and displays public holidays for both the **United States** and **Kuwait**.
* **Kuwait-Specific Weekends**: Corrected logic to highlight **Friday and Saturday** as weekends.
* **Zero-Maintenance**: GitHub Actions runs the script daily at midnight to update the "Today" highlight.
* **Aesthetic Fade**: Includes a global opacity setting with a smooth hover-to-brighten transition.

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
3.  Paste the following line:
    ```css
    @import url('[https://lglandon1.github.io/tabliss-calendar/calendar.css](https://lglandon1.github.io/tabliss-calendar/calendar.css)');
    ```
    *Note: If changes don't appear immediately, use `.../calendar.css?v=1` to bypass browser cache.*

## 🦁 Brave Browser Troubleshooting

If your settings (including the CSS snippet) disappear when you restart Brave:
1.  **Disable "Clear on Exit"**: Go to `brave://settings/cookies` and ensure "Clear cookies and site data when you close all windows" is **OFF**.
2.  **Disable Shields**: Click the Lion icon in the address bar on your Tabliss page and toggle Shields **DOWN**.
3.  **Persist Settings**: In Tabliss Settings (General), toggle **Persist Settings** to **ON**.

## 📂 File Structure

* `generate_calendar.py`: The Python engine that calculates dates, fetches holidays, and builds the SVG-encoded CSS.
* `calendar.css`: The auto-generated file hosted via GitHub Pages.
* `.github/workflows/daily.yml`: The automation schedule (Cron) that triggers the update.

## 🎨 Customization

To change the look, edit the `CONFIG` section in `generate_calendar.py`:

| Variable | Description |
| :--- | :--- |
| `C_BG` | Background color (supports Hex or RGBA) |
| `C_PINK` | The highlight color for the current day |
| `opacity` | Change from `0.6` to `1.0` in the CSS string for a solid look |

## 📜 License
MIT License - Feel free to use and modify for your own dashboard!
