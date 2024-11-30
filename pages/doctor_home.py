import streamlit as st


def app(): 

    st.title('Post-Appointment Form')

    patient_ID = st.text_input('Appointment ID')

    doctor_name = st.text_input("Doctor Name")

    status = st.selectbox('Pending/Completed', ['Pending', 'Completed'])

    symptoms = st.text_input('Symptoms', disabled=(status == 'Pending'))

    diagnose = st.text_input('Diagnose', disabled=(status == 'Pending')) 

    treatment =  st.text_input('Treatment', disabled=(status == 'Pending'))

    if st.button('Save'):
        if status == "Pending":
            st.warning("Cannot save summary while the status is Pending!")
        else:
            st.success('Successfully Saved')

    



app()