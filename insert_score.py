import pandas as pd
import numpy as np
import os


def insert_scores_to_gradebook(collected_dir, gradebook_file=None, scores_file=None):
    """
    将LLM评分结果导入到成绩统计表中

    Args:
        collected_dir: 学生作业收集目录
        gradebook_file: 成绩统计表文件路径（可选）
        scores_file: LLM评分结果文件路径（可选）
    """

    # --- 文件路径定义 ---
    if scores_file is None:
        scores_file = os.path.join(collected_dir, 'LLM_评分结果.xlsx')

    if gradebook_file is None:
        # 查找成绩统计表
        possible_gradebook_names = [
            '成绩统计表.xlsx',
            '成绩统计表-软件测试综合实验.xlsx',
            '成绩统计表-单元测试实验报告.xlsx',
            '成绩表.xlsx'
        ]
        gradebook_file = None
        for name in possible_gradebook_names:
            test_path = os.path.join(
                collected_dir, '..', '..', 'list', name)  # 向上查找
            if os.path.exists(test_path):
                gradebook_file = test_path
                break
            test_path = os.path.join(collected_dir, '..', name)
            if os.path.exists(test_path):
                gradebook_file = test_path
                break

        if gradebook_file is None:
            print("错误：未找到成绩统计表文件，请指定文件路径。")
            return False

    # --- 列名定义 ---
    # 成绩表中的姓名列和目标分数写入列
    grades_name_col = '姓名'
    grades_target_col = '软件测试综合实验'  # 更新列名

    # 评分结果表中的姓名列和分数来源列
    scores_name_col = '姓名'
    scores_score_col = '分数'

    try:
        # --- 检查文件是否存在 ---
        if not os.path.exists(scores_file):
            print(f"错误：评分结果文件不存在：{scores_file}")
            return False

        if not os.path.exists(gradebook_file):
            print(f"错误：成绩统计表文件不存在：{gradebook_file}")
            return False

        print(f"正在读取评分结果：{scores_file}")
        print(f"正在读取成绩统计表：{gradebook_file}")

        # --- 读取Excel文件 ---
        df_scores = pd.read_excel(scores_file)
        df_grades = pd.read_excel(gradebook_file)

        print(f"评分结果表包含 {len(df_scores)} 条记录")
        print(f"成绩统计表包含 {len(df_grades)} 条记录")

        # --- 检查列是否存在 ---
        if grades_name_col not in df_grades.columns:
            print(f"错误：成绩统计表中没有找到 '{grades_name_col}' 列")
            print(f"可用的列：{list(df_grades.columns)}")
            return False

        if scores_name_col not in df_scores.columns:
            print(f"错误：评分结果表中没有找到 '{scores_name_col}' 列")
            print(f"可用的列：{list(df_scores.columns)}")
            return False

        # --- 检查目标列是否存在，如果不存在则创建 ---
        if grades_target_col not in df_grades.columns:
            print(f"目标列 '{grades_target_col}' 不存在，正在创建...")
            df_grades[grades_target_col] = np.nan

        # --- 遍历成绩表，更新分数 ---
        updated_count = 0
        not_found_count = 0

        for index, row in df_grades.iterrows():
            # 获取当前行的学生姓名
            student_name = row[grades_name_col]

            # 检查姓名是否有效（非空）
            if pd.isna(student_name) or not str(student_name).strip():
                continue

            # 在评分结果表中查找该学生的分数
            match = df_scores[df_scores[scores_name_col] == student_name]

            # 如果找到了匹配项
            if not match.empty:
                # 获取分数
                score = match.iloc[0][scores_score_col]

                # 将分数写入成绩表
                df_grades.loc[index, grades_target_col] = score
                print(f"✓ 找到 {student_name} 的分数为 {score}，已更新。")
                updated_count += 1
            else:
                print(f"⚠ 警告：未找到学生 {student_name} 的分数记录。")
                not_found_count += 1

        # --- 保存更新后的数据 ---
        output_file = gradebook_file.replace('.xlsx', '_已更新.xlsx')
        df_grades.to_excel(output_file, index=False)

        print(f"\n处理完成！")
        print(f"- 成功更新了 {updated_count} 名学生的成绩")
        print(f"- {not_found_count} 名学生未找到评分记录")
        print(f"- 结果已保存到：{output_file}")

        return True

    except FileNotFoundError as e:
        print(f"错误：文件未找到 - {e}")
        return False
    except Exception as e:
        print(f"处理过程中发生错误：{e}")
        return False


if __name__ == '__main__':
    # 配置路径
    collected_dir = '/home/tyrfly1001/LabTask/task1/collected'

    # 运行成绩导入
    success = insert_scores_to_gradebook(collected_dir)

    if success:
        print("\n成绩导入完成！")
    else:
        print("\n成绩导入失败，请检查错误信息。")
