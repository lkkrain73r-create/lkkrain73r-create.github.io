import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
for item in json.loads((root / "media-parts.json").read_text(encoding="utf-8")):
    target = root / "site" / item["file"]
    target.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    with target.open("wb") as output:
        for part in item["parts"]:
            content = (root / "media-parts" / part).read_bytes()
            digest.update(content)
            output.write(content)
    if target.stat().st_size != item["size"] or digest.hexdigest() != item["sha256"]:
        raise ValueError(f"Media integrity check failed for {item['file']}")
    print(f"Verified {item['file']}")
