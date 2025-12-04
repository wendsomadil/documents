// src/services/api.js
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Intercepteur pour ajouter le token JWT
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Services API
export const chatAPI = {
    sendMessage: async (message, sessionId = null) => {
        const response = await apiClient.post('/chat/send', {
            message,
            session_id: sessionId,
        });
        return response.data;
    },
    
    getHistory: async (sessionId) => {
        const response = await apiClient.get(`/chat/history/${sessionId}`);
        return response.data;
    },
};

export const audioAPI = {
    uploadAudio: async (audioBlob) => {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.wav');
        
        const response = await apiClient.post('/audio/transcribe', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
        return response.data;
    },
};

export default apiClient;
