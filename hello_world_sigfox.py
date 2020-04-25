from network import Sigfox
import socket
import binascii
import time

# init Sigfox for RCZ4 (Chile)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ4)
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

# print Sigfox Device ID
print("ID: ", binascii.hexlify(sigfox.id()))
# print Sigfox PAC number
print("PAC: ", binascii.hexlify(sigfox.pac()))

# make the socket blocking

s.setblocking(True)

# configure it as uplink only
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

s.settimeout(10)
# send some bytes

for i in range(5):
    payload = bytes(str(i).encode())
    print("Sending...")
    s.send(payload)
    print("Sent.")
    print(payload)
    time.sleep(30)

print("Done")
