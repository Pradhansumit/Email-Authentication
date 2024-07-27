import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

function PasswordResetForm() {
  const [password, setPassword] = useState(null);
  const [confirmPassword, setConfirmPassword] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("verify-token");
      if (!token) {
        throw new Error("Token not found");
      }
      const res = await api.post("api/auth/password-reset-confirm", {
        password: password,
        confirm_password: confirmPassword,
        token: token,
      });

      if (res.status === 200) {
        navigate("/message", {
          state: { message: "Your password has been reset." },
        });
      } else {
        navigate("failed-to-process");
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="LoginForm">
      <h1 className="title">Password Reset</h1>
      <div className="input-box">
        <span className="details">New Password</span>
        <input
          className="emailInput"
          type="password"
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      <div className="input-box">
        <span className="details">Confirm Password</span>
        <input
          className="passwordInput"
          type="password"
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
      </div>
      <button onSubmit={handleSubmit} className="button" type="submit">
        Submit
      </button>
    </form>
  );
}

export default PasswordResetForm;
