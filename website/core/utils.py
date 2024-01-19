from enum import StrEnum


class CIStrEnum(StrEnum):
    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.value == value.lower():
                return member


# class CITupleEnum(CIStrEnum):
#     def __new__(cls, *values):
#         obj = str.__new__(cls)
#         # first value is canonical value
#         obj._value_ = values[0]
#         for other_value in values[1:]:
#             cls._value2member_map_[other_value] = obj
#         # obj._all_values = values
#         return obj
