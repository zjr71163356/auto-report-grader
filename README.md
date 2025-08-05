# 学生实验报告自动评分系统

这是一个基于大语言模型（LLM）的学生实验报告自动评分系统，能够智能分析和评估学生提交的各种格式文件，并生成详细的评分报告。

## 功能特性

- 🤖 **智能评分**: 使用 OpenAI API（支持 DeepSeek 等模型）进行智能评分
- 📄 **多格式支持**: 支持 `.txt`, `.md`, `.py`, `.java`, `.pdf`, `.docx` 等多种文件格式
- 🔍 **OCR 识别**: 自动识别文档中的图片并提取文字内容
- 📁 **批量处理**: 自动解压 ZIP 文件并批量处理多个学生作业
- 📊 **Excel 报告**: 生成详细的 Excel 评分报告
- 🔄 **成绩导入**: 支持将评分结果导入到现有的成绩统计表

## 系统要求

- Python 3.7+
- OpenAI API 密钥
- Tesseract OCR（用于图片文字识别）

## 安装配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 安装 Tesseract OCR

**Ubuntu/Debian:**

```bash
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim
```

**CentOS/RHEL:**

```bash
sudo yum install tesseract tesseract-langpack-chi-sim
```

**macOS:**

```bash
brew install tesseract tesseract-lang
```

### 3. 配置环境变量

设置 OpenAI API 相关环境变量：

```bash
export OPENAI_API_KEY="your_api_key_here"
export OPENAI_BASE_URL="https://api.deepseek.com"  # 可选，默认使用OpenAI官方API
```

## 使用方法

### 1. 主要评分脚本 (`score.py`)

用于批量评分学生实验报告：

```bash
python score.py
```

**功能说明：**

- 自动扫描指定目录下的学生文件夹
- 解压学生提交的 ZIP 文件
- 提取各种格式文件的文本内容
- 使用 LLM 根据评分标准进行智能评分
- 生成 `LLM_评分结果.xlsx` 报告

**目录结构要求：**

```

├── scripts/          # 脚本目录
├── 学生1/           # 学生文件夹
│   ├── 报告.docx
│   └── 代码.zip
├── 学生2/
└── 测试管理评分标准.txt  # 评分标准文件
```

### 2. 成绩导入脚本 (`insert_score.py`)

将 LLM 评分结果导入到成绩统计表：

```bash
python insert_score.py
```

**功能说明：**

- 读取 `LLM_评分结果2.xlsx` 中的评分结果
- 根据学生姓名匹配并更新 `成绩统计表-单元测试实验报告.xlsx`
- 自动保存更新后的成绩表

### 3. 文件扩展名统计脚本 (`list.py`)

扫描目录中的所有文件类型：

```bash
python list.py
```

**功能说明：**

- 递归扫描指定目录
- 统计所有文件的扩展名
- 帮助了解学生提交文件的类型分布

## 支持的文件格式

| 格式           | 描述       | 特殊功能          |
| -------------- | ---------- | ----------------- |
| `.txt`, `.md`  | 纯文本文件 | 直接读取          |
| `.py`, `.java` | 代码文件   | 语法高亮支持      |
| `.pdf`         | PDF 文档   | 自动处理加密文件  |
| `.docx`        | Word 文档  | 支持图片 OCR 识别 |
| `.zip`         | 压缩文件   | 自动解压处理      |

## 配置说明

### 评分标准文件

在项目根目录创建 `测试管理评分标准.txt` 文件，包含详细的评分标准。LLM 将根据此文件进行评分。

### LLM 模型配置

在 `score.py` 中可以修改使用的模型：

```python
LLM_MODEL = "deepseek-chat"  # 可改为其他支持的模型
```

### 文件路径配置

在 `insert_score.py` 中可以修改文件路径：

```python
grades_file = '成绩统计表-单元测试实验报告.xlsx'  # 成绩表文件
scores_file = 'LLM_评分结果2.xlsx'              # 评分结果文件
```

## 输出文件

- `LLM_评分结果.xlsx`: 包含每个学生的详细评分和评语
- 更新后的成绩统计表: 包含导入的 LLM 评分结果

## 注意事项

1. **API 限制**: 注意 OpenAI API 的调用频率和费用限制
2. **文件编码**: 确保所有文本文件使用 UTF-8 编码
3. **内存使用**: 处理大量文件时可能占用较多内存
4. **网络连接**: 需要稳定的网络连接访问 LLM API
5. **权限设置**: 确保脚本有读写相关文件和目录的权限

## 故障排除

### 常见问题

1. **API 密钥错误**

   ```
   错误：未找到 OpenAI API 密钥
   ```

   解决：检查环境变量 `OPENAI_API_KEY` 是否正确设置

2. **Tesseract 未安装**

   ```
   TesseractNotFoundError
   ```

   解决：安装 Tesseract OCR 软件并确保在 PATH 中

3. **文件权限问题**

   ```
   PermissionError: [Errno 13] Permission denied
   ```

   解决：检查文件和目录的读写权限

4. **ZIP 文件损坏**
   ```
   BadZipFile: File is not a zip file
   ```
   解决：检查 ZIP 文件完整性，脚本会自动跳过损坏文件

## 贡献

欢迎提交 Issue 和 Pull Request 来改进此项目。

## 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。

## 更新日志

- **v1.0**: 初始版本，支持基本的文档评分功能
- **v1.1**: 添加 OCR 支持，支持 Word 文档中的图片识别
- **v1.2**: 优化错误处理，添加更多文件格式支持
