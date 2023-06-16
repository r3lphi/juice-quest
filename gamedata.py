from dataclasses import dataclass, field
from date import date_t
from world import interactable_t

@dataclass
class gamedata_t:
    date: date_t=field(default_factory=date_t)
    pockets: list[interactable_t]=None
