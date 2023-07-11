from pwn import remote

conn = remote("02.cr.yp.toc.tf", "31377")

def flag() -> tuple[int, ...]:
    conn.sendlineafter(b"Options:", b"E")
    conn.recvuntil(b"=")
    return tuple(map(int, conn.recvuntil(b"]").decode().strip("[ ]").split(", ")))


def encrypt(msg: str) -> int:
    conn.sendlineafter(b"Options:", b"T")
    conn.sendlineafter(b":", msg.encode())
    conn.recvuntil(b"=")
    return int(conn.recvuntil(b"]").decode().strip("[ ]"))


def main():
    # flags = ["CCTF{Boldyreva_5", "ymMe7rIC_0rD3r_p", "Re5Erv!n9_3nCryp", "7i0n!_LStfig9TM}"]
    flags = []
    for enc_flag in flag()[len(flags):]:
        print(f"{enc_flag=}")
        plain = ""
        for i in range(len(plain), 16):
            l, r = 0, 127
            while r - l > 1:
                c = (l + r) // 2
                _plain = plain + chr(c) + "\x00" * (15 - i)
                result = encrypt(_plain)
                print(f"{_plain} {result=}")
                if result <= enc_flag:
                    l = c
                else:
                    r = c - 1

            if encrypt(plain + chr(r) + "\x00" * (15 - i)) < enc_flag:
                plain += chr(r)
            else:
                plain += chr(l)

        flags.append(plain)
        print("".join(flags))


if __name__ == "__main__":
    main()
    # CCTF{Boldyreva_5ymMe7rIC_0rD3r_pRe5Erv!n9_3nCryp7i0n!_LStfig9TM}
