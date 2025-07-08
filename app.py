import streamlit as st
from datetime import datetime
import random
import requests
import pandas as pd

# ================================
# ✅ CONFIG
# ================================
# 📌 Public Google Sheet CSV export link
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR-uzwsqbnhmyb8IwSydFkFlEkZj0gpdBXsn_ZyMoxiJTePIvYGEU60PPqJQte_o8HjVpX3jPBAn1PE/pub?output=csv"

# 📌 Google Form POST link — replace with your actual Form POST link
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/REPLACE_WITH_YOUR_FORM_ID/formResponse"

# 📌 Form field entry IDs — replace with your actual IDs from Inspect Element
FORM_FIELDS = {
    "order_id": "entry.YOUR_ID_1",
    "datetime": "entry.YOUR_ID_2",
    "items": "entry.YOUR_ID_3",
    "total": "entry.YOUR_ID_4",
    "payment": "entry.YOUR_ID_5",
}

# ================================
# ✅ MENU
# ================================
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

# ================================
# ✅ UI
# ================================
st.title("🔥 The Hot Chick — Order Now!")

# Cart state
if "cart" not in st.session_state:
    st.session_state.cart = []

# Select item
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

# Cart
if st.session_state.cart:
    st.write("## 🛒 Current Order Summary")
    total_order_amount = sum(i["item_total"] for i in st.session_state.cart)
    for idx, i in enumerate(st.session_state.cart, 1):
        st.write(f"{idx}. {i['qty']} x {i['item']} {i['portion_note']} = ₹{i['item_total']}")
    st.write(f"### 💵 Current Total: ₹{total_order_amount}")

payment_method = st.selectbox("Payment Method", ["Cash", "UPI"])

if st.button("Place Order"):
    if not st.session_state.cart:
        st.warning("⚠️ Add at least one item!")
    else:
        now = datetime.now()
        order_id = f"HC-{now.strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"
        order_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        items_summary = "; ".join([f"{i['qty']} x {i['item']} {i['portion_note']}" for i in st.session_state.cart])
        total_amount = sum(i["item_total"] for i in st.session_state.cart)

        payload = {
            FORM_FIELDS["order_id"]: order_id,
            FORM_FIELDS["datetime"]: order_datetime,
            FORM_FIELDS["items"]: items_summary,
            FORM_FIELDS["total"]: total_amount,
            FORM_FIELDS["payment"]: payment_method,
        }

        response = requests.post(GOOGLE_FORM_URL, data=payload)

        if response.status_code == 200 or response.status_code == 302:
            st.success(f"🎉 Order submitted! **Order ID:** `{order_id}`")
            st.session_state.cart = []
        else:
            st.error("❌ Failed to submit order. Please check Form URL and entries.")

# Show all orders
st.write("## 📄 All Orders")
df = pd.read_csv(CSV_URL)
st.dataframe(df)
