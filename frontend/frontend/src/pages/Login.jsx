import { jwtDecode } from "jwt-decode";
import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import api from "../api.js";
import LoginForm from "../components/LoginForm.jsx";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants.js";

export default function Login() {
  const [isAuthorized, setIsAuthorized] = useState(null);

  useEffect(() => {
    auth().catch(() => setIsAuthorized(false));
  }, [isAuthorized]);

  // FOR RETRIEVING ACCESS AND NEW REFRESH TOKEN FROM API
  const refreshToken = async () => {
    const refreshToken = localStorage.getItem(REFRESH_TOKEN);
    try {
      const res = await api.post("/api/auth/refresh", {
        refresh: refreshToken,
      });
      if (res.status === 200) {
        localStorage.setItem(ACCESS_TOKEN, res.data["access-token"]);
        localStorage.setItem(REFRESH_TOKEN, res.data["refresh-token"]);
        setIsAuthorized(true);
      } else {
        setIsAuthorized(false);
      }
    } catch (error) {
      console.error(error);
      setIsAuthorized(false);
    }
  };

  // FOR CHECKING THE TOKEN IS VALID
  const auth = async () => {
    const accesstoken = localStorage.getItem(ACCESS_TOKEN); // get access token from localstorage
    const refreshtoken = localStorage.getItem(REFRESH_TOKEN); // get refresh token from localstorage

    // CHECK FOR REFRESH TOKEN
    if (refreshtoken === null || refreshtoken === "") {
      setIsAuthorized(false);
      return;
    }

    // CHECK FOR ACCESS TOKEN
    if (accesstoken === null || accesstoken === "") {
      await refreshToken(); // call for new access token and refresh token
    } else {
      const decoded = jwtDecode(accesstoken);
      const tokenExpiration = decoded.exp;
      const now = Date.now() / 1000;

      // CHECK FOR TOKEN EXPIRY
      if (tokenExpiration < now) {
        await refreshToken();
      } else {
        setIsAuthorized(true);
      }
    }
  };
  if (isAuthorized === null) {
    return <div>Loading...</div>;
  }

  if (isAuthorized === true) {
    return <Navigate to="/" />;
  } else {
    return <LoginForm route={"api/auth/login"} />;
  }
}

// FAILED
