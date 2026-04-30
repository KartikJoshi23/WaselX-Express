# AI-ASSISTED — WaselX Express: Unified Streamlit Application (v3 - Plotly Interactive)
"""
WaselX Express — Delivery Network Simulator
Group 3 | SP Jain MAIB | DSA Final Project
Kartik Joshi, Gagandeep Singh, Samuel Alex, Prem Kukreja
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="WaselX Express", page_icon="🚚", layout="wide", initial_sidebar_state="expanded")

# ── CSS ──
st.markdown("""<style>
.block-container{padding-top:1.2rem}
h1{background:linear-gradient(90deg,#E67E22,#1ABC9C);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:2.2rem!important}
.stMetric{background:rgba(230,126,34,0.08);border-radius:12px;padding:12px;border-left:4px solid #E67E22}
.route-card{background:linear-gradient(135deg,rgba(230,126,34,0.12),rgba(26,188,156,0.12));border-radius:12px;padding:18px;margin:8px 0;border-left:5px solid #E67E22;font-size:1.05em}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#1a1a2e,#16213e)}
[data-testid="stSidebar"] *{color:#e0e0e0!important}
</style>""", unsafe_allow_html=True)

# ═══════════════ DATA ═══════════════
NODES = {
    'H1':'Dubai Marina Hub','H2':'Business Bay Hub','H3':'Deira Hub','H4':'JLT Hub',
    'H5':'Abu Dhabi Corniche Hub','H6':'Khalifa City Hub','H7':'Sharjah Al Nahda Hub',
    'D1':'Downtown Dubai','D2':'Al Quoz Industrial','D3':'Jumeirah','D4':'Silicon Oasis',
    'D5':'Ajman City Centre','D6':'Yas Island','D7':'Al Reem Island','D8':'Muwaileh',
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
POS = {
    'H1':(1,6),'H2':(4,5.5),'H3':(7,7),'H4':(2.5,8),'H5':(-5,2),'H6':(-3,0.5),
    'H7':(10,8),'D1':(3,4),'D2':(4.5,3),'D3':(1.5,4),'D4':(8,3),
    'D5':(12,9),'D6':(-4,-1),'D7':(-6,2.5),'D8':(11,5),
}
ALL_NODES = sorted(NODES.keys())
CRITERIA = {'Distance (km)':0, 'Time (min)':1, 'Cost (AED)':2}

# ═══════════════ ALGORITHMS (from scratch) ═══════════════
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
    a={n:[] for n in ALL_NODES}
    for u,v,rd,d,t,c in EDGES:
        if blocked and ((u,v)==blocked or (v,u)==blocked): continue
        a[u].append((v,d,t,c)); a[v].append((u,d,t,c))
    return a

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

# ═══════════════ PLOTLY GRAPH ═══════════════
def make_graph(paths_data=None, blocked=None, title="WaselX Express Network", height=700):
    fig = go.Figure()
    if paths_data is None: paths_data = []
    path_edge_set = set()
    path_node_set = set()
    for pd_item in paths_data:
        p = pd_item['path']
        for i in range(len(p)-1):
            path_edge_set.add((p[i],p[i+1]))
            path_edge_set.add((p[i+1],p[i]))
        path_node_set.update(p)

    # --- Base edges ---
    for u,v,rd,d,t,c in EDGES:
        if blocked and ((u,v)==blocked or (v,u)==blocked): continue
        if (u,v) in path_edge_set: continue
        x0,y0=POS[u]; x1,y1=POS[v]
        mx,my=(x0+x1)/2,(y0+y1)/2
        fig.add_trace(go.Scatter(
            x=[x0,x1,None], y=[y0,y1,None], mode='lines',
            line=dict(width=2, color='rgba(150,150,170,0.4)'),
            hoverinfo='skip', showlegend=False
        ))
        fig.add_annotation(x=mx, y=my, text=f"<b>{d}km</b>", showarrow=False,
                          font=dict(size=10, color='rgba(100,100,120,0.7)'),
                          bgcolor='rgba(255,255,255,0.8)', borderpad=2)

    # --- Blocked edge ---
    if blocked and blocked[0] in POS and blocked[1] in POS:
        x0,y0=POS[blocked[0]]; x1,y1=POS[blocked[1]]
        fig.add_trace(go.Scatter(
            x=[x0,x1], y=[y0,y1], mode='lines+markers',
            line=dict(width=4, color='red', dash='dash'),
            marker=dict(size=18, symbol='x', color='red'),
            name=f'Blocked: {blocked[0]}-{blocked[1]}', showlegend=True
        ))

    # --- Highlighted path edges ---
    pcolors = ['#E74C3C','#2980B9','#27AE60']
    for idx, pd_item in enumerate(paths_data):
        p = pd_item['path']; col = pcolors[idx % 3]
        if len(p)<2: continue
        ex=[]; ey=[]
        for i in range(len(p)-1):
            x0,y0=POS[p[i]]; x1,y1=POS[p[i+1]]
            ex+=[x0,x1,None]; ey+=[y0,y1,None]
            # Find edge weight for annotation
            for u,v,rd,d,t,c in EDGES:
                if (u==p[i] and v==p[i+1]) or (v==p[i] and u==p[i+1]):
                    mx,my=(x0+x1)/2,(y0+y1)/2
                    fig.add_annotation(x=mx, y=my, text=f"<b>{d}km</b>", showarrow=False,
                                      font=dict(size=11, color=col),
                                      bgcolor='rgba(255,255,255,0.9)', borderpad=3,
                                      bordercolor=col, borderwidth=1)
                    break
        fig.add_trace(go.Scatter(
            x=ex, y=ey, mode='lines', line=dict(width=6, color=col),
            name=pd_item['label'], showlegend=True
        ))

    # --- Hub nodes ---
    hx=[POS[n][0] for n in ALL_NODES if n.startswith('H')]
    hy=[POS[n][1] for n in ALL_NODES if n.startswith('H')]
    hn=[n for n in ALL_NODES if n.startswith('H')]
    ht=[f"<b>{n}</b><br>{NODES[n]}" for n in hn]
    hsz=[28 if n in path_node_set else 22 for n in hn]
    fig.add_trace(go.Scatter(
        x=hx, y=hy, mode='markers+text', text=hn, textposition='middle center',
        textfont=dict(size=13, color='white', family='Arial Black'),
        marker=dict(size=hsz, color='#E67E22', line=dict(width=3, color='#2C3E50'),
                    symbol='circle'),
        hovertext=ht, hoverinfo='text', name='Hubs', showlegend=False
    ))

    # --- Zone nodes ---
    dx=[POS[n][0] for n in ALL_NODES if n.startswith('D')]
    dy=[POS[n][1] for n in ALL_NODES if n.startswith('D')]
    dn=[n for n in ALL_NODES if n.startswith('D')]
    dt=[f"<b>{n}</b><br>{NODES[n]}" for n in dn]
    dsz=[26 if n in path_node_set else 20 for n in dn]
    fig.add_trace(go.Scatter(
        x=dx, y=dy, mode='markers+text', text=dn, textposition='middle center',
        textfont=dict(size=12, color='white', family='Arial Black'),
        marker=dict(size=dsz, color='#1ABC9C', line=dict(width=3, color='#2C3E50'),
                    symbol='circle'),
        hovertext=dt, hoverinfo='text', name='Zones', showlegend=False
    ))

    fig.update_layout(
        title=dict(text=f'<b>{title}</b>', font=dict(size=18, color='#2C3E50'), x=0.5, xanchor='center'),
        plot_bgcolor='#FAFBFC', paper_bgcolor='#FAFBFC',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, scaleanchor='y'),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=height, margin=dict(l=20,r=20,t=80,b=60),
        legend=dict(orientation='h', yanchor='top', y=-0.02, xanchor='center', x=0.5,
                    font=dict(size=12), bgcolor='rgba(255,255,255,0.9)'),
        hoverlabel=dict(bgcolor='white', font_size=13, font_family='Arial'),
        dragmode='pan'
    )
    return fig

# ═══════════════ SIDEBAR ═══════════════
with st.sidebar:
    st.markdown("## 🚚 WaselX Express")
    st.markdown("**DSA Final Project - Group 3**")
    st.caption("SP Jain School of Global Management")
    st.markdown("---")
    page = st.radio("Navigate", ["🏠 Overview","🗺️ Q6: Path Visualizer","🛣️ Q27: Path Simulator"],
                    label_visibility="collapsed")
    st.markdown("---")
    st.caption("**Team:** Kartik Joshi, Gagandeep Singh,\nSamuel Alex, Prem Kukreja")

# ═══════════════ OVERVIEW ═══════════════
if page == "🏠 Overview":
    st.title("🚚 WaselX Express - Delivery Network Simulator")
    st.markdown("**Optimizing Last-Mile Delivery Across the UAE Using DSA**")
    st.markdown("---")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("🏢 Nodes","15"); c2.metric("🛤️ Edges","24")
    c3.metric("📦 Hubs","7"); c4.metric("📍 Zones","8")
    st.plotly_chart(make_graph(title="WaselX Express - Full Network (15 Nodes, 24 Edges)", height=650),
                    use_container_width=True)
    with st.expander("📋 Edge Table"):
        st.dataframe(pd.DataFrame(
            [(u,v,rd,d,t,c) for u,v,rd,d,t,c in EDGES],
            columns=['From','To','Road','Dist (km)','Time (min)','Cost (AED)']
        ), use_container_width=True, hide_index=True)
    st.info("⚠️ **Two disconnected components:** Dubai-Sharjah (H1-H4,H7,D1-D5,D8) and Abu Dhabi (H5,H6,D6,D7).")

# ═══════════════ Q6 ═══════════════
elif page == "🗺️ Q6: Path Visualizer":
    st.title("🗺️ Q6 - Interactive Shortest Path Visualizer")
    st.markdown("Dijkstra's shortest path with optional dual-path overlay. **Zoom, pan, and hover** for details.")
    st.markdown("---")
    adj = build_adj()
    c1,c2 = st.columns(2)
    with c1:
        st.markdown("#### Path 1")
        s1=st.selectbox("Source",ALL_NODES,index=ALL_NODES.index('H1'),key='s1')
        d1=st.selectbox("Destination",ALL_NODES,index=ALL_NODES.index('D4'),key='d1')
        cr1=st.selectbox("Criterion",list(CRITERIA.keys()),key='c1')
    with c2:
        st.markdown("#### Path 2 (Overlay)")
        en2=st.checkbox("Enable second path")
        s2=st.selectbox("Source",ALL_NODES,index=ALL_NODES.index('H3'),key='s2',disabled=not en2)
        d2=st.selectbox("Destination",ALL_NODES,index=ALL_NODES.index('D3'),key='d2',disabled=not en2)
        cr2=st.selectbox("Criterion",list(CRITERIA.keys()),key='c2',disabled=not en2)

    if st.button("🔍 Compute Shortest Paths", type="primary", use_container_width=True):
        pdata=[]
        p1,_=dijkstra(adj,s1,d1,CRITERIA[cr1])
        if p1 and len(p1)>1:
            dd,tt,cc=path_costs(p1,adj)
            pdata.append({'path':p1,'label':f'Path 1: {s1}->{d1} ({dd}km, {tt}min, {cc}AED)'})
            st.markdown(f'<div class="route-card">✅ <b>Path 1:</b> {" -> ".join(p1)}<br>📏 {dd} km | ⏱️ {tt} min | 💰 {cc} AED</div>', unsafe_allow_html=True)
        else:
            st.error(f"❌ No path from {s1} to {d1} - nodes in different components")
        if en2:
            p2,_=dijkstra(adj,s2,d2,CRITERIA[cr2])
            if p2 and len(p2)>1:
                dd,tt,cc=path_costs(p2,adj)
                pdata.append({'path':p2,'label':f'Path 2: {s2}->{d2} ({dd}km, {tt}min, {cc}AED)'})
                st.markdown(f'<div class="route-card">✅ <b>Path 2:</b> {" -> ".join(p2)}<br>📏 {dd} km | ⏱️ {tt} min | 💰 {cc} AED</div>', unsafe_allow_html=True)
            else:
                st.error(f"❌ No path from {s2} to {d2}")
        if pdata:
            st.plotly_chart(make_graph(pdata, title="Q6 - Shortest Path Visualization", height=650),
                           use_container_width=True)

# ═══════════════ Q27 ═══════════════
elif page == "🛣️ Q27: Path Simulator":
    st.title("🛣️ Q27 - Comprehensive Path Simulator")
    st.markdown("Multi-criteria optimization with road closure. **Interactive graphs** - zoom, pan, hover.")
    st.markdown("---")
    c1,c2,c3=st.columns(3)
    with c1: src=st.selectbox("Source",ALL_NODES,index=ALL_NODES.index('H1'),key='qs')
    with c2: dst=st.selectbox("Destination",ALL_NODES,index=ALL_NODES.index('D4'),key='qd')
    with c3: crit=st.selectbox("Criterion",list(CRITERIA.keys()),key='qc')

    st.markdown("#### 🚧 Road Closure")
    elabels=["None"]+[f"{u} - {v} ({rd})" for u,v,rd,_,_,_ in EDGES]
    closure=st.selectbox("Block an edge",elabels,key='qcl')
    blocked=None
    if closure!="None":
        idx=elabels.index(closure)-1
        blocked=(EDGES[idx][0],EDGES[idx][1])

    if st.button("🚀 Compute Optimal Paths", type="primary", use_container_width=True):
        wi=CRITERIA[crit]
        adj_o=build_adj()
        adj_c=build_adj(blocked) if blocked else None

        st.markdown("### 📊 Multi-Criteria Comparison")
        rows=[]
        for cn,ci in CRITERIA.items():
            p,_=dijkstra(adj_o,src,dst,ci)
            if p and len(p)>1:
                dd,tt,cc=path_costs(p,adj_o)
                rows.append({'Criterion':cn,'Path':' -> '.join(p),'Distance (km)':dd,'Time (min)':tt,'Cost (AED)':cc})
            else:
                rows.append({'Criterion':cn,'Path':'NO PATH','Distance (km)':'-','Time (min)':'-','Cost (AED)':'-'})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        uniq=set(r['Path'] for r in rows if r['Path']!='NO PATH')
        if len(uniq)>1: st.warning("⚠️ Different criteria produce **different** optimal paths!")
        elif len(uniq)==1: st.info("✅ All criteria produce the **same** optimal path.")

        if blocked and adj_c:
            st.markdown(f"### 🚧 Road Closure: {blocked[0]} - {blocked[1]}")
            p_o,_=dijkstra(adj_o,src,dst,wi)
            p_c,_=dijkstra(adj_c,src,dst,wi)
            d1=t1=c1v=0
            if p_o and len(p_o)>1: d1,t1,c1v=path_costs(p_o,adj_o)
            if p_c and len(p_c)>1:
                d2,t2,c2v=path_costs(p_c,adj_c)
                st.markdown(f'<div class="route-card">🔄 <b>Rerouted:</b> {" -> ".join(p_c)}<br>📏 {d2}km | ⏱️ {t2}min | 💰 {c2v}AED</div>', unsafe_allow_html=True)
                if d1>0:
                    st.dataframe(pd.DataFrame({
                        'Metric':['Distance (km)','Time (min)','Cost (AED)'],
                        'Original':[d1,t1,c1v],'Rerouted':[d2,t2,c2v],
                        'Delta':[f"+{d2-d1}",f"+{t2-t1}",f"+{round(c2v-c1v,1)}"]
                    }), use_container_width=True, hide_index=True)
            else:
                st.error("❌ No alternative path with this road closed!")

            st.markdown("### 🗺️ Visual Comparison")
            ca,cb=st.columns(2)
            with ca:
                st.markdown("**Original**")
                if p_o and len(p_o)>1:
                    st.plotly_chart(make_graph([{'path':p_o,'label':f'Original: {d1}km'}],
                                   title=f"Original: {' -> '.join(p_o)}", height=500),
                                   use_container_width=True)
            with cb:
                st.markdown("**After Closure**")
                if p_c and len(p_c)>1:
                    st.plotly_chart(make_graph([{'path':p_c,'label':f'Rerouted: {d2}km'}],
                                   blocked=blocked,
                                   title=f"Rerouted: {' -> '.join(p_c)}", height=500),
                                   use_container_width=True)
        else:
            p_m,_=dijkstra(adj_o,src,dst,wi)
            if p_m and len(p_m)>1:
                dd,tt,cc=path_costs(p_m,adj_o)
                st.markdown(f'<div class="route-card">✅ <b>Optimal:</b> {" -> ".join(p_m)}<br>📏 {dd}km | ⏱️ {tt}min | 💰 {cc}AED</div>', unsafe_allow_html=True)
                st.plotly_chart(make_graph([{'path':p_m,'label':f'{crit}: {" -> ".join(p_m)}'}],
                               title=f"Q27 - Optimal Path by {crit}", height=650),
                               use_container_width=True)
