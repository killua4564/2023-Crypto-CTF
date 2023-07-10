## Blue office - easy (solved)

* 把 flag byte by byte 的跟每一個 round `(seed >> 16) & 0xff)` 做 xor
* 已知 flag 的 prefix 為 `CCTF{`，則第一 round 的 seed 是 `((enc[0] ^ ord("C")) << 16) + i`
* 而 `i` 只有 16 bits，爆搜一下即可
```python
for i in range(2 ** 16):
    s = ((enc[0] ^ ord("C")) << 16) + i
    if (reseed(s) >> 16) & 0xff == enc[1] ^ ord("C"):
        if (reseed(reseed(s)) >> 16) & 0xff == enc[2] ^ ord("T"):
            return s
```
* flag: `CCTF{__B4ck_0r!F1c3__C1pHeR_!!}`
