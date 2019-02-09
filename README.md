# 3競技の順位積による総合順位について

ミキペディアさんの疑問に対する解答です。

https://twitter.com/mic_u/status/1094029193178824704

> わからない算数の問題があるので解けたら教えて欲しいです
> 「クライミングは3種目の順位の掛け算(合計pt)が小さい上位6人が予選を通過する。
> 絶対に予選通過できる合計ptの最大値は何点か」
> 設定を簡単にするため現実とは異なりますが
> ・同着は無し
> ・合計ptが同じ人が複数人でたら7人以上通過
> とする

結論から言うと、私の解答は **60** である

ある選手P0の順位が(1,1,60)のとき、他の選手の順位がどのような組み合わせであっても、6位の選手の総合ptは60より小さくはできず、選手P0は絶対に予選突破する

以下、解法・証明など

---

# 略語の説明

- 求めたい総合ptを持つ選手を P0
- それ以外の6選手を P1, P2, P3, P4, P5, P6
- 3種目の競技を A, B, C

とする

- i ∈ { 0, 1, ..., 6 } において
  - 選手Piの競技Aの順位を ai
  - 選手Piの競技Bの順位を bi
  - 選手Piの競技Cの順位を ci
  - 選手Piの総合ptを ti (= ai * bi * ci)

とする

- 例
  - 選手P3の競技Bの順位は b3
  - 選手P5の総合ptは t5

---

# 解放の指針

*漏れなく場合分けしたつもりだけど、勘違いがありそう...*

循環構造があるので<br>
a0 <= b0 <= c0 の場合のみ考える --- (h1)

循環構造があるので<br>
a1 < a2 < a3 < a4 < a5 < a6 の場合のみ考える

a0 < 7 の場合のみ考えれば十分である<br>
なぜなら、a0 >= 7のとき、b0 >= 7, c0 >= 7となり、P1~P6が3競技で1~6位を独占することで確実にP0を予選敗退にできるから

選手P0が6位の選手の総合pt（=上位6人の総合ptの最大値）と同じもしくは下回れば予選通過できる<br>
"絶対に予選通過できる"というのは、『「選手P1~P6の総合ptの最大値」の最小値』を考えれば良い<br>

b0, c0について、3つの場合に分けて考える

---

### (i) b0 <= 6, c0 <= 6の場合

bi (i=1~6)は b0以外の{1,2,3,4,5,6,7}からなる場合<br>
ci (i=1~6)は c0以外の{1,2,3,4,5,6,7}からなる場合<br>
だけを考えれば十分

*具体例を使って感覚的に理由を説明する*<br>
*例えばb0=3のとき、*<br>
*bi(i=1~6)が{1,2,4,5,6,8}のときの「選手P1~P6の総合ptの最大値」*<br>
*が*<br>
*bi(i=1~6)が{1,2,4,5,6,7}ののとき「選手P1~P6の総合ptの最大値」*<br>
*より小さくなることはない*

*※場合の数は 6! * 6! = 518,400通り*

---

### (ii) b0 <= 6, c0 >= 7の場合

#### Step1: c0 == 7 の場合

c0 を 7 に固定し<br>
bi (i=1~6)は b0以外の{1,2,3,4,5,6,7}からなる場合<br>
ci (i=1~6)は {1,2,3,4,5,6}からなる場合<br>
のときの『「選手P1~P6の総合ptの最大値」の最小値』`X`を求める

#### Step2: c0 >= 8 の場合

Step1で求めた解 `X` と a0, b0 から c0>=8 のときの解を探索する

---

### (iii) b0 >= 7, c0 >= 7の場合

#### Step1: c0 == 7 の場合

b0 と c0 を 7 に固定し<br>
bi (i=1~6)は {1,2,3,4,5,6}からなる場合<br>
ci (i=1~6)は {1,2,3,4,5,6}からなる場合<br>
のときの『「選手P1~P6の総合ptの最大値」の最小値』`X`を求める

#### Step2:

Step1で求めた解 `X` と a0 から b0>=8, c0>=8 のときの解を探索する

*しかし、プログラムを動かした結果、Step1で解が存在しないことがわかった*

---

*(i)と(ii)(iii)のStep1に限定して考えると*<br>
*h1の条件下で、(a0, b0, c0)の組み合わせは83通り*<br>
*このあたりで手計算するには大きいけど、計算機なら手元のマシンでも総当たり的に解けるかもと思いました*

---

# 結果

[選手P0の順位でソートした結果](./results_sorted_by_a0_b0_c0)
[選手P0の総合ptでソートした結果](./results_sorted_by_t0)

- 読み方
  - inserted_at: 上記の解放で、どのstepによって求められたのか
  - min_max_ti: 「選手P1~P6の総合ptの最大値」の最小値
  - must_go_final: 選手P0は"絶対に"予選突破できるか
  - p0: 選手P0の各競技における順位
  - p1p6: 選手P1~P6の各競技における順位
  - t0: 選手P0の総合ポイント

[選手P0の総合ptでソートした結果](./results_sorted_by_t0)をみると、`"must_go_final"` が `true` の行で最も大きい `t0` は 60 である。よって答えは 60

---

### 結果ファイルの例

https://twitter.com/mic_u/status/1094029367984906240

> 例えば3種目で1位、7位、7位を取り、合計ptが49点の人は確実に通過できるか？
> これは実は確実ではなくて、(3,3,3)=27、(6,1,6)=36、(2,4,5)=40の循環3人、(7,6,1)=42、の6人に負けてしまう可能性があります。

この選手P0の順位が [1,7,7] の場合は [選手P0の総合ptでソートした結果](./results_sorted_by_t0) の123行目にある

```
{"inserted_at": "step1", "min_max_ti": 40, "must_go_final": false, "p0": [1, 7, 7], "p1p6": [[2, 3, 6], [3, 4, 3], [4, 5, 2], [5, 2, 4], [6, 6, 1], [7, 1, 5]], "t0": 49}
```

これを見ると `"must_go_final": false` であり、予選突破できないケースがあることを意味している

---

# プログラムの実行

実行環境: python 3.6~

```
$ python -V
Python 3.6.3
```

実行方法

```
$ python no_tied_rank_product.py
```

*手元の環境、MacBook Pro 2016, Intel Core i5では、実行時間約80秒でした*