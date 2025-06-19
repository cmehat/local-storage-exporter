import re
import logging
import os


def convert_storage_capacity_to_bytes(storage_capacity: str) -> int:
    # fmt: off
    # Compile the regex pattern once
    STORAGE_CAPACITY_PATTERN = re.compile(r"(\d*[,|\.]?\d+)([a-zA-Z]+)")
    STORAGE_UNITS = {
        "Ki": 1024, "Mi": 1024**2, "Gi": 1024**3, "Ti": 1024**4, "Pi": 1024**5, "Ei": 1024**6,
        "k": 10**3, "M": 10**6,    "G": 10**9,    "T": 10**12,   "P": 10**15,   "E": 10**18
    }
    # fmt: on

    match = STORAGE_CAPACITY_PATTERN.match(storage_capacity)
    if match:
        value, unit = match.groups()
        if unit in STORAGE_UNITS:
            return int(float(value) * STORAGE_UNITS[unit])
    return int(storage_capacity)


def convert_str_to_seconds(timestr: str) -> float:
    units = {
        "ms": 0.001,
        "s": 1,
        "m": 60,
        "h": 3600,
    }
    number = 0
    unit = ""

    # Extract number and unit from string
    for char in timestr:
        if char.isdigit() and unit == "":
            number = number * 10 + int(char)
        else:
            unit += char

    if not unit:
        # default to seconds if no unit is provided
        return number
    if unit not in units:
        raise ValueError(f"Invalid time unit: {unit}")
    return number * units[unit]

def createLogger(name: str) -> logging.Logger:
    """
    Create a logger with the specified name and set its level to LOGLEVEL env or INFO.
    """
    LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
    loglevel = logging.getLevelNamesMapping().get(LOGLEVEL, logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(loglevel)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)
    logger.addHandler(handler)
    if LOGLEVEL not in logging.getLevelNamesMapping():
        # This check is redundant but ensures that we log a warning if the LOGLEVEL is invalid and we need to create the logger first.
        logger.warning(f"Invalid log level: {LOGLEVEL}. Must be one of {list(logging.getLevelNamesMapping().keys())}, defaulting to INFO.")

    return logger