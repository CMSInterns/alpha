from netmiko import ConnectHandler
import time
ssh=ConnectHandler(device_type="cisco_ios",host='10.7.14.14',username="rit",password="pan")

print(ssh.find_prompt())
output = ssh.send_command("sh int counters error | ex 0")
int_l = []
int_l = output.split('\n')
print(output.split('\n'))
print('\n\n\n')

if(int_l[2]):
	for i in int_l:
		print(i+'\n')
else:
	print("Sorry Empty")
m1 = {}
map_return = {}
output_span= ssh.send_command("sh spanning-tree active")
print(output_span.split('\n'))
print('\n\n\n')
flag= 0
print(output_span.split('\n')[6])
l = output_span.split('\n')
p=12
for k in range(len(output_span.split('\n'))):
	if(k == p):
		print(output_span.split('\n')[k])
		print(output_span.split('\n')[k+6])
		m1[output_span.split('\n')[k]] = output_span.split('\n')[k+6] 
		p+=9
p=12
time.sleep(3)
for lo in range(0,2):
	for k in range(len(l)):
		if(k == p):
			#print(l[k])
			#print(l[k+6])
			if(m1[l[k]] != l[k+6]):
				map_return[l[k]] = l[k+6]
				print(l[k] + "\n" + l[k+6])
				flag = 1
			else:
				print("No change Observed")
				flag = 0
			p+=9
	p=12
	time.sleep(3)
if(flag == 0):
	print("No Changes in the Past 1 minute")
#print(output_span,sep='\n- ')

///FOR THE SPANNING-TREE KPI ,PLEASE RETURN map_return WHICH HAS THE RESULT
/// FOR THE "sh int counters" KPI,PLEASE RETURN int_l WHICH HAS THE RESULT