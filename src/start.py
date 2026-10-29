"""Khởi tạo process instance.

  python src/start.py 24020001 "Nguyễn Văn An" "Bổ sung hồ sơ học bổng"
  python src/start.py --batch 10      # tạo 10 yêu cầu ngẫu nhiên để test
"""
import random
import sys

import camunda_api as api
from sample_db import SINH_VIEN

PROCESS_ID = "xac_nhan_sv_demo"
MUC_DICH = ["Hồ sơ học bổng", "Vay vốn ngân hàng", "Thực tập", "Miễn giảm nghĩa vụ quân sự"]


def tao(mssv: str, ho_ten: str, muc_dich: str) -> None:
    r = api.start_instance(PROCESS_ID, {"mssv": mssv, "hoTen": ho_ten, "mucDich": muc_dich})
    print(f"Đã tạo instance {r['processInstanceKey']} cho {mssv}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["--batch"]:
        n = int(args[1]) if len(args) > 1 else 10
        pool = list(SINH_VIEN) + ["99999999"]  # có cả MSSV không tồn tại
        for _ in range(n):
            mssv = random.choice(pool)
            tao(mssv, SINH_VIEN.get(mssv, {}).get("hoTen", "Không rõ"), random.choice(MUC_DICH))
    elif len(args) >= 2:
        tao(args[0], args[1], args[2] if len(args) > 2 else MUC_DICH[0])
    else:
        print(__doc__)
