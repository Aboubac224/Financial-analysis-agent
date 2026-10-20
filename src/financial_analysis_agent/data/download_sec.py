import  json
from pathlib import Path

import  requests

SEC_BASE_URL = "https://data.sec.gov/api/xbrl/companyfacts"


def download_company_facts(
        cik: str,
        user_agent: str,
        output_dir: Path,
) -> Path:
    """Download company facts XBRL of a company from SEC."""

    # 1. Build URL from CIK
    cik = str(cik).zfill(10)
    url = f"{SEC_BASE_URL}/CIK{cik}.json"

    # 2. Identify our application with SEC
    headers = {
        "User-Agent": user_agent,
        "Accept": "application/json",
    }

    # 3. Send HTTP request
    response = requests.get(url, headers=headers, timeout=60)
    response.raise_for_status()

    # 4. Convert the JSON responses to the Python dictionary
    data = response.json()

    # 5. Check the main fields
    if not isinstance(data, dict) or not isinstance(data.get("facts"), dict):
        raise ValueError("Invalid response company facts.")

    # 6. Create the target directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # 7. Save the raw data
    output_path = output_dir / f"CIK{cik}_companyfacts.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    return output_path