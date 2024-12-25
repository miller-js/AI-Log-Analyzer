"""
Author: Miller Swank    12/24/2024
"""

import json
import time
import datetime
import os
import openai
from openai import OpenAI

# Creates an instance of the OpenAI client using an API key.
client = OpenAI(
  api_key="<API Key Here>"
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
    combined_logs = "\n\n".join(log_entries)  # Combines multiple logs into a single string, separated by double newlines.
    try:
        response = client.chat.completions.create(  # Sends a request to the API.
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a security analyst."},
                {"role": "user", "content": f"Analyze these logs for security threats:\n{combined_logs}"}
            ],
            temperature=0.3,
            max_tokens=500, # Limits the number of tokens in the response in order to optimize API usage.
        )

        # Returns the analysis as a string.
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error analyzing logs: {e}")
        return "Error analyzing logs."

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
        analysis = analyze_logs_batch(batch)
        for log, analysis_result in zip(batch, analysis.split("\n\n")):  # Split results for each log
            results.append({"log": log, "analysis": analysis_result.strip()})

        # Add a slight delay to avoid hitting API rate limits
        time.sleep(1)

    # Print results
    print("\nAnalysis Complete:")
    for result in results:
        print(f"\nLog: {result['log']}\nAnalysis: {result['analysis']}")
    
    # Generate a filename with the current date and time
    timestamp = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M")
    filename = f"analysis_{timestamp}.json"
    
    # Specify the directory for the file, or use os.getcwd() for the current directory.
    save_directory = os.getcwd()
    filename = os.path.join(save_directory, f"analysis_{timestamp}.json")

    # Save results of the analysis to a JSON file, including the date and time
    with open(filename, "w") as f:
        json.dump(results, f, indent=4)
    print(f"\nResults saved to {filename}.")

if __name__ == "__main__":

    # Log file path is specified here
    log_file_path = "examplelog.txt"
    
    process_logs(log_file_path)
