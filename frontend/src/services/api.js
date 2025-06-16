import axios from "axios";

const instance = axios.create({
  baseURL: "http://localhost:8000", // update if running elsewhere
  timeout: 10000,
});

export default instance;
