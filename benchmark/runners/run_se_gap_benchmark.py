"""Benchmark the SE algorithms that were missing from benchmark.tex.

Runs on the same 4 datasets as the existing benchmark:
  Karate (N=34, K=2), Caveman (N=100, K=10), SBM-Clean (N=150, K=3), SBM-Noisy (N=150, K=3)

Methods:
  - SEClust-Agglo      : agglomerative_se_clustering
  - SEClust-LocalMove  : multistart_se_heuristic  (free K, incremental backend)
  - SEClust-ConstrainedK: constrained_k_multistart (K fixed = ground truth K)
  - SEClust-MultiLevel : multilevel_se_clustering
  - HCSE               : hierarchical_se_clustering  (cuts at ground-truth K)

Usage:
    python experiments/run_se_gap_benchmark.py

Output: prints a markdown table and saves JSON to results/se_gap_benchmark.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import networkx as nx
import numpy as np
import scipy.sparse as sp
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

sys.path.insert(0, str(Path(__file__).parent.parent / "code" / "survey_support" / "src"))

from glass.seclust import (
    SparseGraph,
    agglomerative_se_clustering,
    constrained_k_multistart,
    hierarchical_se_clustering,
    multilevel_se_clustering,
    multistart_se_heuristic,
)

# ────────────────────────────────────────────────────────────────────────────
# Dataset constructors (same protocol as existing benchmark)
# ────────────────────────────────────────────────────────────────────────────

def karate_dataset():
    G = nx.karate_club_graph()
    labels = np.array([G.nodes[n]["club"] == "Officer" for n in sorted(G.nodes)], dtype=int)
    adj = nx.to_numpy_array(G, nodelist=sorted(G.nodes))
    return adj, labels, "Karate"


def caveman_dataset(seed=0):
    G = nx.connected_caveman_graph(10, 10)  # 10 cliques × 10 nodes = N=100, K=10
    labels = np.array([n // 10 for n in sorted(G.nodes)], dtype=int)
    adj = nx.to_numpy_array(G, nodelist=sorted(G.nodes))
    return adj, labels, "Caveman"


def sbm_dataset(noisy: bool, seed: int):
    rng = np.random.default_rng(seed)
    K, n_per = 3, 50  # N=150, K=3
    # Match the paper's parameters (verified against Louvain baseline)
    p_in  = 0.15 if noisy else 0.30
    p_out = 0.08 if noisy else 0.05
    sizes = [n_per] * K
    probs = [[p_in if i == j else p_out for j in range(K)] for i in range(K)]
    G = nx.stochastic_block_model(sizes, probs, seed=int(rng.integers(0, 2**31 - 1)))
    labels = np.array([G.nodes[n]["block"] for n in sorted(G.nodes)], dtype=int)
    adj = nx.to_numpy_array(G, nodelist=sorted(G.nodes))
    name = "SBM-Noisy" if noisy else "SBM-Clean"
    return adj, labels, name


DATASETS = {
    "Karate":    lambda seed: karate_dataset(),
    "Caveman":   lambda seed: caveman_dataset(seed),
    "SBM-Clean": lambda seed: sbm_dataset(False, seed),
    "SBM-Noisy": lambda seed: sbm_dataset(True, seed),
}

# ────────────────────────────────────────────────────────────────────────────
# Method runners
# ────────────────────────────────────────────────────────────────────────────

def run_method(name: str, adj: np.ndarray, K: int, seed: int) -> np.ndarray:
    """Return predicted labels for the given method."""
    if name == "deDoc":
        # Li et al. 2016: greedy agglomerative SE minimization — O(N^3)
        result = agglomerative_se_clustering(adj, target_clusters=K)
        return result.labels
    if name == "SEClust-Auto":
        # multistart local-move SE, free K (no K constraint)
        result = multistart_se_heuristic(adj, starts=8, seed=seed, backend="incremental")
        return result.labels
    if name == "SEClust-ConstrainedK":
        labels, _ = constrained_k_multistart(adj, target_clusters=K, starts=8, seed=seed)
        return labels
    if name == "SEClust-MultiLevel":
        result = multilevel_se_clustering(adj, starts=6, seed=seed)
        return result.labels
    if name == "HCSE":
        result = hierarchical_se_clustering(adj, target_clusters=K, seed=seed)
        return result.labels
    raise ValueError(f"Unknown method: {name}")


METHODS = [
    "deDoc",           # agglomerative SE (O(N^3), Karate only)
    "SEClust-Auto",    # multistart free-K (fast)
    "SEClust-ConstrainedK",
    "SEClust-MultiLevel",
    "HCSE",
]

# deDoc is O(N^3) — only run on very small graphs
DEDOC_MAX_NODES = 50
# SEClust-Agglo is O(N^3) — only run on tiny graphs (Karate N=34)
AGGLO_MAX_NODES = 40

SEEDS = [0, 1, 2, 3, 4]

# ────────────────────────────────────────────────────────────────────────────
# Main benchmark loop
# ────────────────────────────────────────────────────────────────────────────

def run_all() -> dict:
    results: dict[str, dict[str, list[dict]]] = {}

    for ds_name, ds_factory in DATASETS.items():
        results[ds_name] = {}
        print(f"\n=== {ds_name} ===")
        # Build once to get N for filtering
        sample_adj, _, _ = ds_factory(0)
        N = sample_adj.shape[0]
        active_methods = METHODS[:]
        if N > DEDOC_MAX_NODES and "deDoc" in active_methods:
            active_methods.remove("deDoc")
        if N > AGGLO_MAX_NODES and "SEClust-Agglo" in active_methods:
            active_methods.remove("SEClust-Agglo")
        for method in active_methods:
            aris, nmis = [], []
            for seed in SEEDS:
                adj, gt_labels, _ = ds_factory(seed)
                K = int(np.unique(gt_labels).size)
                try:
                    pred = run_method(method, adj, K, seed)
                except Exception as exc:
                    print(f"  {method} seed={seed} FAILED: {exc}")
                    continue
                aris.append(float(adjusted_rand_score(gt_labels, pred)))
                nmis.append(float(normalized_mutual_info_score(gt_labels, pred)))
            if aris:
                mean_ari = float(np.mean(aris))
                ci_ari   = float(1.96 * np.std(aris) / np.sqrt(len(aris)))
                mean_nmi = float(np.mean(nmis))
                ci_nmi   = float(1.96 * np.std(nmis) / np.sqrt(len(nmis)))
                print(f"  {method:<25} ARI={mean_ari:.3f}±{ci_ari:.3f}  NMI={mean_nmi:.3f}±{ci_nmi:.3f}")
                results[ds_name][method] = {
                    "ari_mean": mean_ari, "ari_ci": ci_ari,
                    "nmi_mean": mean_nmi, "nmi_ci": ci_nmi,
                    "ari_raw": aris, "nmi_raw": nmis,
                }
            else:
                results[ds_name][method] = None

    return results


def print_markdown(results: dict):
    methods = list({m for ds in results.values() for m in ds.keys()})
    methods.sort()
    datasets = list(DATASETS.keys())
    print("\n\n## Markdown table\n")
    print("| Dataset | Method | ARI | NMI |")
    print("|---------|--------|-----|-----|")
    for ds in datasets:
        for m in methods:
            r = results[ds].get(m)
            if r is None:
                print(f"| {ds} | {m} | FAILED | FAILED |")
            else:
                print(f"| {ds} | {m} | {r['ari_mean']:.3f}±{r['ari_ci']:.3f} | {r['nmi_mean']:.3f}±{r['nmi_ci']:.3f} |")


if __name__ == "__main__":
    results = run_all()
    print_markdown(results)
    out_path = Path(__file__).parent.parent / "results" / "se_gap_benchmark.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to {out_path}")
