from dataclasses import dataclass
from datetime import datetime
from functools import reduce
from struct import pack
from typing import List


date_time_seconds_since = datetime(1989, 12, 31, 0, 0, 0).timestamp()


FIT_BASE_TYPES = {
    "enum": 0,
    "sint8": 1,
    "uint8": 2,
    "sint16": 131,
    "uint16": 132,
    "sint32": 133,
    "uint32": 134,
    "string": 7,
    "float32": 136,
    "float64": 137,
    "uint8z": 10,
    "uint16z": 139,
    "uint32z": 140,
    "byte": 13,
    "sint64": 142,
    "uint64": 143,
    "uint64z": 144,
}


@dataclass
class Type:
    number: int
    size: int
    format: str


@dataclass
class Field:
    number: int
    name: str
    type: Type
    value: int


@dataclass
class Message:
    name: str
    number: int
    fields: List[Field]


FIT_MESSAGES = {
    "file_id": Message(
        name="file_id",
        number=0,
        fields=[
            Field(
                number=0,
                name="type",
                type=Type(FIT_BASE_TYPES["enum"], 1, "B"),
                value=34  # segment
            ),
            Field(
                number=1,
                name="manufacturer",
                type=Type(FIT_BASE_TYPES["uint16"], 2, "H"),
                value=1  # garmin
            ),
            Field(
                number=2,
                name="product",
                type=Type(FIT_BASE_TYPES["uint16"], 2, "H"),
                value=3121  # edge_530
            ),
            Field(
                number=3,
                name="serial_number",
                type=Type(FIT_BASE_TYPES["uint32z"], 4, "I"),
                value=0
            ),
            Field(
                number=4,
                name="time_created",
                type=Type(FIT_BASE_TYPES["uint32"], 4, "I"),
                value=int(datetime.now().timestamp() - date_time_seconds_since)
            ),
        ]
    ),
    "file_creator": Message(
        name="file_creator",
        number=49,
        fields=[
            Field(
                number=0,
                name="software_version",
                type=Type(FIT_BASE_TYPES["uint16"], 2, "H"),
                value=0
            ),
            Field(
                number=1,
                name="hardware_version",
                type=Type(FIT_BASE_TYPES["uint8"], 1, "B"),
                value=1  # garmin
            ),
        ]
    ),
}


class Record:
    """Contains definition and data message of the message global_msg."""
    def __init__(self, global_msg: str, architecture: int = 0):
        if global_msg not in FIT_MESSAGES:
            raise Exception(f"{global_msg} is not a supported message")

        endian = "<" if architecture == 0 else ">"
        message = FIT_MESSAGES[global_msg]
        number_of_fields = len(message.fields)

        self._definition_header = pack(endian + "B", 64)
        self._definition_message = pack(endian + "BBHB", 0, architecture, message.number, number_of_fields)
        self._definition_fields = [pack(endian + "BBB", f.number, f.type.size, f.type.number) for f in message.fields]

        self._data_header = pack(endian + "B", 0)
        self._data_messages = [pack(endian + f.type.format, f.value) for f in message.fields]

    @property
    def bytes(self):
        return (
            self._definition_header + self._definition_message +
            reduce(lambda x, y: x + y, self._definition_fields) +
            self._data_header + reduce(lambda x, y: x + y, self._data_messages)
        )
