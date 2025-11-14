from enum import Enum

class QualityLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    very_high = "very_high"
