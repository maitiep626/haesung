import os
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Báo cáo Vận hành Máy móc", page_icon="📊", layout="wide"
)

DATA_FILE = "dulieu_chinh.xlsx"

st.title("📊 Dashboard Tổng Hợp Vận Hành Máy Móc")

# --- THANH BÊN (SIDEBAR): KHU VỰC DÀNH CHO ADMIN ---
st.sidebar.header("🔐 Quản trị hệ thống (Admin)")
password = st.sidebar.text_input("Nhập mật khẩu Admin:", type="password")

# Đặt mật khẩu đơn giản ở đây là 'admin123' (bạn có thể đổi tùy ý)
if password == "admin123":
  st.sidebar.success("Đã đăng nhập quyền Admin!")
  uploaded_file = st.sidebar.file_uploader(
      "Tải lên file dữ liệu mới (.xlsx/.csv)", type=["xlsx", "xls", "csv"]
  )

  if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
      df_new = pd.read_csv(uploaded_file)
    else:
      df_new = pd.read_excel(uploaded_file)

    # Lưu đè file vào hệ thống chung
    df_new.to_excel(DATA_FILE, index=False)
    st.sidebar.success("Cập nhật dữ liệu thành công!")
elif password != "":
  st.sidebar.error("Sai mật khẩu!")

# --- KHU VỰC HIỂN THỊ CHO TẤT CẢ MỌI NGƯỜI (VIEWER) ---
if os.path.exists(DATA_FILE):
  df = pd.read_excel(DATA_FILE)

  # 1. Các thẻ thông số tổng quan (Metrics)
  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(
        label="📦 Tổng sản phẩm OK", value=f"{df['So_luong_OK'].sum():,}"
    )
  with col2:
    st.metric(
        label="⚠️ Tổng sản phẩm lỗi (NG)",
        value=f"{df['So_luong_NG'].sum():,}",
    )
  with col3:
    st.metric(
        label="🌡️ Nhiệt độ trung bình",
        value=f"{df['Nhiet_do_C'].mean():.1f} °C",
    )
  with col4:
    st.metric(
        label="⚡ Công suất trung bình",
        value=f"{df['Cong_suat_kW'].mean():.1f} kW",
    )

  st.divider()

  # Bộ lọc tùy chọn xem theo mã máy
  danh_sach_may = df["Ma_may"].unique().tolist()
  selected_may = st.multiselect(
      "🔍 Lọc hiển thị theo mã máy:",
      options=danh_sach_may,
      default=danh_sach_may,
  )

  df_filtered = (
      df[df["Ma_may"].isin(selected_may)] if selected_may else df
  )

  # 2. Biểu đồ tương tác
  col_left, col_right = st.columns(2)
  with col_left:
    st.subheader("📈 Biểu đồ Công suất theo thời gian")
    fig_power = px.line(
        df_filtered,
        x="Thoi_gian",
        y="Cong_suat_kW",
        color="Ma_may",
        markers=True,
    )
    fig_power.update_layout(hovermode="x unified")
    st.plotly_chart(fig_power, use_container_width=True)

  with col_right:
    st.subheader("🌡️ Biểu đồ Nhiệt độ theo thời gian")
    fig_temp = px.line(
        df_filtered,
        x="Thoi_gian",
        y="Nhiet_do_C",
        color="Ma_may",
        markers=True,
    )
    fig_temp.update_layout(hovermode="x unified")
    st.plotly_chart(fig_temp, use_container_width=True)

  # 3. Bảng chi tiết
  st.subheader("📋 Bảng chi tiết dữ liệu vận hành")
  st.dataframe(df_filtered, use_container_width=True)

else:
  st.warning(
      "⚠️ Hệ thống chưa có dữ liệu. Vui lòng nhập mật khẩu Admin ở thanh bên"
      " trái để tải file lên lần đầu."
  )