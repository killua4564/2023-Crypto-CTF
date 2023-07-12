## Marjan - hard (unsolved)

* 變種的 ECDSA 要偽造簽章
* 系統提供的 sign 功能只能簽小於長度 10 的 msg，但要給出 `I love all cryptographers!!!` 的簽章才會給你 flag
* 先來看最重要的 sign 部分
```sage
def sign(msg, skey):
    _tail = bytes_to_long(sha256(str(skey).encode('utf-8')).digest()) % (1 << 24)
    while True:
        K = [randint(1, 2**255) // (1 << 24) + _tail for _ in '__']
        r, s = int((K[0] * G).xy()[0]), int((K[1] * G).xy()[1])
        if r * s != 0:
            break
    h = bytes_to_long(sha256(msg).digest())
    t = inverse(K[0], _o) * (h * r - s * skey) % _o
    return (r, s, t)
```
* 比賽時只想到要找出 `(k, skey)` 但沒想法要怎麼求，encrypt 功能又感覺是來混淆視聽的
* 賽後參考了 maple3142 的 [writeup](https://blog.maple3142.net/2023/07/09/cryptoctf-2023-writeups/#marjan) 才驚覺居然是 LLL
* 因為 `k` 在 generate 的時候被薛弱成只有 232 bits，所以可以拿很多的 `k` 用 LLL 算出來
* 首先把每一組的 `(h, r, s, t)` 搜集起來
```sage
sigs = [sign(os.urandom(4).hex()) for _ in range(n)]
P = PolynomialRing(Zmod(order), ["skey"] + [f"k{i}" for i in range(n)])
skey, *ks = P.gens()
```
* 建成每組的 eqs，並把 `d` 消去做成 eqs2 (沒想到可以用[西爾維斯特矩陣](https://en.wikipedia.org/wiki/Sylvester_matrix))
```sage
eqs = [t * k - (h * r - s * skey) for (h, r, s, t), k in zip(sigs, ks)]
eqs2 = [f.sylvester_matrix(g, skey).det() for f, g in zip(eqs, eqs[1:])]
```
* 把 `ks` 的係數拆出來 (這裡滿足 `M * v = eqs2`)
```sage
M, v = Sequence(eqs2).coefficient_matrix()
```
* 開始來準備要做 LLL 的 matrix，因為目的是要求出 `ks` 的值，所以要把參數 M transpose 過來做 dense，右邊放上 1 的 diagonal matrix 當作求出來的答案，左下角放 order 的 diagonal matrix 讓 LLL 能去對參數做 mod (如下示意圖)
```sage
L = block_matrix(ZZ, [[M.T.dense_matrix(), 1], [order, 0]])
```
```
L = [
    [ k0,  0,  0,  0,  0 | 1, 0, 0, 0, 0, 0]
    [ k1, k1,  0,  0,  0 | 0, 1, 0, 0, 0, 0]
    [  0, k2, k2,  0,  0 | 0, 0, 1, 0, 0, 0]
    [  0,  0, k3, k3,  0 | 0, 0, 0, 1, 0, 0]
    [  0,  0,  0, k4,  0 | 0, 0, 0, 0, 1, 0]
    [ c0, c1, c2, c3, c4 | 0, 0, 0, 0, 0, 1]
    [--------------------------------------]
    [ord,  0,  0,  0,  0 | 0, 0, 0, 0, 0, 0]
    [  0,ord,  0,  0,  0 | 0, 0, 0, 0, 0, 0]
    [  0,  0,ord,  0,  0 | 0, 0, 0, 0, 0, 0]
    [  0,  0,  0,ord,  0 | 0, 0, 0, 0, 0, 0]
    [  0,  0,  0,  0,ord | 0, 0, 0, 0, 0, 0]
]
```
* 然而如果直接對 `L` 做 LLL 的話 `ks` 的參數會有剩餘(非0)，這樣右上角的 `ks` 算出來就會不準，所以需要把參數做相當的加成，這邊讓參數的部分乘上 `2**1024` 並把 `ks` 的部分調成 `2**512`，但因為求的 `ks` 裡面有常數和變數，變數本身是 `2**232` 了，所以只要再乘上 `2**280` 即可
```sage
B = diagonal_matrix([1<<1024] * len(eqs2) + [1<<(512 - (256 - 24))] * len(ks) + [1<<512])
```
```
B = [
    [2**1024,       0,       0,       0,       0,      0,      0,      0,      0,      0]
    [      0, 2**1024,       0,       0,       0,      0,      0,      0,      0,      0]
    [      0,       0, 2**1024,       0,       0,      0,      0,      0,      0,      0]
    [      0,       0,       0, 2**1024,       0,      0,      0,      0,      0,      0]
    [      0,       0,       0,       0, 2**1024,      0,      0,      0,      0,      0]
    [      0,       0,       0,       0,       0, 2**280,      0,      0,      0,      0]
    [      0,       0,       0,       0,       0,      0, 2**280,      0,      0,      0]
    [      0,       0,       0,       0,       0,      0,      0, 2**280,      0,      0]
    [      0,       0,       0,       0,       0,      0,      0,      0, 2**280,      0]
    [      0,       0,       0,       0,       0,      0,      0,      0,      0, 2**512]
]
```
* 這樣 `L` 乘上 `B` 後做完 LLL 在除回來 `B` 就可以輕鬆地得到 `ks` 的值了
```sage
L = (L * B).LLL() / B
ks_sol = vector(ZZ, L[0][len(eqs2):-1])
```
* 算出來 `k` 之後就能算出 `skey`
```sage
skey = eqs[0].subs({ks[0]: ks_sol[0]}).univariate_polynomial().roots(multiplicities=False)[0]
```
* 接下來就是快樂的偽造時間
```sage
def do_sign(
    skey: int,
    msg: str = "I love all cryptographers!!!",
) -> tuple[int, int, int]:
    while True:
        k = randint(1, 1 << 128)
        r, s = map(int, (k * G).xy())
        if r * s != 0:
            break

    h = bytes_to_long(hashlib.sha256(msg.encode()).digest())
    t = inverse(k, order) * (h * r - s * skey) % order
    return r, s, t
```
* 最後發現官方在 print flag 的時候忘記 decode 了 :p
* flag: `CCTF{L4T71c3_atTAck5_a9A!nS7_ECDSA!}`
