# WaselX Express — Optimizing Last-Mile Delivery Operations Using DSA

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://waselx-express.streamlit.app)

## 📋 Project Overview

WaselX Express is a fictional UAE-based last-mile delivery company. This project solves three critical business problems using Data Structures & Algorithms:

1. **Inefficient delivery routes** → Graph algorithms (Dijkstra, Floyd-Warshall, MST)
2. **Slow order dispatch** → Priority Queue with Min-Heap
3. **Poor order lookup** → Binary Search Tree & AVL Tree

## 👥 Team Information

| | |
|---|---|
| **Institution** | SP Jain School of Global Management, Dubai |
| **Program** | Masters in AI with Business (MAIB) |
| **Subject** | Data Structures and Algorithms |
| **Group** | Group 3 |
| **Members** | Kartik Joshi, Gagandeep Singh, Samuel Alex, Prem Kukreja |

## 📁 Repository Structure

```
WaselX-Express/
├── WaselX_MAIB_Final_Project.ipynb   # Main Jupyter notebook (27 questions)
├── app.py                            # Unified Streamlit app (Q6 + Q27)
├── report.tex                        # LaTeX report source
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
└── figures/
    ├── graph_network_full.png        # Q1 — Full 15-node network
    ├── dijkstra_path_h1_d1.png       # Q2 — Shortest path H1→D1
    ├── floyd_warshall_hubs.png       # Q3 — All-pairs hub heatmap
    ├── mst_kruskal.png               # Q4a — Kruskal's MST
    ├── mst_prim.png                  # Q4c — Prim's MST
    ├── bfs_tree_h3.png               # Q7a — BFS tree from H3
    ├── bst_initial.png               # Q8a — Initial BST
    ├── bst_after_deletion.png        # Q8d — BST after deleting 1078
    ├── avl_tree_final.png            # Q9b — Final AVL tree
    ├── sorting_performance.png       # Q22c — Merge vs Quick Sort
    └── road_closure_comparison.png   # Q27d — Road closure comparison
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.10 or later
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/KartikJoshi23/WaselX-Express.git
cd WaselX-Express

# Install dependencies
pip install -r requirements.txt
```

### Running the Jupyter Notebook

```bash
jupyter notebook WaselX_MAIB_Final_Project.ipynb
```

### Running the Streamlit App

```bash
streamlit run app.py
```

The app includes three modules accessible via the sidebar:
- **🏠 Overview** — Network map and edge table
- **🗺️ Q6: Path Visualizer** — Interactive shortest path with dual-path overlay
- **🛣️ Q27: Path Simulator** — Multi-criteria optimization + road closure simulation

## 🌐 Live Deployment

| App | Link |
|-----|------|
| Streamlit App | [waselx-express.streamlit.app](https://waselx-express.streamlit.app) |

## 📊 Network Data

- **15 nodes**: 7 Hubs (H1–H7) + 8 Delivery Zones (D1–D8)
- **24 bidirectional edges** with 3 weight types: Distance (km), Time (min), Cost (AED)
- **Coverage**: Dubai, Abu Dhabi, Sharjah, Ajman
- **Note**: Network has 2 disconnected components (Dubai–Sharjah and Abu Dhabi)

## 🔧 Technical Standards

- All data structures (heap, BST, AVL, linked list, stack, queue) implemented **from scratch**
- `heapq` and `collections` used **only** for benchmark comparisons
- `NetworkX` used **only** for graph visualization (no algorithm computation)
- All AI-assisted code marked with `# AI-ASSISTED` comments
- Reproducible with `seed=42` for all random operations

## 📝 Academic Integrity

This project was developed with AI assistance as a learning and debugging aid. All algorithmic logic, implementations, and business analysis were reviewed, understood, and verified by Group 3: Kartik Joshi, Gagandeep Singh, Samuel Alex, and Prem Kukreja.
