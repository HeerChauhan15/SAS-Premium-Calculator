import streamlit as st

GST_RATE = 0.18


def calc_premiums(sum_assured, rate):
    premium_inc_gst = (sum_assured * rate) / 100000
    premium_ex_gst = premium_inc_gst / (1 + GST_RATE)
    return premium_ex_gst, premium_inc_gst


def format_inr(x):
    return f"₹{x:,.2f}"


st.title("SAS Premium Calculator")

# INPUTS
sum_assured = st.number_input("Sum Assured", min_value=0.0, step=1000.0)
age = st.number_input("Age", min_value=0, step=1)
loan_amount = st.number_input("Loan Amount", min_value=0.0, step=1000.0)

# FIXED RATE
rate = 650.0

st.info("Rate is fixed: 650 (GST inclusive)")

# BUTTON
if st.button("Calculate"):
    ex, inc = calc_premiums(sum_assured, rate)

    st.success("Calculation Completed")

    st.write("### Details Entered")
    st.write("Age:", age)
    st.write("Loan Amount:", format_inr(loan_amount))
    st.write("Sum Assured:", format_inr(sum_assured))

    st.write("### Premium Result")
    st.write("Premium (Ex GST):", format_inr(ex))
    st.write("Premium (Inc GST):", format_inr(inc))


