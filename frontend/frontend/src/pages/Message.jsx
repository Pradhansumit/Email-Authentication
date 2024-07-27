import { useLocation } from "react-router-dom";
export default function Message() {
  const location = useLocation();
  return (
    <>
      <h3>{location.state.message}.</h3>
    </>
  );
}
