"""
文本提取模块
负责从各种文件格式中提取文本内容
"""
from ocr import extract_text_from_image, is_ocr_available
from config import SUPPORTED_EXTENSIONS, VERBOSE_LOGGING
import os
import io
import subprocess
from typing import List

# 将可选依赖的导入移至函数内部，避免 Pylance 警告
PYPDF2_AVAILABLE = None
DOCX_AVAILABLE = None


def extract_text_from_folder(folder_path: str) -> str:
    """
    从文件夹中递归提取所有支持文件的文本内容

    Args:
        folder_path: 文件夹路径

    Returns:
        提取的文本内容
    """
    import glob

    if VERBOSE_LOGGING:
        print(f"  - 开始从 {os.path.basename(folder_path)} 提取文本...")

    full_text = ""
    supported_extensions = SUPPORTED_EXTENSIONS

    # 查找所有支持的文件
    files_to_process = []
    for ext in supported_extensions:
        pattern = os.path.join(folder_path, '**', ext)
        files_to_process.extend(glob.glob(pattern, recursive=True))

    if not files_to_process:
        if VERBOSE_LOGGING:
            print("    - 未找到支持的文本文件。")
        return "[内容为空或文件格式不支持]"

    # 处理每个文件
    for file_path in files_to_process:
        content = extract_text_from_file(file_path)
        if content:
            file_name = os.path.basename(file_path)
            full_text += f"\n\n--- 文件: {file_name} ---\n\n{content}"

    if not full_text:
        return "[内容为空或所有文件均无法提取]"

    return full_text


def extract_text_from_file(file_path: str) -> str:
    """
    从单个文件中提取文本内容

    Args:
        file_path: 文件路径

    Returns:
        提取的文本内容
    """
    file_name = os.path.basename(file_path)
    file_ext = os.path.splitext(file_name)[1].lower()

    try:
        if file_ext == '.docx':
            return extract_text_from_docx(file_path)
        elif file_ext == '.pdf':
            return extract_text_from_pdf(file_path)
        elif file_ext == '.doc':
            return extract_text_from_doc(file_path)
        elif file_ext in ['.txt', '.md', '.py', '.java']:
            return extract_text_from_plain_text(file_path)
        else:
            return ""

    except Exception as e:
        error_message = f"提取失败: {e}"
        if VERBOSE_LOGGING:
            print(f"    - 警告: 无法从 {file_path} 提取文本: {e}")
        return f"[{error_message}]"


def extract_text_from_docx(file_path: str) -> str:
    """
    从 DOCX 文件中提取文本内容（包含图片 OCR）

    Args:
        file_path: DOCX 文件路径

    Returns:
        提取的文本内容
    """
    global DOCX_AVAILABLE
    if DOCX_AVAILABLE is None:
        try:
            import docx
            DOCX_AVAILABLE = True
        except ImportError:
            DOCX_AVAILABLE = False

    if not DOCX_AVAILABLE:
        return "[DOCX 处理功能不可用，请安装 python-docx]"

    import docx

    try:
        doc = docx.Document(file_path)
        content_parts = []

        for para in doc.paragraphs:
            # 添加段落文本
            if para.text.strip():
                content_parts.append(para.text)

            # 检查并处理图片
            if is_ocr_available():
                for run in para.runs:
                    if run.element.xpath('.//pic:pic'):
                        # 提取图片并进行 OCR
                        ocr_text = extract_ocr_from_docx_run(run)
                        if ocr_text:
                            ocr_block = f"\n--- [图片OCR内容开始] ---\n{ocr_text}\n--- [图片OCR内容结束] ---\n"
                            content_parts.append(ocr_block)
                            if VERBOSE_LOGGING:
                                print(
                                    f"      - 成功对 {os.path.basename(file_path)} 中的一张图片进行OCR。")

        return "\n".join(content_parts)

    except Exception as e:
        if VERBOSE_LOGGING:
            print(f"    - DOCX 处理失败: {e}")
        return f"[DOCX 文件处理失败: {e}]"


def extract_ocr_from_docx_run(run) -> str:
    """
    从 DOCX 的 run 对象中提取图片并进行 OCR

    Args:
        run: DOCX run 对象

    Returns:
        OCR 提取的文本
    """
    try:
        # 获取图片的 rId
        for r in run.element.xpath(".//a:blip"):
            rId = r.get(
                '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
            if rId:
                image_part = run.part.related_parts[rId]
                image_data = image_part.blob
                return extract_text_from_image(image_data)
    except Exception as e:
        if VERBOSE_LOGGING:
            print(f"      - 图片 OCR 失败: {e}")
    return ""


def extract_text_from_pdf(file_path: str) -> str:
    """
    从 PDF 文件中提取文本内容

    Args:
        file_path: PDF 文件路径

    Returns:
        提取的文本内容
    """
    global PYPDF2_AVAILABLE
    if PYPDF2_AVAILABLE is None:
        try:
            import PyPDF2
            PYPDF2_AVAILABLE = True
        except ImportError:
            PYPDF2_AVAILABLE = False

    if not PYPDF2_AVAILABLE:
        return "[PDF 处理功能不可用，请安装 PyPDF2]"

    import PyPDF2

    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)

            # 检查是否加密
            if reader.is_encrypted:
                return "[文件已加密，无法提取内容]"

            content = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    content += extracted + "\n"

            return content

    except Exception as e:
        if VERBOSE_LOGGING:
            print(f"    - PDF 处理失败: {e}")
        return f"[PDF 文件处理失败: {e}]"


def extract_text_from_doc(file_path: str) -> str:
    """
    从 DOC 文件中提取文本内容（通过转换为 DOCX）

    Args:
        file_path: DOC 文件路径

    Returns:
        提取的文本内容
    """
    try:
        # 尝试使用 libreoffice 转换为 DOCX
        docx_path = os.path.splitext(file_path)[0] + '.docx'

        # 检查转换后的文件是否已存在
        if not os.path.exists(docx_path):
            if VERBOSE_LOGGING:
                print(
                    f"    - 正在尝试将 {os.path.basename(file_path)} 转换为 .docx...")

            # 使用 subprocess 调用 libreoffice
            result = subprocess.run(
                ['libreoffice', '--headless', '--convert-to', 'docx',
                 '--outdir', os.path.dirname(file_path), file_path],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=30
            )

        # 读取转换后的 DOCX 文件
        if os.path.exists(docx_path):
            if VERBOSE_LOGGING:
                print(f"    - 已从转换后的 {os.path.basename(docx_path)} 中读取内容。")
            content = extract_text_from_docx(docx_path)
            # 可选：清理转换生成的文件
            # os.remove(docx_path)
            return content
        else:
            return "[DOC 文件转换失败]"

    except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
        if VERBOSE_LOGGING:
            print(f"    - DOC 文件转换失败: {e}")
        return "[DOC 文件处理失败，请确保已安装 LibreOffice]"
    except Exception as e:
        if VERBOSE_LOGGING:
            print(f"    - DOC 文件处理失败: {e}")
        return f"[DOC 文件处理失败: {e}]"


def extract_text_from_plain_text(file_path: str) -> str:
    """
    从纯文本文件中提取内容

    Args:
        file_path: 文本文件路径

    Returns:
        文件内容
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        if VERBOSE_LOGGING:
            print(f"    - 文本文件读取失败: {e}")
        return f"[文本文件读取失败: {e}]"
