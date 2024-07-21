import axios from 'axios'
import { ACCESS_TOKEN } from "./constants"

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  //withCredentials: true // for allowing the cookies from different origin to be stored and visible in the current origin
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(ACCESS_TOKEN)
    if (token) {
      config.headers.Authorization = `${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default api