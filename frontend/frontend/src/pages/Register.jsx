import RegistrationForm from "../components/RegisterForm.jsx";


function Register({ setUser }) {
    return <RegistrationForm route="api/auth/register" setUser={setUser} />
}


export default Register;