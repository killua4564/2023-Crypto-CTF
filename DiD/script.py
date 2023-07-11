import collections
import contextlib
import random

from pwn import remote

conn = remote("00.cr.yp.toc.tf", "11337")
conn.recvlines(3)

n = 127

def get_answers(wrong: set[int]) -> list[int]:
    return tuple(i for i in range(0, n) if i not in wrong)


def get_wrongs(data: list[int]) -> set[int]:
    wrong: set[int] = set()
    did_map: dict[int, set[int]] = collections.defaultdict(set)
    for i in data:
        did_map[pow(i, 2, n)].add(i)
        did_map[pow(i, 2, n) + 1].add(i)

    conn.sendline(",".join(map(str, data)).encode())
    conn.recvuntil(b"=")

    did: dict[int, int] = {}
    with contextlib.suppress(ValueError):
        did = collections.Counter(
            map(int, conn.recvuntil(b"]").decode().strip("[ ]").split(", "))
        )

    for num, counter in did.items():
        if counter == len(did_map[num]):
            wrong |= did_map[num]
    return wrong


def main():
    wrong: set[int] = set()
    for i in range(0, 120, 20):
        wrong |= get_wrongs(list(range(i, i+20)))

    ans: list[int] = get_answers(wrong)
    while len(ans) > 20:
        wrong |= get_wrongs(random.choices(ans, k=20))
        ans = get_answers(wrong)
        print(f"{len(ans)=} {ans=}")

    conn.sendline(",".join(map(str, ans)).encode())
    conn.interactive()


if __name__ == "__main__":
    main()
    # CCTF{W4rM_Up_CrYpt0_Ch4Ll3n9e!!}
