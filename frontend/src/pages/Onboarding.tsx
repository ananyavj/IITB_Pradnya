import { Link } from 'react-router-dom'

export default function Onboarding() {
    return (
        <div className="page">
            <h1>Onboarding Screen</h1>
            <p>Welcome to AI Aarohan! This is where new users will learn about the app.</p>
            <Link to="/home" className="button">Get Started</Link>
        </div>
    )
}
