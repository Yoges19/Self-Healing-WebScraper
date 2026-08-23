import os
import sys
from google import genai

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY env variable not found")
    sys.exit(1)

client = genai.Client(api_key=api_key)

try:
    # It reads the failure_dump.txt file that we've created in the scraper.py

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

print("Sending context to Gemini for self-healing....")
response = client.models.generate_content(
    model="gemin-2.5-flash",
    content=prompt
)

fixed_code = response.text.strip()

if fixed_code.startswith("```python"):
    fixed_code = fixed_code[9:]
if fixed_code.startswith("```"):
    fixed_code = fixed_code[3:]
if fixed_code.endswith("```"):
    fixed_code = fixed_code[:-3]

fixed_code = fixed_code.strip()

with open("src/scraper.py", "w", encoding="utf-8") as f:
    f.write(fixed_code)

print("Self-healing process complete. scraper.py updated succesfully")