import { SiteHeader } from "@/components/layout/site-header";
import { AiSystemsSection } from "@/components/sections/ai-systems-section";
import { CertificationsSection } from "@/components/sections/certifications-section";
import { ContactSection } from "@/components/sections/contact-section";
import { ExperienceSection } from "@/components/sections/experience-section";
import { HeroSection } from "@/components/sections/hero-section";
import { ProjectsSection } from "@/components/sections/projects-section";
import { SkillsSection } from "@/components/sections/skills-section";
import { ToolsSection } from "@/components/sections/tools-section";
import { profile } from "@/data/portfolio";
import { asSafeUrl, siteConfig } from "@/lib/config";

export default function HomePage() {
  const linkedinUrl = asSafeUrl(siteConfig.linkedinUrl);
  const githubUrl = asSafeUrl(siteConfig.githubUrl);

  return (
    <>
      <SiteHeader />
      <main>
        <HeroSection linkedinUrl={linkedinUrl} githubUrl={githubUrl} />
        <ExperienceSection />
        <AiSystemsSection />
        <SkillsSection />
        <ToolsSection />
        <ProjectsSection />
        <CertificationsSection />
        <ContactSection linkedinUrl={linkedinUrl} githubUrl={githubUrl} publicContactEmail={siteConfig.contactEmail || undefined} />
      </main>
      <footer className="border-t border-zinc-800/80 py-8">
        <div className="mx-auto flex w-full max-w-6xl flex-col gap-3 px-5 text-sm text-zinc-400 sm:px-8">
          <p>
            {profile.name} · {profile.title}
          </p>
          <p className="font-mono text-xs">This portfolio intentionally marks unverified details as editable placeholders.</p>
        </div>
      </footer>
    </>
  );
}
