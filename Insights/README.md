## Insights - medium (solved)

* RSA 題目，來看重點的條件
    * `d = next_prime(pow(n, 0.2919))`
    * `p, q = "Practical" || nonce`
* 很明顯就是 Private Exponent Attack 了，而且 `0.292` 這麼熟悉的數字當然先搬出 `boneh-durfee`
* 那 B-D 是求雙變數的 small_roots `(x, y) = (2k, - (p + q) // 2)`，其中 `y` 的 `p, q` 的 high bits 是知道的，所以把差額先補上去可以更縮小 y 的範圍
```sage
p_bits = bytes_to_long(b"Practical")
k = 1024 - (len(bin(p_bits)) - 2)

X = 2 * int(n ** delta)
Y = 1 << k

P = PolynomialRing(ZZ, ["x", "y"])
x, y = P.gens()
A = int((n + 1) // 2 - (p_bits << k))
pol = 1 + x * (A + y)
```
* 之後再調整一下 m, t 去讓 coppersmith method 裡的 shift 多做一點就好
* flag: `CCTF{RSA_N3w_rEc0rd5_4Nd_nEw_!nSi9h75!}`
