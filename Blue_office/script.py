enc = bytes.fromhex("b0cb631639f8a5ab20ff7385926383f89a71bbc4ed2d57142e05f39d434fce")


def reseed(s):
	return s * 214013 + 2531011


def get_seed() -> int:
    for i in range(2 ** 16):
        s = ((enc[0] ^ ord("C")) << 16) + i
        if (reseed(s) >> 16) & 0xff == enc[1] ^ ord("C"):
            if (reseed(reseed(s)) >> 16) & 0xff == enc[2] ^ ord("T"):
                return s


def main():
    flag = []
    s = get_seed()
    for c in enc:
        flag.append(c ^ ((s >> 16) & 0xff))
        s = reseed(s)

    print(bytes(flag).decode())


if __name__ == "__main__":
    main()
    # CCTF{__B4ck_0r!F1c3__C1pHeR_!!}
