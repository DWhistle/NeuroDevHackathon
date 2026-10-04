# Validation record

Date: 2026-09-12. Baseline: `9080b328cf95c23e9547f565ee9383419831e958`
(default branch `master`). Host: macOS Darwin 24.3.0, Python 3.12.6,
Node 24.4.0, npm 11.4.2.

## Baseline

- Python source failed parsing with `TabError` at line 55.
- README named a missing `requirements.txt`; no automated tests were supplied.
- Root and manual-demo npm test scripts were placeholders that exit unsuccessfully.
- Native dependencies, MySQL schema, and original device/service access were unverified.
- One commit credits Андрей Шибаев. No individual task allocation was documented.
- No tracked node_modules, compiled binaries, or IDE directories were found.
  The notebook contained regenerable outputs; raw CSVs are retained source inputs.

## Results

| Check | Result |
| --- | --- |
| `python -m pip install -r requirements.txt` in a new venv | Passed; NumPy 2.5.3, Pandas 2.3.3, ZeroRPC 0.6.3 |
| `python -m unittest discover -s tests -v` | Passed: 9 tests |
| Synthetic generator followed by `build_plot` | Passed: 20 generated packets, 10 selected records |
| `python tests/rpc_smoke.py` | Passed: Python server/client IPC round trip, JSON result plus second stream item |
| `npm test` | Passed: missing configuration, fake-placeholder rejection, synthetic valid configuration |
| `python -m py_compile model_builder.py examples/generate_packets.py` | Passed |
| `node --check` on root and manual-demo JavaScript | Passed |
| `npm ci` with original lock | Failed: NAN 2.14 / V8 compile incompatibility in native ZeroMQ 4.6.0 on Node 24 |
| Temporary NAN 2.28 lock update and `npm ci` | Failed: ZeroMQ binding directly uses removed V8 `Get` API; update reverted |
| Node → Python RPC, MySQL, HTTP/Socket.IO workflow, device execution | Not run: native Node install blocked; no database/device setup |

The first Python IPC attempt timed out inside the restricted sandbox. Repeating the
local-only check with socket permissions succeeded. No original external endpoint,
credential, or private recording was used.

## Compatibility and scope

The committed Node dependency versions and lock are unchanged: the narrow NAN
update did not repair installation. Do not interpret syntax/config checks as a
working Node integration. A separate bounded update of the Node ZeroMQ/ZeroRPC
binding and a supported-runtime test matrix remain necessary.

The new Python requirements constrain the libraries actually used by the processor;
there was no original requirements file. Unused Matplotlib, Requests, and SciPy
imports were removed from that entry point. Notebook Matplotlib use remains.
Behavioral changes (validation, short inputs, and removing the contradictory
variance-filter deletion) are described in the README; no trained model or
algorithm-quality improvement is claimed.

The full HTTP bridge still contains the source-level failures listed in the README.
No production build, device benchmark, detector-quality evaluation, or complete
security audit was performed.
