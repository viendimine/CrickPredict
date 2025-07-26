# import json
# import requests

# # Get ISO code to country name mapping
# resp = requests.get("https://flagcdn.com/en/codes.json")
# codes = resp.json()

# # Flip the key-value so country name is key, ISO is value
# mapping = {
#     country_name: f"https://flagcdn.com/w320/{iso_code}.png"
#     for iso_code, country_name in codes.items()
# }

# # Print as formatted JSON
# print(json.dumps(mapping, indent=2))


