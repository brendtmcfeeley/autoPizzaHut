from scapy.all import *
import autoPH
import json

with open('custInfo.json') as data_file:
	dataStream = json.load(data_file)

def arp_display(pkt):
	print("Listening...")
	if pkt[ARP].op == 1: #who-has (request)
		if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
			if pkt[ARP].hwsrc == dataStream[0]['dashMacAddress']: # IoT
				autoPH.main()
			else:
        		print ("ARP Probe from unknown device: " + pkt[ARP].hwsrc)
        		print ("No click found.")

print (sniff(prn=arp_display, filter="arp", store=0, count=10))