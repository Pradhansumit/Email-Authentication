import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

export default function RegistrationForm({ route }) {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [address, setAddress] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");

  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();
    try {
      const res = await api.post(route, {
        first_name: firstName,
        last_name: lastName,
        address: address,
        email: email,
        password: password,
        phone_number: phoneNumber,
      });
      if (res.status === 201) {
        navigate("/message", {
          state: {
            message: "Your account have been successfully registered.",
          },
        });
      } else {
        navigate("/api/auth/register");
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };
  return (
    <form onSubmit={handleSubmit} className="RegistrationForm">
      <h1 className="title">Registration Form</h1>
      <div className="content">
        <div className="input-box">
          <span className="details">First Name</span>
          <input
            className="firstName"
            type="text"
            placeholder="Enter your first name"
            onChange={(e) => setFirstName(e.target.value)}
          />
        </div>
        <div className="input-box">
          <span className="details">Last Name</span>
          <input
            className="lastName"
            type="text"
            placeholder="Enter your last name"
            onChange={(e) => setLastName(e.target.value)}
          />
        </div>
        <div className="input-box">
          <span className="details">Address</span>
          <input
            className="address"
            type="text"
            placeholder="Enter your address"
            onChange={(e) => setAddress(e.target.value)}
          />
        </div>
        <div className="input-box">
          <span className="details">Phone Number</span>
          <input
            className="phoneNumber"
            type="text"
            placeholder="Enter your phone number"
            onChange={(e) => setPhoneNumber(e.target.value)}
          />
        </div>
        <div className="input-box">
          <span className="details">Email</span>
          <input
            className="emailInput"
            type="email"
            placeholder="Email Address"
            onChange={(e) => setEmail(e.target.value)}
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
          Register
        </button>
      </div>
    </form>
  );
}
