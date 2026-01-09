import os
import google.generativeai as genai
import json

# Configure Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_variant(original_content: str, subject: str = "math") -> dict:
    prompt = f"""
    あなたは数学・物理の教材作成のプロフェッショナルです。
    以下の問題の「構造」や「解法」を維持したまま、数値や設定を変えた「類題」を1つ作成してください。
    
    # 元の問題
    分野: {subject}
    内容: {original_content}

    # 制約
    - 出力は必ずJSON形式のみにしてください。
    - キーは "content" (問題文) と "solution" (解説) の2つのみです。
    - 数式はLaTeX形式を使い、文中の数式は $x^2$ のように、独立した数式は $$x^2$$ のようにドル記号で囲んでください。
    - Markdown形式で記述してください。
    """

    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )

    return json.loads(response.text)