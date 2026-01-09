"use client";

import { useState } from "react";
import 'katex/dist/katex.min.css';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

export default function Home() {
  const [inputData, setInputData] = useState({
    content: "",
    subject: "math",
    difficulty: 1,
  });

  const [generatedProblem, setGeneratedProblem] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");

  const handleGenerate = async () => {
    if (!inputData.content) return;
    setLoading(true);
    setStatus("問題を保存中...");
    setGeneratedProblem(null);

    try {
      const saveRes = await fetch("http://127.0.0.1:8000/problems/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(inputData), // inputDataの形がAPIと一致しているのでそのまま送れる
      });

      if (!saveRes.ok) throw new Error("保存に失敗しました");
      const savedProblem = await saveRes.json();

      // 2. 生成
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
        </header>

        <div className="flex flex-col md:flex-row gap-6 flex-grow">

          {/* 左側: 入力エリア */}
          <div className="w-full md:w-1/2 flex flex-col gap-4">
            <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-200 h-full flex flex-col">
              <h2 className="font-semibold text-lg mb-4">📝 元の問題を入力</h2>

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
                placeholder="ここに問題文を入力してください。"
                value={inputData.content}
                onChange={(e) => setInputData({ ...inputData, content: e.target.value })}
              />

              <div className="mt-4">
                <button
                  onClick={handleGenerate}
                  disabled={loading || !inputData.content}
                  className="w-full bg-indigo-600 text-white font-bold py-3 rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 transition-all flex justify-center items-center gap-2"
                >
                  {loading ? <span>🔄 {status}</span> : <span>✨ 類題を生成する</span>}
                </button>
              </div>
            </div>
          </div>

          {/* 右側: 生成結果エリア */}
          <div className="w-full md:w-1/2">
            <div className="bg-white p-6 rounded-xl shadow-lg border border-indigo-100 h-full min-h-[500px] flex flex-col relative overflow-hidden">
              <div className="absolute top-0 left-0 w-2 h-full bg-indigo-500"></div>

              <h2 className="font-semibold text-lg mb-6 text-indigo-900">🤖 生成された類題</h2>

              {generatedProblem ? (
                <div className="flex-grow flex flex-col gap-6 overflow-y-auto">

                  <div className="prose max-w-none text-gray-800">
                    <ReactMarkdown
                      remarkPlugins={[remarkMath]}
                      rehypePlugins={[rehypeKatex]}
                    >
                      {generatedProblem.content_text || generatedProblem.content_latex}
                    </ReactMarkdown>
                  </div>

                  <hr className="border-gray-200" />

                  {/* 解説 */}
                  {(generatedProblem.solution_text || generatedProblem.solution_latex) && (
                    <div className="bg-gray-50 p-4 rounded-lg text-sm text-gray-600">
                      <h3 className="font-bold mb-2">解説 / 解答</h3>
                      <ReactMarkdown
                        remarkPlugins={[remarkMath]}
                        rehypePlugins={[rehypeKatex]}
                      >
                        {generatedProblem.solution_text || generatedProblem.solution_latex}
                      </ReactMarkdown>
                    </div>
                  )}
                </div>
              ) : (
                <div className="flex-grow flex flex-col items-center justify-center text-gray-400">
                  <p>生成結果がここに表示されます</p>
                </div>
              )}
            </div>
          </div>

        </div>
      </div>
    </main>
  );
}