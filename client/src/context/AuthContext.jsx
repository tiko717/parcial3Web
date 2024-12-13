import { useContext, createContext, useState } from "react";
import {
    getAuth,
    signInWithPopup,
    GoogleAuthProvider,
    FacebookAuthProvider,
} from "firebase/auth";
import { useAPI } from "./APIContext";
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
const AuthContext = createContext();
// Firebase configuration
const firebaseConfig = {
    apiKey: import.meta.env.VITE_API_KEY,
    authDomain: import.meta.env.VITE_AUTH_DOMAIN,
    projectId: import.meta.env.VITE_PROJECT_ID,
    storageBucket: import.meta.env.VITE_STORAGE_BUCKET,
    messagingSenderId: import.meta.env.VITE_MESSAGING_SENDER_ID,
    appId: import.meta.env.VITE_APP_ID,
    measurementId: import.meta.env.VITE_MEASUREMENT_ID,
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    const { users } = useAPI();

    // Obtiene el usuario actual
    const getUser = () => user;

    // Verifica si hay un usuario logueado
    const isLogged = () => user !== undefined && user !== null;

    // Comprueba si un usuario existe en la base de datos
    const isUser = async (uid) => {
        try {            
            const response = await users.getByOauthID(uid);
            return response.status === 200;
        } catch (error) {
            console.error("Error checking user:", error);
            return false;
        }
    };

    // Maneja el inicio de sesión con un proveedor
    const login = async (providerName) => {
        let provider;

        if (providerName === "google") {
            provider = new GoogleAuthProvider();
        } else if (providerName === "facebook") {
            provider = new FacebookAuthProvider();
        }

        try {
            const result = await signInWithPopup(auth, provider);
            const { user: firebaseUser } = result;
            const token = await firebaseUser.getIdToken();

            // Verifica si el usuario existe
            const userExists = await isUser(firebaseUser.uid);

            if (!userExists) {
                // Si el usuario no existe, lo registra
                await register(firebaseUser, token, providerName);
            } else {
                // Si existe, actualiza el estado del usuario
                const response = await users.getByOauthID(firebaseUser.uid);

                const id = response.data[0]._id;
                const name = response.data[0].name
                setUser({
                    uid: firebaseUser.uid,
                    email: firebaseUser.email,
                    authMethod: providerName,
                    id: id,
                    name: name
                });
            }
        } catch (error) {
            console.error("Error during login:", error);
        }
    };

    // Registra un nuevo usuario en la base de datos
    const register = async (firebaseUser, token, providerName) => {
        try {
            const userPayload = {
                email: firebaseUser.email || "",
                name: firebaseUser.displayName || "",
                surname: "", // Puede ajustarse si tienes un campo para el apellido en el proveedor
                description: "New user registered", // Descripción predeterminada o personalizada
                userName: firebaseUser.email?.split("@")[0] || firebaseUser.uid, // Usa la parte local del correo como nombre de usuario o el UID
                oauthId: firebaseUser.uid || "",
                oauthProvider: providerName || "",
                oauthToken: token || "",
                profilePicture:
                    firebaseUser.photoURL || "https://example.com/default-profile.jpg", // URL predeterminada o la que proporciona Firebase
            };

            const response = await users.create(userPayload, "v1");

            if (response.status === 201) {
                console.log("User created successfully:", response.data);
                setUser({
                    uid: response.data.result._id,
                    email: response.data.result.email,
                    authMethod: providerName,
                    id: response.data.result._id,
                });
                return response.data; // Devuelve los datos del usuario creado
            } else {
                console.error("Failed to create user:", response.status, response.data);
                throw new Error("Error creating user");
            }
        } catch (error) {
            console.error("Error during user creation:", error);
            throw error; // Re-lanzar el error para manejarlo más arriba
        }
    };

    // Cierra sesión del usuario actual
    const logout = () => {
        auth.signOut();
        setUser(null);
    };

    return (
        <AuthContext.Provider
            value={{
                getUser,
                isLogged,
                isUser,
                login,
                register,
                logout,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
