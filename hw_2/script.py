import ipaddress
import validators
import argparse
import subprocess

def validate_ip_address(address):
    try:
        ip = ipaddress.ip_address(address)
        return True
    except ValueError:
        print("Host {} is not valid".format(address))
        exit(1)
        
        
##parsing arguments to get host
parser = argparse.ArgumentParser(description='PMTUD')
parser.add_argument('host', help='host')
args = parser.parse_args()
host = args.host

##checking host validity
host_is_valid = validators.domain(host)
if not host_is_valid and not validate_ip_address(host):
    #error will be printed in function
    exit(1)

##checking if icmp is enabled
sub_process = subprocess.run(
    ["cat", "/proc/sys/net/ipv4/icmp_echo_ignore_all"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

if sub_process.stdout == 1:
    print('ICMP is blocked.')
    exit(1)

##binary search for mtu
left = 0
right = 8973

while left < right - 1:
    middle = (left + right) // 2
    
    sub_process = subprocess.run(
        ["ping", host, "-M", "do", "-s", str(middle), "-c", "5"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if sub_process.returncode == 1:
        right = middle
    elif sub_process.returncode == 0:
        left = middle
    else:
        print(sub_process.stderr)
        exit(1)

print("MTU = ", left + 28)