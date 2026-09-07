# Drywall Calculator

A robust, multilingual, and unit-swappable desktop application designed to calculate drywall partition materials accurately based on area and perimeter parameters.

## 🚀 Features

* Dual unit support (Metric and Imperial with automatic input scaling)
* Multilingual interface (English, Spanish, and Portuguese)
* Smart calculation logic for height splices (> 2.60 m)
* Comprehensive material breakdown (Tracks, Studs, Boards, Anchors, T1/T2 Screws, Paper Tape, Joint Compound)
* Linux AppImage distribution

## 📦 Installation

### AppImage

Download the latest AppImage from the Releases page.

Make it executable:

```bash
chmod +x Drywall_Calculator-x86_64.AppImage

```

Run the application:

```bash
./Drywall_Calculator-x86_64.AppImage

```

## 🛠️ Development

Clone the repository:

```bash
git clone https://github.com/necrisscript/drywall-calculator.git
cd drywall-calculator

```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate

```

Install the dependencies:

```bash
pip install -r requirements.txt

```

Run the application:

```bash
python main.py

```

## 🔨 Build

The project uses PyInstaller to create the Linux executable and linuxdeploy to package it as an AppImage.

Build the executable:

```bash
pyinstaller --clean drywall_calculator.spec

```

The executable will be generated in:

```bash
dist/drywall-calculator

```

The resulting AppImage can then be generated using linuxdeploy.

## 📄 License

This project is licensed under the MIT License — see the LICENSE file for details.