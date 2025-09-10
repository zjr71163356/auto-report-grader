# 自动评分系统 - 模块化版本

## 📁 项目结构

```
src/
├── __init__.py          # 包初始化
├── config.py            # 配置文件（路径、参数等）
├── models.py            # 数据模型定义
├── file_utils.py        # 文件处理工具
├── text_extractor.py    # 文本提取模块
├── ocr.py              # OCR 功能模块
├── llm_client.py       # LLM 客户端模块
├── report.py           # 报告生成模块
├── score.py            # 主程序入口
├── test_config.py      # 配置测试脚本
└── test_refactor.py    # 重构测试脚本
```

## 🔧 模块说明

### config.py
- **作用**: 集中管理所有配置信息
- **内容**: API 密钥、文件路径、模型参数等
- **优势**: 便于不同环境配置，无需修改代码

### models.py
- **作用**: 定义数据结构
- **内容**: `StudentSubmission`, `ScoreResult`, `ProcessingResult`
- **优势**: 类型安全，代码可读性强

### file_utils.py
- **作用**: 文件处理功能
- **内容**: 压缩文件解压、文件类型检测
- **优势**: 解耦文件操作逻辑，便于测试

### text_extractor.py
- **作用**: 文本提取功能
- **内容**: 从各种文件格式提取文本
- **优势**: 支持多种文件格式，包含 OCR 功能

### ocr.py
- **作用**: OCR 文本识别
- **内容**: 图片文本提取
- **优势**: 可选功能，依赖检查

### llm_client.py
- **作用**: LLM 交互
- **内容**: API 调用、评分逻辑、错误处理
- **优势**: 封装外部依赖，便于测试和替换

### report.py
- **作用**: 报告生成
- **内容**: Excel 报告、统计信息
- **优势**: 专注报告功能，便于扩展

### score.py
- **作用**: 主程序协调器
- **内容**: 流程控制，模块调用
- **优势**: 简洁清晰，只负责调度

## 🚀 使用方法

### 基本运行
```bash
cd src
python score.py
```

### 自定义路径
```bash
python score.py --collected-dir /path/to/students --rubric-file /path/to/criteria.md
```

### 测试
```bash
# 测试配置
python test_config.py

# 测试重构
python test_refactor.py
```

## 📋 重构优势

1. **可维护性**: 每个模块职责单一，易于修改
2. **可测试性**: 模块独立，便于单元测试
3. **可扩展性**: 新功能可轻松添加
4. **可复用性**: 模块可在其他项目中使用
5. **类型安全**: 使用 dataclass 和类型注解
6. **错误处理**: 每个模块独立处理异常
7. **配置集中**: 所有配置统一管理

## 🔧 依赖包

- `pandas`: 数据处理和 Excel 生成
- `openpyxl`: Excel 文件操作
- `python-docx`: Word 文档处理
- `PyPDF2`: PDF 文本提取
- `rarfile`: RAR 文件解压
- `pytesseract`: OCR 功能
- `Pillow`: 图片处理

## 📝 开发说明

- 所有模块都包含完善的错误处理
- 使用条件导入处理可选依赖
- 配置信息集中管理，便于部署
- 代码结构清晰，易于理解和维护

## 🎯 下一步优化

1. 添加单元测试覆盖
2. 实现并发处理加速
3. 添加命令行参数支持
4. 实现日志系统
5. 添加性能监控
