import cloudsight
from nutritionix import Nutritionix
import json

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

auth = cloudsight.SimpleAuth('uquMfLmzXYvnSwR6g52zFA')
api = cloudsight.API(auth)

nix = Nutritionix(app_id="29a3ea8f", api_key="f04d3ef0949ad6d732ee4397afe6f374")

with open('coke.jpg', 'rb') as f:
    response = api.image_request(f, 'your-file.jpg', {
        'image_request[locale]': 'en-US',
    })
status = api.image_response(response['token'])
print status
if status['status'] != cloudsight.STATUS_NOT_COMPLETED:
    # Done!
    pass
status = api.wait(response['token'], timeout=60)
result = nix.search(status["name"], results="0:1").json()["hits"][0]["fields"]["item_id"]
result=nix.item(id=result).json()
updated_list=dict()
with open("list.txt", "r") as filestream:
    for line in filestream:
        print line
        currentline = line.split(",")
        print currentline[1][:-1]
        updated_list[currentline[0]] = result[currentline[1][:-1]]
print updated_list
