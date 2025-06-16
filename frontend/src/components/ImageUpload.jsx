import { useState } from "react";
import axiosInstance from "../services/api";

export default function ImageUpload({ token, setResult }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult(null);
  };

  const handleSubmit = async () => {
    if (!file) return alert("Please select an image.");

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      const response = await axiosInstance.post("/moderate", formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      });
      setResult(response.data);
    } catch (err) {
      alert("Moderation failed: " + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <label className="block mb-1 text-sm font-medium text-gray-700">Upload Image</label>
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
      />
      <button
        onClick={handleSubmit}
        disabled={!file || loading}
        className={`mt-3 w-full py-2 px-4 rounded text-white ${
          loading ? "bg-gray-400 cursor-not-allowed" : "bg-green-600 hover:bg-green-700"
        }`}
      >
        {loading ? "Processing..." : "Moderate Image"}
      </button>
    </div>
  );
}
