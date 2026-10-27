
import json
from pathlib import Path
from decimal import Decimal, InvalidOperation

data_dir = Path(__file__).parent / "data"
data_dir.mkdir(exist_ok=True)

# API에서 수집했다고 가정한 데이터
raw_data = [
    {"symbol": "QQQ", "date": "2026-10-26", "close": "620.50"},
    {"symbol": "SPY", "date": "2026-10-26", "close": "680.20"},
    {"symbol": "QQQ", "date": "2026-10-26", "close": "620.50"},
    {"symbol": "SPY", "date": "2026-10-27", "close": None},
]

# 1. Raw 데이터 보존
with open(data_dir / "raw.json", "w", encoding="utf-8") as f:
    json.dump(raw_data, f, ensure_ascii=False, indent=2)

# 2. 유효성 검사와 중복 제거
cleaned = []
seen = set()
invalid_count = 0

for row in raw_data:
    key = (row["symbol"], row["date"])

    if key in seen:
        continue

    try:
        price = Decimal(str(row["close"]))
        if not price.is_finite() or price <= 0:
            raise ValueError("Invalid price")
    except (InvalidOperation, ValueError):
        invalid_count += 1
        continue

    seen.add(key)
    cleaned.append({
        "symbol": row["symbol"],
        "date": row["date"],
        "close": str(price),
    })

# 3. Clean 데이터 저장
with open(data_dir / "clean.json", "w", encoding="utf-8") as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)

print(f"원본: {len(raw_data)}건")
print(f"정제 완료: {len(cleaned)}건")
print(f"유효하지 않은 가격: {invalid_count}건")
