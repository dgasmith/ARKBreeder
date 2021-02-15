import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict

import tqdm

# Add a relative system path for arkbreeder since it isn't an installable module
sys.path.insert(1, str(Path(".").absolute().parent.parent))

from arkbreeder.models import Species


# Utility functions
def change_case(string: str) -> str:
    string = string
    ret = [string[0]]
    for c in string[1:]:
        if c in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            ret.append("_")
            ret.append(c.lower())
        else:
            ret.append(c)

    return "".join(ret).lower()


def change_dict_case(dictionary: Dict[str, Any]) -> Dict[str, Any]:
    return {change_case(k): v for k, v in dictionary.items()}


with open("values.json") as handle:
    raw_data = json.load(handle)

BASE_STAT_ORDER = [
    "health",
    "stamina",
    "oxygen",
    "food",
    "water",
    "temperature",
    "weight",
    "melee_damage_multiplier",
    "speed_multiplier",
    "temperature_fortitude",
    "crafting_speed_multiplier",
    "torpidity",
]

STAT_DATA_ORDER = ["base", "f1", "f2", "f3", "f4"]

parsed_data = {
    "version": raw_data["version"],
    "format": raw_data["format"],
}
"""
        {
            "name": "Rockwell",
            "blueprintPath": "/Game/Aberration/Boss/Rockwell/Rockwell_Character_BP_Easy.Rockwell_Character_BP_Easy",
            "variants": [ "Aberration", "Boss", "Gamma" ],
            "fullStatsRaw": [
                [ 42000, 0.2, 0.2, 0.3, 0 ],
                [ 400, 0.1, 0.1, 0, 0 ],
                [ 350, 0.06, 0, 0.5, 0 ],
                [ 2000, 0.1, 0.1, 0, 0 ],
                [ 2600, 0.1, 0.1, 0, 0 ],
                null,
                null,
                [ 3000, 0.02, 0.02, 0, 0 ],
                [ 1, 0.05, 0.04, 0.3, 0.3 ],
                [ 1, 0, 0, 0, 0 ],
                null,
                null
            ],
            "immobilizedBy": [],
            "taming": {
                "nonViolent": false,
                "violent": false,
                "tamingIneffectiveness": 1.5,
                "affinityNeeded0": 8500,
                "affinityIncreasePL": 150,
                "foodConsumptionBase": 0.002066,
                "foodConsumptionMult": 150
            },
            "TamedBaseHealthMultiplier": 1,
            "NoImprintingForSpeed": false,
            "doesNotUseOxygen": false,
            "displayedStats": 927
        },
"""

species = defaultdict(list)
total_parsed = 0
for species_raw in raw_data["species"]:
    # print(species_raw["name"])

    full_stats_raw = species_raw.pop("fullStatsRaw")

    species_raw = change_dict_case(species_raw)
    species_raw["taming"] = change_dict_case(species_raw["taming"])
    species_raw["taming"]["affinity_increase_pl"] = species_raw["taming"].pop("affinity_increase_p_l")

    if len(full_stats_raw) != len(BASE_STAT_ORDER):
        raise KeyError("Stat lengths do not match!")

    for key, stat_data in zip(BASE_STAT_ORDER, full_stats_raw):

        # Not all dino's have data for each stat
        if stat_data is None:
            continue

        if len(stat_data) != len(STAT_DATA_ORDER):
            raise KeyError("Stat data lengths do not match")

        species_raw[key] = {k: v for k, v in zip(STAT_DATA_ORDER, stat_data)}

    # Final cleanup
    if "colors" in species_raw:
        species_raw["colors"] = [x for x in species_raw["colors"] if x is not None]

    if ("variants" in species_raw) and (species_raw["variants"] is not None):
        skip = False
        for skip_key in ["Mission", "Boss", "Minion", "Mega"]:
            if skip_key in species_raw["variants"]:
                skip = True

        if skip:
            continue

    #        if "Genesis" not in species_raw["variants"]:
    #            continue

    model = Species(**species_raw)
    species[model.name].append(model)
    total_parsed += 1

print(f"Total species parsed:  {total_parsed}")
print(f"Total species skipped: {len(raw_data['species']) - total_parsed}")

final_data = []

for name, species_list in species.items():

    # Easy cases
    if len(species_list) == 1:
        final_data.append(species_list[0].dict())
        continue

    # Known bad stats
    if name in ["Ferox", "Jerboa"]:
        print(f"Skipping {name} due to unresolvable conflicts")
        continue

    # Edge cases
    for x in species_list:
        if species_list[0].health.base != x.health.base:
            raise ValueError(f"Species {name} stats values do not match")

    final_data.append(species_list[0].dict())

with open("species_data.json", "w") as handle:
    json.dump(final_data, handle, indent=2)
