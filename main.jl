using Combinatorics
using JSON

struct Result
  p0
  t0
  ranks
  min_max_ti
  must_go_final
  inserted_at
end

# 全てのcの順列における「P0以外の選手の総合ptの最大値」の最小値
#
# AとBの順位が決まったとき「P0以外の選手の総合ptの最大値」の最小にするには、
# AとBの順位積の大きいほどCの順位が小さくなるような組み合わせにする
#
# これは証明できていない...
# ただn=6では総当たりと結果が一致した
# Cを総当たりする場合O(n!)以上の計算量になってしまうが、この関数ならO(n*log(n))
function min_max_abc_in_all_c(a, b, c)
  ab = map(x -> [x[1],x[2][1]*x[2][2]], enumerate(zip(a, b)))
  sorted_ab = sort!(ab, by = x -> x[2])
  reversed_c = sort!(copy(c), rev=true)
  abc_c = map(x -> [x[1][1], x[1][2]*x[2], x[2]], zip(sorted_ab, reversed_c))
  sorted_abc_c = sort!(abc_c, by = x -> x[1])
  best_c = map(x -> x[3], sorted_abc_c)
  abc = map(x -> x[2], sorted_abc_c)
  max_abc = maximum(abc)
  return (max_abc, best_c)
end

# 全てのbとcの順列の組み合わせにおける「P0以外の選手の総合ptの最大値」の最小値
function min_max_abc_in_all_b_and_c(n, a0, b0, c0, array_n, array_n_plus_1)
  # 1 ~ n+1 位のうち、a0,b0,c0以外のものを ranks_a,ranks_b,ranks_c とする
  ranks_a = setdiff(array_n_plus_1, [a0])
  ranks_b = b0 <= n ? setdiff(array_n_plus_1, [b0]) : array_n
  ranks_c = c0 <= n ? setdiff(array_n_plus_1, [c0]) : array_n

  # 初期値
  min_max_ti = 100000
  best_ranks_b = ranks_b
  best_ranks_c = copy(ranks_c)

  # すべてのbの順列を総当たりする
  for ranks_b_f in permutations(ranks_b)
    k = min_max_abc_in_all_c(ranks_a, ranks_b_f, ranks_c)
    if min_max_ti > k[1]
      min_max_ti = k[1]
      best_ranks_b = ranks_b_f
      best_ranks_c = k[2]
    end
  end

  # [[a1,b1,c1],[a2,b2,c2], ... , [an,bn,cn]]
  ranks = map(i -> [ranks_a[i], best_ranks_b[i], best_ranks_c[i]], array_n)

  return Result(
    [a0, b0, c0],
    a0 * b0 * c0,
    ranks,
    min_max_ti,
    a0 * b0 * c0 <= min_max_ti,
    "step1"
  )
end

# step1の結果から、c0>nである「P0以外の選手の総合ptの最大値」の最小値を探索する
function search_larger_c0_results(result)
  a0 = result.p0[1]
  b0 = result.p0[2]
  c0 = result.p0[3] + 1

  additional_results = []

  while a0 * b0 * c0 <= result.min_max_ti
    new_result = Result(
      [a0, b0, c0],
      a0 * b0 * c0,
      result.ranks,
      result.min_max_ti,
      true,
      "step2"
    )
    push!(additional_results, new_result)
    c0 += 1
  end

  return additional_results
end

# 結果をファイルに書き込む
function output(n, results)
  t0_sorted_results = sort!(results, by = r -> r.t0)
  open("./results_sorted_by_t0/$(n)_finalists", "w") do f
    for result in t0_sorted_results
      write(f, json(result) * "\n")
    end
  end

  a0_b0_c0_key = r -> lpad(r.p0[1], 4, "0") * lpad(r.p0[2], 4, "0") * lpad(r.p0[3], 4, "0")
  a0_b0_c0_sorted_results = sort!(results, by = a0_b0_c0_key)
  open("./results_sorted_by_a0_b0_c0/$(n)_finalists", "w") do f
    for result in a0_b0_c0_sorted_results
      write(f, json(result) * "\n")
    end
  end
end

function main()
  println("--- start ---")
  # 予選通過人数 n
  n = 6
  for a in ARGS
    n = parse(Int, a)
  end

  println("finalists: " * string(n))

  # step1
  println("step1")
  array_n = [1:n...]
  array_n_plus_1 = [1:n+1...]
  results = []
  for a0 in 1:n
    for b0 in a0:n+1
      for c0 in b0:n+1
        x = min_max_abc_in_all_b_and_c(n,a0,b0,c0,array_n,array_n_plus_1)
        push!(results, x)
        println(x)
      end
    end
  end

  # step2
  println("step2")
  is_step2_target = x -> r -> r.must_go_final && r.p0[2] <= x && r.p0[3] == x + 1
  c0_is_n = filter(is_step2_target(n), results)
  if length(c0_is_n) == 0
    println("No step2 targets")
  end
  for result in c0_is_n
    println(result)
    additional_results = search_larger_c0_results(result)
    append!(results, additional_results)
  end

  # step3
  println("step3")
  is_step3_target = x -> r -> r.must_go_final && r.p0[2] == x + 1 && r.p0[3] == x + 1
  b0_and_c0_are_n = filter(is_step3_target(n), results)
  if length(b0_and_c0_are_n) == 0
    println("No step3 targets")
  else
    println("Warning! There are probably more results")
    # n=10のときは存在する
  end
  for result in b0_and_c0_are_n
    println(result)
    # もし存在したら search_larger_b0_c0_results 関数を用意する
    # n=1,2,3,4,5,6,7,8,9のときは存在しないようなので省略
  end

  output(n, results)

  println("--- finished ---")
end

main()
