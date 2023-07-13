#To check the health of the system...
import os
import sys
import shutil
import socket
import psutil

def check_reboot():
    """Returns True if the computer has a pending reboot."""
    return os.path.exists("/run/reboot-required")

def check_disk_full(disk,min_GB,min_percent):
    """Returns True if there isn't enough disk space, False otherwise."""
    du=shutil.disk_usage(disk)
    #calculate the persentage of free space
    percent_free = 100 * du.free / du.total
    #calculate how many free gigabytes
    gigabytes_free = du.free / 2**30
    if gigabytes_free < min_GB or percent_free < min_percent:
        return True
    return False


def check_root_full():
    """Returns True if the root partition is full, False otherwise."""
    return check_disk_full(disk="/", min_GB=2, min_percent=10)

def check_cpu_constrained():
    """Returns True if the cpu is having too much usage, False otherwise."""
    return psutil.cpu_percent(1) > 75

def check_no_network():
    """Returns True if it fails to resolve google's URL, False otherwise."""
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True

def main():
    checks=[
        (check_reboot, "Pending Reboot"),
        (check_root_full, "Root partition full"),
        (check_cpu_constrained, "CPU load too high."),
        (check_no_network, "No working network."),
    ]
    everything_ok= True
    for check, msg in checks:
        if check():
            print(msg)
            everything_ok= False


    if not everything_ok:
        sys.exit(1)


    print("Everything ok.")
    sys.exit(0)

main()
