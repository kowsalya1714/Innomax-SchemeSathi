import json, os, re
from pathlib import Path
import requests
import streamlit as st
from dotenv import load_dotenv

BASE = Path(__file__).parent
load_dotenv(BASE / ".env")
SCHEMES = json.loads((BASE / "data" / "schemes.json").read_text(encoding="utf-8"))
LANGUAGES = json.loads((BASE / "data" / "languages.json").read_text(encoding="utf-8"))

st.set_page_config(page_title="SchemeSathi", page_icon="🇮🇳", layout="wide")

UI = {
 "en": {"tag":"AI-powered government scheme discovery","title":"Find government schemes that may fit you",
        "subtitle":"Explore verified scheme summaries, check basic conditions and follow official links.",
        "language":"Choose language","profile":"Your basic profile","age":"Age","state":"State / Union Territory",
        "occupation":"Occupation","income":"Approx. annual household income (₹)","gender":"Gender",
        "category":"Social category (optional)","land":"Do you / your family hold agricultural land?",
        "unorganised":"Do you work in the unorganised sector?","search":"Search schemes",
        "ask":"Ask SchemeSathi","question":"Ask a question about schemes",
        "results":"Potentially relevant schemes","check":"Check basic conditions","documents":"Document checklist",
        "official":"Open official source","disclaimer":"This is an informational prototype, not a government service. It does not guarantee eligibility, application acceptance or benefits. Confirm current rules with the official department.",
        "translation":"Translation provider","translate_missing":"For full content translation, configure GOOGLE_TRANSLATE_API_KEY in .env. Without it, scheme details remain in English.",
        "no_match":"No strong match found in this small demo dataset. Try the official myScheme portal.",
        "matched":"Possible match based on the limited rules in this prototype",
        "not_matched":"One or more known conditions may not match",
        "unknown":"Not enough profile information to assess this condition",
        "all":"All schemes","all_users":"All citizens","student":"Student","farmer":"Farmer","worker":"Unorganised worker","woman":"Woman","other":"Other",
        "search_placeholder":"Try: farmer schemes, pension for workers, LPG connection, bank account",
        "chat_hint":"Ask in English or a supported Indian language. This demo searches its curated scheme records; it is not a general legal or benefits adviser."},
 "te": {"tag":"కృత్రిమ మేధస్సుతో ప్రభుత్వ పథకాల అన్వేషణ","title":"మీకు సరిపడే ప్రభుత్వ పథకాలను కనుగొనండి",
        "subtitle":"పథకాల వివరాలు చూడండి, ప్రాథమిక అర్హతలను పరిశీలించండి, అధికారిక లింకులను అనుసరించండి.",
        "language":"భాషను ఎంచుకోండి","profile":"మీ ప్రాథమిక వివరాలు","age":"వయస్సు","state":"రాష్ట్రం / కేంద్రపాలిత ప్రాంతం",
        "occupation":"వృత్తి","income":"సుమారు వార్షిక కుటుంబ ఆదాయం (₹)","gender":"లింగం",
        "category":"సామాజిక వర్గం (ఐచ్ఛికం)","land":"మీకు / మీ కుటుంబానికి వ్యవసాయ భూమి ఉందా?",
        "unorganised":"మీరు అసంఘటిత రంగంలో పనిచేస్తున్నారా?","search":"పథకాలను వెతకండి",
        "ask":"SchemeSathi ని అడగండి","question":"ప్రభుత్వ పథకాల గురించి ప్రశ్న అడగండి",
        "results":"మీకు ఉపయోగపడే అవకాశమున్న పథకాలు","check":"ప్రాథమిక అర్హతను పరిశీలించండి","documents":"పత్రాల జాబితా",
        "official":"అధికారిక మూలాన్ని తెరవండి","disclaimer":"ఇది సమాచార ప్రోటోటైప్ మాత్రమే; ప్రభుత్వ సేవ కాదు. అర్హత లేదా ప్రయోజనం హామీ కాదు. తాజా నియమాలను అధికారిక శాఖ వద్ద నిర్ధారించండి.",
        "translation":"అనువాద సేవ","translate_missing":"పూర్తి అనువాదం కోసం .env లో GOOGLE_TRANSLATE_API_KEY ఇవ్వండి. లేకపోతే పథక వివరాలు ఇంగ్లీషులో ఉంటాయి.",
        "no_match":"ఈ చిన్న డెమో డేటాలో సరిపోలే పథకం లేదు. అధికారిక myScheme పోర్టల్ చూడండి.",
        "matched":"ఈ ప్రోటోటైప్‌లోని పరిమిత నియమాల ప్రకారం సాధ్యమైన సరిపోలిక",
        "not_matched":"తెలిసిన ఒకటి లేదా అంతకంటే ఎక్కువ షరతులు సరిపోకపోవచ్చు",
        "unknown":"ఈ షరతును అంచనా వేయడానికి వివరాలు సరిపోవడం లేదు",
        "all":"అన్ని పథకాలు","all_users":"అందరూ","student":"విద్యార్థి","farmer":"రైతు","worker":"అసంఘటిత కార్మికుడు","woman":"మహిళ","other":"ఇతరులు",
        "search_placeholder":"ఉదా: రైతు పథకాలు, కార్మికుల పెన్షన్, LPG కనెక్షన్",
        "chat_hint":"ఇంగ్లీష్ లేదా మద్దతు ఉన్న భారతీయ భాషలో అడగండి. ఈ డెమోలోని పథక రికార్డులనే శోధిస్తుంది."},
 "hi": {"tag":"AI आधारित सरकारी योजना खोज","title":"अपने लिए उपयोगी सरकारी योजनाएँ खोजें",
        "subtitle":"योजना की जानकारी देखें, बुनियादी शर्तें जाँचें और आधिकारिक लिंक खोलें।",
        "language":"भाषा चुनें","profile":"आपकी मूल जानकारी","age":"आयु","state":"राज्य / केंद्र शासित प्रदेश",
        "occupation":"व्यवसाय","income":"अनुमानित वार्षिक पारिवारिक आय (₹)","gender":"लिंग",
        "category":"सामाजिक श्रेणी (वैकल्पिक)","land":"क्या आपके / परिवार के पास कृषि भूमि है?",
        "unorganised":"क्या आप असंगठित क्षेत्र में काम करते हैं?","search":"योजनाएँ खोजें",
        "ask":"SchemeSathi से पूछें","question":"सरकारी योजनाओं के बारे में प्रश्न पूछें",
        "results":"संभावित रूप से उपयोगी योजनाएँ","check":"बुनियादी शर्तें जाँचें","documents":"दस्तावेज़ सूची",
        "official":"आधिकारिक स्रोत खोलें","disclaimer":"यह केवल एक सूचना प्रोटोटाइप है, सरकारी सेवा नहीं। पात्रता या लाभ की गारंटी नहीं है। वर्तमान नियम आधिकारिक विभाग से सत्यापित करें।",
        "translation":"अनुवाद सेवा","translate_missing":"पूर्ण अनुवाद के लिए .env में GOOGLE_TRANSLATE_API_KEY सेट करें। अन्यथा योजना विवरण अंग्रेज़ी में रहेंगे।",
        "no_match":"इस छोटे डेमो डेटासेट में उपयुक्त योजना नहीं मिली। आधिकारिक myScheme पोर्टल देखें।",
        "matched":"इस प्रोटोटाइप के सीमित नियमों के आधार पर संभावित मेल",
        "not_matched":"एक या अधिक ज्ञात शर्तें मेल नहीं खा सकतीं",
        "unknown":"इस शर्त का आकलन करने के लिए पर्याप्त जानकारी नहीं है",
        "all":"सभी योजनाएँ","all_users":"सभी","student":"विद्यार्थी","farmer":"किसान","worker":"असंगठित श्रमिक","woman":"महिला","other":"अन्य",
        "search_placeholder":"जैसे: किसान योजना, श्रमिक पेंशन, LPG कनेक्शन",
        "chat_hint":"अंग्रेज़ी या समर्थित भारतीय भाषा में पूछें। यह डेमो अपने चुने हुए योजना रिकॉर्ड खोजता है।"}
}

