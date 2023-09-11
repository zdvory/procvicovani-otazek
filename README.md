# Procvičování Otázek

Aplikace pro procvičování otázek z různých oblastí. Umožňuje výběr otázek z vybraných oblastí, zobrazuje náhodné otázky a poskytuje uživatelům zpětnou vazbu o správnosti odpovědí. Aplikace dále zobrazuje statistiky úspěšnosti odpovědí.

### 📋 Funkce
- Výběr oblastí pro procvičování.
- Náhodný výběr otázek na základě vybraných oblastí.
- Zpětná vazba pro uživatele.
- Statistiky úspěšnosti odpovědí.
- Možnost podpořit autora aplikace.

### 🔧 Konfigurace
Aplikace nahrává data s otázkami z Google Sheets, které je veřejně sdíleno. Pro nahrání těchto dat:

1. Vložte odkaz k veřejně sdílenému Google Sheetu do souboru `.streamlit/secrets.toml` nebo do sekce secrets na streamlit.io.
    
    **Příklad pro `.streamlit/secrets.toml`**
    ```toml
    [global]
    public_gsheets_url = "https://docs.google.com/spreadsheets/d/{sheetID}/edit"
    ```

2. **Struktura Google Sheetu**
    Vaše Google Sheets by mělo mít následující strukturu:

    | Oblast | Podoblast | Číslo otázky | Otázka | Odpověď A | Odpověď B | Odpověď C | Správná odpověď | Zdroje |
    | ------ | --------- | ------------ | ------ | --------- | --------- | --------- | --------------- | ------ |
    | Organizace XYZ | T 1.1 | 1 | Otázka příkladu | Náhodná odpověď A | Náhodná odpověď B | Náhodná odpověď C | a | [odkaz](#) |

### 🚀 Jak spustit aplikaci
1. **Instalace potřebných knihoven**
    ```bash
    pip install streamlit pandas PIL
    ```

2. **Stáhněte tento repozitář** a navigujte do jeho složky v příkazovém řádku.

3. **Spusťte aplikaci**
    ```bash
    streamlit run app.py
    ```

### 💙 Podpora
Pokud se vám aplikace líbí a chcete podpořit její další vývoj, navštivte [Buy me a coffee ☕](https://www.buymeacoffee.com/bbscout).
