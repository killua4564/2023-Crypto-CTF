## ASIv1 - medium (solved)

* 這題是 curious 解的，後來 upsolve
* 由題意可知是在 `GF(3)` 做線性代數
    * R * seed = S
* 要求出 seed 的話需要 `R.inverse()` 所以從 R 的 l^2 rows 裡面挑出 independent 的 rows 做成 square matrix 就可以把 seed 算回來了
```python
rr, ss = get_independent_matrixes()
RR, SS = matrix(F, rr), vector(F, ss)
seed = int("".join(map(str, RR.inverse() * SS)), 3)
print(f"CCTF{{{long_to_bytes(seed).decode()}}}")
```
* flag: `CCTF{3Xpl0i7eD_bY_AtT4ck3r!}`
