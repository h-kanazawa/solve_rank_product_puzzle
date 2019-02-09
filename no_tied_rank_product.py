import itertools
import json


T0_SORTED_RESULTS_FILE_NAME = './results_sorted_by_t0'
A0_B0_C0_SORTED_RESULTS_FILE_NAME = './results_sorted_by_a0_b0_c0'


def min_max_rank_product(a0, b0, c0):
    """
    ある(a0,b0,c0)における「t1~t6の最大値」の最小値と
    その最小値を構成する、選手P1~P6の競技A,B,Cの順位組のひとつ

    Arguments:
        a0 {int} -- 競技Aにおける選手P0の順位 1 <= a0 <= 7
        b0 {int} -- 競技Bにおける選手P0の順位 a0 <= b0 <= 7
        c0 {int} -- 競技Cにおける選手P0の順位 b0 <= c0 <= 7

    Returns:
        {tuple} -- 0個目の要素: 選手P1~P6の競技A,B,Cの順位の配列
                        [[a1,b1,c1], [a2,b2,c2], [a3,b3,c3], [a4,b4,c4], [a5,b5,c5], [a6,b6,c6]]
                   1個目の要素: 「t1~t6の最大値」の最小値
    """
    # 循環構造があるので、a1 < a2 < a3 < a4 < a5 < a6 の場合のみ考える
    a1a6_rank_set = set([1, 2, 3, 4, 5, 6, 7]) - set([a0])
    a1a6 = sorted(list(a1a6_rank_set))

    if (b0 < 7 and c0 < 7):
        b1b6_rank_set = set([1, 2, 3, 4, 5, 6, 7]) - set([b0])
        c1c6_rank_set = set([1, 2, 3, 4, 5, 6, 7]) - set([c0])
    elif (b0 < 7 and c0 >= 7):
        b1b6_rank_set = set([1, 2, 3, 4, 5, 6, 7]) - set([b0])
        c1c6_rank_set = set([1, 2, 3, 4, 5, 6])
    else:
        b1b6_rank_set = set([1, 2, 3, 4, 5, 6])
        c1c6_rank_set = set([1, 2, 3, 4, 5, 6])

    # 競技B, Cにおける選手P1~P6の順位の組み合わせ
    b1b6_permutation = list(itertools.permutations(b1b6_rank_set))
    c1c6_permutation = list(itertools.permutations(c1c6_rank_set))

    # 競技B, Cにおける選手P1~P6の順位の全組み合わせから最小となる「t1~t6の最大値」を求める
    min_max_ti = float('inf')
    min_max_ti_elements = None
    for b1b6 in b1b6_permutation:
        for c1c6 in c1c6_permutation:
            max_ti = float('-inf')
            max_ti_elements = None
            for i in [1, 2, 3, 4, 5, 6]:
                ti = a1a6[i - 1] * b1b6[i - 1] * c1c6[i - 1]
                if max_ti < ti:
                    max_ti = ti
                    max_ti_elements = [b1b6, c1c6]
            if min_max_ti > max_ti:
                min_max_ti = max_ti
                min_max_ti_elements = max_ti_elements

    # 最小値のときの選手P1~P6の順位の組
    [b1b6, c1c6] = min_max_ti_elements
    p1 = (a1a6[0], b1b6[0], c1c6[0])
    p2 = (a1a6[1], b1b6[1], c1c6[1])
    p3 = (a1a6[2], b1b6[2], c1c6[2])
    p4 = (a1a6[3], b1b6[3], c1c6[3])
    p5 = (a1a6[4], b1b6[4], c1c6[4])
    p6 = (a1a6[5], b1b6[5], c1c6[5])

    return [p1, p2, p3, p4, p5, p6], min_max_ti


def search_larger_c0_results(p0, min_max_ti, p1p6):
    """
    step1で求めた答えから、より大きいc0の解を探索する

    Arguments:
        p0 {list} -- 選手P0の競技A,B,Cの順位 [a0, b0, c0]
        min_max_ti {int} -- step1で求めた p0における「t1~t6の最大値」の最小値
        p1p6 {list} -- step1で求めた 選手P1~P6の競技A,B,Cの順位の配列

    Returns:
        [list] -- より大きいc0の解の配列
    """
    [a0, b0, c0] = p0
    additional_results = []
    c0_temp = c0 + 1
    while a0 * b0 * c0_temp <= min_max_ti:
        additional_results.append({
            'p0': [a0, b0, c0_temp],
            't0': a0 * b0 * c0_temp,
            'p1p6': p1p6,
            'min_max_ti': min_max_ti,
            'must_go_final': True,
            'inserted_at': 'step2'
        })
        c0_temp += 1
    return additional_results


def output(results):
    # t0でソートして結果出力
    t0_sorted_results = sorted(results, key=lambda r: r['t0'])
    with open(T0_SORTED_RESULTS_FILE_NAME, 'w') as f:
        for result in t0_sorted_results:
            f.write(json.dumps(result, sort_keys=True) + '\n')

    # a0, b0, c0でソートして結果出力
    a0_b0_c0_key = lambda r: '{0:04d},{1:04d},{2:04d}'.format(r['p0'][0], r['p0'][1], r['p0'][2])
    a0_b0_c0_sorted_results = sorted(results, key=a0_b0_c0_key)
    with open(A0_B0_C0_SORTED_RESULTS_FILE_NAME, 'w') as f:
        for result in a0_b0_c0_sorted_results:
            f.write(json.dumps(result, sort_keys=True) + '\n')


def main():
    results = []

    # step1: 1<=a0<=6, a0<=b0<=7, b0<=c0<=7 における解を探索する
    for a0 in [1, 2, 3, 4, 5, 6]:
        for b0 in range(a0, 8):
            for c0 in range(b0, 8):
                p1p6, min_max_ti = min_max_rank_product(a0, b0, c0)

                # 選手P0は必ず決勝にいけるか
                t0 = a0 * b0 * c0
                must_go_final = t0 <= min_max_ti

                result = {
                    'p0': [a0, b0, c0],
                    't0': t0,
                    'p1p6': [list(pi) for pi in p1p6],
                    'min_max_ti': min_max_ti,
                    'must_go_final': must_go_final,
                    'inserted_at': 'step1'
                }

                print(result)
                results.append(result)

    # step2: 1<=a0<=6, a0<=b0<=7, 8<=c0 における解を探索する
    print('must_go_final=Trueである結果の中で、b0<=6 かつ c0==7 のもの')

    def is_step2_target(r):
        return r['must_go_final'] and r['p0'][1] <= 6 and r['p0'][2] == 7

    c0_is_7 = list(filter(is_step2_target, results))
    if len(c0_is_7) == 0:
        print('└ 存在しない')
    for result in c0_is_7:
        print(result)
        additional_results = search_larger_c0_results(
            result['p0'], result['min_max_ti'], result['p1p6'])
        results.extend(additional_results)

    # step3: 1<=a0<=6, 8<=b0, 8<=c0 における解を探索する
    print('must_go_final=Trueである結果の中で、b0==7 かつ c0==7 のもの')

    def is_step3_target(r):
        return r['must_go_final'] and r['p0'][1] == 7 and r['p0'][2] == 7

    b0_and_c0_are_7 = list(filter(is_step3_target, results))
    if len(b0_and_c0_are_7) == 0:
        print('└ 存在しない')
    for result in b0_and_c0_are_7:
        print(result)
        # もし存在したら search_larger_b0_c0_results 関数を用意する
        # 今回は存在しないようなので省略

    # 結果出力
    output(results)


if __name__ == "__main__":
    main()
