import React from "react";

const style = {
    position: "fixed",
    top: "0",
    left: "0",
    width: "100%",
    height: "100%",
    backgroundColor: "rgba(0, 0, 0, 0.5)",
    zIndex: "9999",
    display: "none",
    color: "white"
}

export default function LoadingScreen() {
    return (
        <div id="loading-screen" style={{ display: "none" }}>
            <div className="d-flex flex-column justify-content-center align-items-center" style={style}>
                <div className="spinner-border" style={{ width: "100px", height: "100px" }} role="status">
                    <span className="visually-hidden">Cargando...</span>
                </div>

                <div className="m-5 d-none">
                    <h1 className="text-white">Si estás viendo esto es porque la página está haciendo una llamada a la API</h1>
                    <p className="text-white">
                        Es un coñazo, así que deberíamos coger y en cada sitio donde se hace una llamada a la API,
                        meter algo que se ajuste bien a esa carga. Por ejemplo, en la página principal, en vez de poner
                        esta pedazo de pantalla de cargando, se puede poner donde aparece la lista de wikis un spinner
                        cargando, así no se bloquea la pantalla entera, sino simplemente esa parte
                    </p>
                </div>
            </div>
        </div>
    );
}