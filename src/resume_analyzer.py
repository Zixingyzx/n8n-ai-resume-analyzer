"""Credential-free resume analyzer used for reproducible portfolio testing."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

SKILL_GROUPS: dict[str, tuple[str, ...]] = {
    "Python": ("python",),
    "C++": ("c++", "cpp"),
    "MATLAB": ("matlab", "simulink"),
    "Git": ("git", "github", "gitlab"),
    "n8n": ("n8n",),
    "REST API": ("rest api", "restful", "api integration"),
    "Webhooks": ("webhook", "webhooks"),
    "JSON": ("json",),
    "Machine Learning": ("machine learning", "ml model", "pytorch", "tensorflow"),
    "Data Analysis": ("data analysis", "data analytics", "pandas", "numpy"),
    "SQL": ("sql", "postgres", "mysql", "sqlite"),
    "Docker": ("docker", "container"),
    "Linux": ("linux", "ubuntu"),
    "Cloud": ("aws", "azure", "gcp", "cloud platform"),
    "RAG": ("rag", "retrieval augmented generation", "vector database"),
    "Robotics": ("robotics", "ros", "robot"),
    "Signal Processing": ("signal processing", "fft", "filtering"),
    "PLC": ("plc", "siemens s7", "tia portal"),
}


def _contains_any(text: str, aliases: tuple[str, ...]) -> bool:
    return any(alias in text for alias in aliases)


def _extract_candidate_name(resume_text: str) -> str:
    for raw_line in resume_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if len(line) <= 60 and not re.search(r"[@|:/]", line):
            return line
        break
    return "Not reliably detected"


def validate_input(resume_text: str, job_description: str) -> None:
    if len(resume_text.strip()) < 150:
        raise ValueError(
            "Resume text is missing or too short. Use a text-based PDF or provide more content."
        )
    if len(job_description.strip()) < 80:
        raise ValueError("Job description is missing or too short for a meaningful comparison.")


def analyze_resume(
    resume_text: str, job_description: str, target_role: str = "Not specified"
) -> dict[str, Any]:
    """Return a transparent ATS-style heuristic analysis.

    The score is not a hiring prediction. It combines job-relevant keyword overlap,
    basic resume structure, contact information, and evidence-oriented bullet signals.
    """

    validate_input(resume_text, job_description)

    resume_lower = resume_text.lower()
    jd_lower = job_description.lower()

    required_skills = [
        skill for skill, aliases in SKILL_GROUPS.items() if _contains_any(jd_lower, aliases)
    ]
    matched_skills = [
        skill
        for skill in required_skills
        if _contains_any(resume_lower, SKILL_GROUPS[skill])
    ]
    missing_skills = [skill for skill in required_skills if skill not in matched_skills]

    if required_skills:
        keyword_score = 70 * len(matched_skills) / len(required_skills)
    else:
        keyword_score = 35

    section_terms = ("profile", "education", "experience", "projects", "skills")
    section_hits = sum(term in resume_lower for term in section_terms)
    structure_score = min(15, section_hits * 3)

    has_email = bool(re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", resume_text))
    has_link = "github.com" in resume_lower or "linkedin.com" in resume_lower
    contact_score = 5 if has_email else 0
    contact_score += 3 if has_link else 0

    evidence_terms = ("developed", "built", "implemented", "analyzed", "improved", "created")
    evidence_hits = sum(resume_lower.count(term) for term in evidence_terms)
    evidence_score = min(7, evidence_hits)

    ats_score = int(round(min(100, keyword_score + structure_score + contact_score + evidence_score)))

    strengths: list[str] = []
    if matched_skills:
        strengths.append("Documented overlap with key technical requirements: " + ", ".join(matched_skills[:6]))
    if section_hits >= 4:
        strengths.append("Clear resume structure with multiple ATS-readable sections")
    if evidence_hits >= 3:
        strengths.append("Uses evidence-oriented action verbs to describe technical work")
    if has_email and has_link:
        strengths.append("Contact information and a professional project link are easy to find")
    if not strengths:
        strengths.append("The resume provides enough text for an initial structured review")

    weaknesses: list[str] = []
    if missing_skills:
        weaknesses.append("The resume does not explicitly document: " + ", ".join(missing_skills[:6]))
    if not has_link:
        weaknesses.append("No GitHub or LinkedIn URL was detected")
    if evidence_hits < 3:
        weaknesses.append("Project bullets could use more action verbs and measurable outcomes")
    if section_hits < 4:
        weaknesses.append("Some common ATS sections are missing or use unusual headings")

    recommendations: list[str] = []
    for skill in missing_skills[:4]:
        recommendations.append(
            f"Add {skill} only if you have real experience; otherwise build a small demonstrable project first"
        )
    recommendations.extend(
        [
            "Rewrite the strongest two project bullets using action + method + measurable result",
            "Place the most role-relevant skills and project evidence in the top half of the resume",
            "Keep formatting simple and verify that PDF text can be selected and copied",
        ]
    )

    interview_questions = [
        f"Explain one project that best demonstrates your fit for {target_role}.",
        "Describe how you validated your results and handled an unexpected failure.",
        "Which part of this workflow would you keep in n8n and which part would you implement in Python?",
    ]
    if missing_skills:
        interview_questions.append(
            f"How would you close the gap in {missing_skills[0]} during your first month?"
        )

    return {
        "analysis_mode": "mock",
        "candidate_name": _extract_candidate_name(resume_text),
        "target_role": target_role or "Not specified",
        "ats_score": ats_score,
        "professional_summary": (
            f"The resume shows {len(matched_skills)} of {len(required_skills)} detected job-relevant "
            "skill groups and should be reviewed together with the evidence in the project and experience sections."
        ),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "strengths": strengths[:5],
        "weaknesses": weaknesses[:5],
        "recommended_actions": recommendations[:7],
        "interview_questions": interview_questions[:5],
        "disclaimer": "Credential-free heuristic demo; not a hiring decision or validated ATS score.",
    }


def to_markdown(analysis: dict[str, Any]) -> str:
    def bullets(values: list[str]) -> str:
        return "\n".join(f"- {value}" for value in values) if values else "- None detected"

    return f"""# Resume Analysis Report

**Mode:** {analysis['analysis_mode']}  
**Candidate:** {analysis['candidate_name']}  
**Target role:** {analysis['target_role']}  
**ATS-style score:** {analysis['ats_score']}/100

## Summary

{analysis['professional_summary']}

## Matched skills

{bullets(analysis['matched_skills'])}

## Missing or under-documented skills

{bullets(analysis['missing_skills'])}

## Strengths

{bullets(analysis['strengths'])}

## Weaknesses / resume gaps

{bullets(analysis['weaknesses'])}

## Recommended actions

{bullets(analysis['recommended_actions'])}

## Suggested interview questions

{bullets(analysis['interview_questions'])}

---

*{analysis['disclaimer']}*
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the credential-free resume analyzer.")
    parser.add_argument("--resume", required=True, type=Path)
    parser.add_argument("--job", required=True, type=Path)
    parser.add_argument("--target-role", default="Not specified")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    try:
        resume_text = args.resume.read_text(encoding="utf-8")
        job_description = args.job.read_text(encoding="utf-8")
        analysis = analyze_resume(resume_text, job_description, args.target_role)
        report = to_markdown(analysis)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "analysis.json").write_text(
            json.dumps(analysis, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        (args.output_dir / "report.md").write_text(report, encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    print(f"Analysis complete: {args.output_dir / 'analysis.json'}")
    print(f"Report complete:   {args.output_dir / 'report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
