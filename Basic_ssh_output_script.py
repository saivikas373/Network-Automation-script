from netmiko import ConnectHandler      

device = {
    'device_type':'cisco_ios', #change as per device details 
    'host':'10.10.10.5',
    'username':'QOPNSJ12',
    'password':'OEDJFK12R@jd'
}

connect = ConnectHandler(**device)

output = connect.send_command("sh run ")
print(output)


