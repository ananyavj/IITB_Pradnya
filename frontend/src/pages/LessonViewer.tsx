import { useParams } from 'react-router-dom'

export default function LessonViewer() {
    const { lessonId, screenId } = useParams()

    return (
        <div className="page">
            <h1>Lesson Viewer Screen</h1>
            <p>Lesson ID: <strong>{lessonId || 'Not specified'}</strong></p>
            <p>Screen ID: <strong>{screenId || 'Not specified'}</strong></p>
            <p>Lesson content and navigation will appear here.</p>
        </div>
    )
}
