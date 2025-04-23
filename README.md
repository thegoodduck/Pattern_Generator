# 🌈 Pattern Generator

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.7%2B-blue.svg" alt="Python 3.7+"/>
  <img src="https://img.shields.io/badge/Flask-2.0%2B-green.svg" alt="Flask 2.0+"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"/>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen.svg" alt="Status: Active"/>
</div>

## 📋 Overview

Pattern Generator is a web application that creates customized patterns for various use cases including testing, education, and creative projects. The tool allows users to generate patterns with different complexity levels and character sets, outputting the results in a visually appealing PDF format with random placement and colorful text.

### 🎯 Key Features

- **Customizable Pattern Generation**: Control pattern complexity with adjustable difficulty levels
- **Character Set Selection**: Use digits, letters, or custom character sets for pattern creation
- **Multiple Pattern Generation**: Create several different patterns in a single PDF document
- **Beautiful Output**: Colorful, visually appealing PDF output with rainbow-colored text
- **Flexible Rendering Options**: Supports WeasyPrint (emoji-friendly) and ReportLab PDF backends

[Proof of Concept (ptgen.pythonanywhere.com)](https://ptgen.pythonanywhere.com)
## 🚀 Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/thegoodduck/Pattern_Generator.git
cd Pattern_Generator
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install flask weasyprint reportlab
```

## 💻 Usage

### Running the Application

1. Start the Flask server:
```bash
python main.py
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

### Creating Patterns

1. Set your desired **Difficulty Level** (higher values create more complex patterns)
2. Enter a **Character Set** (digits for numeric patterns, any characters for text patterns)
3. Optionally add additional patterns using the "Add Another Pattern" button
4. Click "Generate PDF" to create and download your custom pattern document

### Examples

#### Numeric Pattern
- **Difficulty**: 5
- **Character Set**: 0123456789
- **Result**: A pattern using random digits with mathematical operations applied

#### Text Pattern
- **Difficulty**: 3
- **Character Set**: ABCDEF
- **Result**: A repeating sequence of randomly selected letters

## ⚙️ Pattern Generation Algorithms

The application uses three different algorithms to generate patterns:

1. **Simple Repetition**: Repeats a randomly generated character sequence
2. **Selective Digit Modification**: Applies mathematical operations to specific positions in a sequence
3. **Full Sequence Transformation**: Applies operations to every character in a sequence

## 🔧 Customization

### PDF Backend Selection

The application supports two PDF generation backends:

```python
# In main.py:
USE_WEASYPRINT = True  # Set to False to use ReportLab instead
```

- **WeasyPrint**: Better support for emoji and complex characters
- **ReportLab**: More lightweight, fewer dependencies

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

Made with ❤️ by [@thegoodduck](https://github.com/thegoodduck)

---

<div align="center">
  <p>⭐ Star this repository if you find it useful! ⭐</p>
  <p>
    <a href="https://github.com/thegoodduck/Pattern_Generator/issues">Report Bug</a> ·
    <a href="https://github.com/thegoodduck/Pattern_Generator/issues">Request Feature</a>
  </p>
</div>
