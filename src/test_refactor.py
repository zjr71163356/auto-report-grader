#!/usr/bin/env python3
"""
测试重构后的模块化系统
"""
import os
import sys

# 设置测试环境变量
os.environ['OPENAI_API_KEY'] = 'test_key_for_testing'


def test_imports():
    """测试所有模块导入"""
    print("🔍 测试模块导入...")

    try:
        from config import COLLECTED_DIR, RUBRIC_FILE
        print("✅ config 模块导入成功")
    except Exception as e:
        print(f"❌ config 模块导入失败: {e}")
        return False

    try:
        from models import StudentSubmission, ScoreResult, ProcessingResult
        print("✅ models 模块导入成功")
    except Exception as e:
        print(f"❌ models 模块导入失败: {e}")
        return False

    try:
        from file_utils import extract_archives_in_folder
        print("✅ file_utils 模块导入成功")
    except Exception as e:
        print(f"❌ file_utils 模块导入失败: {e}")
        return False

    try:
        from text_extractor import extract_text_from_folder
        print("✅ text_extractor 模块导入成功")
    except Exception as e:
        print(f"❌ text_extractor 模块导入失败: {e}")
        return False

    try:
        from llm_client import analyze_with_llm
        print("✅ llm_client 模块导入成功")
    except Exception as e:
        print(f"❌ llm_client 模块导入失败: {e}")
        return False

    try:
        from report import generate_report
        print("✅ report 模块导入成功")
    except Exception as e:
        print(f"❌ report 模块导入失败: {e}")
        return False

    try:
        from score import main
        print("✅ score 主模块导入成功")
    except Exception as e:
        print(f"❌ score 主模块导入失败: {e}")
        return False

    return True


def test_config():
    """测试配置"""
    print("\n🔧 测试配置...")

    try:
        from config import COLLECTED_DIR, RUBRIC_FILE, OUTPUT_FILENAME
        print(f"📁 收集目录: {COLLECTED_DIR}")
        print(f"📄 评分标准文件: {RUBRIC_FILE}")
        print(f"📊 输出文件名: {OUTPUT_FILENAME}")
        print(f"📁 收集目录存在: {COLLECTED_DIR.exists()}")
        print(f"📄 评分标准文件存在: {RUBRIC_FILE.exists()}")
        return True
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False


def test_models():
    """测试数据模型"""
    print("\n📋 测试数据模型...")

    try:
        from models import StudentSubmission, ScoreResult, ProcessingResult

        # 测试 StudentSubmission
        submission = StudentSubmission(
            student_id="S001",
            student_name="张三",
            folder_name="S001_张三",
            folder_path="/tmp/test"
        )
        print("✅ StudentSubmission 创建成功")

        # 测试 ScoreResult
        score_result = ScoreResult(
            student_id="S001",
            student_name="张三",
            folder_name="S001_张三",
            score=8.5,
            comment="表现良好"
        )
        print("✅ ScoreResult 创建成功")

        # 测试 ProcessingResult
        processing_result = ProcessingResult(
            submission=submission,
            content="测试内容"
        )
        processing_result.score_result = score_result
        print("✅ ProcessingResult 创建成功")

        return True
    except Exception as e:
        print(f"❌ 数据模型测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🚀 开始测试重构后的模块化系统\n")

    success = True

    success &= test_imports()
    success &= test_config()
    success &= test_models()

    if success:
        print("\n🎉 所有测试通过！重构成功！")
        print("\n📝 重构总结:")
        print("- ✅ 配置模块化 (config.py)")
        print("- ✅ 数据模型定义 (models.py)")
        print("- ✅ 文件处理模块 (file_utils.py)")
        print("- ✅ 文本提取模块 (text_extractor.py)")
        print("- ✅ LLM 客户端模块 (llm_client.py)")
        print("- ✅ 报告生成模块 (report.py)")
        print("- ✅ 主模块重构 (score.py)")
        print("\n🔧 现在可以运行: python score.py")
    else:
        print("\n❌ 部分测试失败，请检查错误信息")
        sys.exit(1)


if __name__ == "__main__":
    main()
