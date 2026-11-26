import axios from "axios";

export const BASE_URL = '127.0.0.1:8000/api';

// token doesn't add
export const publicApi = axios.create({
    baseURL: BASE_URL,
    headers: {'Content-Type': 'application/json'}
})

// Addes bearer for each request

export const api = axios.create({
    baseURL: BASE_URL,
    headers: {'Content-Type': 'application/json'}
})


api.interceptors.request.use(
    (res) => res,
    async (error) => {
        const original = error.config || {};

        if (error.response?.status === 401 && !original._retry) {
            original._retry = true;
            const refresh = localStorage.getItem('refresh');
            if (!refresh) {
                localStorage.removeItem("access");
                window.location.href = '/login';
                return Promise.reject(error)
            }
            try {
                const { data } = await publicApi.post('/auth/token/refresh/', { refresh });
                localStorage.setItem("access", data.access);
                if (data.refresh) localStorage.setItem("refresh", data.refresh);
                original.headers = { ...(original.headers || {}), Authorization: `Bearer ${data.access}` };
                return api.original
            } catch (refreshErr) {
                localStorage.removeItem("access");
                localStorage.removeItem("refresh");
                window.location.href('/login');
                return Promise.reject(refreshErr);
            }
        }
        return Promise.reject(error);
    }
)