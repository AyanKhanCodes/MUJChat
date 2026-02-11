import React from 'react';

const ChatBox = ({ messages }) => {
    return (
        <div className="chat-box">
            {messages.map((msg, index) => (
                <div key={index} className={`message ${msg.sender}`}>
                    <div className="message-content">
                        {msg.text}
                    </div>
                </div>
            ))}
        </div>
    );
};

export default ChatBox;
