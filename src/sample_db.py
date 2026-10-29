"""CSDL sinh viên giả lập (thay cho hệ thống quản lý đào tạo thật)."""
SINH_VIEN = {
    "24020001": {"hoTen": "Nguyễn Văn An", "trangThai": "Đang học"},
    "24020002": {"hoTen": "Trần Thị Bình", "trangThai": "Đang học"},
    "23020003": {"hoTen": "Lê Minh Châu", "trangThai": "Bảo lưu"},
    "22020004": {"hoTen": "Phạm Quốc Dũng", "trangThai": "Thôi học"},
}
HOP_LE = {"Đang học"}


def tra_cuu(mssv: str) -> dict:
    sv = SINH_VIEN.get(mssv)
    if sv is None:
        return {"hopLe": False, "trangThaiHocTap": "Không tìm thấy MSSV"}
    return {"hopLe": sv["trangThai"] in HOP_LE, "trangThaiHocTap": sv["trangThai"]}
