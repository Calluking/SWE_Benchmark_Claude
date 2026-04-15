# Visualization helpers

This folder contains a simple count-based comparison chart for the
`sqlfluff__sqlfluff-2419` clean vs og-memory runs.

The chart is based on the tool counts summarized in
[sqlfluff_2419_clean_vs_ogmem.md](../sqlfluff_2419_clean_vs_ogmem.md):

- og-memory: `Read 18`, `Bash 17`, `Edit 1`, `Write 1`, `TaskOutput 4`
- clean: `Read 11`, `Bash 67`, `Edit 1`, `Write 1`

Run it with:

```bash
python3 visualize/plot_tool_counts.py \
  --output visualize/sqlfluff_2419_tool_counts.svg
```
