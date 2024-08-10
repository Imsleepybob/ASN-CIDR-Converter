#Script created by Imsleepy
import gzip
import json
from ipaddress import ip_network, summarize_address_range, ip_address
from google.colab import files

# Upload ipinfo dataset JSON (.gz) file
uploaded = files.upload()

file_name = list(uploaded.keys())[0]

entries = []

with gzip.open(file_name, 'rt', encoding='utf-8') as file:
    for line in file:
        try:
            entry = json.loads(line)
            entries.append(entry)
        except json.JSONDecodeError:
            continue

#  Extract `start_ip` and `end_ip` for the specific ASN
as_number = "AS0000"  # Specify the ASN here
ip_ranges = []

for entry in entries:
    if entry.get('asn') == as_number:
        start_ip = entry.get('start_ip')
        end_ip = entry.get('end_ip')
        if start_ip and end_ip:
            ip_ranges.append((start_ip, end_ip))

# Converting (start_ip, end_ip) pairs to CIDR
cidr_blocks = []

for start_ip, end_ip in ip_ranges:
    start = ip_address(start_ip)
    end = ip_address(end_ip)
    cidr_range = list(summarize_address_range(start, end))
    cidr_blocks.extend([str(cidr) for cidr in cidr_range])

for cidr in cidr_blocks:
    print(cidr)
