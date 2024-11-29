import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Health First", layout="centered")

st.markdown("# Health First Database")

# dataframe from patients.csv
df = pd.read_csv(".\dataset\patients.csv", sep=";")

# st.write(df)

option_menu(None, ["Patient", "Doctor",  "Appointment"], 
    icons=['person-wheelchair', 'bandaid', "clipboard-heart"], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        # "container": {"padding": "0!important", "background-color": "#fafafa"},
        # "icon": {"color": "orange", "font-size": "25px"},
        "nav-link": {"opacity": 0.6},
        "nav-link-selected": {"font-weight": "initial", "opacity": 1}
    }
)

col1, col2 = st.columns([2, 5])

filter = col1.selectbox("Filters", ["Patient ID", "Name", "Phone Number", "Email"])

# any value written in search bar will be given to search_bar variable as a String
search_bar = col2.text_input(f"Enter {filter.lower()} to search: ", value="")

# convert names and search value to uppercase to account for different letter casings when searching
df['name'] = df['name'].astype(str).str.upper()
search_bar = search_bar.upper()


mask = df['patient_id'].str.contains(search_bar) | df['name'].str.startswith(search_bar) | df['email'].str.startswith(search_bar) | df['contact'].str.startswith(search_bar)
df_search = df[mask]

df_search['name'] = df_search['name'].astype(str).str.title()

if df_search.empty:
    st.markdown("### No patient found")

elif search_bar:
    st.write(df_search)