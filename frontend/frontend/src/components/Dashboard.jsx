import { jwtDecode } from "jwt-decode";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { REFRESH_TOKEN } from "../constants";
export default function Dashboard() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  function handleClick() {
    navigate("/logout");
  }

  useEffect(() => {
    const token = localStorage.getItem(REFRESH_TOKEN);
    const token_dec = jwtDecode(token);
    const user = token_dec.first_name;
    console.log(user);
    setUser(user);
  });
  return (
    <>
      <div className="btn-container">
        <button className="logout-button" onClick={handleClick}>
          Logout
        </button>
      </div>
      <div>Welcome {user}</div>
    </>
  );
}
