"""Xuất thời gian từng bước của các instance đã chạy ra CSV (dùng cho Task #10).

  python src/kpi.py            -> ghi kpi_element_instances.csv và in tóm tắt
"""
import csv
import re
from datetime import datetime
from statistics import mean

import camunda_api as api
from start import PROCESS_ID


def ts(s: str | None):
    """Đọc thời gian Camunda trả về: '...Z', '...+00:00' hoặc '...+0000'."""
    if not s:
        return None
    s = re.sub(r"([+-]\d{2})(\d{2})$", r"\1:\2", s.replace("Z", "+00:00"))
    return datetime.fromisoformat(s)


if __name__ == "__main__":
    rows = api.search("element-instances", {"processDefinitionId": PROCESS_ID})
    out = []
    for r in rows:
        start, end = ts(r.get("startDate")), ts(r.get("endDate"))
        out.append({"processInstanceKey": r["processInstanceKey"], "elementId": r["elementId"],
                    "elementName": r.get("elementName"), "type": r["type"], "state": r["state"],
                    "startDate": r.get("startDate"), "endDate": r.get("endDate"),
                    "durationSec": round((end - start).total_seconds(), 2) if start and end else None})
    with open("kpi_element_instances.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]) if out else ["processInstanceKey"])
        w.writeheader()
        w.writerows(out)
    print(f"Đã ghi {len(out)} dòng vào kpi_element_instances.csv")
    lead = [o["durationSec"] for o in out if o["type"] == "PROCESS" and o["durationSec"] is not None]
    if lead:
        print(f"Lead time trung bình: {mean(lead):.1f} giây trên {len(lead)} instance đã xong")
