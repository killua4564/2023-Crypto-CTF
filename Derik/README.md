# Derik - medium (unsolved)

* 這邊 curious 用 z3 炸出 `(e, d)` 的可能性，然後就沒有然後了(ry
* 於是賽後參考了 maple3142 的 [writeup](https://blog.maple3142.net/2023/07/09/cryptoctf-2023-writeups/#derik)
* 假設 `(e, d) = (3, 73)` 後 `a ** 3 + b ** 3 + c ** 3 = 73 * a * b * c` 是個橢圓曲線
* 先把方程 transform 生出來 Projective Plane Curve 後再 inverse 成 Elliptic Curve
```python
a, b, c = QQ["a, b, c"].gens()
transform = EllipticCurve_from_cubic(
    a ** e + b ** e + c ** e - d * a * b * c
).inverse()
```
* 之後找 curve 上的 `(a, b, c)` 算回去 `(p, q, r)` 滿足條件的就是答案了
    * matrix 算出來的 `(p, q, r)` 是分數，之後要進行通分
```python
E = transform.domain()
G = E.gen(0)

c_matrix_inverse = matrix([
    [C[0], -C[1], 0],
    [0, C[2], -C[3]],
    [-C[5], 0, C[4]],
]).inverse()

p, q, r = c_matrix_inverse * vector(transform(k * G))
```
* flag: `CCTF{____Sylvester____tHE0r3m_Of_D3r!va7i0n!}`
