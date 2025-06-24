from netmiko import ConnectHandler
import csv
with open("sampletxtf.txt","r") as file:
    each_line = file.readlines()
    each_line = [line.strip() for line in each_line]

ip_list = each_line
 


first_device = {
  'device_type':'a10',
  'username':'P1',
  'password':'O'
}

print(ip_list)

for ip in ip_list:
    device = first_device.copy()
    device['host'] = ip



    try :
        
        connect = ConnectHandler(**device)
        output = connect.send_command("show bootimage")
        connect.disconnect()
        clean = output.strip().replace('\n' , '|')

        with open("a10auditcsvfile.csv", "a", newline='') as csvfile:
           writer = csv.writer(csvfile)
           writer.writerow([device['host'], clean])
           print("output saved to a10auditcsvfile.csv")


    except Exception as e:
        print(f"{device['host']} output failed ")