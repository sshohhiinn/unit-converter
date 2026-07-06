import tkinter as tk
from tkinter import ttk

# ── Conversion data ────────────────────────────────────────────────
CATEGORIES = {
    "Length": {
        "units": {
            "Meter": 1, "Kilometer": 1000, "Centimeter": 0.01,
            "Millimeter": 0.001, "Mile": 1609.344, "Yard": 0.9144,
            "Foot": 0.3048, "Inch": 0.0254, "Nautical Mile": 1852,
        },
        "quick": [("Meter", "Foot"), ("Kilometer", "Mile"),
                  ("Inch", "Centimeter"), ("Yard", "Meter")]
    },
    "Weight": {
        "units": {
            "Kilogram": 1, "Gram": 0.001, "Milligram": 0.000001,
            "Metric Ton": 1000, "Pound": 0.453592, "Ounce": 0.0283495,
            "Stone": 6.35029,
        },
        "quick": [("Kilogram", "Pound"), ("Gram", "Ounce"),
                  ("Stone", "Kilogram"), ("Pound", "Kilogram")]
    },
    "Temperature": {
        "units": {"Celsius": "C", "Fahrenheit": "F", "Kelvin": "K", "Rankine": "R"},
        "quick": [("Celsius", "Fahrenheit"), ("Fahrenheit", "Celsius"),
                  ("Celsius", "Kelvin"), ("Kelvin", "Celsius")]
    },
    "Volume": {
        "units": {
            "Liter": 1, "Milliliter": 0.001, "Cubic Meter": 1000,
            "US Gallon": 3.78541, "US Quart": 0.946353, "US Pint": 0.473176,
            "US Cup": 0.236588, "US Fluid Ounce": 0.0295735,
            "Imperial Gallon": 4.54609, "Tablespoon": 0.0147868, "Teaspoon": 0.00492892,
        },
        "quick": [("Liter", "US Gallon"), ("Milliliter", "US Fluid Ounce"),
                  ("US Cup", "Milliliter"), ("Liter", "Imperial Gallon")]
    },
    "Speed": {
        "units": {
            "Meters/second": 1, "Km/hour": 0.277778, "Miles/hour": 0.44704,
            "Knots": 0.514444, "Feet/second": 0.3048, "Mach": 343,
        },
        "quick": [("Km/hour", "Miles/hour"), ("Meters/second", "Feet/second"),
                  ("Knots", "Km/hour"), ("Miles/hour", "Meters/second")]
    },
    "Time": {
        "units": {
            "Second": 1, "Minute": 60, "Hour": 3600, "Day": 86400,
            "Week": 604800, "Month": 2629800, "Year": 31557600,
            "Millisecond": 0.001,
        },
        "quick": [("Hour", "Minute"), ("Day", "Hour"),
                  ("Week", "Day"), ("Year", "Day")]
    },
    "Area": {
        "units": {
            "Square Meter": 1, "Square Kilometer": 1e6, "Square Centimeter": 0.0001,
            "Square Mile": 2589988, "Square Foot": 0.092903,
            "Square Inch": 0.00064516, "Hectare": 10000, "Acre": 4046.86,
        },
        "quick": [("Square Meter", "Square Foot"), ("Hectare", "Acre"),
                  ("Square Kilometer", "Square Mile"), ("Square Foot", "Square Meter")]
    },
}

# ── Conversion logic ───────────────────────────────────────────────
def convert_temp(val, from_u, to_u):
    if from_u == "Celsius":      c = val
    elif from_u == "Fahrenheit": c = (val - 32) * 5 / 9
    elif from_u == "Kelvin":     c = val - 273.15
    elif from_u == "Rankine":    c = (val - 491.67) * 5 / 9
    else: return None
    if to_u == "Celsius":      return c
    if to_u == "Fahrenheit":   return c * 9 / 5 + 32
    if to_u == "Kelvin":       return c + 273.15
    if to_u == "Rankine":      return (c + 273.15) * 9 / 5

def do_convert(val, from_u, to_u, cat):
    if cat == "Temperature":
        return convert_temp(val, from_u, to_u)
    units = CATEGORIES[cat]["units"]
    return val * units[from_u] / units[to_u]

def fmt(n):
    if n == 0: return "0"
    if 0.0001 <= abs(n) < 1e13:
        return f"{n:.6g}"
    return f"{n:.4e}"

