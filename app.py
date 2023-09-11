import streamlit as st
import pandas as pd
import random
from PIL import Image

image = Image.open('born_to_be.png')

st.set_page_config(page_title="Procvičování otázek")
st.image(image)

# Read in data from the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit", "/export?format=csv")
    return pd.read_csv(csv_url)

# Načtení dat z Google Sheetu namísto lokálního CSV souboru
data = load_data(st.secrets["public_gsheets_url"])

# Vytvoření seznamu oblastí před zamícháním dat
all_areas = data['Oblast'].unique().tolist()

# Zamíchání dat
data = data.sample(frac=1).reset_index(drop=True)

# Funkce pro náhodný výběr otázky z vybraných oblastí
def select_random_question(selected_areas):
    question_row = data[data['Oblast'].isin(selected_areas)].sample(1).iloc[0]
    
    # Uložení správné odpovědi
    correct_answer = question_row[f"Odpověď {question_row['Správná odpověď'].upper()}"]
    
    # Zamíchání odpovědí
    answers = [question_row[f"Odpověď {label}"] for label in ['A', 'B', 'C']]
    random.shuffle(answers)
    
    return question_row, answers, correct_answer

# Hlavní funkce aplikace
def main():
    st.title('Procvičování otázek')

    # Výběr oblastí pomocí zaškrtávacích políček
    with st.expander('Výběr oblastí'):
        selected_areas = [area for area in all_areas if st.checkbox(area, value=True)]
        if st.button("Načíst otázky z vybraných oblastí", use_container_width=True):
            st.session_state.question_data = select_random_question(selected_areas)
            st.session_state.show_feedback = False
            st.experimental_rerun()

    # Náhodný výběr otázky (pokud ještě nebyla vybrána)
    if 'question_data' not in st.session_state:
        st.session_state.question_data = select_random_question(selected_areas)
        st.session_state.show_feedback = False

    question_row, answers, correct_answer = st.session_state.question_data
    
    st.write(f"Otázka č. {question_row['Číslo otázky']} ({question_row['Oblast']} | {question_row['Podoblast']}):")
    st.markdown(f"### {question_row['Otázka']}", unsafe_allow_html=True)
    st.write("---")  # Horizontální čára

    # Zobrazení odpovědí jako tlačítek s plnou šířkou a textem zarovnaným vlevo
    for answer_text in answers:
        if st.button(answer_text, use_container_width=True):
            st.session_state.selected_answer = answer_text
            st.session_state.show_feedback = True

    # Zobrazení zpětné vazby
    if st.session_state.show_feedback:
        st.write("---")
        # Zobrazení zdrojů, pokud jsou k dispozici
        if pd.notnull(question_row['Zdroje']):
            st.markdown(f"**Zdroje:** {question_row['Zdroje']}")
          
        if st.session_state.selected_answer == correct_answer:
            st.success('Správně!')
            
            if st.button("Další otázka"):
                st.session_state.question_data = select_random_question(selected_areas)
                st.session_state.show_feedback = False
                del st.session_state.selected_answer
                st.experimental_rerun()
                
        else:
            st.error(f"Špatně! Správná odpověď je: {correct_answer}")

    st.write("---")  # Horizontální čára
    st.markdown(f"Pokud se vám líbí tato aplikace a chcete podpořit mé další projekty, můžete mě pozvat na kávu přes [Buy me a coffee ☕](https://www.buymeacoffee.com/bbscout). Děkuji za vaši podporu!")

if __name__ == "__main__":
    main()
