# 学生实验报告自动评分系统 / Auto Lab Report Grading System

[English Version](#auto-lab-report-grading-system) | [中文版](#学生实验报告自动评分系统)

---

## 学生实验报告自动评分系统

这是一个基于大语言模型（LLM）的学生实验报告自动评分系统，能够智能分析和评估学生提交的各种格式文件，并生成详细的评分报告。

### 功能特性

- 🤖 **智能评分**: 使用 OpenAI API（支持 DeepSeek 等模型）进行智能评分
- 📄 **多格式支持**: 支持 `.txt`, `.md`, `.py`, `.java`, `.pdf`, `.docx` 等多种文件格式
- 🔍 **OCR 识别**: 自动识别文档中的图片并提取文字内容
- 📁 **批量处理**: 自动解压 ZIP 文件并批量处理多个学生作业
- 📊 **Excel 报告**: 生成详细的 Excel 评分报告
- 🔄 **成绩导入**: 支持将评分结果导入到现有的成绩统计表

### 系统要求

- Python 3.7+
- OpenAI API 密钥
- Tesseract OCR（用于图片文字识别）

### 安装配置

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 安装 Tesseract OCR：
   ```bash
   sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim
   ```

3. 配置环境变量：
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```

### 使用方法

运行评分脚本：
```bash
python score.py
```

---

## Auto Lab Report Grading System

This is an AI-powered auto-grading system for student lab reports based on Large Language Models (LLM). It can intelligently analyze and evaluate various file formats submitted by students and generate detailed grading reports.

### Features

- 🤖 **Intelligent Grading**: Utilizes OpenAI API (supports models like DeepSeek) for intelligent grading.
- 📄 **Multi-format Support**: Supports `.txt`, `.md`, `.py`, `.java`, `.pdf`, `.docx`, and more.
- 🔍 **OCR Recognition**: Automatically recognizes text in images within documents.
- 📁 **Batch Processing**: Automatically extracts ZIP files and processes multiple student submissions.
- 📊 **Excel Reports**: Generates detailed grading reports in Excel format.
- 🔄 **Grade Import**: Supports importing grading results into existing grade sheets.

### System Requirements

- Python 3.7+
- OpenAI API Key
- Tesseract OCR (for image text recognition)

### Installation & Configuration

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install Tesseract OCR:
   ```bash
   sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim
   ```

3. Configure environment variables:
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```

### Usage

Run the grading script:
```bash
python score.py
```