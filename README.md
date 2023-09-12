# Procvičování Otázek

Aplikace pro procvičování otázek z různých oblastí. Umožňuje výběr otázek z vybraných oblastí, zobrazuje náhodné otázky a poskytuje uživatelům zpětnou vazbu o správnosti odpovědí. Aplikace dále zobrazuje statistiky úspěšnosti odpovědí.

### 📋 Funkce
- Výběr oblastí pro procvičování.
- Náhodný výběr otázek na základě vybraných oblastí.
- Zpětná vazba pro uživatele.
- Statistiky úspěšnosti odpovědí.
- Možnost podpořit autora aplikace.
- **Aktuálně podporuje pouze výběr ze 3 otázek.**

### 🔧 Konfigurace

Aplikace nahrává data s otázkami z Google Sheets. Tabulka musí mít nastaveno sdílení na `Všichni, kdo mají odkaz`.

**Struktura Google Sheets**

    Váš Google Sheet by měl mít následující strukturu:

    | Oblast | Podoblast | Číslo otázky | Otázka | Odpověď A | Odpověď B | Odpověď C | Správná odpověď | Zdroje |
    | ------ | --------- | ------------ | ------ | --------- | --------- | --------- | --------------- | ------ |
    | Organizace XYZ | T 1.1 | 1 | Otázka příkladu | Náhodná odpověď A | Náhodná odpověď B | Náhodná odpověď C | a | [odkaz](#) |


### 🚀 Deploy na streamlit.io

Pokud chcete aplikaci rychle a snadno nasadit na streamlit.io, postupujte následovně:

1. **Přihlaste se na [streamlit.io](https://www.streamlit.io/)** a v pravém horním rohu klikněte na tlačítko `New app`.

2. **Zadejte URL vašeho GitHub repozitáře** do pole `GitHub URL`.

3. **Konfigurace secrets**: 
    - V levém menu klikněte na `Secrets`.
    - Klikněte na tlačítko `Add a secret`.
    - Zadejte následující klíč a hodnotu `public_gsheets_url = "https://docs.google.com/spreadsheets/d/{sheetID}/edit"` (Kako hodnotu vložte odkaz na váš veřejně sdílený Google Sheet s otázkami v uvedeném formátu. Ujistěte se, že váš Google Sheet má nastaveno sdílení pro "anyone with the link".)

4. **Spusťte aplikaci** kliknutím na tlačítko `Deploy`.

Vaše aplikace by měla být nyní nasazena a běžet na streamlit.io!


### 🚀 Jak spustit aplikaci lokálně
1. **Instalace potřebných knihoven**
    ```bash
    pip install streamlit pandas PIL
    ```
    
2. **Stáhněte tento repozitář** a navigujte do jeho složky v příkazovém řádku.

3. Vložte odkaz k veřejně sdílenému Google Sheetu do souboru `.streamlit/secrets.toml`.
    
    **Příklad pro `.streamlit/secrets.toml`**
    ```toml
    [global]
    public_gsheets_url = "https://docs.google.com/spreadsheets/d/{sheetID}/edit"
    ```

4. **Spusťte aplikaci**
    ```bash
    streamlit run app.py
    ```

### 💙 Podpora
Pokud se vám aplikace líbí a chcete podpořit její další vývoj, navštivte [Buy me a coffee ☕](https://www.buymeacoffee.com/bbscout).
