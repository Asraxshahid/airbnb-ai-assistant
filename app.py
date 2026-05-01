import streamlit as st
import requests

st.set_page_config(page_title="Islamabad Airbnb Assistant", layout="centered")

# -------- DARK UI --------
st.markdown("""
<style>
body {background-color: #0E1117; color: white;}
.chat-user {
    background-color: #1f77b4;
    padding:10px;
    border-radius:10px;
    margin:5px;
}
.chat-bot {
    background-color: #2ca02c;
    padding:10px;
    border-radius:10px;
    margin:5px;
}
</style>
""", unsafe_allow_html=True)

st.title("🏡 Islamabad Airbnb Assistant")

# -------- MEMORY --------
if "history" not in st.session_state:
    st.session_state.history = []

guest_name = "Ahmed"

# -------- PROPERTY DATA --------
property_data = {
    "wifi": "Airbnb_ISB / 12345678",
    "checkin": "2:00 PM",
    "checkout": "11:00 AM",
}

# -------- API (TomTom) --------
API_KEY = "iYFiF3zXEpoKqfMti4JmseAFA6nM8esX"

def get_restaurants():
    url = f"https://api.tomtom.com/search/2/search/restaurants.json?key={API_KEY}&limit=5&countrySet=PK"
    res = requests.get(url).json()

    results = []
    for r in res.get("results", []):
        name = r["poi"]["name"]
        addr = r["address"]["freeformAddress"]
        results.append(f"{name} - {addr}")

    return results if results else ["No data found"]

# -------- INTENT --------
def detect(q):
    q = q.lower()
    if "wifi" in q:
        return "wifi"
    elif "check" in q:
        return "time"
    elif "food" in q or "restaurant" in q:
        return "food"
    elif "towel" in q or "clean" in q:
        return "request"
    else:
        return "general"

# -------- RESPONSE --------
def respond(q):
    intent = detect(q)

    if intent == "wifi":
        return f" WiFi: {property_data['wifi']}"

    elif intent == "time":
        return f" Check-in: {property_data['checkin']}, Check-out: {property_data['checkout']}"

    elif intent == "food":
        places = get_restaurants()
        return f"Hey {guest_name} \n\n Nearby places:\n" + "\n".join(places)

    elif intent == "request":
        return f"Got it {guest_name}, host has been notified."

    else:
        return f" I’m here to help during your stay, {guest_name}!"

# -------- INPUT --------
query = st.text_input("Ask something:")

if query:
    answer = respond(query)
    st.session_state.history.append((query, answer))

# -------- CHAT UI --------
for q, a in st.session_state.history:
    st.markdown(f'<div class="chat-user"> {q}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chat-bot"> {a}</div>', unsafe_allow_html=True)