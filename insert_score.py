import pandas as pd
import numpy as np

# --- 文件路径定义 ---
# 成绩统计表，需要读取姓名并写入分数
grades_file = '成绩统计表-单元测试实验报告.xlsx'
# LLM评分结果表，需要从中查找姓名并读取分数
scores_file = 'LLM_评分结果2.xlsx'

# --- 列名定义 ---
# 成绩表中的姓名列和目标分数写入列
grades_name_col = '姓名'
grades_target_col = '测试管理实验报告'

# 评分结果表中的学生/文件名列和分数来源列
scores_name_col = '学生/文件名'
scores_score_col = '分数'

try:
    # --- 读取Excel文件 ---
    # 使用 xlrd 引擎读取 .xls 文件
    df_grades = pd.read_excel(grades_file)
    # 读取 .xlsx 文件
    df_scores = pd.read_excel(scores_file)

    # --- 遍历成绩表，更新分数 ---
    # 遍历成绩表中的每一行
    for index, row in df_grades.iterrows():
        # 获取当前行的学生姓名
        student_name = row[grades_name_col]

        # 检查姓名是否有效（非空）
        if pd.isna(student_name) or not str(student_name).strip():
            continue

        # 在评分结果表的 "学生/文件名" 列中查找包含该姓名的行
        # na=False确保在搜索时忽略空值，避免错误
        # .astype(str) 确保该列为字符串类型以便进行子字符串查询
        match = df_scores[df_scores[scores_name_col].astype(str).str.contains(student_name, na=False)]

        # 如果找到了至少一个匹配项
        if not match.empty:
            # 获取找到的第一个匹配行的分数
            score = match.iloc[0][scores_score_col]
            
            # 将分数写入成绩表中对应学生行的 "单元测试实验报告" 列
            # 使用 .loc 来确保准确写入到指定行和列
            df_grades.loc[index, grades_target_col] = score
            print(f"找到 {student_name} 的分数为 {score}，已更新。")
        else:
            print(f"警告：在 {scores_file} 中未找到学生 {student_name} 的分数记录。")

    # --- 保存更新后的数据 ---
    # 将更新后的DataFrame写回到原始的.xls文件中
    # index=False 表示在写入Excel时不要包含DataFrame的索引列
    df_grades.to_excel(grades_file, index=False)

    print("\n处理完成，分数已成功写入到 '成绩统计表-单元测试实验报告.xls'。")

except FileNotFoundError as e:
    print(f"错误：文件未找到 - {e}")
except Exception as e:
    print(f"处理过程中发生错误：{e}")
