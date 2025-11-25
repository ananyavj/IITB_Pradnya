import { Button, SimpleGrid, Title, Container, Text } from "@mantine/core";
import { useParams, useNavigate, Link } from "react-router-dom";

const GRADE_10_SUBJECTS = [
    { name: "English", id: "english" },
    { name: "Math", id: "maths" },
    { name: "Social Science", id: "social_science" },
    { name: "Science", id: "science" },
    { name: "Physical Education", id: "physical_education" },
];

export function GradeSubjects() {
    const { gradeId } = useParams();
    const navigate = useNavigate();

    // Format gradeId for display (e.g. "grade-10" -> "Grade 10")
    const title = gradeId ? gradeId.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase()) : 'Grade';

    const isGrade10 = gradeId === 'grade-10';

    return (
        <Container size="sm" py="xl">
            <Link to="/home" style={{ textDecoration: 'none', color: 'inherit', display: 'inline-block', marginBottom: '1rem' }}>
                &larr; Back to Grades
            </Link>

            <Title order={2} mb="lg" ta="center">
                {title} Subjects
            </Title>

            {isGrade10 ? (
                <SimpleGrid cols={2} spacing="md">
                    {GRADE_10_SUBJECTS.map((subject) => (
                        <Button
                            key={subject.id}
                            variant="light"
                            size="xl"
                            h={80}
                            fz="lg"
                            onClick={() => navigate(`/subject/${subject.id}`)}
                        >
                            {subject.name}
                        </Button>
                    ))}
                </SimpleGrid>
            ) : (
                <Text ta="center" c="dimmed">
                    Subjects for {title} coming soon.
                </Text>
            )}
        </Container>
    );
}
