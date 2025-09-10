"""
自动评分系统主模块
负责协调各个模块完成评分任务
"""
import os
from typing import List

from config import COLLECTED_DIR, RUBRIC_FILE, VERBOSE_LOGGING
from models import StudentSubmission, ScoreResult, ProcessingResult
from file_utils import extract_archives_in_folder
from text_extractor import extract_text_from_folder
from llm_client import analyze_with_llm
from report import generate_report


def process_student_folder(student_folder: StudentSubmission, rubric: str) -> ProcessingResult:
    """
    处理单个学生文件夹

    Args:
        student_folder: 学生提交信息
        rubric: 评分标准

    Returns:
        处理结果
    """
    result = ProcessingResult(submission=student_folder, content="")

    try:
        if VERBOSE_LOGGING:
            print(f"\n正在处理: {student_folder.folder_name}")

        # 1. 解压压缩文件
        extract_archives_in_folder(student_folder.folder_path)

        # 2. 提取文本内容
        content = extract_text_from_folder(student_folder.folder_path)
        result.content = content

        # 3. 使用 LLM 评分
        score, comment = analyze_with_llm(content, rubric)
        score_result = ScoreResult(
            student_id=student_folder.student_id,
            student_name=student_folder.student_name,
            folder_name=student_folder.folder_name,
            score=score,
            comment=comment
        )
        result.score_result = score_result

        if VERBOSE_LOGGING:
            print(f"  - 评分完成: {student_folder.folder_name}, 得分: {score}")

    except Exception as e:
        error_msg = f"处理失败: {e}"
        result.errors.append(error_msg)
        if VERBOSE_LOGGING:
            print(f"  - 处理失败 {student_folder.folder_name}: {e}")

    return result


def collect_student_folders(directory: str) -> List[StudentSubmission]:
    """
    收集目录中的所有学生文件夹

    Args:
        directory: 目录路径

    Returns:
        学生提交列表
    """
    student_folders = []

    try:
        all_items = os.listdir(directory)
        for item in all_items:
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                # 解析学号和姓名
                if '_' in item:
                    parts = item.split('_', 1)
                    student_id = parts[0]
                    student_name = parts[1]
                else:
                    student_id = item
                    student_name = item

                submission = StudentSubmission(
                    student_id=student_id,
                    student_name=student_name,
                    folder_name=item,
                    folder_path=item_path
                )
                student_folders.append(submission)

    except Exception as e:
        if VERBOSE_LOGGING:
            print(f"收集学生文件夹时出错: {e}")

    return student_folders


def main(current_dir=None, rubric_path=None):
    """
    主函数，遍历学生文件夹，处理内部的zip文件，使用LLM分析，并创建Excel报告。
    """
    # 使用配置中的默认路径，如果没有提供参数
    current_dir = current_dir or str(COLLECTED_DIR)
    rubric_path = rubric_path or str(RUBRIC_FILE)

    try:
        # 读取评分标准文件
        with open(rubric_path, 'r', encoding='utf-8') as f:
            rubric = f.read()
    except FileNotFoundError:
        print(f"错误: 评分标准文件 '{rubric_path}' 未找到。")
        return

    # 收集学生文件夹
    student_folders = collect_student_folders(current_dir)

    if not student_folders:
        print(f"在 '{current_dir}' 目录下未找到任何学生作业文件夹。")
        return

    if VERBOSE_LOGGING:
        print(f"找到 {len(student_folders)} 个学生文件夹，开始处理...")

    # 处理所有学生文件夹
    results = []
    for student_folder in student_folders:
        processing_result = process_student_folder(student_folder, rubric)
        if processing_result.score_result:
            results.append(processing_result.score_result)

    # 生成报告
    if results:
        generate_report(results, current_dir)
    else:
        print("没有成功处理的评分结果")


if __name__ == '__main__':
    # 使用配置文件中的路径
    main()
