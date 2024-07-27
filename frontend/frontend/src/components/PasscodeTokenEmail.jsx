import { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import api from "../api";

export default function PasscodeTokenEmail() {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const token = queryParams.get('token');

  const navigate = useNavigate();

  useEffect(() => {
    const verifyToken = async () => {
      try {
        const res = await api.post("api/auth/verify-password-reset", { token: token });

        if (res.status === 202) {
          localStorage.setItem("verify-token", token) // to get the email from token for changing password in backend
          navigate("/password-reset");
        } else {
          navigate("/not-found-error");
        }
      } catch (error) {
        console.error("API call failed:", error);
        navigate("/not-found-error");
      }
    };

    if (token) {
      verifyToken();
    } else {
      navigate("/not-found-error");
    }
  }, [token, navigate]);
}
