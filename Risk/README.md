## Risk - medium (unsolved)

* 經典 RSA 分解 n 的題目
  * `n = (a ** m + r) * (b ** m + s)`
  * `e = r * s`
* 從分解 `e` 且 `r`, `s` bits 數相同可得 `m = 4`
* 剩下就是求出 `a`, `b` 就完事，但天兵的我一直在用 coppersmith 算，想當然 `2**256` 是不夠小啦 XD
* 賽後參考 maple3142 的 [writeup](https://blog.maple3142.net/2023/07/09/cryptoctf-2023-writeups/#risk) 才知道原來國中數學就能解決 :o
* 首先 `n = (a^4 + r) * (b^4 + s) = (ab)^4 + s*a^4 + r*b^4 + rs`，因為 `r`, `s` 都蠻小的，所以 `root(n, 4)` 大概就是 `ab`
* 接下來要求出 `s*a^4` 和 `r*b^4`，先放成兩根之後展開
```
f(x) = (x - s*a^4) * (x - r*b^4)
     = x^2 - (s*a^4 + r*b^4) * x + (rs) * (ab)^4
     = x^2 - (n - e mod (ab)^4) + e * (ab)^4
```
* 之後把 `s*a^4` 和 `ab` 做 gcd 就能算出 `a`，同理 `b` 也是
* 然後把 `r*b^4` 和 `b^4` 相除就能得到 `r`，同理 `s` 也是
* 這樣 `p` 和 `q` 就分解出來了
```sage
ab, _ = Integer(n).nth_root(4, truncate_mode=True)
sa4, rb4 = solve_quadratic(1, (n - e) % (ab ** 4), e * ab ** 4)
a, b = gcd(sa4, ab), gcd(rb4, ab)

r, s = abs(rb4) // b ** 4, abs(sa4) // a ** 4
assert r * s == e

p, q = a ** 4 + r, b ** 4 + s
assert p * q == n
```
* 最後因為 `e` 和 `phi` 不互質，所以只能用 `p`, `q` 開根後再 CRT 組回去 `m`
  * p.s. 這部分詢問 maple3142 的結果是要用 sage10 來跑，目前還沒有 docker 版或是用 [sagecell](https://sagecell.sagemath.org/) 也可以
```sage
for mp in GF(p)(enc).nth_root(e, all=True):
    for mq in GF(q)(enc).nth_root(e, all=True):
        m = long_to_bytes(crt([ZZ(mp), ZZ(mq)], [p, q]))
        if m.startswith(b"CCTF{"):
            print(m.decode())
```
* flag: `CCTF{S!mP1E_A7t4cK_0n_SpEc1aL-5trucTur3D_RSA_pR1me5!}`
