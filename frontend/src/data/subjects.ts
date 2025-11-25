export type SubjectId =
    | "maths"
    | "science"
    | "social_science"
    | "english"
    | "hindi"
    | "sanskrit"
    | "computer_science"
    | "physical_education";

export interface SubjectMeta {
    id: SubjectId;
    name: string;
    tagline: string;
}

export const SUBJECTS: SubjectMeta[] = [
    {
        id: "maths",
        name: "Mathematics",
        tagline: "Number systems, algebra, geometry, trigonometry, and statistics",
    },
    {
        id: "science",
        name: "Science",
        tagline: "Physics, chemistry, and biology concepts",
    },
    {
        id: "social_science",
        name: "Social Science",
        tagline: "History, geography, political science, and economics",
    },
    {
        id: "english",
        name: "English",
        tagline: "Literature, grammar, and composition",
    },
    {
        id: "hindi",
        name: "Hindi",
        tagline: "Hindi literature and language",
    },
    {
        id: "sanskrit",
        name: "Sanskrit",
        tagline: "Sanskrit language and literature",
    },
    {
        id: "computer_science",
        name: "Computer Science",
        tagline: "Programming, algorithms, and computer fundamentals",
    },
    {
        id: "physical_education",
        name: "Physical Education",
        tagline: "Sports, fitness, and health education",
    },
];
