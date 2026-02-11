import { useState, useRef, useEffect } from 'react';
import ChatBox from './components/ChatBox';
import { sendMessage } from './api';
import './App.css';

function App() {
    const [messages, setMessages] = useState([
        {
            text: "Hello! I'm MUJbot. Ask me about Manipal University Jaipur courses, admissions, or contact info!",
            sender: "bot"
        }
    ]);
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage = { text: input, sender: "user" };
        setMessages((prev) => [...prev, userMessage]);
        setInput("");
        setIsLoading(true);

        try {
            const botResponseText = await sendMessage(input);
            const botMessage = { text: botResponseText, sender: "bot" };
            setMessages((prev) => [...prev, botMessage]);
        } catch (error) {
            const errorMessage = { text: "Error connecting to server.", sender: "bot" };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSend();
        }
    };

    return (
        <div className="app-container">
            <header className="chat-header">
                <h1>MUJbot</h1>
                <p>Your Application Consultant & Guide</p>
            </header>

            <div className="chat-window">
                <ChatBox messages={messages} />
                {isLoading && <div className="loading-indicator">Typing...</div>}
                <div ref={messagesEndRef} />
            </div>

            <div className="input-area">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyPress}
                    placeholder="Ask about courses, contacts, or campus life..."
                    disabled={isLoading}
                />
                <button onClick={handleSend} disabled={isLoading || !input.trim()}>
                    Send
                </button>
            </div>
        </div>
    );
}

export default App;
