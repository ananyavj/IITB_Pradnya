import { BrowserRouter, Routes, Route, Link, Outlet, useLocation } from 'react-router-dom'
import Onboarding from './pages/Onboarding'
import { Home } from './routes/Home'
import { GradeSubjects } from './routes/GradeSubjects'
import LessonViewer from './pages/LessonViewer'
import Notes from './pages/Notes'
import Search from './pages/Search'
import Quiz from './pages/Quiz'
import Settings from './pages/Settings'
import Teacher from './pages/Teacher'
import './App.css'

function AppShell() {
    const location = useLocation();

    return (
        <div className="app-shell">
            <header className="shell-header">
                <div className="logo">AI Aarohan</div>
                <nav className="shell-nav">
                    <Link to="/home" className={location.pathname === '/home' ? 'active' : ''}>Home</Link>
                    <Link to="/notes" className={location.pathname === '/notes' ? 'active' : ''}>Notes</Link>
                    <Link to="/search" className={location.pathname === '/search' ? 'active' : ''}>Search</Link>
                    <Link to="/quiz" className={location.pathname === '/quiz' ? 'active' : ''}>Quiz</Link>
                    <Link to="/settings" className={location.pathname === '/settings' ? 'active' : ''}>Settings</Link>
                </nav>
            </header>

            <main className="shell-main">
                <Outlet />
            </main>

            {/* Temporary Debug Links */}
            <footer className="shell-footer">
                <p>Debug Nav:</p>
                <Link to="/onboarding">Onboarding</Link> |
                <Link to="/lessons/123/1">Lesson Demo</Link> |
                <Link to="/teacher">Teacher</Link>
            </footer>
        </div>
    )
}

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<AppShell />}>
                    <Route index element={<Onboarding />} />
                    <Route path="onboarding" element={<Onboarding />} />
                    <Route path="home" element={<Home />} />
                    <Route path="grade/:gradeId" element={<GradeSubjects />} />
                    <Route path="lessons/:lessonId/:screenId?" element={<LessonViewer />} />
                    <Route path="notes" element={<Notes />} />
                    <Route path="search" element={<Search />} />
                    <Route path="quiz" element={<Quiz />} />
                    <Route path="settings" element={<Settings />} />
                    <Route path="teacher" element={<Teacher />} />
                </Route>
            </Routes>
        </BrowserRouter>
    )
}

export default App
