import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useState } from "react";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/Home";
import NotFound from "./pages/NotFound";
import ProtectedRoute from "./components/ProtectedRoute";
import "./styles/main.css"

function Logout() {
    localStorage.clear();
    return <Navigate to="/login" />
}

function RegisterAndLogout({ setUser }) {
    localStorage.clear()
    return <Register setUser={setUser} />
}

function App() {
    const [user, setUser] = useState(null)
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/home" element={
                    <ProtectedRoute>
                        <Home user={user} />
                    </ProtectedRoute>
                }
                />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<RegisterAndLogout setUser={setUser} />} />
                <Route path="/logout" element={<Logout />} />
                <Route path="*" element={<NotFound />} />
            </Routes>
        </BrowserRouter>
    )
}

export default App
