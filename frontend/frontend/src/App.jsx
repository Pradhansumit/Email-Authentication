import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import PasscodeTokenEmail from "./components/PasscodeTokenEmail";
import ProtectedRoute from "./components/ProtectedRoute";
import ForgetPasswordEmailForm from "./pages/ForgetPasswordEmailForm";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Message from "./pages/Message";
import NotFound from "./pages/NotFound";
import PasswordResetForm from "./pages/PasswordResetForm";
import Register from "./pages/Register";
import "./styles/main.css";

function Logout() {
  localStorage.clear();
  return <Navigate to="/login" />;
}

function RegisterAndLogout() {
  localStorage.clear();
  return <Register />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<RegisterAndLogout />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="*" element={<NotFound />} />
        <Route path="/message" element={<Message />} />
        <Route path="/forgot-password" element={<ForgetPasswordEmailForm />} />
        <Route path="/auth" element={<PasscodeTokenEmail />} />
        <Route path="/password-reset" element={<PasswordResetForm />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
