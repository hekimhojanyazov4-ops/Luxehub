import { publicApi, api } from "./client";


export async function register({ email, password, first_name, last_name, ...rest }) {
    const { data } = await publicApi.post("/auth/register/", {
        email, password, first_name, last_name, ...rest
    });
    return data;
}

export const login = async ({ email, password }) => {
    const { data } = await publicApi.post("/auth/token/", { email, password });
    localStorage.setItem("access", data.access);
    localStorage.setItem("refresh", data.refresh);
    return data;
}

export function logout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
}


export async function me() {
    const { data } = await api.get("/auth/me");
    return data
}

