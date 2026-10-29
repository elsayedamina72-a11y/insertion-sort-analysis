"""
Mini Project: Empirical analysis of insertion sort
Steps: 1) Implement  2) Experiment  3) Analyze  4) Report (see report.pdf)
"""
import random
import time
import json
import matplotlib.pyplot as plt


# ---------- 1) Implement ----------
def insertion_sort(arr):
    """Sorts a copy of arr. Returns (sorted_list, comparisons, shifts)."""
    a = arr[:]
    comparisons = 0
    shifts = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]
                shifts += 1
                j -= 1
            else:
                break
        a[j + 1] = key
    return a, comparisons, shifts


def merge_sort(a):
    """Standard top-down merge sort (used only for the comparison)."""
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left, right = merge_sort(a[:mid]), merge_sort(a[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:]); out.extend(right[j:])
    return out


# Sanity checks (examples from the answer key)
_, c, s = insertion_sort([4, 3, 2, 1])
print(f"[4,3,2,1] -> comparisons={c}, shifts={s}  (expected 6, 6)")
_, c, s = insertion_sort([1, 2, 3, 4])
print(f"[1,2,3,4] -> comparisons={c}, shifts={s}  (expected 3, 0)")
test = [random.randint(0, 999) for _ in range(500)]
assert insertion_sort(test)[0] == sorted(test) == merge_sort(test)


# ---------- 2) Experiment ----------
def make_input(kind, n):
    if kind == "sorted":
        return list(range(n))
    if kind == "reverse":
        return list(range(n, 0, -1))
    return random.sample(range(n * 10), n)


random.seed(42)
sizes = [100, 500, 1000, 2000, 3000, 4000, 5000]
kinds = ["sorted", "reverse", "random"]
RUNS = 3

def avg_time_ms(fn, data):
    total = 0.0
    for _ in range(RUNS):
        t = time.perf_counter()
        fn(data)
        total += time.perf_counter() - t
    return total / RUNS * 1000

times = {k: [] for k in kinds}
merge_times = {k: [] for k in kinds}
comps = {k: [] for k in kinds}
shifts_d = {k: [] for k in kinds}

print(f"\n{'type':<9}{'n':>6}{'insertion(ms)':>15}{'merge(ms)':>12}{'comparisons':>14}{'shifts':>12}")
for kind in kinds:
    for n in sizes:
        data = make_input(kind, n)
        _, c, s = insertion_sort(data)
        t_ins = avg_time_ms(insertion_sort, data)
        t_mrg = avg_time_ms(merge_sort, data)
        times[kind].append(t_ins)
        merge_times[kind].append(t_mrg)
        comps[kind].append(c)
        shifts_d[kind].append(s)
        print(f"{kind:<9}{n:>6}{t_ins:>15.2f}{t_mrg:>12.2f}{c:>14}{s:>12}")

with open("results.json", "w") as f:
    json.dump({"sizes": sizes, "insertion_ms": times, "merge_ms": merge_times,
               "comparisons": comps, "shifts": shifts_d}, f, indent=2)


# ---------- 3) Analyze ----------
colors = {"sorted": "green", "reverse": "red", "random": "blue"}
n_max = sizes[-1]

# Plot 1: insertion sort vs O(n) and O(n^2)
plt.figure(figsize=(8, 5))
for kind in kinds:
    plt.plot(sizes, times[kind], marker="o", label=f"{kind} (measured)", color=colors[kind])
scale_n2 = times["reverse"][-1] / n_max ** 2
scale_n = times["sorted"][-1] / n_max
plt.plot(sizes, [scale_n2 * n ** 2 for n in sizes], "--", color="black", label="O(n²) reference")
plt.plot(sizes, [scale_n * n for n in sizes], "--", color="gray", label="O(n) reference")
plt.xlabel("Input size n")
plt.ylabel("Running time (ms)")
plt.title("Insertion Sort: Running Time vs n")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("insertion_sort_plot.png", dpi=150)
plt.close()

# Plot 2: insertion sort vs merge sort (random input)
plt.figure(figsize=(8, 5))
plt.plot(sizes, times["random"], marker="o", color="blue", label="Insertion sort (random)")
plt.plot(sizes, merge_times["random"], marker="s", color="orange", label="Merge sort (random)")
plt.xlabel("Input size n")
plt.ylabel("Running time (ms)")
plt.title("Insertion Sort vs Merge Sort (random input)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("insertion_vs_merge_plot.png", dpi=150)
plt.close()

print("\nSaved: insertion_sort_plot.png, insertion_vs_merge_plot.png, results.json")