# ── GUI ────────────────────────────────────────────────────────────
class UnitConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unit Converter")
        self.root.geometry("650x580")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0efea")

        self.active_cat = tk.StringVar(value="Length")
        self.from_unit  = tk.StringVar()
        self.to_unit    = tk.StringVar()
        self.input_val  = tk.StringVar(value="1")

        self._build_ui()
        self._refresh_units()
        self._convert()

    # ── UI builder ─────────────────────────────────────────────────
    def _build_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#f0efea")
        title_frame.pack(fill="x", padx=20, pady=(20, 10))
        tk.Label(title_frame, text="⇄  Unit Converter",
                 font=("Helvetica", 22, "bold"),
                 bg="#f0efea", fg="#1a1a18").pack(anchor="w")
        tk.Label(title_frame, text="Convert between units across 7 categories",
                 font=("Helvetica", 11), bg="#f0efea", fg="#6b6b67").pack(anchor="w")

        # Category buttons
        self.cat_frame = tk.Frame(self.root, bg="#f0efea")
        self.cat_frame.pack(fill="x", padx=20, pady=(0, 12))
        self.cat_buttons = {}
        for cat in CATEGORIES:
            btn = tk.Button(
                self.cat_frame, text=cat, font=("Helvetica", 10),
                relief="flat", bd=0, padx=10, pady=5, cursor="hand2",
                command=lambda c=cat: self._select_cat(c)
            )
            btn.pack(side="left", padx=3, pady=2)
            self.cat_buttons[cat] = btn
        self._update_cat_buttons()

        # Converter card
        card = tk.Frame(self.root, bg="white",
                        highlightbackground="#d0d0cc", highlightthickness=1)
        card.pack(fill="x", padx=20, pady=4)

        inner = tk.Frame(card, bg="white")
        inner.pack(fill="x", padx=20, pady=16)

        # From / Swap / To row
        row = tk.Frame(inner, bg="white")
        row.pack(fill="x", pady=(0, 12))

        # From
        from_col = tk.Frame(row, bg="white")
        from_col.pack(side="left", fill="x", expand=True)
        tk.Label(from_col, text="FROM", font=("Helvetica", 9, "bold"),
                 bg="white", fg="#6b6b67").pack(anchor="w")
        self.from_cb = ttk.Combobox(from_col, textvariable=self.from_unit,
                                     state="readonly", font=("Helvetica", 11))
        self.from_cb.pack(fill="x", pady=(4, 0))
        self.from_cb.bind("<<ComboboxSelected>>", lambda e: self._convert())

        # Swap button
        swap_col = tk.Frame(row, bg="white")
        swap_col.pack(side="left", padx=10, pady=(18, 0))
        tk.Button(swap_col, text="⇄", font=("Helvetica", 16), relief="flat",
                  bg="#f0efea", fg="#4a3fc7", cursor="hand2", width=3,
                  command=self._swap).pack()

        # To
        to_col = tk.Frame(row, bg="white")
        to_col.pack(side="left", fill="x", expand=True)
        tk.Label(to_col, text="TO", font=("Helvetica", 9, "bold"),
                 bg="white", fg="#6b6b67").pack(anchor="w")
        self.to_cb = ttk.Combobox(to_col, textvariable=self.to_unit,
                                   state="readonly", font=("Helvetica", 11))
        self.to_cb.pack(fill="x", pady=(4, 0))
        self.to_cb.bind("<<ComboboxSelected>>", lambda e: self._convert())

        # Value input
        tk.Label(inner, text="VALUE", font=("Helvetica", 9, "bold"),
                 bg="white", fg="#6b6b67").pack(anchor="w")
        self.entry = tk.Entry(inner, textvariable=self.input_val,
                              font=("Helvetica", 13), relief="flat",
                              bg="#f5f5f4", fg="#1a1a18",
                              insertbackground="#1a1a18")
        self.entry.pack(fill="x", ipady=8, pady=(4, 0))
        self.entry.bind("<KeyRelease>", lambda e: self._convert())

        # Result area
        result_frame = tk.Frame(inner, bg="#f5f5f4",
                                highlightbackground="#d0d0cc", highlightthickness=1)
        result_frame.pack(fill="x", pady=(14, 0))

        self.result_num = tk.Label(result_frame, text="—",
                                    font=("Helvetica", 30, "bold"),
                                    bg="#f5f5f4", fg="#1a1a18")
        self.result_num.pack(pady=(14, 2))

        self.result_unit_lbl = tk.Label(result_frame, text="",
                                         font=("Helvetica", 12),
                                         bg="#f5f5f4", fg="#6b6b67")
        self.result_unit_lbl.pack()

        self.result_formula = tk.Label(result_frame, text="",
                                        font=("Courier", 10),
                                        bg="#e8e7e2", fg="#9b9b96")
        self.result_formula.pack(pady=(6, 14))

        # Quick conversions
        tk.Label(self.root, text="COMMON CONVERSIONS",
                 font=("Helvetica", 9, "bold"),
                 bg="#f0efea", fg="#6b6b67").pack(anchor="w", padx=20, pady=(14, 6))

        self.quick_frame = tk.Frame(self.root, bg="#f0efea")
        self.quick_frame.pack(fill="x", padx=20, pady=(0, 20))

    # ── Logic ──────────────────────────────────────────────────────
    def _select_cat(self, cat):
        self.active_cat.set(cat)
        self._update_cat_buttons()
        self._refresh_units()
        self._convert()
        self._build_quick()

    def _update_cat_buttons(self):
        active = self.active_cat.get()
        for cat, btn in self.cat_buttons.items():
            if cat == active:
                btn.config(bg="#4a3fc7", fg="white")
            else:
                btn.config(bg="#e8e7e2", fg="#6b6b67")

    def _refresh_units(self):
        cat = self.active_cat.get()
        units = list(CATEGORIES[cat]["units"].keys())
        self.from_cb["values"] = units
        self.to_cb["values"]   = units
        self.from_unit.set(units[0])
        self.to_unit.set(units[1] if len(units) > 1 else units[0])
        self._build_quick()

    def _swap(self):
        f, t = self.from_unit.get(), self.to_unit.get()
        self.from_unit.set(t)
        self.to_unit.set(f)
        self._convert()

    def _convert(self):
        cat    = self.active_cat.get()
        from_u = self.from_unit.get()
        to_u   = self.to_unit.get()
        try:
            val = float(self.input_val.get())
        except ValueError:
            self.result_num.config(text="—")
            self.result_unit_lbl.config(text="")
            self.result_formula.config(text="")
            return
        result = do_convert(val, from_u, to_u, cat)
        self.result_num.config(text=fmt(result))
        self.result_unit_lbl.config(text=to_u)
        self.result_formula.config(
            text=f"  {val} {from_u}  =  {fmt(result)} {to_u}  "
        )

    def _build_quick(self):
        for w in self.quick_frame.winfo_children():
            w.destroy()
        cat   = self.active_cat.get()
        pairs = CATEGORIES[cat]["quick"]
        for i, (f, t) in enumerate(pairs):
            res  = do_convert(1, f, t, cat)
            card = tk.Frame(self.quick_frame, bg="white",
                            highlightbackground="#d0d0cc", highlightthickness=1,
                            cursor="hand2")
            card.grid(row=0, column=i, padx=4, sticky="nsew")
            self.quick_frame.columnconfigure(i, weight=1)
            lbl1 = tk.Label(card, text=f"1 {f}", font=("Helvetica", 10, "bold"),
                            bg="white", fg="#1a1a18")
            lbl1.pack(anchor="w", padx=10, pady=(8, 0))
            lbl2 = tk.Label(card, text=f"= {fmt(res)} {t}",
                            font=("Helvetica", 9), bg="white", fg="#6b6b67")
            lbl2.pack(anchor="w", padx=10, pady=(2, 8))
            for widget in (card, lbl1, lbl2):
                widget.bind("<Button-1>",
                            lambda e, f=f, t=t: self._quick_fill(f, t))
                widget.bind("<Enter>",
                            lambda e, c=card: c.config(bg="#eeedfe",
                            highlightbackground="#4a3fc7"))
                widget.bind("<Leave>",
                            lambda e, c=card: c.config(bg="white",
                            highlightbackground="#d0d0cc"))

    def _quick_fill(self, f, t):
        self.from_unit.set(f)
        self.to_unit.set(t)
        self.input_val.set("1")
        self._convert()

# ── Run ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = UnitConverterApp(root)
    root.mainloop()
