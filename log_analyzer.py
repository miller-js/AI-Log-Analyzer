"""
This script processes log entries from a file, analyzes them for security threats using the OpenAI API, 
and saves the analysis results to a timestamped TXT file.
It loads the logs, preprocesses them, sends batches of logs to the OpenAI API for analysis,
and stores the results in a file with the current date and time for easy reference.

Author: Miller Swank    12/24/2024
"""

import time
import datetime
import os
import openai
from openai import OpenAI

# Initialize OpenAI object with your OpenAI API key
client = OpenAI(
  api_key="<Your API Key Here>"
)

def load_logs(log_file):
    """
    Reads all lines from the log file into a list and returns the list of log entries.
    """
    try:
        with open(log_file, 'r') as f:
            logs = f.readlines()
        return logs
    except FileNotFoundError:
        print(f"Error: Log file {log_file} not found.")
        return []

def preprocess_logs(logs):
    """
    A function to clean and format log entries.
    Removes leading/trailing whitespace from each log.
    Truncates each log entry to 1000 characters to reduce input size.
    """
    return [log.strip()[:1000] for log in logs if log.strip()]

def analyze_logs_batch(log_entries):
    """
    Function that uses the OpenAI API to analyze multiple log entries in a single call.
    """
    combined_logs = "\n\n".join(log_entries)  # Combines multiple logs into a single string, separated by double newlines
    try:
        response = client.chat.completions.create(  # Sends a request to the API
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a security analyst."},
                {"role": "user", "content": f"Analyze these logs for potential security threats and provide feedback using the MITRE ATT&CK framework for each log entry:\n{combined_logs}"}
            ],
            temperature=0.3,
            max_tokens=1000,  # Limits the number of tokens in the response in order to optimize API usage
        )

        time.sleep(3)   # Give the response time to complete

        # Returns the entire response object
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Error analyzing logs: {e}")
        return None

def process_logs(log_file, batch_size=10):
    """
    Process logs and analyze them in batches using the OpenAI API.
    """
    logs = load_logs(log_file)
    if not logs:
        print("No logs to process.")
        return

    print(f"Processing {len(logs)} log entries...")
    results = []

    # Preprocess logs
    clean_logs = preprocess_logs(logs)

    # Process logs in batches by iterating through logs in increments of batch_size
    for i in range(0, len(clean_logs), batch_size):
        batch = clean_logs[i:i + batch_size]
        print(f"Analyzing batch {i // batch_size + 1} with {len(batch)} logs...")

        # Get analysis from OpenAI
        response = analyze_logs_batch(batch)
        if response is not None:
            # Append the raw response text to the results
            results.append(response)

        # Add a slight delay to avoid hitting API rate limits
        time.sleep(3)

    # Generate a filename with the current date and time in the format: "analysis_MM_DD_YYYY_HH_MM"
    timestamp = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M")
    filename = f"analysis_{timestamp}.txt"

    # Specify the directory for the file, or use os.getcwd() for the current directory.
    save_directory = os.getcwd()
    filename = os.path.join(save_directory, f"analysis_{timestamp}.txt")

    # Save results of the analysis to a text file, including the date and time
    with open(filename, "w") as f:
        for result in results:
            f.write(result + "\n\n")  # Write each result as plaintext with newlines in between

    print(f"\nResults saved to {filename}.")

if __name__ == "__main__":
    # Log file path is specified here
    log_file_path = "examplelog.txt"
    
    process_logs(log_file_path)
