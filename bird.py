import requests,socket,os,time

response_v4 = requests.get("https://api.ipify.org")
ipv4 = response_v4.text
response_v6 = requests.get("https://api64.ipify.org")
ipv6 = response_v6.text

with open(r'/etc/bird/bird6.conf','w+',encoding='utf-8') as test:
    test.write(f'router id {ipv4};\n')
    test.write('protocol bgp vultr\n')
    test.write('{\n')
    test.write('  local as 216354;\n')
    test.write(f'  source address {ipv6};\n')
    test.write('  import none;\n')
    test.write('  export all;\n')
    test.write('  graceful restart on;\n')
    test.write('  multihop 2;\n')
    test.write('  neighbor 2001:19f0:ffff::1 as 64515; #这个是Vultr服务器的ip\n')
    test.write('  password "Cyf56789.";\n')
    test.write('}\n')
    test.write('\n')
    test.write('protocol static {\n')
    test.write('  route 2a0f:7803:fec1::/48 reject;\n')
    test.write('  import all;\n')
    test.write('  export none;\n')
    test.write('}\n')
    test.write('\n')
    test.write('protocol kernel {\n')
    test.write('  scan time 20;\n')
    test.write('  import none;\n')
    test.write('  export filter {\n')
    test.write('    if source = RTS_STATIC then reject;\n')
    test.write('    krt_prefsrc = 2001:19f0:ffff::1;\n')
    test.write('    accept;\n')
    test.write('  };\n')
    test.write('}\n')
    test.write('\n')
    test.write('protocol device {\n')
    test.write('    scan time 60;\n')
    test.write('}')

os.system('service bird6 restart')
time.sleep(10)
print('Bird6启动完毕！')

hostname = socket.gethostname()
hostip = hostname.replace('ip-','').replace('-','.')
os.system('ip link add dev dummy1 type dummy')
os.system('ip link set dummy1 up')
os.system(f'ip addr add dev dummy1 {hostip}/32')

os.system(f'ping {hostip} -c 10 ')
print(f'广播IP：{hostip} 完毕')




    
