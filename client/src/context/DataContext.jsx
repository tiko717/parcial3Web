import { useContext, createContext, useState } from "react";

const DataContext = createContext();

export const DataProvider = ({ children }) => {
    const [event, setEvent] = useState(undefined);

    const getActualEvent = () => event;

    const setActualEvent = (event) => setEvent(event);

    const clearActualEvent = () => setEvent(undefined);

    return (
        <DataContext.Provider
            value={{
                getActualEvent,
                setActualEvent,
                clearActualEvent,
            }}
        >
            {children}
        </DataContext.Provider>
    );
};

export const useData = () => useContext(DataContext);