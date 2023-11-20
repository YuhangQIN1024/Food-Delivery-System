import axios from "axios"

const aaxios = axios.create({
    baseURL: "http://127.0.0.1:5000",
    timeout: 5000
})


aaxios.interceptors.request.use((config) => {
    let access_token = localStorage.getItem('token');
    if (access_token) {
        config.headers.token = localStorage.getItem('token')
    }

    return config;
});
export default aaxios;