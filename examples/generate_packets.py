#!/usr/bin/env python3
"""Emit deterministic synthetic packets without device or participant data."""
import json


def generate_packets(count=20):
    return [{"Timestamp": i, "DataPacketValue": [i + channel / 10 for channel in range(6)]}
            for i in range(count)]


if __name__ == "__main__":
    print(json.dumps(generate_packets(), indent=2))
