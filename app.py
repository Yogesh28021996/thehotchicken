import streamlit as st
from datetime import datetime
import random
import pandas as pd

# ======================================
# ✅ PUBLIC GOOGLE SHEET CSV URL
# ======================================
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR-uzwsqbnhmyb8IwSydFkFlEkZj0gpdBXsn_ZyMoxiJTePIvYGEU60PPqJQte_o8HjVpX3jPBAn1PE/pub?output=csv"

# ======================================
# ✅ MENU ITEMS
# ======================================
MENU = {
    "Fried chicken wings (3pc/5pc)": [80, 130],
    "Fried chicken lollipop (2pc/5pc)": [100, 180],
    "Fried chicken strips (3pc/6pc)": [90, 160],
    "Crispy chicken popcorn (medium/large)": [70, 120],
    "Jumbo wings (2pc/4pc)": [120, 200],
    "Mini chicken crisper": 79,
    "Classic zinger burger": 110,
    "Chicken cheese burger": 130,
    "Mexican chicken burger": 130,
    "BBQ chicken burger": 150,
    "French Fries": 70,
    "Peri Peri Fries": 80,
    "Fried Mushroom": 100,
    "Fresh Garden Sandwich": 70,
    "Veg Cheese Sandwich": 70,
    "Fried Mushroom Sandwich": 110,
    "Creamy Mushroom Sandwich": 140,
    "Classic Chicken Sandwich": 100,
    "Chicken Cheese Sandwich": 110,
    "Hot Garlic Chicken Sandwich": 130,
    "Mint Lime Mojito": 59,
    "Virgin Lychee Mojito": 79,
    "Green Apple Mojito": 79,
    "Frozen Strawberry Mojito": 79,
    "Blue Sea Mojito": 99,
    "Pina Colada": 99,
    "Bubble Gum Mojito": 99,
    "Hot garlic wings (4pc)": 120,
    "Nashville hot chicken strips (4pc)": 140,
    "Creamy Mushroom": 140,
    "Mac & Cheese": 99,
    "Buffalo Wings": 140,
    "Mac & Cheese with Chicken & Fries": 179,
    "Fish & Chips with Spicy Dip": 179,
    "Lays with Fiery Chicken": 179,
    "6 pc hot and crispy bucket chicken": 179,
    "12 pc hot and crispy bucket chicken": 299,
    "The Hot Chick Feast": 229,
    "Hot Chick Dinner Platter": 299,
    "Spicy Main Chick Burger": 150,
    "Cheesy Side Chick Burger": 150,
    "Sizzlin' Hot Chick Burger": 150,
    "The Flirtini Chick (Mojito)": 99,
    "Thick Thighs": 200,
    "The Chick Stack": 140,
    "Chicks 'N' Fries": 100,
    "Garlic Tease": 150,
}

# ======================================
# ✅ STREAMLIT UI
# ======================================
st.title("🔥 The Hot Chick - Order Now (Public Sheet Version)")

if "cart" not in st.session_state:
    st.session_state.cart = []

item = st.selectbox("Select Item", list(MENU.keys()))
price = MENU[item]

if isinstance(price, list):
    portion = st.radio("Select Portion", [f"Option {i+1}: ₹{p}" for i, p in enumerate(price)])
    portion_index = int(portion.split()[1].replace(":", "")) - 1
    unit_price = price[portion_index]
    portion_note = f"(Portion {portion_index+1})"
else:
    unit_price = price
    portion_note = ""

qty = st.selectbox("Quantity", list(range(1, 11)))
item_total = qty * unit_price

st.write(f"### 🧾 Item Total: ₹{item_total}")

if st.button("Add Item"):
    st.session_state.cart.append({
        "item": item,
        "portion_note": portion_note,
        "qty": qty,
        "unit_price": unit_price,
        "item_total": item_total
    })
    st.success(f"✅ Added {qty} x {item} {portion_note}")

if st.session_state.cart:
    st.write("## 🛒 Current Order")
    total_order_amount = sum(i["item_total"] for i in st.session_state.cart)
    for idx, i in enumerate(st.session_state.cart, 1):
        st.write(f"{idx}. {i['qty']} x {i['item']} {i['portion_note']} = ₹{i['item_total']}")
    st.write(f"### 💵 Total: ₹{total_order_amount}")

payment_method = st.selectbox("Payment Method", ["Cash", "UPI"])

if st.button("Create Order"):
    if not st.session_state.cart:
        st.warning("⚠️ Add at least one item!")
    else:
        total_order_amount = sum(i["item_total"] for i in st.session_state.cart)
        now = datetime.now()
        order_id = f"HC-{now.strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"
        order_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        items_summary = "; ".join([f"{i['qty']} x {i['item']} {i['portion_note']}" for i in st.session_state.cart])

        # ⚠️ You cannot append to a public sheet directly — so we simulate by showing details
        st.write("✅ **Simulated: Order would be saved here**")
        st.write(f"**Order ID:** `{order_id}`")
        st.write(f"**Date & Time:** {order_datetime}")
        st.write(f"**Items:** {items_summary}")
        st.write(f"**Total:** ₹{total_order_amount}")
        st.write(f"**Payment Method:** {payment_method}")

        st.session_state.cart = []

# View existing orders
st.write("## 📄 Existing Orders (Read Only)")

try:
    df = pd.read_csv(SHEET_CSV_URL)
    st.dataframe(df)
except Exception as e:
    st.error(f"❌ Could not read public sheet: {e}")
