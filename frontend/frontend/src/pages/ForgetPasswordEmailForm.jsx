import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
function ForgetPasswordEmailForm() {
  const [email, setEmail] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post("api/auth/password-reset", { email }); // for generating token and sending to email

      if (res.status === 200) {
        navigate("/message", {
          state: {
            message: "Email has been sent to your account",
          },
        });
      } else {
        alert("Failed to send email.");
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="forget-password">
        <h3>Forgot Password</h3>
        <hr />
        <p className="desc">
          Lost your password? <br />
          Please enter your username or email address. You will receive a link
          to create a new password via email.
        </p>

        <p className="email">Username or email</p>
        <input type="email" onChange={(e) => setEmail(e.target.value)} />
        <button className="button" type="submit" onClick={handleSubmit}>
          Reset Password
        </button>
      </div>
    </form>
  );
}

export default ForgetPasswordEmailForm;
