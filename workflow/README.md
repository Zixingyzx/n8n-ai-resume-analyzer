# n8n workflow files

## `n8n_resume_analyzer_mock.json`

Use this first. It requires no credentials and demonstrates the complete data flow:

```text
Form Trigger -> Extract PDF -> Validate -> Mock Analyze -> Markdown Report
```

The analyzer uses explicit keyword-overlap and resume-structure rules. It is intentionally transparent and reproducible.

## `n8n_resume_analyzer_openai.json`

Use this after the mock workflow works. It replaces the deterministic analyzer with:

```text
Basic LLM Chain + OpenAI Chat Model + Structured Output Parser
```

The OpenAI credential is deliberately not included. Add it inside n8n. Never put API keys in exported workflow files.

## Import

Use the workflow menu in n8n and select **Import from file**, or paste the JSON into a blank workflow canvas.
