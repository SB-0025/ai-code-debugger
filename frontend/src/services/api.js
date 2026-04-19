import axios from 'axios';

const API_BASE_URL = '/api';

export const debugCode = async (code, language = 'python') => {
  try {
    const response = await axios.post(`${API_BASE_URL}/debug`, {
      code,
      language
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to debug code');
    } else if (error.request) {
      throw new Error('No response from server. Make sure backend is running on port 8000');
    } else {
      throw new Error('Failed to send request');
    }
  }
};