"""Job worker cho process xac_nhan_sv_demo.

Chạy:  python src/worker.py      (Ctrl+C để dừng)
"""
import time
from datetime import datetime

import camunda_api as api
from sample_db import tra_cuu

WORKER = "nhom16-worker"


def handle_tra_cuu(variables: dict) -> dict:
    mssv = str(variables.get("mssv", "")).strip()
    kq = tra_cuu(mssv)
    print(f"  tra-cuu-mssv: {mssv} -> {kq}")
    return kq


def handle_gui_ket_qua(variables: dict) -> dict:
    # Bản demo: chỉ ghi log. Task #9 sẽ sinh PDF và gửi email thật.
    so = f"XN-{datetime.now():%Y%m%d%H%M%S}"
    print(f"  gui-ket-qua: cấp giấy {so} cho {variables.get('hoTen')} ({variables.get('mssv')})")
    return {"soGiay": so, "ngayCap": datetime.now().isoformat(timespec="seconds")}


HANDLERS = {"tra-cuu-mssv": handle_tra_cuu, "gui-ket-qua": handle_gui_ket_qua}


def main() -> None:
    print(f"Worker '{WORKER}' đang chờ job tại {api.BASE_URL} ...")
    while True:
        for job_type, handler in HANDLERS.items():
            try:
                jobs = api.activate_jobs(job_type, WORKER, request_timeout_ms=5_000)
            except Exception as exc:  # engine chưa chạy, mất kết nối...
                print(f"Lỗi kết nối: {exc}. Thử lại sau 5 giây.")
                time.sleep(5)
                continue
            for job in jobs:
                key = job["jobKey"]
                print(f"[{job_type}] job {key} (instance {job['processInstanceKey']})")
                try:
                    api.complete_job(key, handler(job.get("variables", {})))
                except Exception as exc:
                    api.fail_job(key, max(job.get("retries", 1) - 1, 0), str(exc))
                    print(f"  thất bại: {exc}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Đã dừng worker.")
