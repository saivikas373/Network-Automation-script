from netmiko import ConnectHandler
import csv
import yaml


with open("devices.yaml") as f:
    devices = yaml.safe_load(f)
def bgp_ip_summary(device):
    try:
        connect = ConnectHandler(**device)
        output = connect.send_command("sh ip bgp summary vrf BHN_VIDEO_VRF ")
        connect.disconnect()
        
        clean = output.strip().replace('\n' '|')
        with open("bgp_summary.csv" , "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([device["host'],clean])
        print(f"Done:{device["host"]}"
    except Exception as e:
        print(f"failed for host {device["host"]}-{e}")
for device in devices:
    run bgp_ip_summary(device)