# 📄 Project Documentation — Unit Converter


## 1. Introduction

### 1.1 Purpose
The Unit Converter is a Python-based application that converts values between different units across 7 major categories. It provides instant, accurate conversions with a clean user interface.

### 1.2 Project Scope
The scope of this project is to design and develop a Unit Converter application using Python that enables users to convert between 70+ units across 7 categories including Length, Weight, Temperature, Volume, Speed, Time, and Area, featuring a Tkinter desktop GUI, a Flask web application, and a standalone HTML version deployed on Vercel.

### 1.3 Intended Audience
- Students needing unit conversions for studies
- Engineers and scientists
- Anyone needing quick unit conversions


## 2. System Overview

The Unit Converter is built in three versions:

| Version | Technology | Platform |
|---|---|---|
| Desktop GUI | Python + Tkinter | Windows/Mac/Linux |
| Web App | Python + Flask | Browser (Vercel) |
| Standalone HTML | HTML + CSS + JS | Any Browser |


## 3. Features & Functionality

### 3.1 Categories
| Category | Number of Units |
|---|---|
| 📏 Length | 10 units |
| ⚖️ Weight | 8 units |
| 🌡️ Temperature | 4 units |
| 💧 Volume | 11 units |
| ⚡ Speed | 6 units |
| 🕐 Time | 9 units |
| 📐 Area | 9 units |

### 3.2 Core Features
- Select any category from tabs
- Choose FROM and TO units
- Enter value and get instant result
- Swap units with one click
- Quick conversion cards for common pairs
- Formula display showing full equation

### 3.3 Temperature Conversion
Special logic handles temperature (non-linear conversion):
- Celsius ↔ Fahrenheit
- Celsius ↔ Kelvin
- Celsius ↔ Rankine
- All combinations supported



## 4. Technical Design

### 4.1 Conversion Logic

**Standard Units (multiplier-based):**
```python
result = value × from_unit_factor / to_unit_factor
```

**Temperature (formula-based):**
```python
# Convert to Celsius first, then to target
Celsius → Fahrenheit: (C × 9/5) + 32
Celsius → Kelvin: C + 273.15
Celsius → Rankine: (C + 273.15) × 9/5
```

### 4.2 Unit Factors (Sample)

```python
Length = {
  "Meter": 1,
  "Kilometer": 1000,
  "Centimeter": 0.01,
  "Mile": 1609.344,
  "Foot": 0.3048,
  "Inch": 0.0254
}
```

### 4.3 Key Functions

| Function | Description |
|---|---|
| `convert_temp()` | Handles temperature conversions |
| `do_convert()` | Handles all other conversions |
| `fmt()` | Formats result number nicely |
| `build_cats()` | Builds category tab buttons |
| `build_selects()` | Populates unit dropdowns |
| `update()` | Triggers conversion & updates UI |
| `build_quick()` | Builds quick conversion cards |

### 4.4 Flask API Route

| Route | Method | Description |
|---|---|---|
| `/` | GET | Load converter page |
| `/convert` | POST | Perform conversion |

**Request format:**
```json
{
  "value": 100,
  "from_unit": "Kilometer",
  "to_unit": "Mile",
  "category": "Length"
}
```

**Response format:**
```json
{
  "result": 62.1371
}
```


## 5. Testing

| Test Case | Input | Expected Output | Result |
|---|---|---|---|
| Length conversion | 1 Kilometer | 0.621371 Mile | ✅ Pass |
| Temperature | 100 Celsius | 212 Fahrenheit | ✅ Pass |
| Weight | 1 Kilogram | 2.20462 Pound | ✅ Pass |
| Swap units | Click ⇄ | Units swapped | ✅ Pass |
| Invalid input | Text in value | Shows dash | ✅ Pass |
| Quick card click | Click card | Auto-fills form | ✅ Pass |
| Large number | 1,000,000 m | 1000 km | ✅ Pass |


## 6. Limitations

- No offline mobile support
- Temperature uses simplified Rankine formula
- No history of past conversions
- No copy-to-clipboard button


## 7. Future Enhancements

- 📋 Copy result to clipboard
- 🕐 Conversion history log
- 📱 Mobile app (Kivy)
- 🌍 More units (Currency, Data, Pressure)
- 🗣️ Voice input support


## 8. Conclusion

The Unit Converter application delivers a complete and accurate unit conversion tool supporting 7 categories and 70+ units. It demonstrates Python logic, GUI development, REST API design, and web deployment skills gained during the CodeTech IT Solutions internship.


