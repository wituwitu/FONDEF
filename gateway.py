import requests
import base64


def get_fragments(device_id, limit, username, password):
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
	byte_array = []
	values = parsed["data"]
	for val in values:
		byte_array.append(bytearray.fromhex(val["data"]))
	return byte_array

print(get_fragments("4d5a87", 100, "5dc465f4e833d941f6cc4cd3", "0f245424186a3148cc2d5bbb240509f9"))