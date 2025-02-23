import pyshark
import os

pcap_file = "emotets.pcap"
cap = pyshark.FileCapture(pcap_file, keep_packets=False)  # Avoid memory overload

with open("output.txt", "a") as f:
    for pkt in cap:
        if "IP" in pkt and "TCP" in pkt:
            f.write(f"Source IP: {pkt.ip.src}, Destination IP: {pkt.ip.dst}\n")

cap.close()  # Close capture after processing

os.system("for i in $(cat output.txt | awk -F ' ' '{print $3}' | cut -d ',' -f1 | sort -u); do "
          "curl -s https://ipinfo.io/$i/json | jq -r '\"City: \" + .city + \" Country: \" + .country' >> report.txt; done")
