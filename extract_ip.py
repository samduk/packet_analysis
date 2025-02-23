import pyshark
import requests

pcap_file = "emotets.pcap"
cap = pyshark.FileCapture(pcap_file, keep_packets=False)  # Avoid memory overload

# Extract unique destination IPs
ip_addresses = set()

for pkt in cap:
    if "IP" in pkt and "TCP" in pkt:
        ip_addresses.add(pkt.ip.dst)

cap.close()

with open("output.txt", "w") as f:
    for ip in ip_addresses:
        f.write(ip + "\n")

def get_ip_info(ip):
    url = f"https://ipinfo.io/{ip}/json"
    response = requests.get(url, timeout=5)  # Fetch data with a timeout
    data = response.json()
    city = data.get("city", "Unknown")
    country = data.get("country", "Unknown")
    return f"City: {city}, Country: {country}"

with open("report.txt", "w") as f:
    for ip in ip_addresses:
        location_info = get_ip_info(ip)
        f.write(f"IP: {ip} -> {location_info}\n")

print("Processing complete! Check 'report.txt' for results.")
