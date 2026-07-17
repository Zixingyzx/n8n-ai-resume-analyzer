# Testing strategy

## Local unit tests

Run:

```bash
python -m unittest discover -s tests -v
```

The tests verify:

- Relevant keywords are matched.
- Missing skills are identified.
- Scores remain within 0-100.
- Markdown contains the expected sections.
- Too-short input is rejected.

## n8n manual tests

| Test | Input | Expected result |
|---|---|---|
| Happy path | Valid text PDF + detailed JD | Structured analysis and Markdown report |
| Short JD | Valid PDF + `Python job` | Validation error |
| Scanned PDF | Image-only PDF | Missing/short extracted text error |
| Missing OpenAI credential | AI workflow | Credential configuration error before API call |
| Low skill overlap | Unrelated CV and JD | Lower score and larger missing-skills list |

## Acceptance criteria

The project is release-ready when:

- Local unit tests pass.
- Mock n8n workflow completes once.
- OpenAI workflow completes once, if an API credential is available.
- At least four sanitized screenshots are committed.
- README setup steps match the actual workflow.
