# GitHub publishing checklist

## Rename the existing repository

Recommended repository name:

```text
n8n-ai-resume-analyzer
```

Recommended description:

```text
AI-powered PDF resume analysis with n8n, structured output, a credential-free demo, testing, and an OpenAI upgrade path.
```

Recommended topics:

```text
n8n automation openai resume-analysis workflow-automation python ai-automation json
```

## Commit plan

Use a small, credible history instead of one vague commit:

```text
feat: replace request triage demo with resume analyzer workflow
feat: add credential-free analyzer and sample data
feat: add OpenAI workflow with structured output
 test: add analyzer unit tests and failure cases
 docs: add architecture, setup, privacy, and interview guide
 docs: add sanitized n8n execution screenshots
```

## Release checklist

- [ ] Repository renamed.
- [ ] Old request-triage files removed.
- [ ] New project files uploaded.
- [ ] Mock workflow tested in n8n.
- [ ] Screenshots added.
- [ ] No personal resume or API key committed.
- [ ] README links work.
- [ ] Create GitHub Release `v1.0.0`.

## Release title

```text
v1.0.0 - Portfolio-ready AI Resume Analyzer
```

## Release notes

```text
First stable portfolio release.

- PDF resume intake through n8n Form Trigger
- Built-in PDF text extraction
- Input validation and explicit error handling
- Credential-free deterministic analysis mode
- OpenAI analysis workflow with structured JSON output
- Markdown report generation
- Local unit tests, sample data, privacy guidance, and interview documentation
```
