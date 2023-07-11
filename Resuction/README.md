## Resuction - medium (solved)

* 這題是 curious 解的，後來 upsolve，是說我比賽時完全沒注意到跟 suction 有關係XD
* 題目基本上跟 suction 一樣，只是 `d` 變成很小(64bits)，那就搬出 wiener attack 吧
* 總之先把 `(e, n)` 確定的部分拆出來，然後爆搜一下兩者的後 8 bits，能 owiener 出來的就是答案了吧(我想)
```python
def get_keys() -> tuple[int, int, int]:
    l = pkey.bit_length()
    n = (pkey >> (l - 2040)) << 8
    e = (pkey % (1 << (l - 2040))) << 8
    for i in tqdm.trange(1, 256, 2):
        for j in range(256):
            d = owiener.attack(e + j, n + i)
            if d is not None:
                return n + i, e + j, d
```
* 之後就輪到 enc 被爆搜啦
```python
c = enc << 8
for i in range(256):
    plain = long_to_bytes(pow(c + i, d, n))
    if all(i < 0x7f for i in plain):
        print(f"CCTF{{{plain.decode()}}}")
        break
```
* flag: `CCTF{aIr_pr3s5urE_d!Ff3rEn7i4L_8eTw3eN_ArEa5!}`
