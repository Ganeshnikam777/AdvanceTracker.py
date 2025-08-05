import streamlit as st
import pandas as pd
from datetime import date

# Static instrument list and issuer names
instrument_list = [
    "Lux Meter",
    "Ultrasonic Flow Meter",
    "Clamp On Meter",
    "Multimeter",
    "Egauge",
    "Temperature Logger",
    "Hobo Logger",
    "Distance Gun"
]

issuer_names = ["Vinay", "Pratik", "Ganesh", "Naif", "Murtadha", "Irshad", "Habib", "Rahim"]

# Initialize session state
if "form_data" not in st.session_state:
    st.session_state["form_data"] = []
if "edit_index" not in st.session_state:
    st.session_state["edit_index"] = None

st.title("📋 Instrument Issue Form")

# Entry Form
with st.form("issue_form"):
    if st.session_state["edit_index"] is not None:
        entry = st.session_state["form_data"][st.session_state["edit_index"]]
        default_name = entry["Issuer Name"]
        default_instr = entry["Instrument"]
        default_issue = entry["Issue Date"]
        default_return = entry["Tentative Return Date"]
    else:
        default_name = issuer_names[0]
        default_instr = instrument_list[0]
        default_issue = date.today()
        default_return = date.today()

    name = st.selectbox("Issuer Name", issuer_names, index=issuer_names.index(default_name))
    instrument = st.selectbox("Select Instrument", instrument_list, index=instrument_list.index(default_instr))
    issue_date = st.date_input("Issue Date", value=default_issue)
    return_date = st.date_input("Tentative Return Date", value=default_return)

    submit = st.form_submit_button("Save Entry")

    if submit:
        entry = {
            "Issuer Name": name,
            "Instrument": instrument,
            "Issue Date": issue_date,
            "Tentative Return Date": return_date
        }

        if st.session_state["edit_index"] is not None:
            st.session_state["form_data"][st.session_state["edit_index"]] = entry
            st.success("Entry updated.")
            st.session_state["edit_index"] = None
        else:
            st.session_state["form_data"].append(entry)
            st.success("Entry added successfully!")

# View and Download Table
if st.session_state["form_data"]:
    st.subheader("📦 Issued Instruments")
    df = pd.DataFrame(st.session_state["form_data"])
    st.dataframe(df)

    # Edit Entry
    st.write("### ✏️ Edit Entry")
    edit_row = st.number_input("Enter row number to edit (starting from 0)", min_value=0, max_value=len(df)-1, step=1)
    if st.button("Edit Selected Entry"):
        st.session_state["edit_index"] = edit_row
        st.experimental_rerun()

    # Download CSV and Reset
    st.write("### ⬇️ Download CSV")
    csv = df.to_csv(index=False).encode("utf-8")
    if st.download_button("Download Issued Instruments", data=csv, file_name="issued_instruments.csv", mime="text/csv"):
        st.session_state["form_data"] = []
        st.success("CSV downloaded and form has been reset.")
else:
    st.info("No entries yet.")

