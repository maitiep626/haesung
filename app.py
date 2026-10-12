import pandas as pd
import plotly.express as px
import streamlit as st

# Cấu hình giao diện trang web
st.set_page_config(
    page_title="Báo cáo Vận hành Máy móc", page_icon="📊", layout="wide"
)

st.title("📊 Dashboard Tổng Hợp Vận Hành Máy Móc")
st.markdown("Hệ thống giám sát công suất, nhiệt độ và sản lượng theo thời gian.")

# Khu vực tải file lên (hỗ trợ cả .xlsx và .csv)
uploaded_file = st.file_uploader(
    "Chọn file dữ liệu của bạn (.xlsx hoặc .csv)", type=["xlsx", "xls", "csv"]
)

if uploaded_file is not None:
  # Đọc file dựa vào phần mở rộng
  if uploaded_file.name.endswith(".csv"):
    df = pd.read_csv(uploaded_file)
  else:
    df = pd.read_excel(uploaded_file)

  st.success("Tải và đọc file thành công!")

  # 1. Các thẻ thông số tổng quan (Metrics)
  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(
        label="📦 Tổng sản phẩm OK", value=f"{df['So_luong_OK'].sum():,}"
    )
  with col2:
    st.metric(
        label="⚠️ Tổng sản phẩm lỗi (NG)", value=f"{df['So_luong_NG'].sum():,}"
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

  if selected_may:
    df_filtered = df[df["Ma_may"].isin(selected_may)]
  else:
    df_filtered = df

  # 2. Khu vực Biểu đồ tương tác cao cấp bằng Plotly
  col_left, col_right = st.columns(2)

  with col_left:
    st.subheader("📈 Biểu đồ Công suất theo thời gian")
    if not df_filtered.empty:
      fig_power = px.line(
          df_filtered,
          x="Thoi_gian",
          y="Cong_suat_kW",
          color="Ma_may",
          markers=True,
          labels={
              "Thoi_gian": "Thời gian",
              "Cong_suat_kW": "Công suất (kW)",
              "Ma_may": "Mã máy",
          },
      )
      fig_power.update_layout(
          margin=dict(l=20, r=20, t=30, b=20), hovermode="x unified"
      )
      st.plotly_chart(fig_power, use_container_width=True)

  with col_right:
    st.subheader("🌡️ Biểu đồ Nhiệt độ theo thời gian")
    if not df_filtered.empty:
      fig_temp = px.line(
          df_filtered,
          x="Thoi_gian",
          y="Nhiet_do_C",
          color="Ma_may",
          markers=True,
          labels={
              "Thoi_gian": "Thời gian",
              "Nhiet_do_C": "Nhiệt độ (°C)",
              "Ma_may": "Mã máy",
          },
      )
      fig_temp.update_layout(
          margin=dict(l=20, r=20, t=30, b=20), hovermode="x unified"
      )
      st.plotly_chart(fig_temp, use_container_width=True)

  # 3. Bảng chi tiết dữ liệu
  st.subheader("📋 Bảng chi tiết dữ liệu vận hành")
  st.dataframe(df_filtered, use_container_width=True)

else:
  st.info("👈 Hãy tải file mẫu (.csv hoặc .xlsx) lên để hiển thị biểu đồ.")