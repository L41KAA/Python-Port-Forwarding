# Python-Port-Forwarding
Multi-threaded port forwarding implementation with python3.  
The purpose of this project is for setup port quickly and easily.  
This is helpful if the chisel/ssh/ligolo-ng setup is confusing you, and need something set up quick.  
This also helps in situations in which you're having trouble compiling for the target.

---

# Usage
```
./port_forward.py --help                                           
usage: thread.py [-h] --lport LPORT --dport DPORT --target TARGET --server SERVER

options:
  -h, --help            show this help message and exit
  --lport LPORT, -l LPORT
  --dport DPORT, -d DPORT
  --target TARGET, -t TARGET
  --server SERVER, -s SERVER


./port_forward.py --server <local_ip_to_bind> --lport <listening_port> --target <target_ip> --dport <desitnation_port>  

# Example forward 10.10.10.1:4444 to 10.10.10.2:7777
# 10.10.10.1 is the box you will run this from
./port_forward.py --server 10.10.10.1 --lport 4444 --target 10.10.10.2 --dport 7777 
```
