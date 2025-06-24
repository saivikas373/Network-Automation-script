from netmiko import ConnectHandler
device = {
  'device_type':'a10',    #used a10 device
  'host':'10.10.10.26',
  'username':'frrdvnkjf',
  'password':'rghkenfkrgn'
}


try :
    connect = ConnectHandler(**device)

    output = connect.send_command("show bootimage")
    connect.disconnect()
    clean = output.strip().replace('\n' , '|')     #we are striping the output into single line
    
    linelook = f"{device['host']}{clean} \n"       # formating the output as per needed , in our case we printed ip and output coloumn
    
    with open("singlea10.txt", "a") as f:           #creating the file and appending to f 
         f.write(linelook)                          # adding the output into the file 
         print("output saved ")
except Exception as e:                              # you can keep any object instead of e just to defining the error 
    print(e)
