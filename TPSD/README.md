## TPSD - medium (solved)

* 這題到很後面才解，bacon_cy 找到[文獻](https://ericrowland.github.io/papers/Known_families_of_integer_solutions_of_x%5E3+y%5E3+z%5E3=n.pdf)後才有希望了起來XD
* 題目沒有檔案，畫面如下
```
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+ Welcome, esteemed cryptographers with expertise in number theory!    +
+ It's a pleasure to have you here. Whether you're a seasoned veteran  +
+ or a budding enthusiast, let's dive in and explore the fascinating   +
+ world of cryptography and number theory together!                    +
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+ We are looking for the integer solution of p^3 + q^3 + r^3 = 1, such +
+ that at least one of p, q, or r is prime. Submit each such triple    +
+ at every step with mentioned properties.                             +
+ Send a triple array of integers whose absolute minimum value has     +
+ almost (5, 25)-bits. You are at level 1: 
```
* 總之就是要找限定 bits 且滿足 `p**3 + q**3 + r**3 = 1` 的數對
* 那根據文獻上的組合 `(9*t**3+1, 9*t**4, -9*t**4-3*t)`，遍歷 `t` 然後找到符合條件的就好
```python
a, b, c = 9*t**3+1, 9*t**4, -9*t**4-3*t
t_bit = min(a, b, -c).bit_length()
if l <= t_bit <= r:
    if isPrime(a) or isPrime(b) or isPrime(c):
        print(f"{t=} {a=} {b=} {c=}")
```
* 但 bits 數成長的到後面越來越慢，最後不管了直接放很大的 `t` 做二分搜尋吧XD
```python
tl, tr = 1, 0xffffffffffffffff
while True:
    t = (tl + tr) // 2
    ...
    if t_bit < l:
        tl = t
    elif t_bit > r:
        tr = t
    else:
        tl += 2
```
* flag: `CCTF{pr1m3S_in_7ErnArY_Cu8!c_3qu4tI0nS!}`
