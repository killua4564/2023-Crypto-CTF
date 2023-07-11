import gmpy2
from Crypto.Util.number import inverse, isPrime, long_to_bytes
from sage.all import EllipticCurve, GF, Zmod

n = 6660938713055850877314255610895820875305739186102790477966786501810416821294442374977193379731704125177528590285016474818841859956990486067573436301232301
e = 65537
a = 5539256645640498184116966196249666621079506508209770360679460869295427007578
b = 20151017657582479433586370393795140515103572865771721775868586710594524816458

E = EllipticCurve(Zmod(n), [a, b])
enc = E(
    6641320679869421443758875467781930795132746694454926965779628505713445486895274490835545942727970688359873955019634877304270220728625521646208912044469433,
    2856872654927815636828860866843721158889474116106462420201092148493803550131351543372740950198853438539317164093538508795630146854596724019329887894933972,
)


def get_primes() -> tuple[int, int]:
    B = - (2 ** 256) + 2 ** 129 + 1
    p_test = (-B + int(gmpy2.isqrt(B ** 2 + 8 * n))) // 4

    while n % p_test:
        p_test -= 1

    p = p_test
    q = n // p_test

    assert isPrime(p) and isPrime(q)
    return p, q


def main():
    p, q = get_primes()
    Ep = EllipticCurve(GF(p), [a, b])
    Eq = EllipticCurve(GF(q), [a, b])
    phi = Ep.order() * Eq.order()
    d = int(inverse(e, phi))
    m = int((d * enc).xy()[0])
    while not long_to_bytes(m).endswith(b"}"):
        m -= 1
    print(long_to_bytes(m).decode())


if __name__ == "__main__":
    main()
    # CCTF{a_n3W_4t7aCk_0n_RSA_a9ain!?}
