export type EvidenceStatus = "verified" | "draft" | "placeholder";

export type ExperienceItem = {
  id: string;
  organization: string;
  role: string;
  durationLabel: string;
  status: EvidenceStatus;
  summary: string;
  highlights: string[];
  technologies: string[];
  editableNotes?: string;
};

export type SystemCategory =
  | "AI Research and Web Intelligence"
  | "RAG"
  | "Conversational AI and Chatbots"
  | "Agentic Workflows"
  | "Document Intelligence"
  | "Automation and Data Processing";

export type SystemItem = {
  id: string;
  name: string;
  category: SystemCategory;
  description: string;
  technologies: string[];
  workflow: string[];
  implemented: boolean;
  status: EvidenceStatus;
  notes?: string;
};

export type SkillCategory =
  | "Core AI"
  | "LLM & Prompting"
  | "Engineering"
  | "Data & Analytics"
  | "Delivery";

export type SkillItem = {
  id: string;
  name: string;
  category: SkillCategory;
  description: string;
  relatedTools: string[];
  relatedProjects: string[];
  status: EvidenceStatus;
};

export type ToolCategory =
  | "LLM Providers"
  | "Web Search and Extraction"
  | "Agent Frameworks"
  | "Model/ML Ecosystem"
  | "Programming/Libraries"
  | "Data/Databases"
  | "Development Tools"
  | "Deployment/Infrastructure";

export type ToolItem = {
  id: string;
  name: string;
  category: ToolCategory;
  description: string;
  officialUrl?: string;
  relatedProjects: string[];
  relatedSystems: string[];
  status: EvidenceStatus;
};

export type ProjectCategory =
  | "Healthcare"
  | "Enterprise"
  | "Recommendation"
  | "NLP"
  | "Draft";

export type ProjectItem = {
  id: string;
  name: string;
  category: ProjectCategory;
  summary: string;
  architecture: string[];
  stack: string[];
  contribution: string[];
  challengesAndLearnings: string[];
  externalUrl?: string;
  repoUrl?: string;
  status: EvidenceStatus;
  notes?: string;
};

export type CertificationItem = {
  id: string;
  title: string;
  issuer: string;
  status: EvidenceStatus;
  category: string;
  summary: string;
  certificatePath?: string;
  verificationUrl?: string;
};

export type SocialConfig = {
  linkedin?: string;
  github?: string;
};
