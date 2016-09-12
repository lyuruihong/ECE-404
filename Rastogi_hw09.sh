#! /usr/bin/bash
sudo iptables -A OUTPUT -p all -j ACCEPT 
sudo iptables -A INPUT -s 199.95.207.0/255.255.255.0 -j DROP
sudo iptables -A INPUT -p icmp -j REJECT
sudo iptables -A INPUT -p tcp --dport 22 -s ! ecn.purdue.edu -j REJECT
sudo iptables -A INPUT -p tcp --dport 113 -j ACCEPT
sudo iptables -t nat -A PREROUTING -p tcp -d 192.168.0.102 --dport 10 -j DNAT --to 192.168.0.102:22
sudo iptables -A FORWARD -p tcp -j ACCEPT
sudo iptables -A INPUT --dport 80 -s ! 192.168.0.104 -j REJECT
