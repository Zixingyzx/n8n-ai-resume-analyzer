# Architecture

## Input layer

The n8n Form Trigger provides a minimal frontend with three fields:

- `resume_file`: one PDF upload.
- `target_role`: the intended role.
- `job_description`: the vacancy text.

The form is suitable for a portfolio demo because it avoids building and hosting a separate frontend.

## Extraction layer

The uploaded file arrives as binary data. The Extract From File node converts the PDF into JSON containing extracted text and metadata. The workflow assumes a text-based PDF. Image-only scanned PDFs require OCR and are intentionally outside the first version.

## Validation layer

A Code node checks:

- Resume text exists.
- Resume text is long enough to be meaningful.
- Job description exists and is sufficiently detailed.
- Target role has a fallback value.

Failing early prevents unnecessary model calls and makes debugging clearer.

## Analysis layer

### Mock mode

The mock workflow finds job-relevant terms in the job description and checks whether they also appear in the resume. It combines keyword overlap with simple resume-structure checks. This is not an LLM and is labeled clearly in the output.

### OpenAI mode

The AI workflow uses a Basic LLM Chain rather than an AI Agent. The task is a single bounded transformation and does not need autonomous tool selection. A Structured Output Parser validates the response against JSON Schema.

## Output layer

The final Code node converts the structured result to Markdown. Keeping both JSON and Markdown supports machine processing and human-readable reporting.

## Failure paths

- Unreadable PDF: Extract From File or validation fails.
- Too-short content: validation throws an explicit error.
- Missing credential: OpenAI node stops before an API call.
- Malformed model response: Structured Output Parser rejects it.
- Sensitive data exposure: prevented operationally through `.gitignore`, sanitized samples, and documentation.
