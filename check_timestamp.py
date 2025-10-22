#!/usr/bin/env python3
"""
Check what the timestamp 1761041096000 represents
"""
import datetime

# Convert the timestamp from milliseconds to seconds
timestamp_ms = 1761041096000
timestamp_seconds = timestamp_ms / 1000

# Convert to datetime
dt = datetime.datetime.fromtimestamp(timestamp_seconds)

print(f"Timestamp: {timestamp_ms}")
print(f"Date: {dt}")
print(f"Year: {dt.year}")
print(f"Month: {dt.month}")
print(f"Day: {dt.day}")

# Check what 2025-10-21 should be
target_date = datetime.datetime(2025, 10, 21, 12, 0, 0)
target_timestamp = int(target_date.timestamp()) * 1000

print(f"\nTarget date 2025-10-21 should be around: {target_timestamp}")
print(f"Difference: {timestamp_ms - target_timestamp}")

# Let's also check what the current timestamp generation produces
import random
from datetime import datetime

def get_time_stamp(datestr):
    """Generate timestamp from date string"""
    day = int(datestr.split('-')[2])
    month = int(datestr.split('-')[1])
    year = int(datestr.split('-')[0])

    random_hour = random.randint(10, 15)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)

    random_datetime = datetime(year, month, day, random_hour, random_minute, random_second)
    epoch_timestamp = int(random_datetime.timestamp())

    return epoch_timestamp * 1000

# Test with 2025-10-21
test_timestamp = get_time_stamp("2025-10-21")
test_dt = datetime.fromtimestamp(test_timestamp / 1000)

print(f"\nTest with 2025-10-21:")
print(f"Generated timestamp: {test_timestamp}")
print(f"Generated date: {test_dt}")
