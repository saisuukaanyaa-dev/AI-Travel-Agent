# ✈️ AI Travel Agent

An AI-powered travel assistant that finds real flights and hotels through a simple chat. Tell it where you want to go, and it searches live Google Flights and Google Hotels data, then explains the options in plain English.

🔗 **Live demo:** https://ai-travel-agent-y5wj2azf8yfzbvotalzmzz.streamlit.app/

## Features

- **Natural-language chat:** just type something like "Flights from Delhi to Hyderabad on 26 November 2026".
- **Real flight search:** airlines, departure and arrival times, duration and prices.
- **Real hotel search:** nightly prices, ratings and booking links.
- **Asks for missing details:** if you say "I want to go to Mumbai", it asks for dates and your departure city.
- **Remembers the conversation:** it keeps context across messages, so follow-ups work.
- **Tool-using agent:** the AI decides when to call the flight or hotel tool and reads the results itself.

## Screenshots

### Flight search
<img width="1908" height="931" alt="Flight Search" src="https://github.com/user-attachments/assets/068d7762-7033-4245-a1ae-436d4f990fde" />



### Full trip plan: flights and hotels
<img width="1917" height="932" alt="Full trip plan flights and hotels" src="https://github.com/user-attachments/assets/ba4b48b0-f88b-44f6-8fab-38a2ad748ae8" />

<img width="1917" height="930" alt="Full trip plan flights and hotels 1" src="https://github.com/user-attachments/assets/540aef1d-83e9-4b96-9c88-23a45c3f65b0" />



### It asks follow-up questions
<img width="1917" height="921" alt="It asks follow-up questions" src="https://github.com/user-attachments/assets/6ee43d9c-70a7-4f08-98f1-d98ca0e6a68d" />



### Round-trip results
<img width="1917" height="912" alt="Round-trip results" src="https://github.com/user-attachments/assets/b13b219f-e2b1-4f2d-be72-a586977aafa7" />



## Try these prompts

> Find flights from Delhi to Hyderabad on 26 November 2026

> Plan a trip from Hyderabad to Delhi from 10 to 14 December 2026. Find flights and hotels.

> I want to go to Mumbai

## How it works

1. You type a travel request in the chat.
2. Google Gemini decides whether it needs the `search_flights` or `search_hotels` tool, or whether it should ask you for more details.
3. The tool calls SerpAPI, which returns Google Flights and Google Hotels data.
4. Gemini reads the results and writes a clear answer.

## Tech stack

- Python
- Streamlit (UI and hosting on Streamlit Community Cloud)
- Google Gemini API (`google-genai`)
- SerpAPI (Google Flights and Google Hotels)

## Run it locally

1. Clone the repo:
   ```
   git clone https://github.com/saisuukaanyaa-dev/ai-travel-agent.git
   cd ai-travel-agent
   ```
2. Create a virtual environment and install packages:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project folder:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   SERPAPI_API_KEY=your_serpapi_api_key
   ```
4. Start the app:
   ```
   streamlit run app.py
   ```

## Note

Prices are indicative and come from Google Flights and Google Hotels via SerpAPI. Always confirm on the booking site. This project is not affiliated with any airline, hotel or booking brand.

## Author

Built by [Sukanya](https://github.com/saisuukaanyaa-dev) while learning to build AI agents.
