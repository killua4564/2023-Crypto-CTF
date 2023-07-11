## Roldy - medium (solved)

* 題目用一個叫 [pyope](https://github.com/tonyo/pyope/tree/master) 的東西加密，那根據 github quick start 上寫的
```python
from pyope.ope import OPE
random_key = OPE.generate_key()
cipher = OPE(random_key)
assert cipher.encrypt(1000) < cipher.encrypt(2000) < cipher.encrypt(3000)
assert cipher.decrypt(cipher.encrypt(1337)) == 1337
```
* 那就可以依照這個特性慢慢磨出 flag
* 題目是將 `msg` 每 16 bits 切成 block 再個別去做 encrypt，padding 用 `*` 來補上
```python
def encrypt(msg, key, params):
    if len(msg) % 16 != 0:
        msg += (16 - len(msg) % 16) * b'*'
    p, k1, k2 = params
    msg = [msg[_*16:_*16 + 16] for _ in range(len(msg) // 16)]
    m = [bytes_to_long(_) for _ in msg]
    inra = ValueRange(0, 2**128)
    oura = ValueRange(k1 + 1, k2 * p + 1)
    _enc = enc(key, in_range = inra, out_range = oura)
    C = [_enc.encrypt(_) for _ in m]
    return C
```
* 那就依序對每個 block 做逐字的找吧，一個個遍歷找實在太慢，所以直接二分搜尋就好，不過這邊要注意的是因為 padding 是 `*`，如果直接讓系統 padding 且下一個字的 ascii 比 `*` 小的話這個字就會找錯，所以需要自己補 `\x00` 不要讓系統 padding
```python
flags = []
for enc_flag in flag()[]:
    print(f"{enc_flag=}")
    plain = ""
    for i in range(16):
        l, r = 0, 127
        while r - l > 1:
            c = (l + r) // 2
            _plain = plain + chr(c) + "\x00" * (15 - i)
            result = encrypt(_plain)
            print(f"{_plain} {result=}")
            if result <= enc_flag:
                l = c
            else:
                r = c - 1
        if encrypt(plain + chr(r) + "\x00" * (15 - i)) < enc_flag:
            plain += chr(r)
        else:
            plain += chr(l)
    flags.append(plain)
    print("".join(flags))
```
* flag: `CCTF{Boldyreva_5ymMe7rIC_0rD3r_pRe5Erv!n9_3nCryp7i0n!_LStfig9TM}`
