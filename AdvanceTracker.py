import streamlit as st
import pandas as pd
import os
from datetime import date

DATA_DIR = "data"
CERT_DIR = "certificates"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CERT_DIR, exist_ok=True)

MASTER_FILE = os.path.join(DATA_DIR, "master_inventory.xlsx")
LOG_FILE = os.path.join(DATA_DIR, "issued_log.xlsx")

# Initialize master inventory
if not os.path.exists(MASTER_FILE):
    df_master = pd.DataFrame(columns=["Instrument", "Total_Quantity", "Available_Quantity"])
    df_master.to_excel(MASTER_FILE, index=False)
else:
    df_master = pd.read_excel(MASTER_FILE)

# Initialize log
if not os.path.exists(LOG_FILE):
    df_log = pd.DataFrame(columns=["Name", "Instrument", "Quantity", "Issue_Date", "Return_Date", "Certificate"])
    df_log.to_excel(LOG_FILE, index=False)
else:
    df_log = pd.read_excel(LOG_FILE)

st.title("📦 Instrument Issue Tracker")

with st.form("issue_form"):
    name = st.text_input("Your Name")

    instrument_list = df_master["Instrument"].tolist()
    new_instrument = st.text_input("New Instrument (if not in list)")
    selected_instrument = st.selectbox("Select Instrument", options=[""] + instrument_list)

    instrument = new_instrument if new_instrument else selected_instrument
    if instrument == "":
        st.warning("Please select or enter an instrument.")
        st.stop()

    quantity = st.number_input("Quantity to Issue", min_value=1, step=1)
    issue_date = st.date_input("Issue Date", value=date.today())
    return_date = st.date_input("Proposed Return Date")

    cert_file = st.file_uploader("Upload Calibration Certificate (PDF)", type=["pdf"])

    submitted = st.form_submit_button("Submit")

    if submitted:
        # Add new instrument to master if not exists
        if instrument not in df_master["Instrument"].values:
            df_master = df_master.append({
                "Instrument": instrument,
                "Total_Quantity": quantity,
                "Available_Quantity": quantity
            }, ignore_index=True)

        # Check stock
        idx = df_master[df_master["Instrument"] == instrument].index[0]
        available = df_master.at[idx, "Available_Quantity"]
        if quantity > available:
            st.error(f"Only {available} available. Reduce quantity.")
        else:
            df_master.at[idx, "Available_Quantity"] -= quantity

            # Save certificate
            cert_path = ""
            if cert_file:
                cert_filename = f"{instrument}_{name}_{issue_date}.pdf".replace(" ", "_")
                cert_path = os.path.join(CERT_DIR, cert_filename)
                with open(cert_path, "wb") as f:
                    f.write(cert_file.getbuffer())

            # Append to log
            new_log = {
                "Name": name,
                "Instrument": instrument,
                "Quantity": quantity,
                "Issue_Date": issue_date,
                "Return_Date": return_date,
                "Certificate": cert_path
            }
            df_log = df_log.append(new_log, ignore_index=True)

            # Save all data
            df_master.to_excel(MASTER_FILE, index=False)
            df_log.to_excel(LOG_FILE, index=False)

            st.success(f"{quantity} {instrument}(s) issued to {name}.")

st.subheader("📊 Current Inventory")
st.dataframe(df_master)

st.subheader("🧾 Issued Log")
st.dataframe(df_log[["Name", "Instrument", "Quantity", "Issue_Date", "Return_Date"]])

st.subheader("📁 Calibration Certificates")
for i, row in df_log.iterrows():
    if row["Certificate"]:
        st.markdown(f"🔗 [{row['Instrument']} - {row['Name']}]({row['Certificate']})")
