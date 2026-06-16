from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP
from datetime import datetime
from detector import detect_port_scan
from bruteforce_detector import detect_bruteforce
from anomaly_detector import detect_anomaly


def packet_callback(packet):

    if packet.haslayer(IP):
        detect_anomaly()
        current_time = datetime.now().strftime("%H:%M:%S")

        source_ip = packet[IP].src
        destination_ip = packet[IP].dst

        source_port = "N/A"
        destination_port = "N/A"
        protocol = "OTHER"

        if packet.haslayer(TCP):
            protocol = "TCP"
            source_port = packet[TCP].sport
            destination_port = packet[TCP].dport
            detect_port_scan(
                               source_ip,
                               destination_port
             )
            detect_bruteforce(
               source_ip,
               destination_port
            )


        elif packet.haslayer(UDP):
            protocol = "UDP"
            source_port = packet[UDP].sport
            destination_port = packet[UDP].dport

        print(f"\nTime           : {current_time}")
        print(f"Source         : {source_ip}:{source_port}")
        print(f"Destination    : {destination_ip}:{destination_port}")
        print(f"Protocol       : {protocol}")
        print("-" * 50)

print("Capturing 10 packets...\n")

sniff(prn=packet_callback, count=50)

print("\nCapture Complete")