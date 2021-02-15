from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class DinosaurSexEnum(str, Enum):
    female = "female"
    male = "male"


class _SpeciesTaming(BaseModel):
    non_violent: bool
    violent: bool
    taming_ineffectiveness: float
    affinity_needed0: int
    affinity_increase_pl: int
    food_consumption_base: float
    food_consumption_mult: int
    wake_affinity_mult: Optional[float]
    wake_food_depl_mult: Optional[int]


class _SpeciesStat(BaseModel):
    base: int

    # Still unsure what these are
    f1: int
    f2: float
    f3: int
    f4: float


class _SpeciesColor(BaseModel):
    name: str
    colors: List[str]


class Species(BaseModel):
    name: str
    variants: List[str] = []
    #    colors: Optional[List[_SpeciesColor]] # Parsing trouble
    immobilized_by: List[str]
    taming: _SpeciesTaming

    # Stats
    health: _SpeciesStat
    stamina: _SpeciesStat
    oxygen: Optional[_SpeciesStat]
    food: Optional[_SpeciesStat]
    water: Optional[_SpeciesStat]
    temperature: Optional[_SpeciesStat]
    weight: Optional[_SpeciesStat]
    melee_damage_multiplier: _SpeciesStat
    speed_multiplier: _SpeciesStat
    temperature_fortitude: _SpeciesStat
    crafting_speed_multiplier: Optional[_SpeciesStat]
    torpidity: Optional[_SpeciesStat]

    tamed_base_health_multiplier: int
    no_imprinting_for_speed: bool
    does_not_use_oxygen: bool
    displayed_stats: int


# Runtime check the columns/models
