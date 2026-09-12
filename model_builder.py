#!/usr/bin/env python3
"""Hackathon packet conversion and rank-based event selection (no trained model)."""
import json
import os

import numpy as np
import pandas as pd

CHANNELS = [f"Value_{i}" for i in range(6)]


def packets_to_table(packets):
    """Expand six numeric channels; duplicate timestamps retain the last packet."""
    if not isinstance(packets, list):
        raise ValueError("packets must be a list")
    rows = {}
    for packet in packets:
        if not isinstance(packet, dict):
            raise ValueError("each packet must be an object")
        timestamp = packet.get("Timestamp")
        if isinstance(timestamp, bool) or not isinstance(timestamp, (str, int, float)):
            raise ValueError("Timestamp must be a string or finite number")
        if timestamp == "" or (isinstance(timestamp, (int, float)) and not np.isfinite(timestamp)):
            raise ValueError("Timestamp must be a string or finite number")
        values = packet.get("DataPacketValue")
        if not isinstance(values, list) or len(values) != 6:
            raise ValueError("DataPacketValue must contain exactly six channels")
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) for v in values):
            raise ValueError("channels must be finite numbers")
        if not np.isfinite(values).all():
            raise ValueError("channels must be finite numbers")
        rows[timestamp] = dict(zip(CHANNELS, values))
    table = pd.DataFrame.from_dict(rows, orient="index", columns=CHANNELS, dtype=float)
    table.index.name = "Timestamp"
    return table


def detect_events(table):
    """Select values at descending ranks 6-15, retaining ties in arrival order."""
    if not all(channel in table.columns for channel in CHANNELS):
        raise ValueError("table must contain all six channels")
    # Preserve the prototype's five-channel mean: channel 4 is deliberately omitted.
    values = table[["Value_0", "Value_1", "Value_2", "Value_3", "Value_5"]].mean(axis=1)
    selected = sorted(values.tolist(), reverse=True)[5:15]
    records = [{"index": timestamp, "Value": float(value)}
               for timestamp, value in values.items() if value in selected]
    return dict(enumerate(records))


def build_plot(packets):
    """Retain the historical JSON-string RPC result shape."""
    return json.dumps(detect_events(packets_to_table(packets)), allow_nan=False)


def serve():
    import zerorpc

    class StreamingRPC:
        @zerorpc.stream
        def streaming_range(self, stage, packets, arg):
            # Two stream items match the original iterable return contract.
            return (build_plot(packets), arg)

    server = zerorpc.Server(StreamingRPC())
    server.bind(os.environ.get("RPC_ENDPOINT", "tcp://127.0.0.1:4242"))
    server.run()


if __name__ == "__main__":
    serve()
