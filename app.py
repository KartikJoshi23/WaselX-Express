# AI-ASSISTED — WaselX Express: Unified Streamlit Application (v2 - Premium UI)
"""
WaselX Express — Delivery Network Simulator
Group 3 | SP Jain MAIB | DSA Final Project
"""

import streamlit as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import pandas as pd

st.set_page_config(page_title="WaselX Express", page_icon="🚚", layout="wide", initial_sidebar_state="expanded")

# ── Custom CSS ──
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    h1 { background: linear-gradient(90deg, #FF6B35, #4ECDC4); -webkit-background-clip: text;
         -webkit-text-fill-color: transparent; font-size: 2.2rem !important; }
    .stMetric { background: rgba(255,107,53,0.08); border-radius: 12px; padding: 12px; border-left: 4px solid #FF6B35; }
    .stDataFrame { border-radius: 8px; }
    div[data-testid="stImage"] img, .stPlotlyChart, div[data-testid="stpyplot"] {
        border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); }
    .route-card { background: linear-gradient(135deg, rgba(255,107,53,0.1), rgba(78,205,196,0.1));
                  border-radius: 12px; padding: 18px; margin: 8px 0; border-left: 5px solid #FF6B35; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1a1a2e, #16213e); }
    [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# NETWORK DATA
# ═══════════════════════════════════════════════════════════
NODES = {
    'H1':'Dubai Marina Hub','H2':'Business Bay Hub','H3':'Deira Hub','H4':'JLT Hub',
    'H5':'Abu Dhabi Corniche Hub','H6':'Khalifa City Hub','H7':'Sharjah Al Nahda Hub',
    'D1':'Downtown Dubai','D2':'Al Quoz Industrial','D3':'Jumeirah','D4':'Silicon Oasis',
    'D5':'Ajman City Centre','D6':'Yas Island','D7':'Al Reem Island','D8':'Muwaileh (Univ City)',
}
EDGES = [
    ('H1','H4','Sheikh Zayed Rd',5,10,3.5),('H1','D3','Jumeirah Beach Rd',4,12,3.0),
    ('H1','D1','Al Khail Rd',8,15,5.5),('H4','D2','Hessa St',6,14,4.0),
    ('H4','H2','Sheikh Zayed Rd',7,13,5.0),('H2','D1','Financial Centre Rd',3,8,2.5),
    ('H2','H3','Al Maktoum Bridge',9,18,6.0),('H3','D4','Dubai-Al Ain Rd',12,22,8.0),
    ('H3','H7','Emirates Rd',15,25,10.0),('H7','D8','University Rd',4,8,3.0),
    ('H7','D5','Sheikh Mohammed Rd',10,18,7.0),('D1','D3','2nd December St',5,11,3.5),
    ('D1','D2','Al Khail Rd',6,13,4.0),('D2','D4','Hatta Rd',10,20,7.0),
    ('H5','D7','Corniche Rd',6,12,4.0),('H5','H6','Abu Dhabi Ring Rd',14,20,9.0),
    ('H6','D6','Yas Connector',8,15,5.5),('D6','D7','Al Saadiyat Bridge',7,13,5.0),
    ('H5','D6','Island Bypass',12,22,8.0),('D4','D8','Academic City Rd',18,30,12.0),
    ('H3','D2','Al Asayel St',8,16,5.5),('H1','H2','Happiness St',10,18,7.0),
    ('D5','D8','Sharjah Ring Rd',8,15,5.5),('H6','D7','Reem Bridge',10,18,7.0),
]
NODE_POS = {
    'H1':(1,6),'H2':(4,5.5),'H3':(7,7),'H4':(2.5,8),'H5':(-5,2),'H6':(-3,0.5),
    'H7':(10,8),'D1':(3,4),'D2':(4.5,3),'D3':(1.5,4),'D4':(8,3),
    'D5':(12,9),'D6':(-4,-1),'D7':(-6,2.5),'D8':(11,5),
}
ALL_NODES = sorted(NODES.keys())
CRITERIA = {'Distance (km)':0, 'Time (min)':1, 'Cost (AED)':2}

# ═══════════════════════════════════════════════════════════
# MIN-HEAP & DIJKSTRA (from scratch)
# ═══════════════════════════════════════════════════════════
class MinHeap:
    def __init__(self): self.h=[]
    def push(self,x):
        self.h.append(x); i=len(self.h)-1
        while i>0:
            p=(i-1)//2
            if self.h[i][0]<self.h[p][0]: self.h[i],self.h[p]=self.h[p],self.h[i]; i=p
            else: break
    def pop(self):
        if len(self.h)==1: return self.h.pop()
        r=self.h[0]; self.h[0]=self.h.pop(); i=0; s=len(self.h)
        while True:
            sm=i; l=2*i+1; r2=2*i+2
            if l<s and self.h[l][0]<self.h[sm][0]: sm=l
            if r2<s and self.h[r2][0]<self.h[sm][0]: sm=r2
            if sm!=i: self.h[i],self.h[sm]=self.h[sm],self.h[i]; i=sm
            else: break
        return r
    def empty(self): return len(self.h)==0

def build_adj(blocked=None):
    adj={n:[] for n in ALL_NODES}
    for u,v,road,d,t,c in EDGES:
        if blocked and ((u,v)==blocked or (v,u)==blocked): continue
        adj[u].append((v,d,t,c)); adj[v].append((u,d,t,c))
    return adj

def dijkstra(adj,src,dst,wi):
    INF=float('inf'); dist={n:INF for n in adj}; prev={n:None for n in adj}
    dist[src]=0; vis=set(); hp=MinHeap(); hp.push((0,src))
    while not hp.empty():
        d,u=hp.pop()
        if u in vis: continue
        vis.add(u)
        if u==dst: break
        for nb,*w in adj[u]:
            nd=dist[u]+w[wi]
            if nd<dist[nb]: dist[nb]=nd; prev[nb]=u; hp.push((nd,nb))
    path=[]; n=dst
    while n is not None: path.append(n); n=prev[n]
    path.reverse()
    return (path,dist[dst]) if dist[dst]<INF else ([],INF)

def path_costs(path,adj):
    td=tt=tc=0
    for i in range(len(path)-1):
        for nb,d,t,c in adj[path[i]]:
            if nb==path[i+1]: td+=d;tt+=t;tc+=c;break
    return td,tt,tc

# ═══════════════════════════════════════════════════════════
# PREMIUM GRAPH DRAWING
# ═══════════════════════════════════════════════════════════
def draw_network(adj, paths_data, blocked=None, title="WaselX Network", figsize=(18,12)):
    fig, ax = plt.subplots(1,1, figsize=figsize, facecolor='white')
    ax.set_facecolor('white')

    G = nx.Graph()
    for n in NODES: G.add_node(n)
    for u,v,road,d,t,c in EDGES:
        if blocked and ((u,v)==blocked or (v,u)==blocked): continue
        G.add_edge(u,v,dist=d)

    # Base edges
    all_edges = list(G.edges())
    path_edges_set = set()
    colors = ['#E74C3C','#2980B9','#27AE60']
    handles = []
    path_nodes = set()
    for idx, pd_item in enumerate(paths_data):
        path = pd_item['path']
        if len(path) < 2: continue
        pe = [(path[i],path[i+1]) for i in range(len(path)-1)]
        for e in pe: path_edges_set.add(e); path_edges_set.add((e[1],e[0]))
        path_nodes.update(path)

    other_edges = [(u,v) for u,v in all_edges if (u,v) not in path_edges_set and (v,u) not in path_edges_set]
    nx.draw_networkx_edges(G, NODE_POS, edgelist=other_edges, ax=ax, edge_color='#BBBBBB', width=1.8, alpha=0.6)

    for idx, pd_item in enumerate(paths_data):
        col = colors[idx % len(colors)]
        path = pd_item['path']
        if len(path) < 2: continue
        pe = [(path[i],path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G, NODE_POS, edgelist=pe, ax=ax, edge_color=col, width=5.0, alpha=0.9)
        handles.append(mpatches.Patch(color=col, label=pd_item['label']))

    if blocked and blocked[0] in NODE_POS and blocked[1] in NODE_POS:
        bx = [NODE_POS[blocked[0]][0], NODE_POS[blocked[1]][0]]
        by = [NODE_POS[blocked[0]][1], NODE_POS[blocked[1]][1]]
        ax.plot(bx, by, 'X--', color='red', linewidth=3, markersize=18)
        handles.append(mpatches.Patch(color='red', label=f'Blocked: {blocked[0]}<->{blocked[1]}'))

    for n in ALL_NODES:
        is_hub = n.startswith('H')
        in_path = n in path_nodes
        if in_path:
            color = '#D35400' if is_hub else '#E74C3C'
            size = 1100
        elif is_hub:
            color = '#E67E22'
            size = 900
        else:
            color = '#1ABC9C'
            size = 700
        nx.draw_networkx_nodes(G, NODE_POS, nodelist=[n], ax=ax,
                               node_color=color, node_size=size,
                               edgecolors='#2C3E50', linewidths=2.5, alpha=0.95)

    nx.draw_networkx_labels(G, NODE_POS, ax=ax, font_size=12, font_weight='bold',
                            font_color='white', font_family='sans-serif')

    edge_labels = {}
    for u,v,road,d,t,c in EDGES:
        if blocked and ((u,v)==blocked or (v,u)==blocked): continue
        edge_labels[(u,v)] = f"{d}km"
    nx.draw_networkx_edge_labels(G, NODE_POS, edge_labels=edge_labels, ax=ax,
                                  font_size=9, font_color='#555555', font_weight='bold',
                                  bbox=dict(boxstyle='round,pad=0.2', fc='#F8F8F8', ec='#CCCCCC', alpha=0.9))

    if handles:
        ax.legend(handles=handles, loc='lower left', fontsize=12,
                  framealpha=0.95, edgecolor='#333', facecolor='white', handlelength=2)

    ax.set_title(title, fontsize=16, fontweight='bold', color='#2C3E50', pad=15)
    ax.axis('off')
    ax.margins(0.08)
    fig.tight_layout(pad=1.5)
    return fig

# ═══════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🚚 WaselX Express")
    st.markdown("**DSA Final Project — Group 3**")
    st.caption("SP Jain School of Global Management, Dubai")
    st.markdown("---")
    page = st.radio("Navigate", ["🏠 Overview", "🗺️ Q6: Path Visualizer", "🛣️ Q27: Path Simulator"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**Team:**")
    st.caption("Kartik Joshi · Gagandeep Singh\nSamuel Alex · Prem Kukreja")
    st.markdown("---")
    st.caption("Built with Dijkstra's Algorithm\n& from-scratch Min-Heap")

# ═══════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ═══════════════════════════════════════════════════════════
if page == "🏠 Overview":
    st.title("🚚 WaselX Express — Delivery Network Simulator")
    st.markdown("**Optimizing Last-Mile Delivery Operations Across the UAE Using DSA**")
    st.markdown("---")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("🏢 Nodes","15"); c2.metric("🛤️ Edges","24")
    c3.metric("📦 Hubs","7"); c4.metric("📍 Zones","8")

    st.markdown("### 🗺️ Full Network Map")
    adj = build_adj()
    fig = draw_network(adj, [], title="WaselX Express — Full Network (15 Nodes, 24 Edges)")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    with st.expander("📋 View Edge Table", expanded=False):
        edf = pd.DataFrame([(u,v,road,d,t,c) for u,v,road,d,t,c in EDGES],
                           columns=['From','To','Road','Dist (km)','Time (min)','Cost (AED)'])
        st.dataframe(edf, use_container_width=True, hide_index=True)

    st.info("⚠️ The network has **two disconnected components**: Dubai–Sharjah (H1–H4,H7,D1–D5,D8) and Abu Dhabi (H5,H6,D6,D7). Cross-cluster paths are not possible.")

# ═══════════════════════════════════════════════════════════
# PAGE: Q6
# ═══════════════════════════════════════════════════════════
elif page == "🗺️ Q6: Path Visualizer":
    st.title("🗺️ Q6 — Interactive Shortest Path Visualizer")
    st.markdown("Compute Dijkstra's shortest path between any two nodes with optional dual-path overlay.")
    st.markdown("---")

    adj = build_adj()
    c1,c2 = st.columns(2)
    with c1:
        st.markdown("#### Path 1")
        s1 = st.selectbox("Source",ALL_NODES,index=ALL_NODES.index('H1'),key='q6s1')
        d1 = st.selectbox("Destination",ALL_NODES,index=ALL_NODES.index('D4'),key='q6d1')
        cr1 = st.selectbox("Criterion",list(CRITERIA.keys()),key='q6c1')
    with c2:
        st.markdown("#### Path 2 (Overlay)")
        en2 = st.checkbox("Enable second path",value=False)
        s2 = st.selectbox("Source",ALL_NODES,index=ALL_NODES.index('H3'),key='q6s2',disabled=not en2)
        d2 = st.selectbox("Destination",ALL_NODES,index=ALL_NODES.index('D3'),key='q6d2',disabled=not en2)
        cr2 = st.selectbox("Criterion",list(CRITERIA.keys()),key='q6c2',disabled=not en2)

    if st.button("🔍 Compute Shortest Paths", type="primary", use_container_width=True, key='q6btn'):
        pdata = []
        p1,_ = dijkstra(adj,s1,d1,CRITERIA[cr1])
        if p1 and len(p1)>1:
            dd,tt,cc = path_costs(p1,adj)
            pdata.append({'path':p1,'label':f'Path 1: {s1}→{d1} ({dd}km, {tt}min, {cc}AED)'})
            st.markdown(f'<div class="route-card">✅ <b>Path 1:</b> {" → ".join(p1)}<br>📏 {dd} km &nbsp;|&nbsp; ⏱️ {tt} min &nbsp;|&nbsp; 💰 {cc} AED</div>', unsafe_allow_html=True)
        else:
            st.error(f"❌ No path from {s1} to {d1} — nodes in different network components")

        if en2:
            p2,_ = dijkstra(adj,s2,d2,CRITERIA[cr2])
            if p2 and len(p2)>1:
                dd,tt,cc = path_costs(p2,adj)
                pdata.append({'path':p2,'label':f'Path 2: {s2}→{d2} ({dd}km, {tt}min, {cc}AED)'})
                st.markdown(f'<div class="route-card">✅ <b>Path 2:</b> {" → ".join(p2)}<br>📏 {dd} km &nbsp;|&nbsp; ⏱️ {tt} min &nbsp;|&nbsp; 💰 {cc} AED</div>', unsafe_allow_html=True)
            else:
                st.error(f"❌ No path from {s2} to {d2}")

        if pdata:
            fig = draw_network(adj, pdata, title="Q6 — Shortest Path Visualization")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

# ═══════════════════════════════════════════════════════════
# PAGE: Q27
# ═══════════════════════════════════════════════════════════
elif page == "🛣️ Q27: Path Simulator":
    st.title("🛣️ Q27 — Comprehensive Path Simulator")
    st.markdown("Multi-criteria optimization with dynamic road closure simulation.")
    st.markdown("---")

    c1,c2,c3 = st.columns(3)
    with c1: src = st.selectbox("Source",ALL_NODES,index=ALL_NODES.index('H1'),key='q27s')
    with c2: dst = st.selectbox("Destination",ALL_NODES,index=ALL_NODES.index('D4'),key='q27d')
    with c3: crit = st.selectbox("Primary Criterion",list(CRITERIA.keys()),key='q27c')

    st.markdown("#### 🚧 Road Closure")
    elabels = ["None"]+[f"{u} ↔ {v} ({road})" for u,v,road,_,_,_ in EDGES]
    closure = st.selectbox("Block an edge",elabels,key='q27cl')
    blocked = None
    if closure != "None":
        idx = elabels.index(closure)-1
        blocked = (EDGES[idx][0], EDGES[idx][1])

    if st.button("🚀 Compute Optimal Paths", type="primary", use_container_width=True, key='q27btn'):
        wi = CRITERIA[crit]
        adj_o = build_adj()
        adj_c = build_adj(blocked) if blocked else None

        # Multi-criteria table
        st.markdown("### 📊 Multi-Criteria Comparison")
        rows = []
        for cn,ci in CRITERIA.items():
            p,_ = dijkstra(adj_o,src,dst,ci)
            if p and len(p)>1:
                dd,tt,cc = path_costs(p,adj_o)
                rows.append({'Criterion':cn,'Path':' → '.join(p),'Distance (km)':dd,'Time (min)':tt,'Cost (AED)':cc})
            else:
                rows.append({'Criterion':cn,'Path':'NO PATH','Distance (km)':'∞','Time (min)':'∞','Cost (AED)':'∞'})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        uniq = set(r['Path'] for r in rows if r['Path']!='NO PATH')
        if len(uniq)>1: st.warning("⚠️ Different criteria produce **different** optimal paths!")
        elif len(uniq)==1: st.info("✅ All criteria produce the **same** optimal path.")

        if blocked and adj_c:
            st.markdown(f"### 🚧 Road Closure: {blocked[0]} ↔ {blocked[1]}")
            p_o,_ = dijkstra(adj_o,src,dst,wi)
            p_c,_ = dijkstra(adj_c,src,dst,wi)

            d1=t1=c1_v=0
            if p_o and len(p_o)>1: d1,t1,c1_v = path_costs(p_o,adj_o)
            if p_c and len(p_c)>1:
                d2,t2,c2_v = path_costs(p_c,adj_c)
                st.markdown(f'<div class="route-card">🔄 <b>Rerouted:</b> {" → ".join(p_c)}<br>📏 {d2}km &nbsp;|&nbsp; ⏱️ {t2}min &nbsp;|&nbsp; 💰 {c2_v}AED</div>', unsafe_allow_html=True)
                if d1>0:
                    st.dataframe(pd.DataFrame({
                        'Metric':['Distance (km)','Time (min)','Cost (AED)'],
                        'Original':[d1,t1,c1_v], 'Rerouted':[d2,t2,c2_v],
                        'Delta':[f"+{d2-d1}",f"+{t2-t1}",f"+{round(c2_v-c1_v,1)}"]
                    }), use_container_width=True, hide_index=True)
            else:
                st.error("❌ No alternative path with this road closed!")

            # Side-by-side — FULL WIDTH graphs
            st.markdown("### 🗺️ Visual Comparison")
            ca,cb = st.columns(2)
            with ca:
                st.markdown("**Original Network**")
                if p_o and len(p_o)>1:
                    fig1 = draw_network(adj_o,[{'path':p_o,'label':f'Original: {d1}km'}],
                                       title=f"Original: {' → '.join(p_o)}", figsize=(14,10))
                    st.pyplot(fig1, use_container_width=True)
                    plt.close(fig1)
            with cb:
                st.markdown("**After Road Closure**")
                if p_c and len(p_c)>1:
                    fig2 = draw_network(adj_c,[{'path':p_c,'label':f'Rerouted: {d2}km'}],
                                       blocked=blocked,
                                       title=f"Rerouted: {' → '.join(p_c)}", figsize=(14,10))
                    st.pyplot(fig2, use_container_width=True)
                    plt.close(fig2)
        else:
            # No closure — single full-width graph
            p_m,_ = dijkstra(adj_o,src,dst,wi)
            if p_m and len(p_m)>1:
                dd,tt,cc = path_costs(p_m,adj_o)
                st.markdown(f'<div class="route-card">✅ <b>Optimal Path:</b> {" → ".join(p_m)}<br>📏 {dd}km &nbsp;|&nbsp; ⏱️ {tt}min &nbsp;|&nbsp; 💰 {cc}AED</div>', unsafe_allow_html=True)
                st.markdown("### 🗺️ Path Visualization")
                fig = draw_network(adj_o,[{'path':p_m,'label':f'{crit}: {" → ".join(p_m)}'}],
                                   title=f"Q27 — Optimal Path by {crit}")
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)
