## Suction - easy (solved)

* 這題是 curious 解的，後來 upsolve
* 題目是很小 bits 的 RSA，只是 `n`, `e`, `c` 後面的 8bits 通通不給你
* 不給的話，那就逐一爆搜 8 bits 吧
  * 首先是 `n`，然後順便看看能不能分解，這邊 sage 的 factor 可以換成別的可能會比較快
```sage
def get_prime() -> tuple[int, int]:
    n = (pkey >> 8) << 8
    for i in range(1, 256, 2):
        ans = tuple(factor(n + i))
        if len(ans) == 2 and all(i == 1 for _, i in ans):
            factors = tuple(i for i, _ in ans)
            if all(
                isPrime(i) and i.bit_length() <= 128
                for i in factors
            ):
                return factors
```
  * 然後換 `e`，也順便算出 `d`
```python
def get_keys() -> typing.Generator[tuple[int, int], None, None]:
    e = (pkey % (1 << 8)) << 8
    phi = (p - 1) * (q - 1)
    for i in range(1, 256, 2):
        if isPrime(e + i):
            yield e + i, inverse(e + i, phi)
```
  * 最後是 `c`，基本上 flag 就出來了
```python
c = enc << 8
for _, d in get_keys():
    for i in range(1<<8):
        plain = long_to_bytes(pow(c + i, d, n))
        if all(i in plain for i in plain):
            print(f"CCTF{{{plain.decode()}}}")
```
* flag: `CCTF{6oRYGy&Dc$G2ZS}`
