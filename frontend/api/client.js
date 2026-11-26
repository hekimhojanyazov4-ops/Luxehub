import axios from "axios";

const BASE_URL = '127.0.0.1:8000/api';


export const getAllRooms = async () => {
    const response = await axios.get(BASE_URL + '/products/');
    console.log(response.data);
    return response.data;
}