def translate_text(text, target):
    if target == "en": return text
    api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY", "").strip()
    if not api_key: return text
    try:
        r = requests.post(
            "https://translation.googleapis.com/language/translate/v2",
            params={"key": api_key},
            json={"q": text, "target": target, "format": "text"},
            timeout=20
        )
        r.raise_for_status()
        return r.json()["data"]["translations"][0]["translatedText"]
    except Exception:
        return text

def eligibility(s, profile):
    checks = []
    sid = s["id"]
    if sid == "pmuy":
        checks.append(("Applicant is an adult woman", profile.get("gender") == "Woman" and profile.get("age") is not None and profile["age"] >= 18 if profile.get("gender") and profile.get("age") is not None else None))
        checks.append(("Household meets an eligible poor-household/deprivation category", None))
        checks.append(("No other LPG connection in household", None))
    elif sid == "eshram":
        checks.append(("Age is at least 16", profile["age"] >= 16 if profile.get("age") is not None else None))
        checks.append(("Works in the unorganised sector", profile.get("unorganised") if profile.get("unorganised") is not None else None))
        checks.append(("Not a member of ESIC/EPFO", None))
    elif sid == "pmsym":
        checks.append(("Age is between 18 and 40", 18 <= profile["age"] <= 40 if profile.get("age") is not None else None))
        checks.append(("Monthly income is below ₹15,000", None))
        checks.append(("Not a member of EPFO, ESIC or NPS (government-funded)", None))
    elif sid == "pmjdy":
        checks.append(("Does not already have a bank savings account", None))
    elif sid == "pmkisan":
        checks.append(("Family appears in relevant land records as a landholding farmer family", profile.get("land") if profile.get("land") is not None else None))
        checks.append(("No exclusion category applies", None))
    return checks

