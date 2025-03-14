# Elite Dangerous Colony Construction Tracker

**Author:** Commander Toadie Mudguts  
**GitHub:** [@djglass](https://github.com/djglass)

A sleek, immersive Python desktop app that helps Elite Dangerous players track construction commodity deliveries using OCR and journal logs.

## ✨ Features

- 📷 Parses screenshots of commodity requirements using Tesseract OCR
- 📜 Reads Elite Dangerous journal logs to tally MarketSell deliveries
- 📊 Live, filterable delivery tracking table
- 📁 CSV export for wing coordination
- 🎨 Elite-themed UI (dark mode, orange text, Euro Caps font)

## 🖥️ Platform Support

This application is intended for **Windows users** running the Elite Dangerous game and storing logs in the standard `%USERPROFILE%\Saved Games` directory.

## 🚀 Getting Started (Windows)

### Prerequisites

- Python 3.10+ (Windows Store or python.org)
- Tesseract OCR installed and added to your Windows PATH:
  [Tesseract Windows Installer](https://github.com/tesseract-ocr/tesseract/wiki#windows)
- (Optional) Install the **Euro Caps** font locally for full HUD effect
- Install Python dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Installation

```bash
git clone https://github.com/djglass/ed-colony-construction-tracker.git
cd ed-colony-construction-tracker
python colony_tracker_gui.py
```

## 🖼️ How It Works

1. **Take screenshots** of the commodity requirements screen in-game (clean layout preferred).
2. **Launch the app**, click **SELECT SCREENSHOTS**, and choose your images.
3. The app will parse and display required items.
4. It will also scan your local journal logs to track delivery progress.

## 📁 Output

- Filter deliveries by `All`, `Incomplete`, or `Complete`
- Export progress to `.csv` for planning or sharing with your squad

## 🛠️ Tech Stack

- Python + [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
- Tesseract OCR
- PIL (Pillow)
- JSON parsing of in-game logs

## 🤝 Community

This is a fan project for the Elite Dangerous community. Contributions, suggestions, and bug reports welcome!
