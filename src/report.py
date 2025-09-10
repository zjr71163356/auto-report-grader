"""
报告生成模块
负责生成 Excel 报告和统计信息
"""
from models import ScoreResult
from config import OUTPUT_FILENAME, VERBOSE_LOGGING
import os
from typing import List

# 将可选依赖的导入移至函数内部
PANDAS_AVAILABLE = None


def generate_excel_report(results: List[ScoreResult], output_dir: str) -> str:
    """
    生成 Excel 评分报告

    Args:
        results: 评分结果列表
        output_dir: 输出目录

    Returns:
        生成的报告文件路径

    Raises:
        ImportError: 如果 pandas 未安装
    """
    global PANDAS_AVAILABLE
    if PANDAS_AVAILABLE is None:
        try:
            import pandas as pd
            PANDAS_AVAILABLE = True
        except ImportError:
            PANDAS_AVAILABLE = False

    if not PANDAS_AVAILABLE:
        raise ImportError("pandas 未安装，无法生成 Excel 报告")

    import pandas as pd

    # 转换为字典列表
    data = []
    for result in results:
        data.append({
            '学号': result.student_id,
            '姓名': result.student_name,
            '文件夹名': result.folder_name,
            '分数': result.score,
            '评语': result.comment
        })

    # 创建 DataFrame
    df = pd.DataFrame(data)

    # 生成输出文件路径
    output_filename = os.path.join(output_dir, OUTPUT_FILENAME)

    # 保存到 Excel
    df.to_excel(output_filename, index=False, engine='openpyxl')

    if VERBOSE_LOGGING:
        print(f"\n所有评分完成！结果已保存到 {output_filename}")

    return output_filename


def calculate_statistics(results: List[ScoreResult]) -> dict:
    """
    计算评分统计信息

    Args:
        results: 评分结果列表

    Returns:
        统计信息字典
    """
    if not results:
        return {}

    scores = [r.score for r in results]

    stats = {
        '平均分': round(sum(scores) / len(scores), 2),
        '最高分': max(scores),
        '最低分': min(scores),
        '总人数': len(results)
    }

    return stats


def print_statistics(results: List[ScoreResult]) -> None:
    """
    打印评分统计信息

    Args:
        results: 评分结果列表
    """
    if not results:
        if VERBOSE_LOGGING:
            print("没有评分结果可显示")
        return

    stats = calculate_statistics(results)

    if VERBOSE_LOGGING:
        print("\n评分统计:")
        print(f"平均分: {stats['平均分']:.2f}")
        print(f"最高分: {stats['最高分']:.2f}")
        print(f"最低分: {stats['最低分']:.2f}")
        print(f"总人数: {stats['总人数']}")

        # 分数分布
        scores = [r.score for r in results]

        global PANDAS_AVAILABLE
        if PANDAS_AVAILABLE is None:
            try:
                import pandas as pd
                PANDAS_AVAILABLE = True
            except ImportError:
                PANDAS_AVAILABLE = False

        if PANDAS_AVAILABLE:
            import pandas as pd
            score_distribution = pd.Series(scores).value_counts().sort_index()
            print("\n分数分布:")
            for score, count in score_distribution.items():
                print(f"  {score}分: {count}人")


def generate_report(results: List[ScoreResult], output_dir: str) -> str:
    """
    生成完整报告（Excel + 统计信息）

    Args:
        results: 评分结果列表
        output_dir: 输出目录

    Returns:
        生成的报告文件路径
    """
    # 生成 Excel 报告
    report_path = generate_excel_report(results, output_dir)

    # 打印统计信息
    print_statistics(results)

    return report_path
