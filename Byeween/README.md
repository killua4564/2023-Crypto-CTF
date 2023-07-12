## Byeween - hard (unsolve)

* 這題沒有檔案。畫面如下
```
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|  Hi all, I have created a basic and simple cryptography task about   |
|  elliptic curve over rational field. Your mission is to find all     |
|  points Q over E such that 2 * Q = P, such that P is given.          |
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
| Generating parameters, please wait...
| Options: 
|	[I]informations 
|	[S]ubmit points 
|	[Q]uit
```
  * informations 畫面
```
| E = Elliptic Curve defined by y^2 = x^3 - 7677965376*x over Rational Field
| Q = (1445537313025/7441984 : -1551089202771118465/20301732352 : 1)
```
  * submit points 畫面
```
| Please send the points on elliptic curve one by one: 
```
  * 提交對了之後會有 `You have sent {k} correct points already!`
* 當下看到有理域的 ECC 就嚇到看別題了(然後就再也沒打開過)
* 賽後參考 maple3142 的 [writeup](https://blog.maple3142.net/2023/07/09/cryptoctf-2023-writeups/#byeween) 居然這麼簡單我也是傻眼...
* 就...求半點... sagemath 幫你實作完了，print 出來之後就一點一點 submit 上去就好
```sage
E = EllipticCurve(QQ, [-7677965376, 0])
Q = E(1445537313025/7441984, -1551089202771118465/20301732352)

for x in Q.division_points(2):
    print(",".join(map(str, x.xy())))
```
* 然後發現官方又忘記把 flag decode 了 :p
* flag: `CCTF{H4lVin9_pO!ntS_0n_3lLipT1C_cuRve5!}`
