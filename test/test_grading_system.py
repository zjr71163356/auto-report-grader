#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学生作业自动评分系统测试脚本
用于测试和演示整个评分流程
"""

import os
import sys
import subprocess
from pathlib import Path


def check_environment():
    """检查环境配置"""
    print("=== 环境检查 ===")

    # 检查OpenAI API密钥
    if "OPENAI_API_KEY" not in os.environ:
        print("❌ 错误：未设置 OPENAI_API_KEY 环境变量")
        print("请运行：export OPENAI_API_KEY='your_api_key_here'")
        return False
    else:
        print("✅ OPENAI_API_KEY 已设置")

    # 检查必要文件
    required_files = [
        '/home/tyrfly1001/LabTask/task1/collected',
        '/home/tyrfly1001/LabTask/task1/criteria/criteria.md'
    ]

    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} 存在")
        else:
            print(f"❌ {file_path} 不存在")
            return False

    return True


def install_dependencies():
    """安装Python依赖"""
    print("\n=== 安装依赖 ===")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                       check=True, cwd='/home/tyrfly1001/LabTask/auto-report-grader')
        print("✅ 依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败：{e}")
        return False


def run_grading():
    """运行评分脚本"""
    print("\n=== 开始评分 ===")
    try:
        subprocess.run([sys.executable, 'score.py'],
                       check=True, cwd='/home/tyrfly1001/LabTask/auto-report-grader')
        print("✅ 评分完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 评分失败：{e}")
        return False


def run_score_insertion():
    """运行成绩导入脚本"""
    print("\n=== 导入成绩 ===")
    try:
        subprocess.run([sys.executable, 'insert_score.py'],
                       check=True, cwd='/home/tyrfly1001/LabTask/auto-report-grader')
        print("✅ 成绩导入完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 成绩导入失败：{e}")
        return False


def show_results():
    """显示结果"""
    print("\n=== 结果查看 ===")
    results_dir = '/home/tyrfly1001/LabTask/task1/collected'

    result_files = [
        'LLM_评分结果.xlsx',
        '../../list/成绩统计表_已更新.xlsx'  # 调整路径
    ]

    for filename in result_files:
        filepath = os.path.join(results_dir, filename)
        if os.path.exists(filepath):
            print(f"✅ 结果文件：{filepath}")
        else:
            print(f"❌ 未找到：{filepath}")


def main():
    """主函数"""
    print("学生作业自动评分系统")
    print("=" * 50)

    # 1. 环境检查
    if not check_environment():
        print("\n请解决环境问题后重新运行")
        return 1

    # 2. 安装依赖
    if not install_dependencies():
        print("\n依赖安装失败，请手动安装")
        return 1

    # 3. 运行评分
    if not run_grading():
        print("\n评分失败，请检查错误信息")
        return 1

    # 4. 导入成绩（可选）
    print("\n是否要将评分结果导入到成绩统计表？(y/n): ", end="")
    if input().lower().strip() == 'y':
        run_score_insertion()

    # 5. 显示结果
    show_results()

    print("\n=== 完成 ===")
    print("评分系统运行完成！")
    return 0


if __name__ == '__main__':
    sys.exit(main())
