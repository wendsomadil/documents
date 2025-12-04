// src/components/chat/ChatWindow.jsx
import React, { useState, useEffect, useRef } from 'react';
import { chatAPI } from '../../services/api';
import MessageBubble from './MessageBubble';
import InputBar from './InputBar';

const ChatWindow = ({ sessionId }) => {
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    // Auto-scroll vers le bas
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSendMessage = async (messageText) => {
        // Ajout du message utilisateur
        const userMessage = {
            id: Date.now(),
            role: 'user',
            content: messageText,
            timestamp: new Date(),
        };
        setMessages((prev) => [...prev, userMessage]);

        setIsLoading(true);
        
        try {
            // Appel API
            const response = await chatAPI.sendMessage(messageText, sessionId);
            
            // Ajout de la réponse du bot
            const botMessage = {
                id: response.message_id,
                role: 'assistant',
                content: response.response,
                sources: response.sources,
                timestamp: new Date(),
            };
            setMessages((prev) => [...prev, botMessage]);
        
        } catch (error) {
            console.error('Erreur envoi message:', error);
            
            // Message d'erreur utilisateur
            const errorMessage = {
                id: Date.now(),
                role: 'assistant',
                content: '⚠️ Désolé, une erreur est survenue. Veuillez réessayer.',
                timestamp: new Date(),
            };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-gray-50">
            {/* Zone de messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((msg) => (
                    <MessageBubble key={msg.id} message={msg} />
                ))}
                {isLoading && (
                    <div className="flex items-center space-x-2 text-gray-500">
                        <div className="animate-pulse">🤖 Assistant rédige...</div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Barre de saisie */}
            <InputBar onSendMessage={handleSendMessage} disabled={isLoading} />
        </div>
    );
};

export default ChatWindow;
