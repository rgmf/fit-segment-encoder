from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from functools import reduce
from typing import List
from struct import pack

from profile import Record


class LeaderType(str, Enum):
    OVERALL = "overall"
    PERSONAL_BEST = "personal_best"


@dataclass
class FileId:
    serial_number: int
    time_created: int
    manufacturer: str
    type: str = "segment"


@dataclass
class SegmentId:
    name: str
    sport: str
    enabled: bool


@dataclass
class SegmentLeaderboardEntry:
    message_index: int
    segment_time: int
    leader_type: LeaderType
    name: str = None
    activity_id: int = None
    activity_id_string: str = None
    group_primary_key: int = None


@dataclass
class SegmentPoint:
    message_index: int
    latitude: int
    longitude: int
    distance: float
    altitude: float
    best_time: int = None
    leader_time: int = None


class FitSegmentEncoder:
    """Class to be used to encode segment FIT files.

    Segment FIT files will contain:
    - One file_id message with type=segment, time_created, manufacturer, product and other fields.
    - One file_creator.
    - One segment_id message with name, sport and enabled=True.
    - One or two segment_leaderboard_entry messages with information about overall and/or personal_best data.
    - One segment_lap message.
    - Several segment_point messages.
    """

    # According to the SDK date_time is computed counting the seconds since this datetime: UTC 00:00 Dec 31 1989
    date_time_seconds_since = datetime(1989, 12, 31, 0, 0, 0).timestamp()

    def __init__(self, name: str, sport: str):
        self._data_bytes = b""

        self._segment_id = SegmentId(name, sport, True)
        self._leaderboards: List[SegmentLeaderboardEntry] = []

        self._encode_message_file_id()
        self._encode_message_file_creator()

    def _encode_message_file_id(self):
        """Encode the file_id message of type=segment."""
        record = Record("file_id")
        self._data_bytes += record.bytes

    def _encode_message_file_creator(self):
        """Encode the file_creator message."""
        record = Record("file_creator")
        self._data_bytes += record.bytes

    def add_leaderboard(self, segment_time: int, leader_type: LeaderType):
        self._leaderboards.append(SegmentLeaderboardEntry(len(self._leaderboards), segment_time, leader_type))

    def end_and_get(self):
        """Finish FIT segment binary encoded data and return it.

        The return value is ready for saving into a binary file.
        """
        data_size = len(self._data_bytes)

        header = pack("BBHI", 14, 1, 1, data_size)
        header += b".FIT"
        crc_header = Crc()
        crc_header.update(header)
        header += pack("H", crc_header.value)

        crc_file = Crc()
        crc_file.update(self._data_bytes)
        crc_pack = pack("H", crc_file.value)

        return header + self._data_bytes + crc_pack


class Crc(object):
    """FIT file CRC computation."""

    CRC_TABLE = (
        0x0000, 0xCC01, 0xD801, 0x1400, 0xF001, 0x3C00, 0x2800, 0xE401,
        0xA001, 0x6C00, 0x7800, 0xB401, 0x5000, 0x9C01, 0x8801, 0x4400,
    )

    FMT = "H"

    def __init__(self, value=0, byte_arr=None):
        self.value = value
        if byte_arr:
            self.update(byte_arr)

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.value or "-")

    def __str__(self):
        return self.format(self.value)

    def update(self, byte_arr):
        """Read bytes and update the CRC computed."""
        if byte_arr:
            self.value = self.calculate(byte_arr, self.value)

    @staticmethod
    def format(value):
        """Format CRC value to string."""
        return "0x%04X" % value

    @classmethod
    def calculate(cls, byte_arr, crc=0):
        """Compute CRC for input bytes."""
        for byte in bytearray(byte_arr):
            # Taken verbatim from FIT SDK docs
            tmp = cls.CRC_TABLE[crc & 0xF]
            crc = (crc >> 4) & 0x0FFF
            crc = crc ^ tmp ^ cls.CRC_TABLE[byte & 0xF]

            tmp = cls.CRC_TABLE[crc & 0xF]
            crc = (crc >> 4) & 0x0FFF
            crc = crc ^ tmp ^ cls.CRC_TABLE[(byte >> 4) & 0xF]
        return crc


if __name__ == '__main__':
    with open("segment_class.fit", "wb") as fd:
        encoder = FitSegmentEncoder("Nombre", "cycling")
        fd.write(encoder.end_and_get())
