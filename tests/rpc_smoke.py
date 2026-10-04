"""Optional local subprocess/IPC integration check; no MySQL or sensor is required."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

# Permit invocation as a standalone script from the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import zerorpc
from examples.generate_packets import generate_packets

with tempfile.TemporaryDirectory(prefix='neurodev-') as directory:
    endpoint = f'ipc://{directory}/rpc.sock'
    process = subprocess.Popen(
        [sys.executable, 'model_builder.py'],
        env=dict(os.environ, RPC_ENDPOINT=endpoint),
    )
    client = zerorpc.Client(timeout=10)
    try:
        client.connect(endpoint)
        result = list(client.streaming_range(1, generate_packets(), 3))
        assert len(json.loads(result[0])) == 10
        assert result[1] == 3
        print('Python ZeroRPC synthetic round trip: passed')
    finally:
        client.close()
        process.terminate()
        process.wait(timeout=5)
