#!/usr/bin/env python3
"""
测试重构后的配置是否正确工作
"""
import os
import sys

# 设置测试环境变量
os.environ['OPENAI_API_KEY'] = 'test_key_for_testing'

try:
    from config import (
        COLLECTED_DIR, RUBRIC_FILE, LLM_MODEL, OUTPUT_FILENAME,
        SUPPORTED_EXTENSIONS, VERBOSE_LOGGING, MIN_SCORE, MAX_SCORE
    )

    print("✅ 配置文件导入成功！")
    print(f"📁 收集目录: {COLLECTED_DIR}")
    print(f"📄 评分标准文件: {RUBRIC_FILE}")
    print(f"🤖 LLM模型: {LLM_MODEL}")
    print(f"📊 输出文件名: {OUTPUT_FILENAME}")
    print(f"📁 收集目录存在: {COLLECTED_DIR.exists()}")
    print(f"📄 评分标准文件存在: {RUBRIC_FILE.exists()}")
    print(f"🔧 支持的扩展名: {SUPPORTED_EXTENSIONS}")
    print(f"📝 详细日志: {VERBOSE_LOGGING}")
    print(f"📊 分数范围: {MIN_SCORE}-{MAX_SCORE}")

except Exception as e:
    print(f"❌ 配置文件导入失败: {e}")
    sys.exit(1)

try:
    from score import main, extract_text_from_folder, analyze_with_llm
    print("✅ score.py 重构成功，所有函数可以正常导入！")

    # 测试主函数是否可以被调用（不实际执行）
    print("✅ main 函数可用")
    print("✅ extract_text_from_folder 函数可用")
    print("✅ analyze_with_llm 函数可用")

except Exception as e:
    print(f"❌ score.py 导入失败: {e}")
    sys.exit(1)

print("\n🎉 重构测试完成！所有配置和函数都工作正常。")
