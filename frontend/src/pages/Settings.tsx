import { useMantineColorScheme, SegmentedControl, Group, Text, Container, Title, Paper } from '@mantine/core';

export default function Settings() {
    const { colorScheme, setColorScheme } = useMantineColorScheme();

    return (
        <Container size="sm" py="xl">
            <Title order={2} mb="lg">Settings</Title>

            <Paper withBorder p="md" radius="md">
                <Group justify="space-between">
                    <Text fw={500}>Theme</Text>
                    <SegmentedControl
                        value={colorScheme}
                        onChange={(value) => setColorScheme(value as 'light' | 'dark' | 'auto')}
                        data={[
                            { label: 'Light', value: 'light' },
                            { label: 'Dark', value: 'dark' },
                            { label: 'Auto', value: 'auto' },
                        ]}
                    />
                </Group>
            </Paper>
        </Container>
    )
}
