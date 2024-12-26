# AI-Log-Analyzer
Personal project

This script automates the process of analyzing log entries for potential security threats using the OpenAI API. It processes logs from a specified file, sends them in manageable batches to the API for analysis while optimizing token usage, and outputs the results to a file named with the current date and time for easy reference.

How It Can Be Applied
Quickly identify potential security threats in system or network logs.
Automate the review of large volumes of logs to identify anomalies and threat actors.
Use as a tool for proactive threat hunting.

Usage
1. Place your log file in the same directory as the script, or provide the full path to the log file.
2. Run the script.
3. View the results in the generated file, which will be named with the current date and time (e.g., analysis_12_25_2024_15_30.txt).

Requirements
Python 3.7 or higher
OpenAI Python SDK
An OpenAI API key
