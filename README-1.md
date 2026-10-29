# Empirical Analysis of Insertion Sort

Mini project for *Algorithms: Analysis and Design*.

## Files
- `insertion_sort_project.py` - implementation (counts comparisons and shifts), experiments, and plots
- `insertion_sort_plot.png` - running time vs n for sorted / reverse / random inputs, with O(n) and O(n^2) references
- `insertion_vs_merge_plot.png` - insertion sort vs merge sort on random input
- `results.json` - raw measurements
- `report.pdf` - one-page report

## Run
```
pip install matplotlib
python insertion_sort_project.py
```

## Summary
| Input (n = 5000) | Insertion sort | Merge sort |
|---|---|---|
| Sorted | 0.52 ms | 5.70 ms |
| Random | 454 ms | 6.06 ms |
| Reverse | 1000 ms | 3.35 ms |

Insertion sort is O(n) on sorted input and O(n^2) on random and reverse input. Merge sort is O(n log n) in all cases.
