import matplotlib.pyplot as plt
import pandas as pd
import re
from collections import Counter

def visualize_alerts(log_file="ids_alerts.log"):
    try:
        with open(log_file, "r") as f:
            logs = f.readlines()
        
        if not logs:
            print("No alerts found to visualize.")
            return

        attack_types = []
        for log in logs:
            if "PORT SCAN" in log:
                attack_types.append("Port Scan")
            elif "SYN FLOOD" in log:
                attack_types.append("SYN Flood")

        counts = Counter(attack_types)
        
        plt.figure(figsize=(8, 6))
        plt.bar(counts.keys(), counts.values(), color=['#ff4d4d', '#ffa64d'])
        plt.title("Network Intrusion Detection System - Attack Summary")
        plt.xlabel("Attack Type")
        plt.ylabel("Number of Alerts")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig("ids_visualization.png")
        print("📊 Visualization saved as ids_visualization.png")
        plt.show()

    except FileNotFoundError:
        print("Log file not found. Run the NIDS engine first.")

if __name__ == "__main__":
    visualize_alerts()
