from dataclasses import dataclass, field
from messaging import message_t, say

@dataclass
class place_t:
    entrance_lines: list[message_t]=None

def place_load(place=place_t):
    if place.entrance_lines:
        for line in place.entrance_lines:
            say(line)