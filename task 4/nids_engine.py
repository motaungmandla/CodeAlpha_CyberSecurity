from scapy.all import sniff, IP, TCP, UDP
import time
import json
from collections import defaultdict

# manually npcap.exe -v= 1.8
# Custom Detection Rules
RULES = {
    "PORT_SCAN_THRESHOLD": 15,  # Alert if >15 ports hit in 10 seconds
    "SYN_FLOOD_THRESHOLD": 50,  # Alert if >50 SYN packets in 5 seconds
    "TIME_WINDOW": 10           # Time window for analysis (seconds)
}

class NetworkIDS:
    def __init__(self):
        self.connection_counts = defaultdict(set)
        self.syn_counts = defaultdict(int)
        self.alerts = []
        self.start_time = time.time()

    def process_packet(self, packet):
        if packet.haslayer(IP) and packet.haslayer(TCP):
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            dst_port = packet[TCP].dport
            flags = packet[TCP].flags

            # Track unique ports per source IP (Port Scan Detection)
            self.connection_counts[(src_ip, dst_ip)].add(dst_port)

            # Track SYN packets (SYN Flood Detection)
            if flags == 'S':
                self.syn_counts[(src_ip, dst_ip)] += 1

            self.check_alerts(src_ip, dst_ip)

    def check_alerts(self, src_ip, dst_ip):
        # Port Scan Check
        if len(self.connection_counts[(src_ip, dst_ip)]) > RULES["PORT_SCAN_THRESHOLD"]:
            self.trigger_alert("PORT SCAN DETECTED", src_ip, dst_ip)
            # Reset to prevent spamming alerts
            self.connection_counts[(src_ip, dst_ip)] = set()

        # SYN Flood Check
        if self.syn_counts[(src_ip, dst_ip)] > RULES["SYN_FLOOD_THRESHOLD"]:
            self.trigger_alert("SYN FLOOD DETECTED", src_ip, dst_ip)
            self.syn_counts[(src_ip, dst_ip)] = 0

    def trigger_alert(self, alert_type, src_ip, dst_ip):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        alert_msg = f"[{timestamp}] 🚨 {alert_type} | Source: {src_ip} -> Destination: {dst_ip}"
        print(alert_msg)
        self.alerts.append(alert_msg)
        
        # Log to file
        with open("ids_alerts.log", "a") as f:
            f.write(alert_msg + "\n")

    def start_sniffing(self, interface=None):
        print("🛡️  Python NIDS Started. Monitoring traffic... Press Ctrl+C to stop.")
        try:
            # Filter for TCP traffic to reduce load
            sniff(iface=interface, prn=self.process_packet, filter="tcp", store=0)
        except KeyboardInterrupt:
            print("\n🛑 NIDS Stopped. Saving final report...")
            self.save_report()

    def save_report(self):
        with open("ids_report.json", "w") as f:
            json.dump(self.alerts, f, indent=4)
        print(f"✅ Report saved. Total alerts: {len(self.alerts)}")

if __name__ == "__main__":
    # You can specify your network interface, e.g., interface="Ethernet"
    ids = NetworkIDS()
    ids.start_sniffing()
