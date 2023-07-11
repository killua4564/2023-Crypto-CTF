## Keymoted - medium (solved)

* ECC + RSA 有趣的組合
* 題目用 `p` 去找出 `q`，然後 `a`, `b` 在 `p` 底下
```sage
p = getPrime(nbit)
_s = p ^^ ((2 ** (nbit - 1)) + 2 ** (nbit // 2))
q = next_prime(2 * _s + 1)
n = p * q

a, b = [randint(1, p - 1) for _ in '__']
Ep = EllipticCurve(GF(p), [a, b])
Eq = EllipticCurve(GF(q), [a, b])
```
* 之後確認 `e` 跟 `Ep`, `Eq` 的 order 是互質的
```sage
e = 65537
while True:
    if gcd(e, (p**2 - tp**2) * (q**2 - tq**2)) == 1:
        break
    else:
        e = next_prime(e)
```
* encrypt 的部分是先在 `n` 的 ECC 上找 `m` 的點然後加密
```sage
E = EllipticCurve(Zmod(n), [a, b])
P = E(m, x)
enc = e * P
```
* 但 n 是和數所以 `x` 要用 `Ep`, `Eq` 的方程算出來後組 CRT 成 `E` 的點
```sage
while True:
    xp = (m**3 + a*m + b) % p
    xq = (m**3 + a*m + b) % q
    if pow(xp, (p-1)//2, p) == pow(xq, (q-1)//2, q) == 1:
        break
    else:
        m += 1

eq1, eq2 = Mod(xp, p), Mod(xq, q)
rp, rq = sqrt(eq1), sqrt(eq2)
_, x, y = xgcd(p, q)
x = (Z(rp) * Z(q) * Z(y) + Z(rq) * Z(p) * Z(x)) % n
```
* 如此，想要解密就需要知道 `E` 的 order，也就是 `Ep` 和 `Eq` 的 order，也就需要分解 `n`
* 因為 `nbit = 256` 所以可以得出 `n ≈ p * (2 * p - 2 ** 256 ± 2 ** 129 + 1)`，解方程可以就可以算出 `p` 了 (這部分是優化 curious 的 script)
```sage
def get_primes() -> tuple[int, int]:
    B = - (2 ** 256) + 2 ** 129 + 1
    p_test = (-B + int(gmpy2.isqrt(B ** 2 + 8 * n))) // 4

    while n % p_test:
        p_test -= 1

    p = p_test
    q = n // p_test

    assert isPrime(p) and isPrime(q)
    return p, q
```
* 分解出來後就可以造出 `Ep`, `Eq` 算出 `phi` 來 decrypt 了
```sage
Ep = EllipticCurve(GF(p), [a, b])
Eq = EllipticCurve(GF(q), [a, b])
phi = Ep.order() * Eq.order()
d = int(inverse(e, phi))
m = int((d * enc).xy()[0])
while not long_to_bytes(m).endswith(b"}"):
    m -= 1
print(long_to_bytes(m).decode())
```
* flag: `CCTF{a_n3W_4t7aCk_0n_RSA_a9ain!?}`
