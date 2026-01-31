import streamlit as st
import json
import os
import pandas as pd

FILE = "data.json"


# -----------------------
# DB functions
# -----------------------
def load_data():
    if not os.path.exists(FILE):
        return []

    with open(FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


# -----------------------
# UI
# -----------------------
st.set_page_config(page_title="Data Entry App", layout="centered")

st.title("📝 Data Entry Form")

with st.form("entry_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=120, step=1)

    submit = st.form_submit_button("Submit")

    if submit:
        if name:
            data = load_data()

            new_row = {
                "Name": name,
                "Age": age
            }

            data.append(new_row)
            save_data(data)

            st.success("Saved Successfully ✅")
        else:
            st.error("Name required")


# -----------------------
# Show table
# -----------------------
st.divider()
st.subheader("Saved Records")

records = load_data()

if records:
    df = pd.DataFrame(records)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No records yet")
