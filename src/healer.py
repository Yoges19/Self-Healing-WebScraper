import os
import sys
from groq import Groq
from pathlib import Path


api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("Error: GROQ_API_KEY env variable not found")
    sys.exit(1)

client = Groq(api_key=api_key)

try:
    # It first reads the failure_dump.txt file that we've created in the scraper.py

    with open("failure_dump.txt", "r", encoding="utf-8") as f:
        failure_log = f.read()
except FileNotFoundError:
    print("No failure_dump.txt Found. Nothing to heal")
    sys.exit(0)

#if there is a failure file that means we've to heal the scraper.py
with open("src/scraper.py", "r", encoding="utf-8") as f:
    broken_code = f.read()


prompt = f"""
You are an expert AI automated code-healing engine running inside a CI pipeline.
A web scraper script failed during execution.

BROKEN CODE (scraper.py)
{broken_code}

ERROR / FAILURE CONTEXT
{failure_log}

TASK:
Analyze the error and the code. Provide the fully corrected, functional version of `scraper.py`.
STRICT RULES:
1. Return ONLY the raw Python code.
2. Do NOT wrap the code in markdown codeblocks (do NOT include ```python or ```).
3. Do NOT add conversational text or explanations.
"""

print("Sending context to Groq for self-healing...")
response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "system",
            "content": "You are an automated Python code repair bot. Return ONLY valid, executable Python code with no markdown formatting or extra text"
        },
        {
            "role": "user",
            "content": prompt,
        }
    ],
    temperature=1,
    max_completion_tokens=2048,
    top_p=1,
    reasoning_effort="medium",
    stream=True,
    stop=None
)


fixed_code = response.choice[0].message.content.strip()

if fixed_code.startswith("```python"):
    fixed_code = fixed_code[9:]
if fixed_code.startswith("```"):
    fixed_code = fixed_code[3:]
if fixed_code.endswith("```"):
    fixed_code = fixed_code[:-3]

fixed_code = fixed_code.strip()

scraper_file = Path(__file__).resolve().parent / "scraper.py"
scraper_file.write_text(fixed_code, encoding="utf-8")

print("Self-healing process complete. scraper.py updated succesfully")