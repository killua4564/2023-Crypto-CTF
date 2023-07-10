import itertools
import typing

import z3
from Crypto.Util.number import inverse, long_to_bytes
from sage.all import (
    EllipticCurve_from_cubic, QQ, ZZ,
    gcd, is_prime, matrix, vector,
)

enc = 80607532565510116966388633842290576008441185412513199071132245517888982730482694498575603226192340250444218146275844981580541820190393565327655055810841864715587561905777565790204415381897361016717820490400344469662479972681922265843907711283466105388820804099348169127917445858990935539611525002789966360469324052731259957798534960845391898385316664884009395500706952606508518095360995300436595374193777531503846662413864377535617876584843281151030183895735511854
C = [
    5960650533801939766973431801711817334521794480800845853788489396583576739362531091881299990317357532712965991685855356736023156123272639095501827949743772,
    6521307334196962312588683933194431457121496634106944587943458360009084052009954473233805656430247044180398241991916007097053259167347016989949709567530079,
    1974144590530162761749719653512492399674271448426179161347522113979158665904709425021321314572814344781742306475435350045259668002944094011342611452228289,
    2613994669316609213059728351496129310385706729636898358367479603483933513667486946164472738443484347294444234222189837370548518512002145671578950835894451,
    8127380985210701021743355783483366664759506587061015828343032669060653534242331741280215982865084745259496501567264419306697788067646135512747952351628613,
    5610271406291656026350079703507496574797593266125358942992954619413518379131260031910808827754539354830563482514244310277292686031300804846114623378588204,
]


def gen_ed() -> typing.Generator[tuple[int, int], None, None]:
    e = z3.Int("e")
    d = z3.Int("d")

    solver = z3.Solver()
    solver.add(e > 1)
    solver.add(d > 1)
    solver.add(10543 * e - 4 * d == 31337)

    while True:
        assert solver.check() == z3.sat
        ans = solver.model()
        e_value = ans.evaluate(e).as_long()
        d_value = ans.evaluate(d).as_long()
        solver.add(z3.Or(e != e_value, d != d_value))
        if is_prime(e_value) and is_prime(d_value):
            yield e_value, d_value


def get_primes() -> tuple[int, int, int]:
    a, b, c = QQ["a, b, c"].gens()
    c_matrix_inverse = matrix([
        [C[0], -C[1], 0],
        [0, C[2], -C[3]],
        [-C[5], 0, C[4]],
    ]).inverse()

    for e, d in gen_ed():
        transform = EllipticCurve_from_cubic(
            a ** e + b ** e + c ** e - d * a * b * c
        ).inverse()  # transfer to Elliptic Curve

        E = transform.domain()
        G = E.gen(0)

        for k in itertools.count(1):
            x, y, z = transform(k * G)
            if all(i < 0 for i in (x, y, z)):
                x, y, z = -x, -y, -z
            assert x ** e + y ** e + z ** e == d * x * y * z

            for iter in itertools.permutations((x, y, z)):
                p, q, r = c_matrix_inverse * vector(iter)
                p, q, r = (
                    ZZ(p.numerator() * q.denominator() * r.denominator()),
                    ZZ(q.numerator() * p.denominator() * r.denominator()),
                    ZZ(r.numerator() * p.denominator() * q.denominator()),
                )

                l = gcd(gcd(p, q), r)
                p, q, r = [i // l for i in (p, q, r)]

                a, b, c = (
                    C[0] * p - C[1] * q,
                    C[2] * q - C[3] * r,
                    C[4] * r - C[5] * p,
                )
                assert a ** e + b ** e + c ** e == d * a * b * c

                if all(is_prime(i) for i in (p, q, r)):
                    return e, d, p, q, r

def main():
    e, d, p, q, r = get_primes()
    n = e * d * p * q * r
    phi = (e - 1) * (d - 1) * (p - 1) * (q - 1) * (r - 1)
    print(long_to_bytes(pow(enc, inverse(65537, phi), n)).decode())


if __name__ == "__main__":
    main()
    # CCTF{____Sylvester____tHE0r3m_Of_D3r!va7i0n!}
