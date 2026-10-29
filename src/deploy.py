"""Deploy BPMN + form của bản demo lên Camunda.  Chạy: python src/deploy.py"""
from pathlib import Path

import camunda_api as api

ROOT = Path(__file__).resolve().parent.parent
FILES = [ROOT / "bpmn/demo/xac_nhan_sv_demo.bpmn", ROOT / "forms/duyet-yeu-cau.form"]

if __name__ == "__main__":
    print("Kết nối:", api.BASE_URL, "- broker:", len(api.topology().get("brokers", [])))
    result = api.deploy(FILES)
    print("Deployment key:", result["deploymentKey"])
    for d in result["deployments"]:
        print(" -", d)
