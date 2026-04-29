# AI-ASSISTED — WaselX Express: Unified Streamlit Application
"""
WaselX Express — Delivery Network Simulator
Group 3 | SP Jain MAIB | DSA Final Project
Kartik Joshi, Gagandeep Singh, Samuel Alex, Prem Kukreja
"""

import streamlit as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import pandas as pd

# ═══════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="WaselX Express — DSA Simulator",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════
# NETWORK DATA (exact from project brief Section 2)
# ═══════════════════════════════════════════════════════════
NODES = {
    'H1': 'Dubai Marina Hub', 'H2': 'Business Bay Hub', 'H3': 'Deira Hub',
    'H4': 'JLT Hub', 'H5': 'Abu Dhabi Corniche Hub', 'H6': 'Khalifa City Hub',
    'H7': 'Sharjah Al Nahda Hub', 'D1': 'Downtown Dubai', 'D2': 'Al Quoz Industrial',
    'D3': 'Jumeirah', 'D4': 'Silicon Oasis', 'D5': 'Ajman City Centre',
    'D6': 'Yas Island', 'D7': 'Al Reem Island', 'D8': 'Muwaileh (University City)',
}

EDGES = [
    ('H1', 'H4', 'Sheikh Zayed Rd', 5, 10, 3.5),
    ('H1', 'D3', 'Jumeirah Beach Rd', 4, 12, 3.0),
    ('H1', 'D1', 'Al Khail Rd', 8, 15, 5.5),
    ('H4', 'D2', 'Hessa St', 6, 14, 4.0),
    ('H4', 'H2', 'Sheikh Zayed Rd', 7, 13, 5.0),
    ('H2', 'D1', 'Financial Centre Rd', 3, 8, 2.5),
    ('H2', 'H3', 'Al Maktoum Bridge', 9, 18, 6.0),
    ('H3', 'D4', 'Dubai-Al Ain Rd', 12, 22, 8.0),
    ('H3', 'H7', 'Emirates Rd', 15, 25, 10.0),
    ('H7', 'D8', 'University Rd', 4, 8, 3.0),
    ('H7', 'D5', 'Sheikh Mohammed Rd', 10, 18, 7.0),
    ('D1', 'D3', '2nd December St', 5, 11, 3.5),
    ('D1', 'D2', 'Al Khail Rd', 6, 13, 4.0),
    ('D2', 'D4', 'Hatta Rd', 10, 20, 7.0),
    ('H5', 'D7', 'Corniche Rd', 6, 12, 4.0),
    ('H5', 'H6', 'Abu Dhabi Ring Rd', 14, 20, 9.0),
    ('H6', 'D6', 'Yas Connector', 8, 15, 5.5),
    ('D6', 'D7', 'Al Saadiyat Bridge', 7, 13, 5.0),
    ('H5', 'D6', 'Island Bypass', 12, 22, 8.0),
    ('D4', 'D8', 'Academic City Rd', 18, 30, 12.0),
    ('H3', 'D2', 'Al Asayel St', 8, 16, 5.5),
    ('H1', 'H2', 'Happiness St', 10, 18, 7.0),
    ('D5', 'D8', 'Sharjah Ring Rd', 8, 15, 5.5),
    ('H6', 'D7', 'Reem Bridge', 10, 18, 7.0),
]

NODE_POS = {
    'H1': (1, 6), 'H2': (4, 5.5), 'H3': (7, 7), 'H4': (2.5, 8),
    'H5': (-5, 2), 'H6': (-3, 0.5), 'H7': (10, 8),
    'D1': (3, 4), 'D2': (4.5, 3), 'D3': (1.5, 4), 'D4': (8, 3),
    'D5': (12, 9), 'D6': (-4, -1), 'D7': (-6, 2.5), 'D8': (11, 5),
}

ALL_NODES = sorted(NODES.keys())
CRITERIA = {'Distance (km)': 0, 'Time (min)': 1, 'Cost (AED)': 2}

