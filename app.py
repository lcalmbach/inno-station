import streamlit as st
import json
from datetime import datetime
import time
import pandas as pd


# Funktion, um Vorschläge zu laden und anzuzeigen
def load_and_display_suggestions():
    list_of_dicts = []
    try:
        with open('suggestions.json', 'r') as f:
            lines = f.readlines()
            for line in lines:
                entry = json.loads(line)
                if not entry.get("is_private"):
                    list_of_dicts.append(entry)
            df = pd.DataFrame(list_of_dicts)
            st.dataframe(df)
    except FileNotFoundError:
        st.write("Noch keine Vorschläge vorhanden.")


if "mode" not in st.session_state:
    st.session_state.mode = 0

# Title of the page
st.image('./splash.png', width=800)
st.title("StatA InnoStation")
# Anzeige der eingegangenen Vorschläge
if st.session_state.mode == 0:
    load_and_display_suggestions()
    if st.button("Neuer Vorschlag"):
        st.session_state.mode = 1
        st.experimental_rerun()
else:
    with st.form(key='my_form'):
        # Employee selection dropdown
        employee_list = {
            1: "Fritz Muster",
            2: "Clare Matter",
            3: "Pratt Pitt",
            4: "Joan Doe",
        }
        employee_selection = st.selectbox("Mitarbeiter", options=list(employee_list.values()))

        # Title for the suggestion
        suggestion_title = st.text_input("Titel des Vorschlags", help="Titel für deinen Vorschlag.")
        
        problem = st.text_area("Problem", help="Detaillierte Beschreibung Zustands, der verbessert werden soll.")

        # Suggestion text area
        suggestion = st.text_area("Vorschlag", help="Detaillierte Beschreibung des Vorschlags")
        
        # Desired Effect text area
        desired_effect = st.text_area("Erwünschte Wirkung", help="Detaillierte Beschreibung was der Vorschlag bewirken soll.")
        
        # Private checkbox
        is_private = st.checkbox("privat", help="Als privat markierte Einträge werden nicht öffentlich angezeigt in der Liste der eingegangenen Vorschläge.")
        
        # Submit button
        submit_button = st.form_submit_button(label='Absenden')
        if submit_button:
            if employee_selection and suggestion_title and suggestion and desired_effect:
                # Save data to a JSON file with a timestamp
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data = {
                    'employee': employee_selection,
                    'suggestion_title': suggestion_title,
                    'problem': problem,
                    'suggestion': suggestion,
                    'desired_effect': desired_effect,
                    'is_private': is_private,
                    'timestamp': timestamp
                }

                with open('suggestions.json', 'a') as f:
                    json.dump(data, f)
                    f.write('\n')

                st.success("Vielen Dank für deinen Vorschlag!")
                time.sleep(2)
                st.session_state.mode = 0
                st.experimental_rerun()
            else:
                st.error("Bitte fülle alle Felder aus.")


