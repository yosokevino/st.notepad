import streamlit as st
import pandas as pd
import time
import datetime
from st_aggrid import AgGrid

users = ('Mollyrose', 'Kevin')

st.title("The Schaffner Family Notepad App")

if 'sesion_submit' not in st.session_state:
    st.session_state['sesion_submit'] = 1
    
if 'authentication' not in st.session_state:
    st.session_state['authentication'] = False
    
if 'username' not in st.session_state:
    st.session_state['username'] = ''
    
if 'password' not in st.session_state:
    st.session_state['password'] = ''

# save annotated results after every button click
def save_results(results, button_press, time, note, category):
    results.at[button_press, 'note'] = note
    results.at[button_press, 'category'] = str(category)
    results.at[button_press, 'time'] = str(datetime.datetime.now())[:-7]
    results.to_csv('family_notes.csv', index=None)
    return None

# load spreadsheet with data to be annotated
@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_csv('family_notes.csv')
    return df

results = load_data()

# track which row of results_df to read
with open("progress.txt", "r") as f:
        button_press = f.readline()  # starts as a string
        button_press = 0 if button_press == "" else int(button_press)  # check if its an empty string, otherwise should 
        
#login

if st.session_state['authentication'] == False:
    
    st.session_state['username'] = st.text_input("Enter Your Username:",value='')
    st.session_state['password'] = st.text_input("Enter Your Password", value='', type='password')
    
if (st.session_state['username'] == 'Kevin') & (st.session_state['password'] == 'admin'):

    with st.form("my_form", clear_on_submit=True):

        category = st.selectbox("Select the Note Category:",
                           ('Oliver', 'Grocery', 'House', 'Other'))

        note = st.text_area("Enter Your Note Here:")

        if (len(note) >0) & (st.form_submit_button("Save Note")):
            button_press += 1
            st.session_state['sesion_submit'] += 1
            save_results(results, button_press, time, note, category)
            st.success("Note Saved!")

        elif (len(note) <=0) & (st.session_state['sesion_submit'] > 0):
            st.error("No Text Entered!")
            time.sleep(1)
            st.session_state['sesion_submit'] = 1

    AgGrid(results.sort_values('time', ascending = False, inplace = False),
           editable=True,
           fit_columns_on_grid_load=True,
           theme = 'dark')

    
# track which row of results_df to write to
with open("progress.txt", "w") as f:
        f.truncate()
        f.write(f"{button_press}")
