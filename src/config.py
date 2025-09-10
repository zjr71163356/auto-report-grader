import os
from pathlib import Path

# === API 配置 ===
# OpenAI API 配置
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_BASE_URL = os.environ.get(
    "OPENAI_BASE_URL", "https://api.siliconflow.cn/v1")

# LLM 模型配置
LLM_MODEL = "deepseek-ai/DeepSeek-V3"

# === 文件路径配置 ===
# 项目根目录 - 使用绝对路径确保稳定性
PROJECT_ROOT = Path("/home/tyrfly1001/LabTask")

# 任务目录
TASK_DIR = PROJECT_ROOT / "task1"

# 学生作业收集目录
COLLECTED_DIR = TASK_DIR / "collected"

# 评分标准文件
RUBRIC_FILE = TASK_DIR / "criteria" / "criteria.md"

# 输出文件名
OUTPUT_FILENAME = "LLM_评分结果.xlsx"

# === 文件处理配置 ===
# 支持的文件扩展名
SUPPORTED_EXTENSIONS = ['*.txt', '*.md', '*.py',
                        '*.java', '*.pdf', '*.docx', '*.doc']

# 压缩文件扩展名
ZIP_EXTENSIONS = ['*.zip']
RAR_EXTENSIONS = ['*.rar']

# === OCR 配置 ===
# Tesseract OCR 语言设置
OCR_LANGUAGES = 'eng+chi_sim'

# === 评分配置 ===
# 评分温度参数
SCORING_TEMPERATURE = 0.2

# 分数范围
MIN_SCORE = 0
MAX_SCORE = 10
DEFAULT_SCORE = 5.0

# === 日志配置 ===
# 是否显示详细日志
VERBOSE_LOGGING = True
