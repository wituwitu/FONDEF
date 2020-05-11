import requests
import base64
import csv
import json


def get_messages(device_id, limit, username, password):
	key = "{}:{}".format(username, password)
	auth = "Basic {}".format(base64.b64encode(key.encode()).decode("utf-8"))
	url = "https://api.sigfox.com/v2/devices/{}/messages".format(device_id)
	payload = ''
	headers = {
		"Accept": "application/json",
		"Content-Type": "application/x-www-form-urlencoded",
		"Authorization": auth,
		"cache-control": "no-cache"
	}
	params = {"limit": limit}
	response = requests.request("GET", url, data=payload, headers=headers, params=params)
	parsed = response.json()
	msg_array = []
	values = parsed["data"]
	for val in values:
		msg_array.append(bytes.fromhex(val["data"]).decode())
	return msg_array


with open("datos.json") as js:
	datos = json.load(js)
msg_array = get_messages(datos['device_id'], 100, datos["username"], datos["password"])

# (here we assume that messages can't be received out of order (the last message payload is always greater))
# Check if msg_array is naturally sorted from low to high
# If not, there are messages from a previous execution and there have been losses
# Filter msg_array so that it is sorted from low to high


def sorting_index(ls, i=0):
	if ls == sorted(ls):
		return i
	else:
		return sorting_index(ls[1:], i + 1)


sorted_array = msg_array[sorting_index(msg_array):]

n = 10
n_received = len(sorted_array)
c = int(msg_array[0][:3])
ratio = (n_received * 100 / n)
print("Received %d messages from %d [m] underwater." % (n_received, c))
print("%d percent of all messages." % ratio)


with open('datos.csv', 'a') as write:
	writer = csv.writer(write, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	writer.writerow([c, ratio])
