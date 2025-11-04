import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authService = {
  getLoginUrl: () => `${API_URL}/auth/google/login`,
  
  setToken: (token) => {
    localStorage.setItem('token', token);
  },
  
  getToken: () => {
    return localStorage.getItem('token');
  },
  
  logout: () => {
    localStorage.removeItem('token');
  },
  
  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  },
};

export const recordingService = {
  createRecording: async () => {
    const response = await api.post('/recordings');
    return response.data;
  },
  
  listRecordings: async () => {
    const response = await api.get('/recordings');
    return response.data;
  },
  
  getRecording: async (recordingId) => {
    const response = await api.get(`/recordings/${recordingId}`);
    return response.data;
  },
  
  uploadChunk: async (recordingId, chunkIndex, audioBlob) => {
    const formData = new FormData();
    formData.append('chunk_index', chunkIndex);
    formData.append('audio_chunk', audioBlob, `chunk_${chunkIndex}.webm`);
    
    const response = await api.post(`/recordings/${recordingId}/chunks`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
  
  pauseRecording: async (recordingId) => {
    const response = await api.patch(`/recordings/${recordingId}/pause`);
    return response.data;
  },
  
  finishRecording: async (recordingId) => {
    const response = await api.post(`/recordings/${recordingId}/finish`);
    return response.data;
  },
  
  updateNotes: async (recordingId, notes) => {
    const response = await api.patch(`/recordings/${recordingId}/notes`, { notes });
    return response.data;
  },
};

export default api;
