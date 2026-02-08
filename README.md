# 📦 Inventory Tag OCR Scanner

An AI-powered Streamlit app that automatically extracts data from inventory tag photos using OCR technology.

## 🎯 Features

- ✅ **OCR Image Processing** - Automatically extract text from tag photos
- ✅ **Smart Field Extraction** - Captures Book No., Tag Sr No., Material No., Quantity, and Location
- ✅ **Single & Batch Processing** - Process one or multiple tags at once
- ✅ **Editable Results** - Review and correct OCR results before export
- ✅ **Excel & CSV Export** - Download data in multiple formats
- ✅ **Real-time Validation** - Confidence levels for extracted data

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/tushardusra/inventory-tag-scanner.git
cd inventory-tag-scanner
```

2. **Create virtual environment** (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📸 Usage

### Single Tag Mode
1. Upload a tag image
2. OCR automatically extracts text
3. Review and edit fields if needed
4. Click "Add to List" to save entry

### Batch Processing Mode
1. Upload multiple tag images
2. Click "Process All Images"
3. Review all extracted data
4. Export to Excel/CSV

## 📋 Extracted Fields

- **Book No.** - Book reference number
- **Tag Sr No.** - Tag serial number
- **Material No.** - Material/Item number
- **Quantity** - Item quantity
- **Mat. Location** - Material location/warehouse

## 🛠️ Troubleshooting

### Port already in use
```bash
streamlit run app.py --server.port 8502
```

### Dependencies installation fails
```bash
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

### OCR taking too long
First run will download the OCR model (~100MB). Subsequent runs will be faster.

## 📝 Example Tag Format

The app is optimized for TPEML Sanand standard inventory tags with:
- Book No. (top right)
- Tag Sr No. (top right)
- Material No. (alphanumeric code)
- Quantity (numeric value)
- Mat. Location (warehouse/location code)

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

MIT License - feel free to use this project!

## 👤 Author

[tushardusra](https://github.com/tushardusra)

---

**Need help?** Open an issue on GitHub or check the troubleshooting section above.