def score_scheme(s, profile, query):
    text = (s["name"]+" "+s["category"]+" "+s["summary"]+" "+" ".join(s["eligibility"])).lower()
    q = query.lower().strip()
    words = [w for w in re.findall(r"[a-zA-Z]{3,}", q) if w not in {"the","and","for","how","can","what","scheme"}]
    score = sum(2 for w in words if w in text)
    occ = (profile.get("occupation") or "").lower()
    if s["id"] == "pmkisan" and ("farmer" in occ or profile.get("land") is True): score += 4
    if s["id"] in ("eshram","pmsym") and profile.get("unorganised") is True: score += 4
    if s["id"] == "pmuy" and profile.get("gender") == "Woman": score += 2
    if s["id"] == "pmjdy": score += 1
    return score

def render_scheme(s, lang, profile):
    name = translate_text(s["name"], lang)
    summary = translate_text(s["summary"], lang)
    st.subheader(name)
    st.caption(s["category"] + " · Source checked in prototype: " + s["checked_on"])
    st.write(summary)
    checks = eligibility(s, profile)
    known_false = any(v is False for _,v in checks)
    known_true = any(v is True for _,v in checks)
    if known_false:
        st.warning(UI.get(lang, UI["en"])["not_matched"])
    elif known_true:
        st.success(UI.get(lang, UI["en"])["matched"])
    else:
        st.info(UI.get(lang, UI["en"])["unknown"])
    with st.expander(UI.get(lang, UI["en"])["check"]):
        for label, value in checks:
            translated_label = translate_text(label, lang)
            if value is True: st.write("✅ " + translated_label)
            elif value is False: st.write("❌ " + translated_label)
            else: st.write("❔ " + translated_label + " — " + translate_text("Please verify / provide more details.", lang))
    with st.expander(UI.get(lang, UI["en"])["documents"]):
        for d in s["documents"]: st.write("• " + translate_text(d, lang))
    st.caption("Source: " + s["source_name"])
    st.link_button(UI.get(lang, UI["en"])["official"], s["official_url"])
    st.caption(translate_text(s["notes"], lang))

st.title("🇮🇳 SchemeSathi")
st.caption("AI for Bharat · Government scheme discovery prototype")
lang_names = {x["name"]:x["code"] for x in LANGUAGES}
selected_name = st.selectbox("🌐 Language / భాష / भाषा", list(lang_names.keys()), index=0)
lang = lang_names[selected_name]
t = UI.get(lang, UI["en"])

st.markdown(f"### {t['title']}")
st.write(t["subtitle"])
if lang not in ("en","te","hi"):
    st.info(t["translate_missing"])
if lang in ("en","te","hi"):
    pass
