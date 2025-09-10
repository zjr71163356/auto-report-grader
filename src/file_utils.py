"""
文件处理工具模块
负责压缩文件的解压、文件类型检测等功能
"""
from config import ZIP_EXTENSIONS, RAR_EXTENSIONS, VERBOSE_LOGGING
import os
import zipfile
import glob
from pathlib import Path
from typing import List, Optional

# 全局导入 rarfile 会导致 Pylance 警告，因为在 except 块中它可能为 None。
# 我们将在使用它的函数内部进行导入。
RARFILE_AVAILABLE = None


def find_archive_files(folder_path: str, archive_extensions: List[str]) -> List[str]:
    """
    在文件夹中递归查找指定类型的压缩文件

    Args:
        folder_path: 要搜索的文件夹路径
        archive_extensions: 压缩文件扩展名列表，如 ['*.zip', '*.rar']

    Returns:
        找到的压缩文件路径列表
    """
    archive_files = []
    for ext in archive_extensions:
        pattern = os.path.join(folder_path, '**', ext)
        archive_files.extend(glob.glob(pattern, recursive=True))
    return archive_files


def extract_zip_file(zip_path: str, extract_to: Optional[str] = None) -> bool:
    """
    解压 ZIP 文件

    Args:
        zip_path: ZIP 文件路径
        extract_to: 解压目标目录，如果为 None 则解压到文件所在目录

    Returns:
        解压是否成功
    """
    try:
        if extract_to is None:
            extract_to = os.path.dirname(zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(extract_to)

        if VERBOSE_LOGGING:
            print(f"    - 已解压 ZIP: {os.path.basename(zip_path)}")

        # 解压成功后删除原压缩文件
        os.remove(zip_path)
        if VERBOSE_LOGGING:
            print(f"    - 已删除原文件: {os.path.basename(zip_path)}")

        return True

    except zipfile.BadZipFile:
        if VERBOSE_LOGGING:
            print(f"    - 警告: {os.path.basename(zip_path)} 不是有效的 ZIP 文件")
        return False
    except Exception as e:
        if VERBOSE_LOGGING:
            print(f"    - 警告: 解压 {os.path.basename(zip_path)} 失败: {e}")
        return False


def extract_rar_file(rar_path: str, extract_to: Optional[str] = None) -> bool:
    """
    解压 RAR 文件

    Args:
        rar_path: RAR 文件路径
        extract_to: 解压目标目录，如果为 None 则解压到文件所在目录

    Returns:
        解压是否成功
    """
    global RARFILE_AVAILABLE
    if RARFILE_AVAILABLE is None:
        try:
            import rarfile
            RARFILE_AVAILABLE = True
        except ImportError:
            RARFILE_AVAILABLE = False

    if not RARFILE_AVAILABLE:
        if VERBOSE_LOGGING:
            print(f"    - 警告: rarfile 包未安装，无法解压 {os.path.basename(rar_path)}")
        return False

    # 在这里，我们已经确认 rarfile 是被导入的
    import rarfile

    try:
        if extract_to is None:
            extract_to = os.path.dirname(rar_path)

        with rarfile.RarFile(rar_path) as rf:
            rf.extractall(extract_to)

        if VERBOSE_LOGGING:
            print(f"    - 已解压 RAR: {os.path.basename(rar_path)}")

        # 解压成功后删除原压缩文件
        os.remove(rar_path)
        if VERBOSE_LOGGING:
            print(f"    - 已删除原文件: {os.path.basename(rar_path)}")

        return True

    except rarfile.RarCannotExec:
        if VERBOSE_LOGGING:
            print(
                f"    - 警告: 无法解压 {os.path.basename(rar_path)}，请确保系统已安装 unrar 工具")
        return False
    except Exception as e:
        if VERBOSE_LOGGING:
            print(f"    - 警告: 解压 {os.path.basename(rar_path)} 失败: {e}")
        return False


def extract_archives_in_folder(folder_path: str) -> None:
    """
    在文件夹中查找并解压所有压缩文件

    Args:
        folder_path: 要处理的文件夹路径
    """
    # 查找 ZIP 文件
    zip_files = find_archive_files(folder_path, ZIP_EXTENSIONS)
    if zip_files:
        if VERBOSE_LOGGING:
            print(f"  - 找到 {len(zip_files)} 个 ZIP 文件，正在解压...")
        for zip_file in zip_files:
            extract_zip_file(zip_file)

    # 查找 RAR 文件
    rar_files = find_archive_files(folder_path, RAR_EXTENSIONS)
    if rar_files:
        if VERBOSE_LOGGING:
            print(f"  - 找到 {len(rar_files)} 个 RAR 文件，正在解压...")
        for rar_file in rar_files:
            extract_rar_file(rar_file)


def is_archive_file(file_path: str) -> bool:
    """
    检查文件是否为压缩文件（基于扩展名）

    Args:
        file_path: 文件路径

    Returns:
        是否为压缩文件
    """
    file_ext = Path(file_path).suffix.lower()
    return (file_ext in ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'] or
            file_ext in ['.tar.gz', '.tar.bz2', '.tar.xz', '.tgz', '.tbz2', '.txz'])
