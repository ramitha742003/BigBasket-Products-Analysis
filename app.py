import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# -------------------- Page Config --------------------
st.set_page_config(page_title="🛍️ BigBasket Products Analysis Dashboard", layout="wide")

# -------------------- Load Dataset --------------------
@st.cache_data
def load_data():
    df = pd.read_csv("C:/Users/ramit/OneDrive/Desktop/dash/BigBasket Products Analysis.csv")
    df.columns = df.columns.str.lower().str.strip()

    # Convert numeric columns
    for col in ['sale_price', 'market_price', 'rating']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Remove missing values
    df.dropna(subset=['sale_price', 'market_price'], inplace=True)

    # Add discount %
    df['discount_percent'] = ((df['market_price'] - df['sale_price']) / df['market_price']) * 100
    df['discount_percent'] = df['discount_percent'].replace([np.inf, -np.inf], np.nan).fillna(0)

    return df

df = load_data()

# -------------------- Dashboard Title --------------------
st.markdown("<h1 style='text-align:center;color:#2E86C1;'>🛍️ BigBasket Products Analysis Dashboard</h1>", unsafe_allow_html=True)

st.divider()

# -------------------- KPIs --------------------
col1, col2, col3, col4 = st.columns(4)

total_products = len(df)
avg_rating = round(df['rating'].mean(), 2)
avg_sale = round(df['sale_price'].mean(), 2)
avg_market = round(df['market_price'].mean(), 2)

col1.metric("📦 Total Products", total_products)
col2.metric("🏷️ Avg Sale Price", f"₹{avg_sale}")
col3.metric("🛒 Avg Market Price", f"₹{avg_market}")
col4.metric("⭐ Avg Rating", avg_rating)

st.divider()

# -------------------- Product Filters --------------------
st.subheader("🎯 Product Filter Selection")
product = st.selectbox("Select Product", sorted(df['product'].dropna().unique()))

# -------------------- Filtered Data --------------------
filtered_df = df[df['product'] == product]

# -------------------- Product Info --------------------
st.subheader("🧾 Selected Product Information in Table")
if not filtered_df.empty:
    st.dataframe(filtered_df)
else:
    st.warning("⚠️ No matching data found for the selected filters.")

# -------------------- Product-Level KPIs --------------------
if not filtered_df.empty:
    st.subheader("📈 Selected Product Details")
    prod = filtered_df.iloc[0]

    # --- KPI Metrics Row ---
    c1, c2, c3 = st.columns(3)
    c1.metric("🏷️ Sale Price", f"₹{prod['sale_price']:.2f}")
    c2.metric("🛒 Market Price", f"₹{prod['market_price']:.2f}")
    c3.metric("⭐ Rating", f"{prod['rating']:.2f}" if not np.isnan(prod['rating']) else "N/A")

    # --- Additional Product Info ---
    st.markdown("### 🧩 Additional Product Details")
    c5, c6 = st.columns(2)
    with c5:
        # st.markdown(f"**🏷️ Sale Price:** ₹{prod['sale_price']:.2f}")
        # st.markdown(f"**🛒 Market Price:** ₹{prod['market_price']:.2f}")
        # st.markdown(f"**⭐ Rating:** {prod['rating']:.2f}" if not np.isnan(prod['rating']) else "N/A")
        st.markdown(f"**📦 Category:** {prod.get('category', 'N/A')}")
        st.markdown(f"**📂 Sub-Category:** {prod.get('sub_category', 'N/A')}")
        st.markdown(f"**🏷️ Brand:** {prod.get('brand', 'N/A')}")
        st.markdown(f"**🔖 Type:** {prod.get('type', 'N/A')}")
    with c6:
        st.markdown("**📝 Description:**")
        st.info(str(prod.get('description', 'No description available.')))

else:
    st.warning("⚠️ Product details not found.")

# -------------------- Footer --------------------
st.write("---")
# st.caption("**© 2025** BigBasket Products Analysis Dashboard. All Rights Reserved.")
st.markdown("<p style='text-align:center;'><b>@ 2025</b> 🛍️ BigBasket Products Analysis Dashboard. All Rights Reserved.</p>", unsafe_allow_html=True)
