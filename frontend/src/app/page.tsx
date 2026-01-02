"use client";

import { useState } from "react";
import 'katex/dist/katex.min.css';
import katex from 'katex';

// --- 文章と数式($...$)が混ざったテキストを表示するコンポーネント ---
const MixedLatex = ({ text }: { text: string }) => {
  if (!text) return null;

  // $で囲まれた部分を分割して処理する簡易パーサー
  // 例: "解は $x=1$ です" -> ["解は ", "x=1", " です"]
  const parts = text.split(/\$(.*?)\$/g);

  return (
    <span>
      {parts.map((part, index) => {
        // 偶数番目は普通のテキスト、奇数番目は数式($の中身)
        if (index % 2 === 0) {
          return <span key={index}>{part}</span>;
        } else {
          try {
            const html = katex.renderToString(part, { throwOnError: false });
            return <span key={index} dangerouslySetInnerHTML={{ __html: html }} className="mx-1 text-indigo-700" />;
          } catch {
            return <span key={index} className="text-red-500">${part}$</span>;
          }
        }
      })}
    </span>
  );
};
// ---------------------------------------------------------------

export default function Home() {
  // 入力データ
  const [inputData, setInputData] = useState({
    content: "", // ここに文章と数式をまとめて入れる
    subject: "math",
    difficulty: 1,
  });

  // AI生成された問題データ
  const [generatedProblem, setGeneratedProblem] = useState<any>(null);

  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");

  const handleGenerate = async () => {
    if (!inputData.content) return;
    setLoading(true);
    setStatus("問題を保存中...");
    setGeneratedProblem(null);

    try {
      // 1. オリジナル問題を保存
      // APIの仕様上 content_text と content_latex が必要なので、同じものを送る
      const saveRes = await fetch("http://127.0.0.1:8000/problems/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          content_text: inputData.content,
          content_latex: inputData.content, // 暫定的に同じものを入れる
          subject: inputData.subject,
          difficulty: inputData.difficulty
        }),
      });

      if (!saveRes.ok) throw new Error("保存に失敗しました");
      const savedProblem = await saveRes.json();

      // 2. AI生成APIを叩く
      setStatus("AIが類題を生成中...");
      const genRes = await fetch(`http://127.0.0.1:8000/problems/${savedProblem.id}/generate`, {
        method: "POST",
      });

      if (!genRes.ok) throw new Error("AI生成に失敗しました");
      const genData = await genRes.json();

      setGeneratedProblem(genData);
      setStatus("完了");

    } catch (err) {
      console.error(err);
      setStatus("エラーが発生しました");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 text-gray-800 p-6">
      <div className="max-w-7xl mx-auto h-full flex flex-col">
        <header className="mb-6 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-indigo-800">ProbForge</h1>
          <span className="text-sm text-gray-500">AI Powered Problem Generator</span>
        </header>

        <div className="flex flex-col md:flex-row gap-6 flex-grow">

          {/* 左側: 入力エリア */}
          <div className="w-full md:w-1/2 flex flex-col gap-4">
            <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-200 h-full flex flex-col">
              <h2 className="font-semibold text-lg mb-4 flex items-center gap-2">
                📝 元の問題を入力
              </h2>

              <div className="flex gap-4 mb-4">
                <select
                  className="p-2 border rounded-md text-sm"
                  value={inputData.subject}
                  onChange={(e) => setInputData({ ...inputData, subject: e.target.value })}
                >
                  <option value="math">数学</option>
                  <option value="physics">物理</option>
                </select>
                <select
                  className="p-2 border rounded-md text-sm"
                  value={inputData.difficulty}
                  onChange={(e) => setInputData({ ...inputData, difficulty: Number(e.target.value) })}
                >
                  <option value="1">難易度: 1</option>
                  <option value="2">難易度: 2</option>
                  <option value="3">難易度: 3</option>
                  <option value="4">難易度: 4</option>
                  <option value="5">難易度: 5</option>
                </select>
              </div>

              <textarea
                className="w-full flex-grow p-4 border rounded-md bg-gray-50 focus:ring-2 focus:ring-indigo-300 outline-none resize-none font-mono text-base"
                placeholder={`ここに問題文を入力してください。\n数式は $x^2$ のようにドルマークで囲んでください。\n\n例:\n放物線 $y = x^2 - 4x$ の頂点の座標を求めよ。`}
                value={inputData.content}
                onChange={(e) => setInputData({ ...inputData, content: e.target.value })}
              />

              <div className="mt-4">
                <button
                  onClick={handleGenerate}
                  disabled={loading || !inputData.content}
                  className="w-full bg-indigo-600 text-white font-bold py-3 rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 transition-all flex justify-center items-center gap-2"
                >
                  {loading ? (
                    <span>🔄 {status}</span>
                  ) : (
                    <span>類題を生成する</span>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* 右側: 生成結果エリア */}
          <div className="w-full md:w-1/2">
            <div className="bg-white p-6 rounded-xl shadow-lg border border-indigo-100 h-full min-h-[500px] flex flex-col relative overflow-hidden">
              <div className="absolute top-0 left-0 w-2 h-full bg-indigo-500"></div>

              <h2 className="font-semibold text-lg mb-6 text-indigo-900 flex items-center gap-2">
                🤖 生成された類題
              </h2>

              {generatedProblem ? (
                <div className="flex-grow flex flex-col gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">

                  {/* 問題文の表示 */}
                  <div className="prose max-w-none">
                    <div className="text-xl leading-relaxed text-gray-800">
                      {/* 修正: AIが返すJSONキーに合わせて表示 */}
                      <MixedLatex text={generatedProblem.content_text || generatedProblem.content_latex} />
                    </div>
                  </div>

                  <hr className="border-gray-200" />

                  {/* 解説の表示（あれば） */}
                  {(generatedProblem.solution_text || generatedProblem.solution_latex) && (
                    <div className="bg-gray-50 p-4 rounded-lg text-sm text-gray-600">
                      <h3 className="font-bold mb-2">解説 / 解答</h3>
                      <MixedLatex text={generatedProblem.solution_text || generatedProblem.solution_latex} />
                    </div>
                  )}
                </div>
              ) : (
                <div className="flex-grow flex flex-col items-center justify-center text-gray-400">
                  <div className="text-6xl mb-4">💡</div>
                  <p>左側のフォームに入力して<br />ボタンを押すとここに類題が表示されます</p>
                </div>
              )}
            </div>
          </div>

        </div>
      </div>
    </main>
  );
}