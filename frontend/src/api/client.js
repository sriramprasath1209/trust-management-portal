import axios from 'axios'

const devApiBaseUrl = 'http://127.0.0.1:8000/api'

export const API_BASE_URL =
  import.meta.env.VITE_API_URL || (import.meta.env.DEV ? devApiBaseUrl : '/api')

export const api = axios.create({
  baseURL: API_BASE_URL
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
