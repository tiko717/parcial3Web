import React, { createContext, useContext, useState } from "react";

const DataContext = createContext();

export const DataProvider = ({ children }) => {
    const [country, setCountry] = useState(undefined);

    const getActualCountry = () => country;

    const setActualCountry = (country) => setCountry(country);

    const clearActualCountry = () => setCountry(undefined);

    return (
        <DataContext.Provider
            value={{
                getActualCountry,
                setActualCountry,
                clearActualCountry,
            }}
        >
            {children}
        </DataContext.Provider>
    );
};

export const useData = () => useContext(DataContext);