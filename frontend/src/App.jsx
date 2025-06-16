import { useState } from "react";
import TokenInput from "./components/TokenInput";
import ImageUpload from "./components/ImageUpload";
import ResultDisplay from "./components/ResultDisplay";

export default function App() {
  const [token, setToken] = useState("");
  const [result, setResult] = useState(null);

  return (
    <div className="min-h-screen bg-gray-50 px-4 py-10 font-sans">
      <div className="max-w-xl mx-auto bg-white rounded-xl shadow-md p-6 space-y-6">
        <h1 className="text-2xl font-bold text-center text-gray-800">🛡️ Image Moderation</h1>
        <TokenInput token={token} setToken={setToken} />
        <ImageUpload token={token} setResult={setResult} />
        <ResultDisplay result={result} />
      </div>
    </div>
  );
}
