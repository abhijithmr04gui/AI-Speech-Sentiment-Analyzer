
from textblob import TextBlob


def get_sentiment(text):
    if text:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        if polarity > 0:
            sentiment = "Positive"
        elif polarity < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        return sentiment, polarity, subjectivity
    else:
        return "No input", 0, 0


Real_time_semtiment.py
import time
from speech_to_text import recognize_speech
from sentiment_analysis import get_sentiment


def main():
    print("Starting the real-time sentiment analysis...")
    while True:
        text = recognize_speech()

        if text:
            sentiment, polarity, subjectivity = get_sentiment(text)
            print(f"Sentiment: {sentiment}")
            print(f"Polarity: {polarity}, Subjectivity: {subjectivity}")

        # Check for the "stop listening" command
        if text and "stop listening" in text.lower():
            print("Stopping the system...")
            break

        # Wait a moment before listening again
        time.sleep(1)


if __name__ == "__main__":
    main()