# ═══════════════════════════════════════════════════════════
# DATA STRUCTURES — ALL FROM SCRATCH
# ═══════════════════════════════════════════════════════════

class MinHeap:
    """Min-heap priority queue — implemented from scratch."""
    def __init__(self):
        self.heap = []

    def push(self, item):
        self.heap.append(item)
        i = len(self.heap) - 1
        while i > 0:
            parent = (i - 1) // 2
            if self.heap[i][0] < self.heap[parent][0]:
                self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
                i = parent
            else:
                break

    def pop(self):
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return root

    def _sift_down(self, i):
        size = len(self.heap)
        while True:
            smallest = i
            left = 2 * i + 1
            right = 2 * i + 2
            if left < size and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < size and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right
            if smallest != i:
                self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
                i = smallest
            else:
                break

    def is_empty(self):
        return len(self.heap) == 0


# ═══════════════════════════════════════════════════════════
# GRAPH ALGORITHMS
# ═══════════════════════════════════════════════════════════

def build_adj(blocked=None):
    """Build adjacency list, optionally blocking an edge."""
    adj = {n: [] for n in ALL_NODES}
    for u, v, road, d, t, c in EDGES:
        if blocked and ((u, v) == blocked or (v, u) == blocked):
            continue
        adj[u].append((v, d, t, c))
        adj[v].append((u, d, t, c))
    return adj


def dijkstra(adj, source, target, weight_idx):
    """Dijkstra's shortest path using from-scratch MinHeap."""
    INF = float('inf')
    dist = {n: INF for n in adj}
    prev = {n: None for n in adj}
    dist[source] = 0
    visited = set()
    heap = MinHeap()
    heap.push((0, source))

    while not heap.is_empty():
        d, u = heap.pop()
        if u in visited:
            continue
        visited.add(u)
        if u == target:
            break
        for neighbor, *weights in adj[u]:
            w = weights[weight_idx]
            new_dist = dist[u] + w
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = u
                heap.push((new_dist, neighbor))

    # Reconstruct path
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()

    if dist[target] == INF:
        return [], INF
    return path, dist[target]


def path_costs(path, adj):
    """Compute total distance, time, and cost for a path."""
    total_dist = total_time = total_cost = 0
    for i in range(len(path) - 1):
        for neighbor, d, t, c in adj[path[i]]:
            if neighbor == path[i + 1]:
                total_dist += d
                total_time += t
                total_cost += c
                break
    return total_dist, total_time, total_cost


# ═══════════════════════════════════════════════════════════
# VISUALIZATION
# ═══════════════════════════════════════════════════════════

