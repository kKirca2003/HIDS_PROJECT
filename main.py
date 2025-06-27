# main.py
import json
import time

def load_config():
    try:
        with open("config.json", "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print("[ERROR] config.json not found.")
        return None

def analyze_logs(config):
    log_file_path = config["log_file_to_monitor"]
    rules = config["alert_rules"]
    alerts_output_file = config["alerts_output_file"]

    # Create a sample log file for testing if it doesn't exist
    try:
        with open(log_file_path, "x") as f:
            f.write("Jun 27 20:30:20 server sshd[1235]: Failed password for root from 192.168.1.100 port 22 ssh2\n")
    except FileExistsError:
        pass # File already exists, which is fine.

    print(f"Analyzing '{log_file_path}'...")

    with open(log_file_path, "r") as file:
        for line in file:
            for rule in rules:
                if rule["keyword"] in line:
                    alert_message = f"[ALERT] Rule '{rule['rule_name']}' triggered: {line.strip()}\n"
                    with open(alerts_output_file, "a") as alert_file:
                        alert_file.write(f"{time.ctime()} - {alert_message}")

if __name__ == "__main__":
    config = load_config()
    if config:
        analyze_logs(config)