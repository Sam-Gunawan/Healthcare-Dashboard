import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Health First", layout="centered")

st.markdown("# Health First Database")

def init_search_value(filters: list[str]):
    """Returns an uppercase string of the value typed into the search bar and the filter chosen. Filters param is a list of attributes option"""
    col1, col2 = st.columns([2, 5])

    filter = col1.selectbox("Search by", filters)

    # any value written in search bar will be given to search_value variable as a String
    search_value = col2.text_input(f"Enter {filter.lower()} to search: ", value="")

    return [search_value.upper(), filter]

def search_result(df, search_value, filter, attr_id, name_attr=""):
    """Returns the dataframe for the search result. Needs the df selected, filter selected, the label for attribute's id, and [optional] the label for attribute's name"""
    # convert names and search value to uppercase to account for different letter casings when searching
    df[name_attr] = df[name_attr].astype(str).str.upper()
    
    if filter == attr_id:
        mask = df[attr_id].str.contains(search_value)
    else:
        mask = df[f'{filter}'].str.startswith(search_value)

    df_search = df[mask]

    if name_attr:
        df_search[name_attr] = df_search[name_attr].astype(str).str.title()
    
    return df_search

def display_search_result(chosen_table, df_search):
    if df_search.empty:
        st.markdown(f"### No {chosen_table} found")
    elif search_value:
        st.write(df_search)

chosen_table = option_menu(None, ["Patient", "Doctor",  "Appointment"], 
    icons=['person-wheelchair', 'bandaid', "clipboard-heart"], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "nav-link": {"opacity": 0.6},
        "nav-link-selected": {"font-weight": "initial", "opacity": 1}
    }
)

# dataframe from chosen table
# NOTE: CSV filename MUST BE in format of "{option_title}s.csv", e.g. patients has Patient when displayed in UI, so csv filename should be patients.csv
try:
    df = pd.read_csv(f".\dataset\{chosen_table}s.csv", sep=";")
except:
    st.write("No data found")

# st.write(df)

if chosen_table == "Patient":
    search_value, filter = init_search_value(["Patient ID", "Name", "Contact", "Email"])
    attr_id, attr_name = 'Patient ID', 'Name'
elif chosen_table == "Doctor":
    search_value, filter = init_search_value(["Doctor ID", "Name", "Specialization", "Office"])
    attr_id, attr_name = 'Doctor ID', 'Name'

    # # convert names and search value to uppercase to account for different letter casings when searching
    # df['Name'] = df['Name'].astype(str).str.upper()

    # if filter == "Patient ID":
    #     mask = df['Patient ID'].str.contains(search_value)
    # else:
    #     mask = df[f'{filter}'].str.startswith(search_value)

    # df_search = df[mask]

    # df_search['Name'] = df_search['Name'].astype(str).str.title()

    # if df_search.empty:
    #     st.markdown("### No patient found")

    # elif search_value:
    #     st.write(df_search)

    # NOTE keep the above commented code for reference first, delete later.

df_search = search_result(df, search_value, filter, attr_id, attr_name)
display_search_result(chosen_table, df_search)