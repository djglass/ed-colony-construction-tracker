"""
Elite Dangerous Colony Construction Tracker

This Python GUI app helps Elite Dangerous players track commodities delivered
for colony construction by parsing screenshots and scanning journal logs.

Features:
- OCR parsing of construction requirement screenshots
- Journal log scanning for MarketSell events
- Real-time delivery tracking
- Table filtering (all / complete / incomplete)
- CSV export
- Elite-themed UI styling with Euro Caps font

Author: Commander Toadie Mudguts
GitHub: https://github.com/djglass
"""

import os
import re
import json
import pytesseract
import customtkinter as ctk

# Apply Elite Dangerous theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("custom_theme.json")

from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image

class EDConstructionParserApp(ctk.CTk):
    """
    A customtkinter-based GUI application for Elite Dangerous players
    to parse construction commodity requirements from screenshots and
    track delivery progress by reading in-game journal logs.

    Features:
    - OCR-based parsing of commodity names and required amounts.
    - Automatic delivery log tracking from Elite Dangerous journal files.
    - Interactive table showing delivery progress.
    - CSV export support.
    - Elite Dangerous styled theme and layout.
    """

    def __init__(self):
        super().__init__()
        self.title("Elite Dangerous Colony Construction Tracker")
        self.geometry("1000x700")

        self.result_data = {}
        self.deliveries = {}
        self.filter_mode = ctk.StringVar(value="all")

        ctk.CTkLabel(self, text="SELECT CONSTRUCTION REQUIREMENT SCREENSHOTS:").pack(pady=10)
        ctk.CTkButton(self, text="SELECT SCREENSHOTS", command=self.select_files).pack(pady=5)

        ctk.CTkLabel(self, text="TEXT SIZE:").pack(pady=5)
        self.font_slider = ctk.CTkSlider(
            self,
            from_=10,
            to=24,
            number_of_steps=7,
            command=self.set_font_size,
            button_color="#FFA500",
            progress_color="#555555"
        )
        self.font_slider.set(16)
        self.font_slider.pack(pady=5)

        self.tree = ttk.Treeview(
            self,
            columns=("Commodity", "Delivered", "Required", "Remaining"),
            show="headings",
            style="Custom.Treeview"
        )
        for col in ("Commodity", "Delivered", "Required", "Remaining"):
            self.tree.heading(col, text=col.upper(), command=lambda c=col: self.sort_tree(c, False))

        self.tree.column("Commodity", width=300, anchor="w")
        self.tree.column("Delivered", width=100, anchor="center")
        self.tree.column("Required", width=100, anchor="center")
        self.tree.column("Remaining", width=100, anchor="center")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        filter_frame = ctk.CTkFrame(self)
        filter_frame.pack(pady=5)
        ctk.CTkLabel(filter_frame, text="FILTER:").pack(side="left", padx=(0, 10))
        ctk.CTkRadioButton(filter_frame, text="ALL", variable=self.filter_mode, value="all", command=self.display_delivery_progress, border_color="#FFA500", fg_color="#FFA500", hover_color="#FF8C00").pack(side="left")
        ctk.CTkRadioButton(filter_frame, text="INCOMPLETE", variable=self.filter_mode, value="incomplete", command=self.display_delivery_progress).pack(side="left")
        ctk.CTkRadioButton(filter_frame, text="COMPLETE", variable=self.filter_mode, value="complete", command=self.display_delivery_progress).pack(side="left")
        ctk.CTkButton(self, text="EXPORT TO CSV", command=self.export_to_csv).pack(pady=5)

    def set_font_size(self, val):
        """Update Treeview font size from the slider."""
        new_size = int(float(val))
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Euro Caps", new_size, "bold"))

    def select_files(self):
        """Allow user to select screenshots and trigger parsing and log reading."""
        paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if paths:
            self.file_paths = list(paths)
            self.parse_requirements()
            self.load_logs()

    def extract_text_from_images(self):
        """Perform OCR on selected screenshots and return line-separated text."""
        lines = []
        for file_path in self.file_paths:
            try:
                img = Image.open(file_path)
                text = pytesseract.image_to_string(img)
                lines.extend([line.strip() for line in text.splitlines() if line.strip()])
            except Exception as e:
                messagebox.showerror("OCR Error", f"Error processing {file_path}: {e}")
        return lines

    def parse_requirements(self):
        """Extract commodities and required quantities from OCR lines."""
        lines = self.extract_text_from_images()
        commodities = [line for line in lines if not re.match(r"^[\d,]+$", line)]
        numbers = [int(line.replace(",", "")) for line in lines if re.match(r"^[\d,]+$", line)]
        self.result_data = dict(zip(commodities, numbers))
        self.display_delivery_progress()

    def load_logs(self):
        """Parse Elite Dangerous journal logs and tally MarketSell deliveries."""
        folder = os.path.expandvars(r"%USERPROFILE%\\Saved Games\\Frontier Developments\\Elite Dangerous")
        if not folder:
            return

        self.deliveries = {}
        for filename in os.listdir(folder):
            if not filename.startswith("Journal") or not filename.endswith(".log"):
                continue
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
                for line in f:
                    if '"event":"MarketSell"' not in line:
                        continue
                    try:
                        entry = json.loads(line)
                        name = entry.get("Type", "").replace("_", " ").title()
                        self.deliveries[name] = self.deliveries.get(name, 0) + entry.get("Count", 0)
                    except:
                        continue
        self.display_delivery_progress()

    def display_delivery_progress(self):
        """Update the Treeview to reflect delivery progress and current filter."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        mode = self.filter_mode.get()
        for name, required in self.result_data.items():
            delivered = self.deliveries.get(name, 0)
            remaining = max(0, required - delivered)

            if mode == "incomplete" and remaining == 0:
                continue
            if mode == "complete" and remaining > 0:
                continue

            self.tree.insert("", "end", values=(name, delivered, required, remaining))

    def export_to_csv(self):
        """Export current delivery progress to a CSV file."""
        from csv import writer
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = writer(f)
                w.writerow(["Commodity", "Delivered", "Required", "Remaining"])
                for row in self.tree.get_children():
                    w.writerow(self.tree.item(row)["values"])
            messagebox.showinfo("Exported", f"Data exported to {path}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    def sort_tree(self, col, reverse):
        """Sort the Treeview by a specific column, optionally in reverse."""
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        try:
            l.sort(key=lambda t: int(t[0].replace(",", "")), reverse=reverse)
        except:
            l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
        self.tree.heading(col, command=lambda: self.sort_tree(col, not reverse))

if __name__ == "__main__":
    app = EDConstructionParserApp()

    style = ttk.Style(master=app)
    style.theme_use("clam")
    style.configure(
        "Custom.Treeview",
        font=("Euro Caps", 16, "bold"),
        rowheight=28,
        background="#000000",
        fieldbackground="#000000",
        foreground="#FFA500",
        bordercolor="#000000",
        borderwidth=0
    )
    style.map("Custom.Treeview",
              background=[("selected", "#333333")],
              foreground=[("selected", "#FFA500")])

    style.configure("Treeview.Heading",
                    background="#FFA500",
                    foreground="#000000",
                    font=("Euro Caps", 16, "bold"))

    app.configure(fg_color="#000000")
    app.mainloop()
