

import streamlit as st

GST_RATE = 0.18

def calc_premiums(sum_assured, rate):
    premium_inc_gst = (sum_assured * rate) / 100000
    premium_ex_gst = premium_inc_gst / (1 + GST_RATE)
    return premium_ex_gst, premium_inc_gst

def format_inr(x):
    return f"₹{x:,.2f}"

st.title("GTL Premium Calculator")

sum_assured = st.number_input("Sum Assured", min_value=0.0, step=1000.0)

rate = 650.0  # FIXED RATE ONLY

if st.button("Calculate"):
    ex, inc = calc_premiums(sum_assured, rate)

    st.success("Result")

    st.write("Premium (Ex GST):", format_inr(ex))
    st.write("Premium (Inc GST):", format_inr(inc))
