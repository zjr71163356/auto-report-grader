#!/bin/bash
# 学生作业自动评分系统启动脚本

echo "学生作业自动评分系统"
echo "===================="

# 检查是否设置了API密钥
if [ -z "$OPENAI_API_KEY" ]; then
    echo "错误：未设置 OPENAI_API_KEY 环境变量"
    echo "请运行：export OPENAI_API_KEY='your_api_key_here'"
    exit 1
fi

# 进入项目目录
cd "$(dirname "$0")"

# 安装依赖
echo "正在安装Python依赖..."
pip install -r requirements.txt

# 运行评分
echo "开始评分..."
python score.py

echo "评分完成！"
echo "结果保存在：/home/tyrfly1001/LabTask/task1/collected/LLM_评分结果.xlsx"

# 询问是否导入成绩
read -p "是否要将评分结果导入到成绩统计表？(y/n): " choice
case "$choice" in 
  y|Y ) 
    echo "开始导入成绩..."
    python insert_score.py
    echo "成绩导入完成！"
    ;;
  * ) 
    echo "跳过成绩导入。"
    ;;
esac

echo "所有任务完成！"
