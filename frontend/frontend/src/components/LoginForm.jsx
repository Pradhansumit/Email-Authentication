import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api.js";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants.js";

export default function LoginForm({ route }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  // const [loading, setLoading] = useState(false)
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    // setLoading(true);
    e.preventDefault();
    try {
      const res = await api.post(route, { username, password });
      if (res.status === 200) {
        navigate("/");
        localStorage.setItem(ACCESS_TOKEN, res.data["access-token"]); //to set the token from response to localStorage
        localStorage.setItem(REFRESH_TOKEN, res.data["refresh-token"]); //to set the token from response to localStorage
      }
    } catch (error) {
      console.log("Found an error in your code :( !!!");
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="LoginForm">
      <h1 className="title">Login Form</h1>
      <div className="input-box">
        <span className="details">Email</span>
        <input
          className="emailInput"
          type="email"
          placeholder="Email Address"
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>
      <div className="input-box">
        <span className="details">Password</span>
        <input
          className="passwordInput"
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      <button onSubmit={handleSubmit} className="button" type="submit">
        Login
      </button>
      <div style={{ textAlign: "center" }}>
        <Link to="/forgot-password">Forgot Password</Link>
        <br />
        <Link to="/register">Sign Up</Link>
      </div>
    </form>
  );
}
