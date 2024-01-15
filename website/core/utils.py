from enum import StrEnum


class CIStrEnum(StrEnum):
    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.value == value.lower():
                return member
