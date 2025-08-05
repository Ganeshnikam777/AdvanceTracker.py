
import streamlit as st
import pandas as pd
from datetime import date

# Static instrument list
instrument_list = [
    "Lux Meter", "Fluke Power Analyzer",
    "Ultrasonic Flow Meter",
    "Clamp On Meter",
    "Multimeter",
    "Egauge",
    "Temperature Logger",
    "Hobo Logger",
    "Distance Gun"
]

# Set up session state for form data
if "form_data" not in st.session_state:
    st.session_state["form_data"] = []

st.title("📋 Instrument Issue Form")

# Issue Form
with st.form("issue_form"):
    name = st.text_input("Issuer Name")
    instrument = st.selectbox("Select Instrument", instrument_list)
    issue_date = st.date_input("Issue Date", value=date.today())
    return_date = st.date_input("Tentative Return Date")
    Quantity = st.number_input("Instrumrnt Quantity")

    submitted = st.form_submit_button("Add Entry")
    if submitted:
        entry = {
            "Issuer Name": name,
            "Instrument": instrument,
            "Issue Date": issue_date,
            "Tentative Return Date": return_date
        }
        st.session_state.form_data.append(entry)
        st.success("Entry added successfully!")

# Show entries
if st.session_state.form_data:
    st.subheader("📦 Issued Instruments")
    df = pd.DataFrame(st.session_state.form_data)
    st.dataframe(df)

    # Download CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", data=csv, file_name="issued_instruments.csv", mime="text/csv")
else:
    st.info("No entries yet.")


