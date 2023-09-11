import streamlit as st
import pandas as pd
import random
from PIL import Image

# Konfigurace stránky
image = Image.open('born_to_be.png')
st.set_page_config(page_title="Procvičování otázek")
st.image(image)

# Pomocné funkce
def is_valid_question(row):
    correct_choice = row["Správná odpověď"]
    if not isinstance(correct_choice, str):
        return False
    correct_choice = correct_choice.upper()
    if correct_choice not in ['A', 'B', 'C']:
        return False
    return pd.notna(row[f"Odpověď {correct_choice}"])

@st.cache_data(ttl=600)
def load_data(sheets_url):
    """Nahrání dat z Google Sheets."""
    csv_url = sheets_url.replace("/edit", "/export?format=csv")
    data = pd.read_csv(csv_url)
    
    # Ověření, zda otázky mají správnou odpověď
    valid_data = data[data.apply(is_valid_question, axis=1)]
    
    return valid_data

def select_random_question(selected_areas):
    """Výběr náhodné otázky z vybraných oblastí."""
    question_row = data[data['Oblast'].isin(selected_areas)].sample(1).iloc[0]
    correct_answer = question_row[f"Odpověď {question_row['Správná odpověď'].upper()}"]
    answers = [question_row[f"Odpověď {label}"] for label in ['A', 'B', 'C']]
    random.shuffle(answers)
    return question_row, answers, correct_answer

def initialize_score():
    """Inicializace proměnných pro evidenci skóre."""
    if "score_by_area" not in st.session_state:
        st.session_state.score_by_area = {area: {"správně": 0, "špatně": 0} for area in all_areas}
        st.session_state.correct_delta = 0
        st.session_state.wrong_delta = 0

# Hlavní aplikace
def main():
    st.title('Procvičování otázek')

    # Výběr oblastí
    with st.expander('Výběr oblastí'):
        selected_areas = [area for area in all_areas if st.checkbox(area, value=True)]
        if st.button("Načíst otázky z vybraných oblastí", use_container_width=True):
            st.session_state.question_data = select_random_question(selected_areas)
            st.session_state.show_feedback = False
            st.experimental_rerun()

    # Nahrání náhodné otázky pokud ještě nebyla vybrána
    if 'question_data' not in st.session_state:
        st.session_state.question_data = select_random_question(selected_areas)
        st.session_state.show_feedback = False

    question_row, answers, correct_answer = st.session_state.question_data

    # Zobrazení otázky
    st.write(f"Otázka č. {question_row['Číslo otázky']} ({question_row['Oblast']} | {question_row['Podoblast']}):")
    st.markdown(f"### {question_row['Otázka']}", unsafe_allow_html=True)
    st.write("---")

    # Zobrazení odpovědí
    for answer_text in answers:
        if st.button(answer_text, use_container_width=True):
            st.session_state.selected_answer = answer_text
            st.session_state.show_feedback = True

    st.write("---")

    # Feedback po odpovědi
    if st.session_state.show_feedback:
        feedback_after_answer(question_row, correct_answer, selected_areas)

    # Zobrazení statistiky
    display_statistics()
    display_additional_statistics()

    # Poděkování a link na podporu
    st.write("---")
    st.markdown(f"Pokud se vám líbí tato aplikace a chcete podpořit mé další projekty, můžete mě pozvat na kávu přes [Buy me a coffee ☕](https://www.buymeacoffee.com/bbscout). Děkuji za vaši podporu!")

def feedback_after_answer(question_row, correct_answer, selected_areas):
    """Zobrazení feedbacku po zodpovězení otázky."""
    if pd.notnull(question_row['Zdroje']):
        st.markdown(f"**Zdroje:** {question_row['Zdroje']}")

    area = question_row['Oblast']
    if 'answered' not in st.session_state:
        st.session_state.answered = False

    if st.session_state.selected_answer == correct_answer:
        st.success('Správně!')
        if not st.session_state.answered:
            st.session_state.score_by_area[area]["správně"] += 1
            st.session_state.answered = True
            st.session_state.correct_delta = 1

        if st.button("Další otázka", use_container_width=True, type="primary"):
            st.session_state.question_data = select_random_question(selected_areas)
            st.session_state.show_feedback = False
            del st.session_state.selected_answer
            del st.session_state.answered
            st.session_state.correct_delta = 0
            st.session_state.wrong_delta = 0
            st.experimental_rerun()
    else:
        st.error(f"Špatně! Správná odpověď je: {correct_answer}")
        if not st.session_state.answered:
            st.session_state.score_by_area[area]["špatně"] += 1
            st.session_state.answered = True
            st.session_state.wrong_delta = 1
            
    st.write("---")

def display_statistics():
    #   Celkové statistiky
    total_correct = sum([score["správně"] for score in st.session_state.score_by_area.values()])
    total_wrong = sum([score["špatně"] for score in st.session_state.score_by_area.values()])
    total_attempts = total_correct + total_wrong
    success_percentage = (total_correct / total_attempts) * 100 if total_attempts != 0 else 0

    # Výpočet rozdílu v procentech
    previous_success_percentage = st.session_state.get("previous_success_percentage", success_percentage)
    percentage_delta = success_percentage - previous_success_percentage
    st.session_state.previous_success_percentage = success_percentage

    # Zobrazení celkových statistik
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        st.metric("Celkem správně", total_correct, st.session_state.correct_delta, "off" if st.session_state.correct_delta == 0 else "normal")
    with col2:
        st.metric("Celkem špatně", total_wrong, st.session_state.wrong_delta, "off" if st.session_state.wrong_delta == 0 else "inverse")
    with col3:
        st.metric("Úspěšnost", f"{success_percentage:.1f}%", f"{percentage_delta:.1f}%", "off" if percentage_delta == 0 else "normal")

def display_additional_statistics():
    """Zobrazení statistiky úspěšnosti."""
    with st.expander("Podrobná Statistika úspěšnosti"):
        stats_df = pd.DataFrame(st.session_state.score_by_area).T
        st.table(stats_df)
        st.bar_chart(stats_df, color=("#f00", "#0f0"))



# Spuštění aplikace
data = load_data(st.secrets["public_gsheets_url"])
all_areas = data['Oblast'].unique().tolist()
data = data.sample(frac=1).reset_index(drop=True)  # Randomizace dat

initialize_score()
main()