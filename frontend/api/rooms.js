import { api } from "./client";

export const getRooms = async (params = {}) => {
    const { data } = await api.get("/rooms/", { params });
    return data;
}

export const getRoom = async (id) => {
    const { data } = await api.get(`rooms/${id}/`);
    return data;
}