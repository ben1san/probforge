# backend/app/services/ai.py
import os
from openai import OpenAI
from ..models.schemas import ProblemCreate
import json

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_variant(original_text: str, original_latex: str, subject: str = "math") -> dict:
    prompt = f"""
    あなたは数学・物理の教材作成のプロフェッショナルです。
    以下の問題の「構造」や「解法」を維持したまま、数値や設定を変えた「類題」を1つ作成してください。
    
    # 元の問題
    分野: {subject}
    問題文: {original_text}
    数式: {original_latex}

    # 制約
    - 出力は必ずJSON形式のみにしてください。
    - JSONのキーは "content_text", "content_latex", "solution_text", "solution_latex" です。
    - 数式はLaTeX形式で記述してください。
    - 解説(solution)も詳しく作成してください。
    """

    response = client.chat.completions.create(
        model="gpt-4o", # または gpt-3.5-turbo
        messages=[{"role": "system", "content": "JSON形式で出力してください。"},
                  {"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)