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

#### 快速开始

1. **设置环境变量**：
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```

2. **安装依赖**：
   ```bash
   cd /home/tyrfly1001/LabTask/auto-report-grader
   pip install -r requirements.txt
   ```

3. **运行评分脚本**：
   ```bash
   python score.py
   ```

4. **（可选）导入成绩到统计表**：
   ```bash
   python insert_score.py
   ```

#### 一键测试

运行测试脚本，自动完成所有步骤：
```bash
python test_grading_system.py
```

#### 文件说明

- `score.py`: 主要的评分脚本，读取 `/home/tyrfly1001/LabTask/task1/collected` 目录下的学生作业并评分
- `insert_score.py`: 将评分结果导入到现有成绩统计表
- `test_grading_system.py`: 一键测试脚本，自动化整个流程
- `requirements.txt`: Python依赖列表

#### 配置说明

评分系统会自动：
1. 读取 `/home/tyrfly1001/LabTask/task1/collected` 目录下的所有学生文件夹
2. 解压每个文件夹内的ZIP文件
3. 提取支持格式的文件内容（.txt, .md, .py, .java, .pdf, .docx等）
4. 使用LLM根据 `/home/tyrfly1001/LabTask/task1/criteria/criteria.md` 中的评分标准进行评分
5. 生成 `LLM_评分结果.xlsx` 评分报告

#### 输出文件

- `LLM_评分结果.xlsx`: 包含学号、姓名、分数和评语的详细评分结果
- `成绩统计表_已更新.xlsx`: 如果运行了成绩导入，会生成更新后的成绩统计表

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

#### Quick Start

1. **Set Environment Variable**:
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```

2. **Install Dependencies**:
   ```bash
   cd /home/tyrfly1001/LabTask/auto-report-grader
   pip install -r requirements.txt
   ```

3. **Run Grading Script**:
   ```bash
   python score.py
   ```

4. **(Optional) Import Grades to Statistics Table**:
   ```bash
   python insert_score.py
   ```

#### One-click Test

Run the test script to automatically complete all steps:
```bash
python test_grading_system.py
```

#### File Descriptions

- `score.py`: The main grading script that reads and grades student submissions in the `/home/tyrfly1001/LabTask/task1/collected` directory.
- `insert_score.py`: Imports grading results into the existing grade statistics table.
- `test_grading_system.py`: One-click test script that automates the entire process.
- `requirements.txt`: Python dependencies list.

#### Configuration Details

The grading system will automatically:
1. Read all student folders in the `/home/tyrfly1001/LabTask/task1/collected` directory.
2. Extract ZIP files within each folder.
3. Extract content from supported file formats (.txt, .md, .py, .java, .pdf, .docx, etc.).
4. Grade submissions based on the criteria in `/home/tyrfly1001/LabTask/task1/criteria/criteria.md` using the LLM.
5. Generate the `LLM_评分结果.xlsx` grading report.

#### Output Files

- `LLM_评分结果.xlsx`: Detailed grading results including student ID, name, score, and comments.
- `成绩统计表_已更新.xlsx`: Updated grade statistics table if the grade import was run.