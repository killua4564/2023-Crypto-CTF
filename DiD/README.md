## Did it - easy (solved)

* 這題由 curious 寫 payload 之後我有整理過
* 題目會從 `randint(0, 126)` 隨機選 20 個數字當作答案，如果送過去的 input item 如果不在答案裡，就會隨機回傳 `pow(i, 2, n) + randint(0, 1)`
* 那這題會有兩個不同的 item 可能會有重複 output 的問題，所以要確認每次 input 進去的所有可能和對應的 output 數量是一樣的才能排除
```python
wrong: set[int] = set()
did_map: dict[int, set[int]] = collections.defaultdict(set)
for i in data:  # input
    did_map[pow(i, 2, n)].add(i)
    did_map[pow(i, 2, n) + 1].add(i)

for num, counter in did.items():  # output
    if counter == len(did_map[num]):
        wrong |= did_map[num]
```
* flag: `CCTF{W4rM_Up_CrYpt0_Ch4Ll3n9e!!}`
