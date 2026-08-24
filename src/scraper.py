import json
import time
import requests
import sys
import os

# Clean previous failure dump if exists
if os.path.exists("failure_dump.txt"):
    os.remove("failure_dump.txt")

trigger_url = "https://api.brightdata.com/dca/trigger"

BRIGHTDATA_COLLECTOR_ID = os.getenv("BRIGHTDATA_COLLECTOR_ID")
BRIGHTDATA_API_TOKEN = os.getenv("BRIGHTDATA_API_TOKEN")

if not BRIGHTDATA_COLLECTOR_ID:
    raise RuntimeError("BRIGHTDATA_COLLECTOR_ID environment variable is not set")
if not BRIGHTDATA_API_TOKEN:
    raise RuntimeError("BRIGHTDATA_API_TOKEN environment variable is not set")

headers = {
    "Authorization": f"Bearer {BRIGHTDATA_API_TOKEN}",
    "Content-Type": "application/json",
}
params = {"collector": BRIGHTDATA_COLLECTOR_ID}

data = [
    {
        "url": "https://www.glassdoor.co.in/index.htm",
        "company_names": ["Zoho", "Amazon", "FinSurge"]
    },
]

# Trigger the scraping job
response = requests.post(trigger_url, headers=headers, params=params, json=data)
try:
    res_json = response.json()
except json.JSONDecodeError:
    res_json = {}
print("Trigger Response:", res_json)
print("Trigger Status Code:", response.status_code)
print("Trigger Raw Response:", response.text)

collection_id = res_json.get("collection_id")
if not collection_id:
    print("Error: Could not retrieve collection_id.")
    sys.exit(1)

print(f"\nCollector job initiated successfully. Collection ID: {collection_id}")
print("Waiting for Bright Data to scrape the data...")

result_url = f"https://api.brightdata.com/dca/dataset?id={collection_id}"
max_attempts = 35

result_response = None
for attempt in range(1, max_attempts + 1):
    time.sleep(20)
    print(f"Checking job status (Attempt {attempt}/{max_attempts})...")
    result_response = requests.get(result_url, headers=headers)

    if result_response.status_code == 200 and result_response.text.strip():
        print("\n--- Scraped Data Received Successfully ---")
        print(result_response.text)
        with open("scraped_output.json", "w", encoding="utf-8") as f:
            f.write(result_response.text)
        break
    elif result_response.status_code == 202:
        print("Job is still processing... waiting.")
    else:
        print(f"Status: {result_response.status_code}")
else:
    print("Timed out...")
    sys.exit(1)

raw_text = result_response.text.strip()

try:
    # Attempt to parse as a JSON array
    try:
        data_list = json.loads(raw_text)
        if not isinstance(data_list, list):
            data_list = [data_list]
    except json.JSONDecodeError:
        # Fallback to JSON Lines format
        data_list = [json.loads(line) for line in raw_text.splitlines() if line.strip()]

    if not data_list:
        raise ValueError("Scraped dataset is empty.")

    # Validate essential fields
    required_keys = ["company_name"]
    for entry in data_list:
        for key in required_keys:
            if key not in entry or entry[key] is None:
                raise KeyError(f"Missing essential data '{key}' in output")

    print(f"Validation passed: {len(data_list)} company entries scraped successfully.")

    # Write validated JSON (pretty‑printed)
    with open("scraped_output.json", "w", encoding="utf-8") as f:
        json.dump(data_list, f, indent=2, ensure_ascii=False)

    sys.exit(0)

except Exception as error:
    print(f"Validation / Scraping error: {error}")

    with open("failure_dump.txt", "w", encoding="utf-8") as f:
        f.write(f"Error Type: {type(error).__name__}\n")
        f.write(f"Error Details: {str(error)}\n")
        f.write(f"Response Snippet: {result_response.text[:500]}\n")
    sys.exit(1)