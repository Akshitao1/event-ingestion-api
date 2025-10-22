#!/usr/bin/env python3
import json

# Test the JSON format
test_event = {
    "click_event_id": None,
    "click_event_query_parameters": "jz=5mjdx73101267c3b7f3f87636d6477dd46b19AIALVA7UAEAQAAAAAD2AC",
    "conv_type": "3",
    "cookie_event": True,
    "event_timestamp": 1767086892000,
    "family_pixel_hashid": None,
    "id": "JTSE-12345_1cb10176-251e-4b71-bc6f-41de16312a07",
    "ip": "172.56.209.0",
    "jclick_id": "1cb10176-251e-4b71-bc6f-41de16312a07",
    "jx": "",
    "jz": "5mjdx73101267c3b7f3f87636d6477dd46b19AIALVA7UAEAQAAAAAD2AC",
    "pixel_hashid": "mjdx",
    "pixel_s2s_event": False,
    "query_parameters": {"a": "3", "c": "mjdx"},
    "ref_number": "US_EN_97_043800_2250981",
    "referrer_url": None,
    "shadow_event": False,
    "user_agent": "Mozilla/5.0...",
    "user_fp": "817d5da2-bb2c-4b05-ae98-c2f09cb1f8c75",
    "reason": "JTSE-12345"
}

# Test JSON serialization
json_string = json.dumps(test_event)
print("JSON String:")
print(json_string)
print("\nIs valid JSON:", json.loads(json_string) is not None)

# Test writing to file
with open("test_event.json", "w") as f:
    f.write(json_string)

print("\nFile written successfully!")
