import string
import typing

from Crypto.Util.number import inverse, isPrime, long_to_bytes
from sage.all import factor

pkey = 55208723145458976481271800608918815438075571763947979755496510859604544396672
enc = 127194641882350916936065994389482700479720132804140137082316257506737630761
printables: frozenset[int] = frozenset(string.printable.encode())


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

# p, q = get_prime()
p, q = 188473222069998143349386719941755726311, 292926085409388790329114797826820624883


def get_keys() -> typing.Generator[tuple[int, int], None, None]:
    e = (pkey % (1 << 8)) << 8
    phi = (p - 1) * (q - 1)
    for i in range(1, 256, 2):
        if isPrime(e + i):
            yield e + i, inverse(e + i, phi)


def main():
    n = p * q
    c = enc << 8
    for _, d in get_keys():
        for i in range(1<<8):
            plain = long_to_bytes(pow(c + i, d, n))
            if all(i in printables for i in plain):
                print(f"CCTF{{{plain.decode()}}}")


if __name__ == "__main__":
    main()
    # CCTF{6oRYGy&Dc$G2ZS}
