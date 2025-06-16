import { useState, useEffect } from "react";

export default function TokenInput({ token, setToken }) {
  const [inputToken, setInputToken] = useState("");

  useEffect(() => {
    const saved = localStorage.getItem("auth_token");
    if (saved) {
      setToken(saved);
      setInputToken(saved);
    }
  }, [setToken]);

  const handleSave = () => {
    localStorage.setItem("auth_token", inputToken);
    setToken(inputToken);
  };

  return (
    <div>
      <label className="block mb-1 text-sm font-medium text-gray-700">Bearer Token</label>
      <input
        type="text"
        value={inputToken}
        onChange={(e) => setInputToken(e.target.value)}
        placeholder="Enter your token"
        className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
      />
      <button
        onClick={handleSave}
        className="mt-2 px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
      >
        Save Token
      </button>
    </div>
  );
}
