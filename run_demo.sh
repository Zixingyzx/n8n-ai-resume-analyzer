#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 src/resume_analyzer.py \
  --resume sample_data/sample_resume.txt \
  --job sample_data/sample_job_description.txt \
  --target-role "Working Student AI Automation" \
  --output-dir outputs
