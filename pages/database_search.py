import streamlit as st
import pandas as pd

st.set_page_config(page_title="Health First", layout="centered")

st.markdown("# Health First Database")

# any value written in search bar will be given to search_bar variable as a String
search_bar = st.text_input("Enter name to search: ", value="")

# dataframe from patients.csv
df = pd.read_csv(".\dataset\patients.csv", sep=";")

# st.write(df)

# convert names and search value to uppercase to account for different letter casings when searching
df['name'] = df['name'].astype(str).str.upper()
search_bar = search_bar.upper()

# st.selectbox("Filters", ["Patient ID", "Name", "Phone Number", "Email"])

mask = df['patient_id'].str.contains(search_bar) | df['name'].str.startswith(search_bar) | df['email'].str.startswith(search_bar) | df['contact'].str.startswith(search_bar)
df_search = df[mask]

df_search['name'] = df_search['name'].astype(str).str.title()

if df_search.empty:
    st.markdown("### gaada bro")
else:
    st.write(df_search)