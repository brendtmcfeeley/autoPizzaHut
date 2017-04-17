from scapy.all import *

# Code borrowed from Ted Benson
# https://blog.cloudstitch.com/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8

def arp_display(pkt):
  if pkt[ARP].op == 1: #who-has (request)
    if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
      print ("ARP Probe from: " + pkt[ARP].hwsrc)

print (sniff(prn=arp_display, filter="arp", store=0, count=10))
