import { useContext, createContext, useState, useEffect } from "react";
import axios from "axios";

const APIContext = createContext();

//const BASE_URL = import.meta.env.VITE_REACT_APP_BASE_URL || "http://localhost:8000/api";
const BASE_URL = "https://parcial3-web-server.vercel.app";

export const APIProvider = ({ children }) => {
    const [loadCount, setLoadCount] = useState(0);

    const setLoading = (val) =>
        setLoadCount((oldCount) => {
            const newCount = oldCount + (val ? 1 : -1);
            return newCount < 0 ? 0 : newCount;
        });

    useEffect(() => {
        document.getElementById("loading-screen").style.display =
            loadCount === 0 ? "none" : "block";
    }, [loadCount]);

    const requestHandler = async (method, url, data = undefined) => {
        console.log(`${method.toUpperCase()}: ${url}`);
        if (data) console.log("Body", data);

        setLoading(true);

        try {
            const response = await axios({ method, url, data });            
            setLoading(false);
            return response;
        } catch (error) {
            console.log(error.response);
            setLoading(false);
            return error.response;
        }
    };

    const apiMethods = {
        get: (url) => requestHandler("get", url),
        post: (url, data) => requestHandler("post", url, data),
        put: (url, data) => requestHandler("put", url, data),
        delete: (url) => requestHandler("delete", url),
    };

    const createEndpointMethods = (entity, extraEndpoints) => ({
        getAll: (params = "", version = "v1") =>
            apiMethods.get(`${BASE_URL}/${version}/${entity}${params}`),
        getById: (id, params = "", version = "v1") =>
            apiMethods.get(`${BASE_URL}/${version}/${entity}/${id}${params}`),
        create: (body, version = "v1") =>
            apiMethods.post(`${BASE_URL}/${version}/${entity}`, body),
        update: (id, body, version = "v1") =>
            apiMethods.put(`${BASE_URL}/${version}/${entity}/${id}`, body),
        delete: (id, version = "v1") =>
            apiMethods.delete(`${BASE_URL}/${version}/${entity}/${id}`),
        ...extraEndpoints,
    });

    const eventosAPI = createEndpointMethods("eventos", {
        getNearby: (lat, lon, params = "", version = "v1") =>
            apiMethods.get(`${BASE_URL}/${version}/eventos/nearby?lat=${lat}&lon=${lon}${params}`),
    });

    const mediaAPI = createEndpointMethods("media", {
        create: (body, version = "v1") =>
            apiMethods.post(`${BASE_URL}/${version}/media`, body),
        update: () => alert("Method not available"),
        delete: () => alert("Method not available"),
    });

    const usersAPI = createEndpointMethods("users", {
        getProfile: (id, version = "v1") =>
            apiMethods.get(`${BASE_URL}/${version}/users/${id}/profile`),
        getByOauthID: (id, version = "v1") =>
            apiMethods.get(`${BASE_URL}/${version}/users/oauth/${id}`),
        rate: (id, review, version = "v1") =>
            apiMethods.post(`${BASE_URL}/${version}/users/${id}/review`, review),
    });

    return (
        <APIContext.Provider
            value={{
                eventos: eventosAPI,
                media: mediaAPI,
                setLoading: setLoading,
                users: usersAPI,
            }}
        >
            {children}
        </APIContext.Provider>
    );
};

export const useAPI = () => useContext(APIContext);