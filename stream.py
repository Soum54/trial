import streamlit as st
import pandas as pd
from transformers import pipeline
import random

# Load the sentiment analysis pipeline
pipe = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-sentiment-latest")

# Define a function to analyze sentiment and return emoji, score, and the label
def analyze_sentiment(text):
    result = pipe(text)[0]  # Get the first (and only) result
    sentiment = result['label'].strip().upper()  # Normalize sentiment label
    score = result['score']  # Get the confidence score

    # Map the sentiment to an emoji
    if sentiment == "POSITIVE":
        emoji = "😊"
    elif sentiment == "NEGATIVE":
        emoji = "😢"
    elif sentiment == "NEUTRAL":
        emoji = "😐"
    else:
        emoji = "🤔"  # Fallback for any other cases

    # Format the score as a percentage with two decimal places
    score_percent = f"{score * 100:.2f}%"
    return sentiment.capitalize(), emoji, score_percent

# Streamlit UI elements
st.title("Sentiment Analysis with Emoji Spray")

st.write("""
Upload a CSV file with a 'Text' column or input your own text to perform sentiment analysis.
The model used is fine-tuned for customer feedback sentiment analysis.
""")

# Function to display moving emojis based on sentiment with random positions
def display_moving_emojis(sentiment):
    st.markdown('''
    <style>
    @keyframes move {
      0% {top: 100vh;}
      100% {top: -50px;}
    }
    .emoji {
      position: absolute;
      font-size: 50px;
      animation: move 5s infinite ease-in-out;
    }
    </style>
    ''', unsafe_allow_html=True)
    
    # Randomly generate multiple emojis for the "spray" effect
    for i in range(15):  # Create 15 emoji sprays
        left_position = random.randint(0, 100)  # Randomize left position
        animation_delay = random.uniform(0, 5)  # Randomize delay
        if sentiment == "Positive":
            emoji_choice = "😊"
        elif sentiment == "Negative":
            emoji_choice = "😢"
        elif sentiment == "Neutral":
            emoji_choice = "😐"
        else:
            emoji_choice = "🤔"
        
        st.markdown(f'''
        <style>
        .emoji-{i} {{
          left: {left_position}%;
          animation-delay: {animation_delay}s;
        }}
        </style>
        <div class="emoji emoji-{i}">{emoji_choice}</div>
        ''', unsafe_allow_html=True)

# User text input for single sentiment analysis
st.header("Analyze Sentiment of a Single Text")
user_input = st.text_input("Enter text for sentiment analysis")

# Add analyze button for single text input
if st.button("Analyze Text"):
    if user_input:
        sentiment, emoji, score = analyze_sentiment(user_input)
        st.write(f"**Sentiment:** {sentiment} {emoji}")
        st.write(f"**Confidence Score:** {score}")
        display_moving_emojis(sentiment)  # Show moving emojis
    else:
        st.warning("Please enter some text to analyze.")

# File upload for batch sentiment analysis
st.header("Batch Sentiment Analysis via CSV")
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

# Add analyze button for CSV file
if uploaded_file:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)

    # Check if the 'Text' column exists
    if 'Text' in df.columns:
        st.write("**Data Preview:**")
        st.write(df.head())

        if st.button("Analyze CSV"):
            # Perform sentiment analysis and store results
            st.write("Performing sentiment analysis...")
            sentiments = df['Text'].apply(analyze_sentiment)

            # Split the sentiments into separate columns
            df['Sentiment'] = sentiments.apply(lambda x: x[0])
            df['Emoji'] = sentiments.apply(lambda x: x[1])
            df['Confidence Score'] = sentiments.apply(lambda x: x[2])

            # Show the result in Streamlit
            st.write("**Sentiment analysis results:**")
            st.write(df.head())

            # Provide a download button for the updated CSV
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download results as CSV",
                data=csv,
                file_name='sentiment_analysis_results_with_emoji_and_score.csv',
                mime='text/csv',
            )
    else:
        st.error("The uploaded CSV does not contain a 'Text' column.")
else:
    st.write("Please upload a CSV file to perform batch sentiment analysis.")
