import { Button, Stack, Title, Container } from "@mantine/core";
import { useNavigate } from "react-router-dom";

const GRADES = Array.from({ length: 12 }, (_, i) => `Grade ${i + 1}`);

export function Home() {
  const navigate = useNavigate();

  return (
    <Container size="sm" py="xl">
      <Title order={2} mb="lg" ta="center">
        Select Grade
      </Title>

      <Stack gap="md">
        {GRADES.map((grade) => (
          <Button
            key={grade}
            size="xl"
            variant="light"
            fullWidth
            onClick={() => navigate(`/grade/${grade.replace(' ', '-').toLowerCase()}`)}
            styles={{
              root: { height: '60px', fontSize: '1.2rem' }
            }}
          >
            {grade}
          </Button>
        ))}
      </Stack>
    </Container>
  );
}
