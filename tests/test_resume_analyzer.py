import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from resume_analyzer import analyze_resume, to_markdown  # noqa: E402


RESUME = """
Alex Morgan
alex@example.com | github.com/alex
PROFILE
Python automation and data analysis student.
EDUCATION
Master of Engineering.
PROJECTS
Developed Python scripts, implemented REST API integration, and created JSON reports with Git.
EXPERIENCE
Analyzed data and improved validation tests.
SKILLS
Python, Git, JSON, REST API, Linux
"""

JOB = """
Working student role requiring Python, Git, REST API integration, JSON processing,
webhooks, n8n, Docker, documentation, testing, and data analysis experience.
"""


class ResumeAnalyzerTests(unittest.TestCase):
    def test_analysis_returns_bounded_score(self):
        result = analyze_resume(RESUME, JOB, "AI Automation Working Student")
        self.assertGreaterEqual(result["ats_score"], 0)
        self.assertLessEqual(result["ats_score"], 100)

    def test_matches_present_skills(self):
        result = analyze_resume(RESUME, JOB)
        self.assertIn("Python", result["matched_skills"])
        self.assertIn("Git", result["matched_skills"])
        self.assertIn("REST API", result["matched_skills"])

    def test_identifies_missing_skills(self):
        result = analyze_resume(RESUME, JOB)
        self.assertIn("n8n", result["missing_skills"])
        self.assertIn("Docker", result["missing_skills"])
        self.assertIn("Webhooks", result["missing_skills"])

    def test_markdown_contains_expected_sections(self):
        report = to_markdown(analyze_resume(RESUME, JOB))
        self.assertIn("# Resume Analysis Report", report)
        self.assertIn("## Matched skills", report)
        self.assertIn("## Recommended actions", report)

    def test_short_input_is_rejected(self):
        with self.assertRaises(ValueError):
            analyze_resume("too short", JOB)
        with self.assertRaises(ValueError):
            analyze_resume(RESUME, "short")


if __name__ == "__main__":
    unittest.main()
