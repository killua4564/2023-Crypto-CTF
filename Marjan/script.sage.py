import hashlib
import os

from Crypto.Util.number import bytes_to_long, inverse
from pwn import remote
from sage.all import (
    EllipticCurve, GF, PolynomialRing, Sequence, ZZ, Zmod,
    block_matrix, diagonal_matrix, randint, vector,
)

p = 114863632180633827211184132915225798242263961691870412740605315763112513729991
A = -3
B = 105675527217961035404524512435875047840495516468907806313576241823653895562912
E = EllipticCurve(GF(p), [A, B])
order = E.order()

conn = remote("06.cr.yp.toc.tf", "13337")


def pubkey():
    conn.sendlineafter(b": ", b"P")
    conn.recvuntil(b"=")
    px, py, _ = map(int, conn.recvuntil(b")").decode().strip("( )").split(" : "))
    conn.recvuntil(b"=")
    gx, gy, _ = map(int, conn.recvuntil(b")").decode().strip("( )").split(" : "))
    return E(px, py), E(gx, gy)


def sign(msg: str) -> tuple[int, int, int, int]:
    conn.sendlineafter(b": ", b"S")
    conn.sendlineafter(b": ", msg.encode())
    conn.recvuntil(b"=")
    r, s, t = map(int, conn.recvuntil(b")").decode().strip("( )").split(", "))
    h = bytes_to_long(hashlib.sha256((msg + "\n").encode()).digest())
    return h, r, s, t


def verify(sig: tuple[int, int, int]):
    conn.sendlineafter(b": ", b"G")
    conn.sendlineafter(b": ", ",".join(map(str, sig)).encode())
    conn.recvuntil(b": ")
    print(conn.recvuntil(b"\n").decode())


def get_skey() -> int:
    n = 16
    sigs = [sign(os.urandom(4).hex()) for _ in range(n)]
    P = PolynomialRing(Zmod(order), ["skey"] + [f"k{i}" for i in range(n)])
    skey, *ks = P.gens()

    eqs = [
        t * k - (h * r - s * skey)
        for (h, r, s, t), k in zip(sigs, ks)
    ]
    print(f"{eqs=}")

    eqs2 = [
        f.sylvester_matrix(g, skey).det()
        for f, g in zip(eqs, eqs[1:])
    ]
    print(f"{eqs2=}")

    M, v = Sequence(eqs2).coefficient_matrix()  # M * v = eqs2
    print(f"v={vector(v)}")

    L = block_matrix(ZZ, [[M.T.dense_matrix(), 1], [order, 0]])
    B = diagonal_matrix([1<<1024] * len(eqs2) + [1<<(512 - (256 - 24))] * len(ks) + [1<<512])
    L = (L * B).LLL() / B

    ks_sol = vector(ZZ, L[0][len(eqs2):-1])
    if L[0][-1] < 0:
        ks_sol = -ks_sol
    print(f"{ks_sol=}")

    return eqs[0].subs({ks[0]: ks_sol[0]}).univariate_polynomial().roots(multiplicities=False)[0]


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


def main():
    skey = get_skey()
    assert skey * G == pkey
    print(f"{skey=}")
    verify(do_sign(skey))


if __name__ == "__main__":
    pkey, G = pubkey()
    main()
    # CCTF{L4T71c3_atTAck5_a9A!nS7_ECDSA!}
