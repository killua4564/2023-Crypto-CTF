from Crypto.Util.number import isPrime
from pwn import remote

conn = remote("05.cr.yp.toc.tf", "11137")


for level in range(19):
    conn.recvuntil(b"(")
    l, r = map(int, conn.recvuntil(b")").decode().strip("( )").split(", "))
    print(f"{level=} {l=} {r=}")
    tl, tr = 1, 0xffffffffffffffff
    while True:
        t = (tl + tr) // 2
        a, b, c = 9*t**3+1, 9*t**4, -9*t**4-3*t
        t_bit = min(a, b, -c).bit_length()
        if t_bit < l:
            tl = t
        elif t_bit > r:
            tr = t
        else:
            tl += 2
            if isPrime(a) or isPrime(b) or isPrime(c):
                print(f"{t=} {a=} {b=} {c=}")
                conn.sendlineafter(b":", f"{a},{b},{c}".encode())
                break

conn.interactive()
# CCTF{pr1m3S_in_7ErnArY_Cu8!c_3qu4tI0nS!}