def draw_network(adj, paths_data, blocked=None, title="WaselX Network"):
    """Draw the network with highlighted paths."""
    fig, ax = plt.subplots(1, 1, figsize=(14, 9))

    # Build NetworkX graph for drawing
    G = nx.Graph()
    for n in NODES:
        G.add_node(n)
    for u, v, road, d, t, c in EDGES:
        if blocked and ((u, v) == blocked or (v, u) == blocked):
            continue
        G.add_edge(u, v, label=f"{d}km")

    # Draw base edges
    nx.draw_networkx_edges(G, NODE_POS, ax=ax, edge_color='#CCCCCC', width=1.2, alpha=0.5)

    # Draw highlighted paths
    colors = ['#E74C3C', '#2980B9', '#27AE60']
    handles = []
    path_nodes = set()

    for idx, pd_item in enumerate(paths_data):
        col = colors[idx % len(colors)]
        path = pd_item['path']
        if len(path) < 2:
            continue
        pe = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(G, NODE_POS, edgelist=pe, ax=ax,
                               edge_color=col, width=4, alpha=0.85)
        path_nodes.update(path)
        handles.append(mpatches.Patch(color=col, label=pd_item['label']))

    # Draw blocked edge as dashed red X
    if blocked:
        bx = [NODE_POS[blocked[0]][0], NODE_POS[blocked[1]][0]]
        by = [NODE_POS[blocked[0]][1], NODE_POS[blocked[1]][1]]
        ax.plot(bx, by, 'x--', color='red', linewidth=2.5, markersize=18, alpha=0.8)
        handles.append(mpatches.Patch(color='red', label=f'Blocked: {blocked[0]}↔{blocked[1]}'))

    # Draw nodes
    for n in ALL_NODES:
        is_hub = n.startswith('H')
        in_path = n in path_nodes
        color = '#FF6B35' if is_hub else '#4ECDC4'
        if in_path:
            color = '#E74C3C' if not is_hub else '#D35400'
        size = 700 if in_path else 500
        nx.draw_networkx_nodes(G, NODE_POS, nodelist=[n], ax=ax,
                               node_color=color, node_size=size,
                               edgecolors='#333333', linewidths=1.8)

    # Labels
    labels = {n: f"{n}\n{NODES[n].split()[0]}" for n in ALL_NODES}
    nx.draw_networkx_labels(G, NODE_POS, labels=labels, ax=ax, font_size=7, font_weight='bold')

    # Edge labels
    edge_labels = {}
    for u, v, road, d, t, c in EDGES:
        if blocked and ((u, v) == blocked or (v, u) == blocked):
            continue
        edge_labels[(u, v)] = f"{d}km"
    nx.draw_networkx_edge_labels(G, NODE_POS, edge_labels=edge_labels, ax=ax,
                                  font_size=6, font_color='#666666')

    if handles:
        ax.legend(handles=handles, loc='lower left', fontsize=10,
                  framealpha=0.9, edgecolor='#333')

    ax.set_title(title, fontsize=15, fontweight='bold', pad=15)
    ax.set_facecolor('#FAFAFA')
    ax.axis('off')
    fig.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════

