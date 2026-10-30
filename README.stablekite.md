# StableKite delivery

Install the default branch with ordinary pip:

```console
python -m pip install git+https://github.com/StableKite/FTServo_Python.git
```

This fork packages vendor commit `9e6e342f6011dc727ba7144fc835bca5357b3ca9`
as `ftservo-python-sdk` version `2.0.1+stablekite.1`. The vendor source already
converts signed positions with `scs_toscs(position, 15)` in `WritePosEx`,
`RegWritePosEx`, and `SyncWritePosEx`. Its existing `reSet` and `reOfsCal`
methods are included without replacement implementations.

The register-read correction checks the received status LENGTH and packet
size before returning data from `readTxRx` and `readRx`. A mismatched payload
returns `COMM_RX_CORRUPT` and no data; a checksum cannot become a register byte.

Run the tests after installing the package:

```console
python -m unittest discover -s tests -v
```

Tests exercise the genuine SDK through a software UART byte boundary. They
cover both servo families, split and combined register reads, signed position
packets, existing reset/offset packets, and independent ports on eight native
threads. They never open a hardware port or calibrate or reset equipment.
The independent-port test does not establish concurrent transaction support
for multiple callers sharing one physical serial bus.
