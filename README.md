# Cybersecurity Pool: Arachnida 🕷️

## Overview
**Arachnida** is a two-phase project focusing on web scraping and metadata analysis.

The project includes the following sections:
1. **Spider**: A program that recursively downloads images from websites.
2. **Scorpion**: A program that parses and displays metadata from image files.

This project aims to provide practical experience in web data extraction and working with metadata.

---

#### Installation
- Clone the repository:
```bash
git clone https://github.com/whymami/Arachnida
cd Arachnida
```
---

## Features

### Spider 🕸️
- Recursively downloads images from a specified URL.
- Supported image formats: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`.
- Program Options:
  - **`-r`**: Enables recursive downloading.
  - **`-r -l [N]`**: Sets recursive download depth (default: 5).
  - **`-p [PATH]`**: Sets the directory for downloaded files (default: `./data/`).
  - **`-h`**: Provides detailed information about parameters.

#### Usage
```bash
python3 Spider.py [-r] [-l N] [-p PATH] URL
```

# Scorpion 🦂

Analyzes and displays metadata from image files:
- **Creation date.**
- **EXIF data.**
- Compatible with the same formats as Spider.

## Usage

```bash
./python3 Scorpion.py FILE1 [FILE2 ...]
```

#### Bonus Part ✨
- Edit or delete metadata in image files.
- Graphical interface for metadata management.

## Usage
```bash
cd bonus
python3 main.py
```

## Project Structure
```plaintext
.
├── Spider.py               # Spider program
├── Scorpion.py            # Scorpion program
├── data/                  # Default directory for files downloaded by Spider
├── bonus/                 # Bonus section
│   ├── Scorpion.py        # Scorpion program for bonus
│   ├── main.py            # Bonus main file
│   └── gui.py             # Graphical interface file
│   └── requirements.txt   # Requirements file
└── README.md              # Project documentation
```
