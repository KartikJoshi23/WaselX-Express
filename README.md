# WaselX Express — Optimizing Last-Mile Delivery Operations Using DSA

[![Live Demo](https://img.shields.io/badge/Live%20Demo-WaselX%20Express-blueviolet?style=for-the-badge)](https://waselx-express.netlify.app/)

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
├── WaselX_MAIB_Final_Project.ipynb   # Main Jupyter notebook (Q1–Q27)
├── app.py                            # Standalone Python app (graph + pathfinding)
├── web/
│   └── index.html                    # Production web dashboard (deployed on Netlify)
├── index.html                        # Root redirect to web/
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
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
# Local
jupyter notebook WaselX_MAIB_Final_Project.ipynb

# Or open in Google Colab
# Upload the .ipynb file and run all cells
```

### Running the Web Dashboard Locally

Open `web/index.html` in any modern browser — no server required.

## 🌐 Live Deployment

| App | Link |
|-----|------|
| Web Dashboard | [waselx-express.netlify.app](https://waselx-express.netlify.app/) |

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
