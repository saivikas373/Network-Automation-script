from netmiko import ConnectHandler
with open("sampletxtf.txt","r") as file:
    each_line = file.readlines()
    each_line = [line.strip for line in each_line]

ip_list = each_line
 


first_device = {
  'device_type':'a10',
  'username':'Pa',
  'password':'a'
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

        linelook = f"{device['host']}{clean} \n"

        with open("multiplea10.txt", "a") as f:
             f.write(linelook)
             print("output saved to multiplea10.txt ")
    except Exception as e:
        print(f"{device['host']} output failed ")