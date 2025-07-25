<p align="center">
  <a href="https://i.ibb.co/WpVb0QyK/icon.png">
    <img src="https://i.ibb.co/WpVb0QyK/icon.png" alt="ImageCompressor Logo" width="250"/>
  </a>
</p>

<h1 align="center">ImageCompressor – Advanced Image Compression Tool</h1>
<p align="center"><em>(by Jakub Ešpandr)</em></p>

## Overview

**ImageCompressor** is a powerful GUI application for compressing JPG, PNG, and other image formats with advanced resampling and optimization techniques. It features quality controls, smart resizing, multiple resampling algorithms, and a modern interface. Perfect for photographers, web developers, and anyone who needs to reduce image file sizes while maintaining quality.

---

## ✨ Features

- **Multi-Format Support**
  - Input: JPG, JPEG, PNG, BMP, TIFF, WebP
  - Output: JPEG, PNG, WebP (with auto-detection)
  - Batch processing of multiple files or entire folders
- **Advanced Compression Settings**
  - Adjustable quality slider (1–100)
  - Smart resizing with maximum width/height limits
  - 6 resampling methods: LANCZOS, BICUBIC, BILINEAR, NEAREST, BOX, HAMMING
- **Optimization Features**
  - Progressive JPEG for better web loading
  - Optimize flag for enhanced compression
  - EXIF data preservation
  - Format conversion for better compression
- **Real-time Preview & Analysis**
  - Live image preview before compression
  - File size estimation and compression ratio prediction
  - Detailed image properties display
  - Progress tracking with real-time updates
- **Modern UI**
  - Custom fonts and icons
  - Two-column layout for efficient space usage
  - Settings persistence and management

---

## 📦 Requirements

- Python 3.7+
- [Pillow](https://python-pillow.org/) – Image processing library
- Tkinter (usually included with Python)
- Custom fonts (included in `assets/fonts/`)

---

## 🚀 Installation

```bash
git clone https://github.com/Jakub-Espandr/ImageCompressor.git
cd ImageCompressor
```

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

Install required Python libraries:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

---

## 🛠️ Usage

1. **Add Images**: Click "Add Files" to select individual images or "Add Folder" to process entire directories.
2. **Choose Output Directory**: Select where compressed files will be saved.
3. **Configure Settings**: Adjust quality, size limits, resampling method, and format options.
4. **Preview**: Select files to see preview and estimated compression results.
5. **Compress**: Click "Compress Images" to start processing.
6. **Monitor Progress**: Watch the progress bar and log for real-time updates.

### Compression Strategies

**For Maximum Compression:**
- Set quality to 60-70
- Use aggressive size limits (e.g., 800x600)
- Enable "Optimize"
- Convert to JPEG for photos, WebP for web

**For Best Quality:**
- Set quality to 90-95
- Use large size limits (e.g., 3840x2160)
- Use LANCZOS resampling
- Keep original format or use PNG

**For Web Optimization:**
- Set quality to 80-85
- Use moderate size limits (e.g., 1920x1080)
- Enable "Progressive JPEG"
- Convert to WebP when possible

---

## 📁 Project Structure

```
ImageCompressor/
├── main.py                  # Entry point
├── assets/
│   ├── icons/              # Application icons (icon.png, icon.ico, icon.icns)
│   └── fonts/              # Custom fonts (fccTYPO-Regular.ttf, fccTYPO-Bold.ttf)
├── requirements.txt        # Dependencies
└── README.md               # This file
```

---

## 🔐 License

This project is licensed under the **Non-Commercial Public License (NCPL v1.0)**  
© 2025 Jakub Ešpandr - Born4FLight, FlyCamCzech

See the [LICENSE](https://github.com/Jakub-Espandr/imagecompressor/raw/main/LICENSE) file for full terms.

---

## 🙏 Acknowledgments

- Built with ❤️ using Tkinter, Pillow, and open-source libraries 