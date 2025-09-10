"""
LLM 客户端模块
负责与 LLM API 的交互，包括评分和错误处理
"""
from config import (
    OPENAI_API_KEY, OPENAI_BASE_URL, LLM_MODEL,
    SCORING_TEMPERATURE, MIN_SCORE, MAX_SCORE, DEFAULT_SCORE,
    VERBOSE_LOGGING
)
import json
from typing import Tuple, Optional

# 将可选依赖的导入移至函数内部
OPENAI_AVAILABLE = None


class LLMClient:
    """LLM 客户端类"""

    def __init__(self):
        global OPENAI_AVAILABLE
        if OPENAI_AVAILABLE is None:
            try:
                from openai import OpenAI
                OPENAI_AVAILABLE = True
            except ImportError:
                OPENAI_AVAILABLE = False

        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI 包未安装，无法使用 LLM 功能")

        if not OPENAI_API_KEY:
            raise ValueError("未找到 OpenAI API 密钥，请设置环境变量 'OPENAI_API_KEY'")

        from openai import OpenAI
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL
        )

    def score_content(self, student_content: str, rubric: str) -> Tuple[float, str]:
        """
        使用 LLM 对学生内容进行评分

        Args:
            student_content: 学生提交的内容
            rubric: 评分标准

        Returns:
            (分数, 评语) 元组
        """
        system_prompt = """
        你是一名经验丰富的大学计算机课程助教，你的任务是根据提供的评分标准，对学生的软件测试综合实验报告进行细致、公正的评分。

        重要评分原则：
        1. 严格按照评分标准的10分制进行评分
        2. 特别注意识别疑似大模型直接生成的报告（markdown风格明显、图表过于规整等），如未提供prompt过程则不能评为9-10分
        3. 重视报告的个性化、分析思考深度和实验覆盖度
        4. 考虑比例控制：10分(10-15%)、9分(15-25%)、6分及以下(10-20%)，平均分应在8分左右

        你的输出必须是一个JSON对象，包含两个键：
        1. 'score' (一个浮点数): 最终得分(0-10分)
        2. 'comment' (一个字符串): 详细的评分评语，说明得分理由和改进建议
        """

        user_prompt = f"""
        请根据以下【评分标准】对这位学生的【软件测试综合实验报告】进行评分。

        【评分标准】
        {rubric}

        【学生提交内容】
        {student_content}

        请仔细分析报告的以下方面：
        1. 报告格式的清晰性和规范性
        2. 实验要求的覆盖程度
        3. 个性化内容的体现
        4. 分析与思考的深度
        5. 是否疑似大模型直接生成（注意格式风格和是否提供prompt过程）

        根据10分制评分标准，以JSON格式返回评分结果，包含 'score' 和 'comment' 两个键。
        """

        try:
            if VERBOSE_LOGGING:
                print("  - 正在调用 LLM 进行分析...")

            response = self.client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=SCORING_TEMPERATURE,
            )

            response_content = response.choices[0].message.content
            if response_content is None:
                raise ValueError("LLM 返回了空内容")

            result_json = json.loads(response_content)
            score = float(result_json.get('score', DEFAULT_SCORE))
            comment = result_json.get('comment', "LLM未提供评语，请手动检查。")

            # 确保分数在合理范围内
            score = max(MIN_SCORE, min(MAX_SCORE, score))

            if VERBOSE_LOGGING:
                print("  - LLM分析完成。")

            return score, comment

        except Exception as e:
            error_msg = f"LLM分析失败，请手动评分。错误信息: {e}"
            if VERBOSE_LOGGING:
                print(f"  - LLM API 调用失败: {e}")
            return DEFAULT_SCORE, error_msg


# 全局 LLM 客户端实例
_llm_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """
    获取 LLM 客户端实例（单例模式）

    Returns:
        LLM 客户端实例

    Raises:
        ImportError: 如果 OpenAI 包未安装
        ValueError: 如果 API 密钥未设置
    """
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client


def analyze_with_llm(student_content: str, rubric: str) -> Tuple[float, str]:
    """
    分析学生内容并返回评分结果（兼容性函数）

    Args:
        student_content: 学生提交的内容
        rubric: 评分标准

    Returns:
        (分数, 评语) 元组
    """
    try:
        client = get_llm_client()
        return client.score_content(student_content, rubric)
    except (ImportError, ValueError) as e:
        if VERBOSE_LOGGING:
            print(f"  - LLM 客户端初始化失败: {e}")
        return DEFAULT_SCORE, f"LLM功能不可用: {e}"
