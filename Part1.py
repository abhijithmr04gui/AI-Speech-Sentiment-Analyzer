
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from threading import Thread
import time
import csv
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageTk
import plotly.graph_objects as go
import pyttsx3  # Import pyttsx3 for text-to-speech

from speech_to_text import recognize_speech
from sentiment_analysis import get_sentiment

# Global variables
listening = False
sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}  # For trend visualization
session_data = []  # To store analyzed data for export

# Initialize text-to-speech engine
engine = pyttsx3.init()


def speak_feedback(sentiment):
    """Function to speak feedback based on sentiment."""
    if sentiment == "Positive":
        engine.say("Great job! Your statement is positive.")
    elif sentiment == "Negative":
        engine.say("Oops! Your statement is negative.")
    else:
        engine.say("Your statement seems neutral.")
    engine.runAndWait()


def start_listening(output_text, sentiment_label):
    """Start listening for speech and analyzing sentiment."""
    global listening
    listening = True
    while listening:
        # Recognize speech
        text = recognize_speech()

        if text:
            # Display the recognized text in the output box
            output_text.insert(tk.END, f"You said: {text}\n")
            output_text.see(tk.END)

            # Get sentiment analysis
            sentiment, polarity, subjectivity = get_sentiment(text)
            sentiment_color = get_sentiment_color(sentiment)

            # Display sentiment analysis in the text box
            output_text.insert(tk.END, f"Sentiment: {sentiment}\n", sentiment)
            output_text.insert(tk.END, f"Polarity: {polarity:.2f}, Subjectivity: {subjectivity:.2f}\n\n")
            output_text.see(tk.END)

            # Update sentiment label
            sentiment_label.config(text=f"Sentiment: {sentiment}", fg=sentiment_color)

            # Update sentiment counts for visualization
            if sentiment in sentiment_counts:
                sentiment_counts[sentiment] += 1

            # Save session data
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            session_data.append([text, sentiment, polarity, subjectivity, timestamp])

            # Provide feedback using TTS
            speak_feedback(sentiment)

        # Stop listening if the stop command is detected
        if text and "stop listening" in text.lower():
            output_text.insert(tk.END, "Stopping the system...\n")
            output_text.see(tk.END)
            listening = False

        time.sleep(1)


def stop_listening():
    """Stop the listening loop."""
    global listening
    listening = False


def save_to_file(output_text):
    """Save the interaction log to a file."""
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(output_text.get("1.0", tk.END))


def export_to_csv():
    """Export the session data to a CSV file."""
    if not session_data:
        tk.messagebox.showinfo("No Data", "No data to export.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            # Write headers
            writer.writerow(["Text", "Sentiment", "Polarity", "Subjectivity", "Timestamp"])
            # Write session data
            writer.writerows(session_data)
        tk.messagebox.showinfo("Export Successful", f"Data successfully exported to {file_path}")


def get_sentiment_color(sentiment):
    """Return the color corresponding to the sentiment."""
    if sentiment == "Positive":
        return "green"
    elif sentiment == "Negative":
        return "red"
    else:
        return "blue"


def show_trends(trends_label):
    """Generate and display sentiment trends graph."""
    # Create a bar chart using Plotly
    fig = go.Figure(
        data=[
            go.Bar(
                x=list(sentiment_counts.keys()),
                y=list(sentiment_counts.values()),
                marker=dict(color=["green", "red", "blue"]),
            )
        ]
    )
    fig.update_layout(
        title="Sentiment Trends",
        xaxis_title="Sentiment",
        yaxis_title="Count",
        width=500,
        height=400,
    )

    # Convert the Plotly figure to an image
    img_buffer = BytesIO()
    fig.write_image(img_buffer, format="png")
    img_buffer.seek(0)
    img = Image.open(img_buffer)
    img_tk = ImageTk.PhotoImage(img)

    # Display the graph in the GUI
    trends_label.config(image=img_tk)
    trends_label.image = img_tk


def clear_output(output_text):
    """Clear the content of the output text widget."""
    output_text.delete(1.0, tk.END)


# GUI setup
def setup_gui():
    # Create the main window
    window = tk.Tk()
    window.title("Enhanced Real-Time Sentiment Analysis")
    window.geometry("800x800")
    window.config(bg="#f0f0f0")  # Soft background color

    # Instruction label
    instruction_label = tk.Label(window, text="Press 'Start' to begin listening and analyzing sentiment.",
                                 font=("Helvetica", 12), bg="#f0f0f0", fg="#333")
    instruction_label.pack(pady=10)

    # Sentiment display label
    sentiment_label = tk.Label(window, text="Sentiment: None", font=("Arial", 16, "bold"), fg="blue", bg="#f0f0f0")
    sentiment_label.pack(pady=10)

    # Output text box
    output_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=15, font=("Courier", 11), bd=2)
    output_text.tag_config("Positive", foreground="green")
    output_text.tag_config("Negative", foreground="red")
    output_text.tag_config("Neutral", foreground="blue")
    output_text.pack(pady=10)

    # Button frame
    button_frame = tk.Frame(window, bg="#f0f0f0")
    button_frame.pack(pady=20)

    # Start button with modern design
    start_button = tk.Button(button_frame, text="Start Listening", font=("Arial", 12, "bold"), width=20, height=2,
                             bg="#4CAF50", fg="white", activebackground="#45a049", relief="flat",
                             command=lambda: Thread(target=start_listening, args=(output_text, sentiment_label),
                                                    daemon=True).start())
    start_button.pack(side=tk.LEFT, padx=10)

    # Stop button with modern design
    stop_button = tk.Button(button_frame, text="Stop Listening", font=("Arial", 12, "bold"), width=20, height=2,
                            bg="#f44336", fg="white", activebackground="#e53935", relief="flat",
                            command=stop_listening)
    stop_button.pack(side=tk.LEFT, padx=10)

    # Save button with modern design
    save_button = tk.Button(button_frame, text="Save Results", font=("Arial", 12, "bold"), width=20, height=2,
                            bg="#2196F3", fg="white", activebackground="#1e88e5", relief="flat",
                            command=lambda: save_to_file(output_text))
    save_button.pack(side=tk.LEFT, padx=10)

    # Trends button with modern design
    trends_button = tk.Button(button_frame, text="Show Trends", font=("Arial", 12, "bold"), width=20, height=2,
                              bg="#FF9800", fg="white", activebackground="#fb8c00", relief="flat",
                              command=lambda: show_trends(trends_label))
    trends_button.pack(side=tk.LEFT, padx=10)

    # Export to CSV button with modern design
    export_button = tk.Button(button_frame, text="Export to CSV", font=("Arial", 12, "bold"), width=20, height=2,
                              bg="#9C27B0", fg="white", activebackground="#8e24aa", relief="flat",
                              command=export_to_csv)
    export_button.pack(side=tk.LEFT, padx=10)

    # Sentiment trends display area
    trends_label = tk.Label(window)
    trends_label.pack(pady=20)

    # Clear output button
    clear_button = tk.Button(window, text="Clear Output", font=("Arial", 12, "bold"), width=20, height=2,
                             bg="#607D8B", fg="white", activebackground="#455a64", relief="flat",
                             command=lambda: clear_output(output_text))
    clear_button.pack(pady=10)

    # Start the GUI main loop
    window.mainloop()


if __name__ == "__main__":
    setup_gui()