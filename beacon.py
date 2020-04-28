# This is the beacon module to be run for experiments...

from network import Sigfox
import socket
import binascii
import time


def zfill(string, width):
	if len(string) < width:
		return ("0" * (width - len(string))) + string
	else:
		return string


# init Sigfox for RCZ4 (Chile)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ4)
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
s.setblocking(True)
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)
s.settimeout(10)

c = 10
submerged_time = 60

# Wait for the beacon to be submerged
time.sleep(submerged_time)

# Send 10 messages to the Sigfox network to test connectivity
for i in range(100):
	string = "{}{}".format(zfill(str(c), 3), zfill(i, 3))
	payload = bytes(str(i).encode())
	print("Sending...")
	s.send(payload)
	print("Sent.")
	print(payload)
	time.sleep(30)

print("Done")
