"""
OCR 文本提取模块
负责从图片中提取文本内容
"""
import io
from typing import Optional

# 全局导入可能导致 Pylance 警告，移至函数内部
PYTESSERACT_AVAILABLE = None
PILLOW_AVAILABLE = None


def extract_text_from_image(image_data: bytes, lang: Optional[str] = None) -> str:
    """
    从图片数据中提取文本

    Args:
        image_data: 图片的二进制数据
        lang: OCR 语言设置，默认使用配置中的设置

    Returns:
        提取的文本内容
    """
    global PYTESSERACT_AVAILABLE, PILLOW_AVAILABLE
    if PYTESSERACT_AVAILABLE is None:
        try:
            import pytesseract
            PYTESSERACT_AVAILABLE = True
        except ImportError:
            PYTESSERACT_AVAILABLE = False
    if PILLOW_AVAILABLE is None:
        try:
            from PIL import Image
            PILLOW_AVAILABLE = True
        except ImportError:
            PILLOW_AVAILABLE = False

    if not (PYTESSERACT_AVAILABLE and PILLOW_AVAILABLE):
        if VERBOSE_LOGGING:
            print("    - 警告: OCR 功能不可用，请安装 pytesseract 和 Pillow")
        return ""

    # 导入必要的模块
    import pytesseract
    from PIL import Image
    from config import OCR_LANGUAGES, VERBOSE_LOGGING

    try:
        # 使用配置中的语言设置
        ocr_lang = lang or OCR_LANGUAGES

        # 从二进制数据创建图片对象
        image_stream = io.BytesIO(image_data)
        image = Image.open(image_stream)

        # 执行 OCR
        ocr_text = pytesseract.image_to_string(image, lang=ocr_lang)

        # 返回清理后的文本
        return ocr_text.strip()

    except Exception as e:
        if VERBOSE_LOGGING:
            print(f"    - 警告: OCR 提取失败: {e}")
        return ""


def is_ocr_available() -> bool:
    """
    检查 OCR 功能是否可用

    Returns:
        OCR 是否可用
    """
    global PYTESSERACT_AVAILABLE, PILLOW_AVAILABLE
    if PYTESSERACT_AVAILABLE is None:
        try:
            import pytesseract
            PYTESSERACT_AVAILABLE = True
        except ImportError:
            PYTESSERACT_AVAILABLE = False
    if PILLOW_AVAILABLE is None:
        try:
            from PIL import Image
            PILLOW_AVAILABLE = True
        except ImportError:
            PILLOW_AVAILABLE = False
    return PYTESSERACT_AVAILABLE and PILLOW_AVAILABLE
