# Interview guide

## 45-second explanation

> I built an n8n workflow that receives a PDF resume and job description through a form, extracts the resume text, validates the input, evaluates job fit, and returns structured JSON plus a Markdown report. I included a credential-free deterministic version so anyone can reproduce the pipeline, and an OpenAI version with a Structured Output Parser for schema-valid results. I also added tests, explicit failure cases, privacy safeguards, and documentation.

## Why n8n instead of only Python?

> n8n makes the orchestration and data flow visible, which is useful for rapid prototyping and integrations. Python remains better for complex custom algorithms. In this project I used n8n for workflow orchestration and Code nodes or local Python for transparent custom logic.

## Why a Basic LLM Chain instead of an AI Agent?

> The model performs one bounded transformation and does not need to decide which tools to call. A chain is simpler, easier to test, and less likely to behave unpredictably.

## What is a webhook or form trigger?

> A trigger is the workflow entry point. The n8n Form Trigger hosts a web form and starts the workflow when a user submits it. Internally, the form submission reaches a generated HTTP endpoint.

## What is binary data?

> The uploaded PDF is not ordinary JSON text. n8n carries it as binary data. Extract From File reads that binary PDF and produces JSON fields, including the extracted text.

## Why structured output?

> Free-form model text is difficult for downstream automation. The Structured Output Parser validates a JSON schema so later nodes can reliably access fields such as `ats_score` or `missing_skills`.

## Main limitations

- Image-only PDFs need OCR.
- Keyword or LLM scores are heuristic.
- Model output can still contain errors.
- Real hiring systems require legal, privacy, bias, and human-review controls.
- The current project produces a report but does not persist data to a database.

## Sensible next production improvements

- OCR fallback for scanned documents.
- Authentication and rate limiting on the public form.
- Encrypted storage with retention rules.
- Human approval step.
- Evaluation dataset and score calibration.
- Observability, retries, and cost monitoring.
