import os
import json
from datetime import date
from typing import Optional

import requests
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


def get_key(name):
    try:
        return st.secrets[name]      # on Streamlit Cloud
    except Exception:
        return os.getenv(name)       # locally from .env


client = genai.Client(api_key=get_key("GEMINI_API_KEY"))
SERPAPI_KEY = get_key("SERPAPI_API_KEY")
MODEL = "gemini-2.5-flash"   # if this name stops working, check AI Studio for the current Flash model

SYSTEM_PROMPT = f"""You are a friendly AI travel agent. Today's date is {date.today().isoformat()}.
Use the tools to find real flights and hotels. Airport codes must be IATA codes
(e.g. MAA, HYD, DEL, AMS). Convert city names to IATA codes yourself.
If the user is missing key details (cities or dates), ask one short question first.
Dates passed to tools must be YYYY-MM-DD. Default currency is INR unless the user says otherwise.
Present results clearly with prices, and include links when available.
Prices are indicative; remind the user to confirm on the booking site."""


# ---------------- TOOLS ----------------
# Gemini reads the function name, type hints and docstring to understand each tool.

def search_flights(
    origin: str,
    destination: str,
    outbound_date: str,
    return_date: Optional[str] = None,
    currency: str = "INR",
) -> str:
    """Search Google Flights.

    Args:
        origin: Departure airport IATA code, e.g. HYD.
        destination: Arrival airport IATA code, e.g. DEL.
        outbound_date: Departure date in YYYY-MM-DD format.
        return_date: Return date in YYYY-MM-DD format. Leave empty for one-way trips.
        currency: Currency code such as INR or USD.
    """
    params = {
        "engine": "google_flights",
        "departure_id": origin,
        "arrival_id": destination,
        "outbound_date": outbound_date,
        "currency": currency,
        "hl": "en",
        "api_key": SERPAPI_KEY,
    }
    if return_date:
        params["return_date"] = return_date
    else:
        params["type"] = "2"  # one-way
    try:
        data = requests.get("https://serpapi.com/search", params=params, timeout=60).json()
    except Exception as e:
        return f"Error calling flight search: {e}"
    if "error" in data:
        return f"Error: {data['error']}"
    options = (data.get("best_flights", []) + data.get("other_flights", []))[:5]
    results = []
    for o in options:
        legs = o.get("flights", [])
        if not legs:
            continue
        results.append({
            "price": o.get("price"),
            "airline": legs[0].get("airline"),
            "from": legs[0].get("departure_airport", {}).get("name"),
            "departs": legs[0].get("departure_airport", {}).get("time"),
            "to": legs[-1].get("arrival_airport", {}).get("name"),
            "arrives": legs[-1].get("arrival_airport", {}).get("time"),
            "stops": len(legs) - 1,
            "total_minutes": o.get("total_duration"),
        })
    return json.dumps(results) if results else "No flights found."


def search_hotels(
    location: str,
    check_in_date: str,
    check_out_date: str,
    adults: int = 2,
    currency: str = "INR",
) -> str:
    """Search Google Hotels in a city.

    Args:
        location: City name, e.g. Delhi.
        check_in_date: Check-in date in YYYY-MM-DD format.
        check_out_date: Check-out date in YYYY-MM-DD format.
        adults: Number of adult guests.
        currency: Currency code such as INR or USD.
    """
    params = {
        "engine": "google_hotels",
        "q": f"hotels in {location}",
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "adults": adults,
        "currency": currency,
        "hl": "en",
        "api_key": SERPAPI_KEY,
    }
    try:
        data = requests.get("https://serpapi.com/search", params=params, timeout=60).json()
    except Exception as e:
        return f"Error calling hotel search: {e}"
    if "error" in data:
        return f"Error: {data['error']}"
    results = []
    for p in data.get("properties", [])[:5]:
        results.append({
            "name": p.get("name"),
            "price_per_night": p.get("rate_per_night", {}).get("lowest"),
            "rating": p.get("overall_rating"),
            "stars": p.get("extracted_hotel_class"),
            "link": p.get("link"),
        })
    return json.dumps(results) if results else "No hotels found."


# ---------------- AGENT ----------------
def new_chat():
    # The SDK runs the tool-calling loop automatically when you pass Python functions as tools.
    return client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[search_flights, search_hotels],
        ),
    )


# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="AI Travel Agent", page_icon="✈️")
st.title("✈️ AI Travel Agent")

if "chat" not in st.session_state:
    st.session_state.chat = new_chat()
    st.session_state.display = []

with st.sidebar:
    if st.button("Start new chat"):
        st.session_state.chat = new_chat()
        st.session_state.display = []
        st.rerun()

for role, text in st.session_state.display:
    with st.chat_message(role):
        st.markdown(text)

prompt = st.chat_input("e.g. Flights from Delhi to Hyderabad on 2026-11-26, plus hotels")
if prompt:
    st.session_state.display.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            try:
                answer = st.session_state.chat.send_message(prompt).text or "(No answer returned, try rephrasing.)"
            except Exception as e:
                msg = str(e)
                if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                    answer = "Rate limit reached on the free tier. Wait a minute and try again."
                else:
                    answer = f"Something went wrong: {msg}"
        st.markdown(answer)
    st.session_state.display.append(("assistant", answer))