st.sidebar.title("🚚 WaselX Express")
st.sidebar.markdown("**DSA Final Project — Group 3**")
st.sidebar.markdown("SP Jain School of Global Management")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select Module",
    ["🏠 Overview", "🗺️ Q6: Path Visualizer", "🛣️ Q27: Path Simulator"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Team Members:**")
st.sidebar.markdown("- Kartik Joshi\n- Gagandeep Singh\n- Samuel Alex\n- Prem Kukreja")


# ═══════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ═══════════════════════════════════════════════════════════

if page == "🏠 Overview":
    st.title("🚚 WaselX Express — Delivery Network Simulator")
    st.markdown("""
    **Optimizing Last-Mile Delivery Operations Across the UAE Using Data Structures & Algorithms**

    This application demonstrates two key simulation modules from the WaselX Express DSA project:

    | Module | Description |
    |--------|-------------|
    | **Q6: Path Visualizer** | Interactive shortest path computation with dual-path overlay |
    | **Q27: Path Simulator** | Multi-criteria optimization (distance/time/cost) with road closure |
    """)

    st.subheader("📊 Network Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Nodes", "15")
    col2.metric("Edges", "24")
    col3.metric("Hubs", "7")
    col4.metric("Delivery Zones", "8")

    st.subheader("🗺️ Full Network Map")
    adj = build_adj()
    fig = draw_network(adj, [], title="WaselX Express — Full Delivery Network (15 Nodes, 24 Edges)")
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("📋 Edge Table")
    edge_df = pd.DataFrame(
        [(u, v, road, d, t, c) for u, v, road, d, t, c in EDGES],
        columns=['From', 'To', 'Road', 'Distance (km)', 'Time (min)', 'Cost (AED)']
    )
    st.dataframe(edge_df, use_container_width=True, hide_index=True)

    st.info("⚠️ **Note:** The network has two disconnected components — "
            "Dubai–Sharjah cluster (H1–H4, H7, D1–D5, D8) and "
            "Abu Dhabi cluster (H5, H6, D6, D7). Cross-cluster paths are not possible.")


# ═══════════════════════════════════════════════════════════
# PAGE: Q6 — PATH VISUALIZER
# ═══════════════════════════════════════════════════════════

elif page == "🗺️ Q6: Path Visualizer":
    st.title("🗺️ Q6 — Interactive Shortest Path Visualizer")
    st.markdown("Compute Dijkstra's shortest path between any two nodes. "
                "Optionally overlay a second path for comparison.")

    adj = build_adj()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Path 1 (Primary)")
        src1 = st.selectbox("Source", ALL_NODES,
                            index=ALL_NODES.index('H1'), key='q6_s1')
        dst1 = st.selectbox("Destination", ALL_NODES,
                            index=ALL_NODES.index('D4'), key='q6_d1')
        crit1 = st.selectbox("Criterion", list(CRITERIA.keys()), key='q6_c1')

    with col2:
        st.subheader("Path 2 (Overlay)")
        enable2 = st.checkbox("Enable second path", value=False)
        src2 = st.selectbox("Source", ALL_NODES,
                            index=ALL_NODES.index('H3'), key='q6_s2',
                            disabled=not enable2)
        dst2 = st.selectbox("Destination", ALL_NODES,
                            index=ALL_NODES.index('D3'), key='q6_d2',
                            disabled=not enable2)
        crit2 = st.selectbox("Criterion", list(CRITERIA.keys()), key='q6_c2',
                             disabled=not enable2)

    if st.button("🔍 Compute Paths", type="primary", key='q6_btn'):
        paths_data = []

        # Path 1
        p1, cost1 = dijkstra(adj, src1, dst1, CRITERIA[crit1])
        if p1 and len(p1) > 1:
            d, t, c = path_costs(p1, adj)
            paths_data.append({'path': p1, 'label': f'Path 1: {src1}→{dst1} ({d}km, {t}min, {c}AED)'})
            st.success(f"**Path 1:** {' → '.join(p1)} | Distance: {d} km | Time: {t} min | Cost: {c} AED")
        else:
            st.error(f"❌ No path exists from {src1} to {dst1} (nodes in different components)")

        # Path 2
        if enable2:
            p2, cost2 = dijkstra(adj, src2, dst2, CRITERIA[crit2])
            if p2 and len(p2) > 1:
                d, t, c = path_costs(p2, adj)
                paths_data.append({'path': p2, 'label': f'Path 2: {src2}→{dst2} ({d}km, {t}min, {c}AED)'})
                st.success(f"**Path 2:** {' → '.join(p2)} | Distance: {d} km | Time: {t} min | Cost: {c} AED")
            else:
                st.error(f"❌ No path exists from {src2} to {dst2}")

        # Draw
        if paths_data:
            fig = draw_network(adj, paths_data,
                               title="Q6 — Shortest Path Visualization")
            st.pyplot(fig)
            plt.close(fig)


# ═══════════════════════════════════════════════════════════
# PAGE: Q27 — PATH SIMULATOR
# ═══════════════════════════════════════════════════════════

elif page == "🛣️ Q27: Path Simulator":
    st.title("🛣️ Q27 — Comprehensive Path Simulator")
    st.markdown("Multi-criteria path optimization with dynamic road closure simulation.")

    col1, col2, col3 = st.columns(3)
    with col1:
        src = st.selectbox("Source Node", ALL_NODES,
                           index=ALL_NODES.index('H1'), key='q27_src')
    with col2:
        dst = st.selectbox("Destination Node", ALL_NODES,
                           index=ALL_NODES.index('D4'), key='q27_dst')
    with col3:
        criterion = st.selectbox("Primary Criterion", list(CRITERIA.keys()), key='q27_crit')

    # Road closure selector
    st.subheader("🚧 Road Closure (Optional)")
    edge_labels = ["None"] + [
        f"{u} ↔ {v} ({road})" for u, v, road, d, t, c in EDGES
    ]
    closure_choice = st.selectbox("Block an edge", edge_labels, key='q27_closure')

    blocked = None
    if closure_choice != "None":
        idx = edge_labels.index(closure_choice) - 1  # offset by "None"
        blocked = (EDGES[idx][0], EDGES[idx][1])

    if st.button("🚀 Compute Optimal Paths", type="primary", key='q27_btn'):
        w_idx = CRITERIA[criterion]
        adj_orig = build_adj()
        adj_closed = build_adj(blocked) if blocked else None

        # ── All criteria comparison (original network) ──
        st.subheader("📊 Multi-Criteria Comparison (Original Network)")
        rows = []
        for cname, cidx in CRITERIA.items():
            p, _ = dijkstra(adj_orig, src, dst, cidx)
            if p and len(p) > 1:
                dd, tt, cc = path_costs(p, adj_orig)
                rows.append({
                    'Criterion': cname,
                    'Optimal Path': ' → '.join(p),
                    'Distance (km)': dd,
                    'Time (min)': tt,
                    'Cost (AED)': cc
                })
            else:
                rows.append({
                    'Criterion': cname,
                    'Optimal Path': 'NO PATH',
                    'Distance (km)': '∞',
                    'Time (min)': '∞',
                    'Cost (AED)': '∞'
                })

        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        # Check if different criteria produce different paths
        unique_paths = set(r['Optimal Path'] for r in rows if r['Optimal Path'] != 'NO PATH')
        if len(unique_paths) > 1:
            st.warning("⚠️ Different criteria produce **different** optimal paths!")
        elif len(unique_paths) == 1:
            st.info("✅ All criteria produce the **same** optimal path for this pair.")

        # ── Road closure comparison ──
        if blocked and adj_closed:
            st.subheader(f"🚧 Road Closure Impact: {blocked[0]} ↔ {blocked[1]}")

            p_orig, _ = dijkstra(adj_orig, src, dst, w_idx)
            p_closed, _ = dijkstra(adj_closed, src, dst, w_idx)

            if p_orig and len(p_orig) > 1:
                d1, t1, c1 = path_costs(p_orig, adj_orig)
            else:
                d1 = t1 = c1 = float('inf')

            if p_closed and len(p_closed) > 1:
                d2, t2, c2 = path_costs(p_closed, adj_closed)
                st.success(f"**Rerouted Path:** {' → '.join(p_closed)}")

                delta_df = pd.DataFrame({
                    'Metric': ['Distance (km)', 'Time (min)', 'Cost (AED)'],
                    'Original': [d1, t1, c1],
                    'Rerouted': [d2, t2, c2],
                    'Delta': [f"+{d2 - d1}" if d1 != float('inf') else 'N/A',
                              f"+{t2 - t1}" if t1 != float('inf') else 'N/A',
                              f"+{c2 - c1}" if c1 != float('inf') else 'N/A'],
                })
                st.dataframe(delta_df, use_container_width=True, hide_index=True)
            else:
                st.error("❌ No alternative path available with this road closed!")

            # Side-by-side visualization
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Original Network**")
                if p_orig and len(p_orig) > 1:
                    fig1 = draw_network(
                        adj_orig,
                        [{'path': p_orig, 'label': f"Original: {d1}km"}],
                        title=f"Original: {' → '.join(p_orig)}"
                    )
                    st.pyplot(fig1)
                    plt.close(fig1)

            with col_b:
                st.markdown("**After Road Closure**")
                if p_closed and len(p_closed) > 1:
                    fig2 = draw_network(
                        adj_closed,
                        [{'path': p_closed, 'label': f"Rerouted: {d2}km"}],
                        blocked=blocked,
                        title=f"Rerouted: {' → '.join(p_closed)}"
                    )
                    st.pyplot(fig2)
                    plt.close(fig2)

        else:
            # No closure — show single visualization
            p_main, _ = dijkstra(adj_orig, src, dst, w_idx)
            if p_main and len(p_main) > 1:
                d, t, c = path_costs(p_main, adj_orig)
                st.subheader("🗺️ Optimal Path Visualization")
                fig = draw_network(
                    adj_orig,
                    [{'path': p_main, 'label': f"{criterion}: {' → '.join(p_main)}"}],
                    title=f"Q27 — Optimal Path by {criterion}"
                )
                st.pyplot(fig)
                plt.close(fig)
