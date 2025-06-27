# main.py
import json
import time

def load_config():
    """Loads configuration from config.json file."""
    try:
        with open("config.json", "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print("[ERROR] config.json not found.")
        return None


def check_line_for_alerts(line, rules):
    """Checks a single line against all rules and returns an alert message if a match is found."""
    for rule in rules:
        if rule["keyword"] in line:
            # A rule is triggered, create and return the alert message.
            return f"[ALERT] Rule '{rule['rule_name']}' triggered: {line.strip()}\n"
    # No rules were triggered for this line.
    return None

def write_alert_to_log(alert_message, alerts_output_file):
    """Writes a formatted alert message to the specified log file."""
    with open(alerts_output_file, "a") as alert_file:
        # Prepend the current time to the alert message
        alert_file.write(f"{time.ctime()} - {alert_message}")

def main():
    """Main function to run the continuous monitoring."""
    config = load_config()
    if not config:
        return # Exit if config could not be loaded

    log_file_path = config["log_file_to_monitor"]
    rules = config["alert_rules"]
    alerts_output_file = config["alerts_output_file"]

    print("HIDS is starting... Monitoring for new log entries.")
    print(f"Watching file: {log_file_path}")
    print("Press Ctrl+C to stop.")

    with open(log_file_path, "r") as file:
        # Move the cursor to the end of the file.
        # This is the "tail -f" logic. We ignore old entries
        file.seek(0, 2)

        while True:
            # Try to read a new line
            new_line = file.readline()

            if new_line:
                # If a new line was added, check it for alerts.
                alert = check_line_for_alerts(new_line, rules)
                if alert:
                    print(alert, end='')
                    write_alert_to_log(alert, alerts_output_file)
            else:
                # If no new line, wait a bit before checking again.
                time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nHIDS is shutting down. Goodbye!")