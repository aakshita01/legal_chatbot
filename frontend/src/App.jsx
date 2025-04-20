import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const askBot = async () => {
    if (!query.trim()) return;

    const newMessages = [...messages, { role: "user", text: query }];
    setMessages(newMessages);
    setQuery("");
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/ask", { query });
      const botReply = res.data.answer;
      setMessages([...newMessages, { role: "bot", text: botReply }]);
    } catch (error) {
      console.error("Error from backend:", error);
      setMessages([
        ...newMessages,
        { role: "bot", text: "❌ Error: Could not reach the backend." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (file) => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:8000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      alert("✅ File uploaded and processed: " + res.data.message);
    } catch (error) {
      console.error("Upload error:", error);
      alert("❌ Failed to upload file.");
    }
  };

  return (
    <div className="container">
      <div className="app">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <h2>📜 Legal Chatbot</h2>
          <div className="upload-area">
            <label htmlFor="file-upload" className="upload-label">
              📁 Upload Contract
            </label>
            <input
              id="file-upload"
              type="file"
              accept=".pdf,.txt"
              onChange={(e) => handleFileUpload(e.target.files[0])}
              style={{ display: "none" }}
            />
          </div>

        </div>

        <div className="chat-box">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="bubble">{msg.text}</div>
            </div>
          ))}
          {loading && (
            <div className="message bot">
              <div className="bubble typing">
                <span>.</span>
                <span>.</span>
                <span>.</span>
              </div>
            </div>
          )}
        </div>

        <div className="input-area">
          <textarea
            placeholder="Ask a legal question..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button onClick={askBot} disabled={loading}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
