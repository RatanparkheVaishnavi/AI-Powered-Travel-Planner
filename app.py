import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
st.set_page_config(page_title="AI Powered Travel Planner",layout="centered",page_icon="✈️")
st.title(" 🌍 AI Powered Travel Planner ✈️")
st.write("Enter details to get estimated travel costs for various travel modes.")
source = st.text_input("📍 Source:")
destination = st.text_input("🎯 Destination:")
st.markdown(
    """
    <style>
        body {
            background-color: #f0f2f6;
            color: #333333;
            font-family: Arial, sans-serif;
        }
        .stApp {
            background: linear-gradient(to right, #4facfe, #00f2fe);
            padding: 20px;
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)
if st.button("Get Travel plan"):
    if source and destination:
        with st.spinner("Fetching all travel options ...."):
            chat_template = ChatPromptTemplate(messages=[
                ("system", """
                You are an AI-powered travel assistant designed to help users find the best travel options between a given source and destination.
                Upon receiving the source and destination, generate a list of travel options, including cab, bus, train, and flight choices. 
                For each option, provide the following details:For each mode, include all possible subcategories (e.g., Bus: AC Sleeper, Non-AC Sleeper, AC Push Back, Non-AC Push Back; Car: Sedan & SUV with base fare and toll charges; Train: Sleeper, 3rd AC, 2nd AC, 1st AC; Aeroplane: Economy, Business; Bike: Fuel Cost, Wear & Tear).
                You generate the output while following the below mentioned format, estimated price, travel time, distance and relevant 
                Focus on accuracy, cost-effectiveness, and convenience, ensuring that the user can make an informed decision based on their preferences.
                Keep the output concise, ensuring clarity and ease of understanding.
                Do not include and ouput in tablar format, keep all output as strings. 
                Recommend best possible travel mode and best time to travel at the end.
                """),
                ("human", "Find travel options from {source} to {destination} along with estimated costs.")
            ])
            
            chat_model = ChatGoogleGenerativeAI(api_key="your_api_key", model="gemini-2.0-flash-exp")
            parser = StrOutputParser()
            chain = chat_template | chat_model | parser
            raw_input = {"source": source, "destination": destination}
            response = chain.invoke(raw_input)
            st.success("Possible Travel Routes and Budget Breakdown",icon="🔍")
            travel_modes = response.split("\n")  
            for mode in travel_modes:
                st.markdown(mode)
    else:
        st.error("Error!!! Please enter both source and destination")