else:
    st.caption("Selected language: " + selected_name + ". Dynamic translation is attempted when GOOGLE_TRANSLATE_API_KEY is configured; unsupported provider languages fall back to English.")

with st.sidebar:
    st.header(t["profile"])
    age = st.number_input(t["age"], min_value=0, max_value=120, value=0, step=1)
    state = st.selectbox(t["state"], ["Not specified","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Delhi","Jammu and Kashmir","Ladakh","Puducherry"])
    occupation = st.selectbox(t["occupation"], [t["all_users"],t["farmer"],t["student"],t["worker"],t["woman"],t["other"]])
    gender = st.selectbox(t["gender"], ["Not specified","Woman","Man","Other"])
    income = st.number_input(t["income"], min_value=0, value=0, step=10000)
    land_label = st.selectbox(t["land"], ["Not specified","Yes","No"])
    unorg_label = st.selectbox(t["unorganised"], ["Not specified","Yes","No"])
    st.caption("Do not enter Aadhaar, bank account numbers, OTPs or other sensitive identifiers.")
profile = {
 "age": age if age > 0 else None,
 "state": state,
 "occupation": occupation if occupation != t["all_users"] else "",
 "gender": gender if gender != "Not specified" else None,
 "income": income if income > 0 else None,
 "land": True if land_label == "Yes" else False if land_label == "No" else None,
 "unorganised": True if unorg_label == "Yes" else False if unorg_label == "No" else None
}
profile["occupation"] = {"Farmer":"farmer","किसान":"farmer","రైతు":"farmer","Unorganised worker":"worker","असंगठित श्रमिक":"worker","అసంఘటిత కార్మికుడు":"worker"}.get(profile["occupation"], profile["occupation"])

tab1, tab2, tab3 = st.tabs(["🔎 " + t["search"], "💬 " + t["ask"], "ℹ️ About & sources"])
with tab1:
    query = st.text_input(t["search"], placeholder=t["search_placeholder"])
    if st.button(t["search"], type="primary"):
        ranked = sorted(SCHEMES, key=lambda s: score_scheme(s, profile, query), reverse=True)
        if query.strip():
            ranked = [s for s in ranked if score_scheme(s, profile, query) > 0]
        if not ranked:
            st.info(t["no_match"])
            st.link_button("Official myScheme portal", "https://www.myscheme.gov.in/")
        else:
            st.subheader(t["results"])
            for s in ranked[:5]:
                with st.container(border=True):
                    render_scheme(s, lang, profile)
with tab2:
    st.write(t["chat_hint"])
    question = st.text_input(t["question"], key="chat_question")
    if st.button(t["ask"]):
        q = question
        if lang != "en":
            q = translate_text(question, "en")
        ranked = sorted(SCHEMES, key=lambda s: score_scheme(s, profile, q), reverse=True)
        if ranked and score_scheme(ranked[0], profile, q) > 0:
            best = ranked[0]
            st.success(translate_text("I found a potentially relevant record. Please review the official conditions below.", lang))
            render_scheme(best, lang, profile)
        else:
            st.info(t["no_match"])
            st.link_button("Search the official myScheme catalogue", "https://www.myscheme.gov.in/search")
with tab3:
    st.subheader("What this prototype does")
    st.write("A source-linked retrieval and scheme-discovery demo with profile-based ranking, transparent rule checks, document lists and optional machine translation. The current starter uses deterministic search/rules; an LLM-based RAG answer engine is a next development step, not yet included.")
    st.write("Language menu includes English plus the 22 languages listed in the Eighth Schedule of the Constitution. This is not a list of every language spoken in India. Actual translation coverage depends on the configured translation provider.")
    st.subheader("Curated scheme records")
    for s in SCHEMES:
        st.markdown(f"- **{s['name']}** — [{s['source_name']}]({s['official_url']})")
    st.markdown("**National discovery portal:** [myScheme](https://www.myscheme.gov.in/)")
    st.markdown("**Translation API documentation:** [Google Cloud Translation](https://cloud.google.com/translate/docs)")
    st.markdown("**Language list authority:** [Constitution of India, Eighth Schedule](https://www.legislative.gov.in/static/uploads/2025/08/7af1daa22d65f9d04c00ae9b9aa5a799.pdf)")

st.divider()
st.caption(t["disclaimer"])
