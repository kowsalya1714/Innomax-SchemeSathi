# SchemeSathi 🇮🇳

**AI for Bharat — multilingual government scheme discovery prototype**

SchemeSathi is a prototype that helps citizens search a small curated set of government scheme records, review basic conditions, see document checklists, and open official source pages.

## Important scope and honesty notes

- This bundle contains **5 curated central-scheme records**, not a complete database of every Indian government scheme.
- The language selector includes **English plus the 22 languages in the Eighth Schedule of the Constitution**. India has many additional languages; this is not a claim to cover every language spoken in India.
- English, Hindi and Telugu have built-in translations for the main interface labels. For dynamic translation of scheme descriptions and other interface strings, configure Google Cloud Translation. Provider language availability can vary; if a language is unsupported or no key is configured, the app falls back to English for content.
- The current starter is a deterministic search/rule-checking prototype, not yet a connected LLM or full RAG chatbot. Add an LLM/RAG layer as a clearly tested next step before claiming generative-AI capability.
- The scheme data is a concise summary, not a legal eligibility decision. Scheme rules, dates and document requirements can change. Always verify on the linked official portal.
- The prototype does **not** submit applications, access government databases, verify Aadhaar, guarantee eligibility, or guarantee benefits.
- No Aadhaar numbers, bank account numbers, OTPs or sensitive identity data are needed by this demo.

## Included schemes and official sources

1. **PM Ujjwala Yojana (PMUY)** — https://pmuy.gov.in/faq.html
2. **e-Shram registration** — https://eshram.gov.in/faqs?page=0
3. **PM Shram Yogi Maandhan (PM-SYM)** — https://www.eshram.gov.in/Schemes
4. **Pradhan Mantri Jan-Dhan Yojana (PMJDY)** — https://pmjdy.gov.in/scheme-detail.aspx
5. **PM-KISAN** — https://pmkisan.gov.in/ (the operational guidelines are linked from the portal)

National scheme discovery portal: https://www.myscheme.gov.in/

## Run locally

Requires Python 3.10 or newer.

### Windows

```powershell
cd SchemeSathi
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### macOS / Linux

```bash
cd SchemeSathi
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app opens in your browser (usually `http://localhost:8501`).

## Optional translation setup

The app has a language selector for the 22 scheduled languages plus English. English, Hindi and Telugu include built-in interface translations. For machine translation of dynamic scheme text, create a Google Cloud project, enable Cloud Translation, create an API key with suitable restrictions, and set:

```bash
# macOS/Linux
export GOOGLE_TRANSLATE_API_KEY="YOUR_KEY"
streamlit run app.py
```

```powershell
# Windows PowerShell
$env:GOOGLE_TRANSLATE_API_KEY="YOUR_KEY"
streamlit run app.py
```

Never commit a real API key to GitHub. For deployment, set it in the host's secret/environment-variable settings. You may also copy `.env.example` to `.env` locally and fill the key there; `.env` is ignored by Git. Translation provider coverage for individual Indian languages must be checked before claiming full support; unsupported languages fall back to English.

## Data maintenance

Edit `data/schemes.json` to add records. For every record, keep:
- official government source URL
- source department/name
- date last checked
- eligibility wording faithful to the official source
- documents only when supported by the official source
- notes describing conditions and uncertainties

Do not scrape or bulk-copy scheme content without checking the source site's terms. Prefer official APIs/open data or manually curated summaries with citations. Add state schemes only after checking each state's official department portal.

## Suggested GitHub upload

1. Extract the ZIP.
2. Open the `SchemeSathi` folder.
3. Create a new GitHub repository named `schemesathi`.
4. Upload the files and folders inside `SchemeSathi` (not the outer ZIP).
5. Add your team's real names and contributions to the README if desired.
6. Do not upload `.env`, API keys, Aadhaar data, user records or other secrets.

## Suggested next improvements for a hackathon

- Add official state-level schemes for your target state after verifying them.
- Add a proper retrieval-augmented generation (RAG) pipeline over official scheme PDFs/FAQs with citations and document version dates.
- Add voice input/output with tested Telugu speech models.
- Add an admin review workflow to approve changes to scheme records.
- Add tests for each eligibility rule and a visible “unknown / needs verification” state.
- Add automated freshness checks for official links and scheme update dates.
