# AI-Speech-Sentiment-Analyzer

# Enhanced Real-Time Sentiment Analysis with Voice Feedback

This project provides a real-time, interactive sentiment analysis tool that leverages speech-to-text conversion to analyze spoken input. It features a graphical user interface (GUI) for easy interaction, visual feedback for sentiment, text-to-speech (TTS) audio feedback, and the ability to export session data.

## Features

* **Real-time Speech-to-Text:** Converts spoken words into text using Google Speech Recognition.
* **Sentiment Analysis:** Analyzes the sentiment (Positive, Negative, Neutral) of the recognized text, along with polarity and subjectivity scores.
* **Graphical User Interface (GUI):** A user-friendly interface built with Tkinter for easy interaction.
* **Visual Feedback:** Displays the recognized text and sentiment with color-coded labels.
* **Auditory Feedback:** Provides spoken feedback (using Text-to-Speech) about the detected sentiment for each statement.
* **Sentiment Trend Visualization:** Generates and displays a bar chart of sentiment counts (Positive, Negative, Neutral) during the session.
* **Session Data Export:** Allows users to save the complete interaction log to a text file or export structured sentiment data to a CSV file.
* **Clear Output:** Option to clear the displayed interaction log.

## How it Works

The application operates through several interconnected modules:

1.  **`Gui_sentiment.py` (Main GUI Application):**
    * Initializes the Tkinter GUI.
    * Manages the `start_listening`, `stop_listening`, `save_to_file`, `export_to_csv`, `show_trends`, and `clear_output` functions.
    * Uses `pyttsx3` for providing audio feedback.
    * Integrates `speech_to_text.py` and `sentiment_analysis.py` to process spoken input.
    * Utilizes `Plotly` and `PIL` (Pillow) to generate and display sentiment trend graphs.

2.  **`speech_to_text.py`:**
    * Employs the `speech_recognition` library to capture audio from the microphone.
    * Sends the audio to Google's Web Speech API for conversion into text.
    * Handles various errors such as timeouts, unknown values, or service request issues.

3.  **`sentiment_analysis.py`:**
    * Uses the `TextBlob` library for sentiment analysis.
    * Calculates polarity (ranging from -1.0 for negative to +1.0 for positive) and subjectivity (ranging from 0.0 for objective to 1.0 for subjective) scores.
    * Classifies sentiment as "Positive," "Negative," or "Neutral" based on the polarity score.

4.  **`Real_time_sentiment.py` (Console-based alternative/demonstration):**
    * Provides a simple command-line interface to demonstrate the core speech-to-text and sentiment analysis functionalities without the GUI.

## Tech Stack

* **Python 3.x**
* **`tkinter`:** For building the graphical user interface.
* **`speech_recognition`:** For speech-to-text conversion.
* **`pyttsx3`:** For text-to-speech audio feedback.
* **`TextBlob`:** For sentiment analysis.
* **`plotly`:** For generating interactive data visualizations (sentiment trends).
* **`Pillow` (`PIL`):** For image manipulation, specifically converting Plotly graphs to images for display in Tkinter.
* **`csv`:** For exporting data to CSV files.
* **`threading`:** For running the listening process in a separate thread to keep the GUI responsive.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    ```

2.  **Install the required Python libraries:**
    ```bash
    pip install SpeechRecognition TextBlob pyttsx3 plotly Pillow
    ```
    * **Note for TextBlob:** After installing `TextBlob`, you might need to download its NLTK data:
        ```bash
        python -m textblob.download_corpora
        ```

3.  **Ensure Microphone Access:**
    * Make sure your operating system grants permission for Python applications to access your microphone.

## How to Run

1.  **Run the GUI application:**
    ```bash
    python Gui_sentiment.py
    ```

2.  *(Optional)* **Run the console-based real-time analysis (without GUI):**
    ```bash
    python Real_time_sentiment.py
    ```

## Usage

Once `Gui_sentiment.py` is running:

1.  **"Start Listening" Button:** Click this to begin real-time speech recognition and sentiment analysis.
2.  **Speak Clearly:** Speak into your microphone. The recognized text will appear in the "Output" text box.
3.  **Sentiment Feedback:** The analyzed sentiment, polarity, and subjectivity will be displayed. The sentiment label at the top will change color (green for Positive, red for Negative, blue for Neutral), and you'll receive audio feedback.
4.  **"Stop Listening" Button:** Click this to halt the listening process. You can also say "stop listening" into the microphone.
5.  **"Save Results" Button:** Saves the entire content of the "Output" text box to a `.txt` file.
6.  **"Export to CSV" Button:** Exports all recorded recognized text, sentiment, polarity, subjectivity, and timestamp to a `.csv` file for further analysis.
7.  **"Show Trends" Button:** Generates and displays a bar chart visualizing the counts of Positive, Negative, and Neutral sentiments detected during the current session.
8.  **"Clear Output" Button:** Clears all text from the "Output" display area.

## Troubleshooting

* **Microphone Issues:** Ensure your microphone is properly connected and configured. Check your operating system's privacy settings to allow microphone access for Python.
* **`speech_recognition.RequestError`:** This usually indicates a problem with internet connectivity or Google's speech recognition service. Ensure you have an active internet connection.
* **`speech_recognition.UnknownValueError`:** The service could not understand the audio. Try speaking more clearly or in a quieter environment.
* **`pyttsx3` Issues:** If you hear no sound, check your system's audio output. On some Linux distributions, you might need `espeak` installed: `sudo apt-get install espeak`.

## Contributing

Contributions are welcome! Please feel free to fork the repository, open issues, or submit pull requests with improvements.

## License

[Specify your license here, e.g., MIT License, Apache 2.0 License, etc.]
