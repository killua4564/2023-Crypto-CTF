from Crypto.Util.number import long_to_bytes
from sage.all import GF, matrix, vector

from output import R, S

F = GF(3)
l = len(R[0])


def get_independent_matrixes() -> tuple[list[list[int]], list[int]]:
    idx, count = 0, 0
    result_R, result_S = [], []
    while count < l:
        test_matrix = matrix(F, result_R + [R[idx]])
        if test_matrix.rank() == test_matrix.nrows():
            count += 1
            result_R.append(R[idx])
            result_S.append(S[idx])
        idx += 1
    return result_R, result_S


def main():
    rr, ss = get_independent_matrixes()
    RR, SS = matrix(F, rr), vector(F, ss)
    seed = int("".join(map(str, RR.inverse() * SS)), 3)
    print(f"CCTF{{{long_to_bytes(seed).decode()}}}")


if __name__ == "__main__":
    main()
    # CCTF{3Xpl0i7eD_bY_AtT4ck3r!}
