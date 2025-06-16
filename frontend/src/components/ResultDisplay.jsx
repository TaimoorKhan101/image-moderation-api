export default function ResultDisplay({ result }) {
  if (!result) return null;

  return (
    <div className="border-t pt-4 space-y-2">
      <h2 className="text-lg font-semibold text-gray-800">🧪 Moderation Result</h2>
      <p className="text-sm">
        <strong>Safe:</strong>{" "}
        <span className={result.is_safe ? "text-green-600" : "text-red-600"}>
          {result.is_safe ? "Yes ✅" : "No ❌"}
        </span>
      </p>

      <h3 className="text-sm font-medium text-gray-700">Category Confidence</h3>
      <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
        {Object.entries(result.categories).map(([category, confidence]) => (
          <li key={category}>
            <span className="font-medium">{category.replace(/_/g, " ")}:</span>{" "}
            {(confidence * 100).toFixed(2)}%
          </li>
        ))}
      </ul>
    </div>
  );
}
