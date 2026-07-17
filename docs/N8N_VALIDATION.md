# Validate the project in n8n

Start with the mock workflow. Do not configure OpenAI until the mock path works.

## Part A: import

1. Sign in to n8n Cloud or open your local n8n instance.
2. Create a blank workflow.
3. Open the workflow menu.
4. Select **Import from file**.
5. Choose `workflow/n8n_resume_analyzer_mock.json`.
6. Save the workflow.

Expected result: five connected nodes and explanatory sticky notes appear on the canvas.

## Part B: run the form

1. Open **Resume Analyzer Form**.
2. Select **Test workflow** or **Execute workflow**.
3. n8n opens a test form in a new browser tab.
4. Upload a text-based PDF resume.
5. Enter a target role.
6. Paste a job description with at least several sentences.
7. Submit the form.

The test URL is temporary and listens only while the editor is waiting. The production URL works only after the workflow is saved and activated/published.

## Part C: inspect every node

### 1. Resume Analyzer Form

Check:

- JSON fields: `target_role`, `job_description`, submission timestamp.
- Binary field: `resume_file`.

Meaning: JSON contains ordinary text values; binary contains the uploaded file.

### 2. Extract Resume Text

Check the output for a `text` field containing the resume content.

Meaning: the PDF has been converted from binary data into machine-readable JSON text.

### 3. Validate Input

Check:

- `input_valid: true`
- `resume_text`
- `target_role`
- `job_description`

Meaning: the workflow has normalized the data and rejected unusable input before analysis.

### 4. Analyze Resume - Mock

Check:

- `analysis_mode: mock`
- `ats_score`
- `matched_skills`
- `missing_skills`
- `strengths`
- `recommended_actions`

Meaning: deterministic code has transformed the validated input into structured evaluation data.

### 5. Generate Markdown Report

Check `report_markdown`.

Meaning: machine-readable JSON has been converted into a report suitable for display, email, storage, or later PDF generation.

## Part D: test one failure case

Run the workflow again with a very short job description such as `Python job`.

Expected result: **Validate Input** throws an explicit error. This screenshot is useful evidence of error handling.

## Part E: switch to OpenAI

1. Import `workflow/n8n_resume_analyzer_openai.json`.
2. Open **OpenAI Chat Model**.
3. Create or select an OpenAI credential.
4. Select a model available to your account.
5. Save the node.
6. Run the form again.
7. Open **Analyze Resume with AI** and inspect the `output` object.
8. Open **Generate Markdown Report** and inspect `report_markdown`.

## Screenshots to take

- Entire workflow canvas.
- Upload form.
- Extracted text node output.
- Structured analysis output.
- Markdown report output.
- Optional validation-error execution.

Do not expose real names, addresses, phone numbers, API keys, credential IDs, or private resumes in screenshots.
