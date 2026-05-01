# AI-ASSISTED — WaselX Express: Unified Streamlit App (v4 - Dark Premium)
import streamlit as st, plotly.graph_objects as go, pandas as pd

st.set_page_config(page_title="WaselX Express",page_icon="🚚",layout="wide",initial_sidebar_state="collapsed")

# ── HIDE SIDEBAR + DARK PREMIUM CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
*{font-family:'Inter',sans-serif}
[data-testid="stSidebar"],[data-testid="collapsedControl"]{display:none!important}
.stApp{background:#080b16}
.block-container{padding-top:0.5rem!important;max-width:1200px}

/* Animated BG orbs */
.stApp::before,.stApp::after{content:'';position:fixed;border-radius:50%;filter:blur(120px);opacity:0.12;z-index:0;pointer-events:none;animation:float 12s ease-in-out infinite}
.stApp::before{width:500px;height:500px;background:#7c3aed;top:-10%;left:-5%}
.stApp::after{width:400px;height:400px;background:#06b6d4;bottom:-10%;right:-5%;animation-delay:-6s}
@keyframes float{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(40px) scale(1.08)}}

/* Navbar */
.nav-bar{background:rgba(12,15,30,0.7);backdrop-filter:blur(20px);border-bottom:1px solid rgba(139,92,246,0.15);
  padding:12px 32px;display:flex;align-items:center;gap:24px;margin:-1rem -1rem 1.5rem;border-radius:0 0 16px 16px;flex-wrap:wrap}
.nav-brand{font-size:1.4rem;font-weight:900;background:linear-gradient(135deg,#a78bfa,#06b6d4);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-right:auto;white-space:nowrap}
.nav-meta{font-size:0.78rem;color:#64748b;margin-right:auto}

/* Title */
h1{background:linear-gradient(135deg,#a78bfa,#818cf8,#06b6d4);background-size:200% auto;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  animation:grad 5s ease infinite;font-size:2rem!important;font-weight:900!important}
@keyframes grad{0%,100%{background-position:0% center}50%{background-position:100% center}}
h2,h3,h4{color:#c4b5fd!important}
.stMarkdown p,.stMarkdown li,label{color:#cbd5e1!important}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{background:rgba(15,18,35,0.6);backdrop-filter:blur(12px);
  border-radius:12px;padding:4px;border:1px solid rgba(139,92,246,0.12);gap:4px}
.stTabs [data-baseweb="tab"]{color:#94a3b8!important;border-radius:10px!important;font-weight:600;
  padding:10px 20px!important;transition:all 0.3s}
.stTabs [data-baseweb="tab"]:hover{background:rgba(139,92,246,0.1)!important;color:#c4b5fd!important}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,rgba(139,92,246,0.2),rgba(6,182,212,0.15))!important;
  color:#e0e7ff!important;border-bottom:none!important;box-shadow:0 0 20px rgba(139,92,246,0.15)}
.stTabs [data-baseweb="tab-highlight"]{display:none!important}
.stTabs [data-baseweb="tab-border"]{display:none!important}

/* Metrics */
.stMetric{background:rgba(139,92,246,0.06)!important;backdrop-filter:blur(12px);
  border-radius:14px!important;padding:16px!important;border:1px solid rgba(139,92,246,0.12)!important;
  transition:transform 0.3s,box-shadow 0.3s}
.stMetric:hover{transform:translateY(-3px);box-shadow:0 8px 25px rgba(139,92,246,0.15)}
[data-testid="stMetricValue"]{color:#fff!important;font-weight:700!important}
[data-testid="stMetricLabel"]{color:#94a3b8!important}

/* Cards */
.route-card{background:rgba(139,92,246,0.05);backdrop-filter:blur(16px);
  border-radius:14px;padding:20px;margin:10px 0;border:1px solid rgba(139,92,246,0.12);
  border-left:4px solid #8b5cf6;color:#e0e7ff;transition:transform 0.3s,box-shadow 0.3s}
.route-card:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(139,92,246,0.12)}

/* Buttons */
button[kind="primary"]{background:linear-gradient(135deg,#7c3aed,#6366f1)!important;
  border:none!important;border-radius:12px!important;font-weight:700!important;
  transition:all 0.3s!important;box-shadow:0 4px 15px rgba(124,58,237,0.3)!important}
button[kind="primary"]:hover{transform:translateY(-2px)!important;
  box-shadow:0 8px 25px rgba(124,58,237,0.4)!important}

/* Tables & misc */
.stDataFrame{border-radius:12px!important;overflow:hidden}
.stExpander{background:rgba(139,92,246,0.03)!important;border-radius:12px!important;
  border:1px solid rgba(139,92,246,0.08)!important}
[data-testid="stExpander"] summary{color:#c4b5fd!important}
hr{border-color:rgba(139,92,246,0.1)!important}
.stAlert{backdrop-filter:blur(10px)!important;border-radius:12px!important}
.stSelectbox label,.stCheckbox label{color:#94a3b8!important}
::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-track{background:rgba(0,0,0,0.3)}
::-webkit-scrollbar-thumb{background:rgba(139,92,246,0.3);border-radius:3px}
</style>
""", unsafe_allow_html=True)

# ══════════ DATA ══════════
NODES={'H1':'Dubai Marina Hub','H2':'Business Bay Hub','H3':'Deira Hub','H4':'JLT Hub',
'H5':'Abu Dhabi Corniche Hub','H6':'Khalifa City Hub','H7':'Sharjah Al Nahda Hub',
'D1':'Downtown Dubai','D2':'Al Quoz Industrial','D3':'Jumeirah','D4':'Silicon Oasis',
'D5':'Ajman City Centre','D6':'Yas Island','D7':'Al Reem Island','D8':'Muwaileh'}
EDGES=[('H1','H4','Sheikh Zayed Rd',5,10,3.5),('H1','D3','Jumeirah Beach Rd',4,12,3.0),
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
('D5','D8','Sharjah Ring Rd',8,15,5.5),('H6','D7','Reem Bridge',10,18,7.0)]
POS={'H1':(1,6),'H2':(4,5.5),'H3':(7,7),'H4':(2.5,8),'H5':(-5,2),'H6':(-3,0.5),
'H7':(10,8),'D1':(3,4),'D2':(4.5,3),'D3':(1.5,4),'D4':(8,3),
'D5':(12,9),'D6':(-4,-1),'D7':(-6,2.5),'D8':(11,5)}
AN=sorted(NODES.keys())
CRIT={'Distance (km)':0,'Time (min)':1,'Cost (AED)':2}

# ══════════ ALGORITHMS ══════════
class MinHeap:
    def __init__(s): s.h=[]
    def push(s,x):
        s.h.append(x);i=len(s.h)-1
        while i>0:
            p=(i-1)//2
            if s.h[i][0]<s.h[p][0]:s.h[i],s.h[p]=s.h[p],s.h[i];i=p
            else:break
    def pop(s):
        if len(s.h)==1:return s.h.pop()
        r=s.h[0];s.h[0]=s.h.pop();i=0;n=len(s.h)
        while True:
            sm=i;l=2*i+1;r2=2*i+2
            if l<n and s.h[l][0]<s.h[sm][0]:sm=l
            if r2<n and s.h[r2][0]<s.h[sm][0]:sm=r2
            if sm!=i:s.h[i],s.h[sm]=s.h[sm],s.h[i];i=sm
            else:break
        return r
    def empty(s): return len(s.h)==0

def build_adj(blocked=None):
    a={n:[] for n in AN}
    for u,v,rd,d,t,c in EDGES:
        if blocked and ((u,v)==blocked or (v,u)==blocked):continue
        a[u].append((v,d,t,c));a[v].append((u,d,t,c))
    return a

def dijkstra(adj,src,dst,wi):
    INF=float('inf');dist={n:INF for n in adj};prev={n:None for n in adj}
    dist[src]=0;vis=set();hp=MinHeap();hp.push((0,src))
    while not hp.empty():
        d,u=hp.pop()
        if u in vis:continue
        vis.add(u)
        if u==dst:break
        for nb,*w in adj[u]:
            nd=dist[u]+w[wi]
            if nd<dist[nb]:dist[nb]=nd;prev[nb]=u;hp.push((nd,nb))
    path=[];n=dst
    while n is not None:path.append(n);n=prev[n]
    path.reverse()
    return (path,dist[dst]) if dist[dst]<INF else ([],INF)

def pcosts(path,adj):
    td=tt=tc=0
    for i in range(len(path)-1):
        for nb,d,t,c in adj[path[i]]:
            if nb==path[i+1]:td+=d;tt+=t;tc+=c;break
    return td,tt,tc

# ══════════ PLOTLY DARK GRAPH ══════════
def mkgraph(pdata=None,blocked=None,title="WaselX Network",height=680):
    fig=go.Figure()
    if pdata is None:pdata=[]
    pes=set();pns=set()
    for pd in pdata:
        p=pd['path']
        for i in range(len(p)-1):pes.add((p[i],p[i+1]));pes.add((p[i+1],p[i]))
        pns.update(p)
    for u,v,rd,d,t,c in EDGES:
        if blocked and ((u,v)==blocked or (v,u)==blocked):continue
        if (u,v) in pes:continue
        x0,y0=POS[u];x1,y1=POS[v];mx,my=(x0+x1)/2,(y0+y1)/2
        fig.add_trace(go.Scatter(x=[x0,x1,None],y=[y0,y1,None],mode='lines',
            line=dict(width=2,color='rgba(100,116,160,0.3)'),hoverinfo='skip',showlegend=False))
        fig.add_annotation(x=mx,y=my,text=f"<b>{d}km</b>",showarrow=False,
            font=dict(size=9,color='rgba(148,163,184,0.6)'),bgcolor='rgba(8,11,22,0.7)',borderpad=2)
    if blocked and blocked[0] in POS and blocked[1] in POS:
        x0,y0=POS[blocked[0]];x1,y1=POS[blocked[1]]
        fig.add_trace(go.Scatter(x=[x0,x1],y=[y0,y1],mode='lines+markers',
            line=dict(width=4,color='#ef4444',dash='dash'),
            marker=dict(size=18,symbol='x',color='#ef4444'),
            name=f'Blocked: {blocked[0]}-{blocked[1]}',showlegend=True))
    cols=['#a78bfa','#22d3ee','#34d399']
    for idx,pd in enumerate(pdata):
        p=pd['path'];col=cols[idx%3]
        if len(p)<2:continue
        ex=[];ey=[]
        for i in range(len(p)-1):
            x0,y0=POS[p[i]];x1,y1=POS[p[i+1]];ex+=[x0,x1,None];ey+=[y0,y1,None]
            for u,v,rd,d,t,c in EDGES:
                if (u==p[i] and v==p[i+1]) or (v==p[i] and u==p[i+1]):
                    mx,my=(x0+x1)/2,(y0+y1)/2
                    fig.add_annotation(x=mx,y=my,text=f"<b>{d}km</b>",showarrow=False,
                        font=dict(size=11,color=col),bgcolor='rgba(8,11,22,0.9)',borderpad=3,
                        bordercolor=col,borderwidth=1);break
        fig.add_trace(go.Scatter(x=ex,y=ey,mode='lines',line=dict(width=6,color=col),
            name=pd['label'],showlegend=True))
    # Nodes
    for group,color in [('H','#8b5cf6'),('D','#06b6d4')]:
        ns=[n for n in AN if n.startswith(group)]
        nx_=[POS[n][0] for n in ns];ny_=[POS[n][1] for n in ns]
        ht=[f"<b>{n}</b><br>{NODES[n]}" for n in ns]
        sz=[28 if n in pns else 22 for n in ns]
        fig.add_trace(go.Scatter(x=nx_,y=ny_,mode='markers+text',text=ns,textposition='middle center',
            textfont=dict(size=12,color='white',family='Arial Black'),
            marker=dict(size=sz,color=color,line=dict(width=2,color='rgba(255,255,255,0.3)'),symbol='circle'),
            hovertext=ht,hoverinfo='text',showlegend=False))
    fig.update_layout(
        title=dict(text=f'<b>{title}</b>',font=dict(size=17,color='#c4b5fd'),x=0.5,xanchor='center'),
        plot_bgcolor='rgba(8,11,22,0.5)',paper_bgcolor='rgba(8,11,22,0.5)',
        xaxis=dict(showgrid=False,zeroline=False,showticklabels=False,scaleanchor='y'),
        yaxis=dict(showgrid=False,zeroline=False,showticklabels=False),
        height=height,margin=dict(l=10,r=10,t=70,b=50),
        legend=dict(orientation='h',yanchor='top',y=-0.02,xanchor='center',x=0.5,
            font=dict(size=12,color='#c4b5fd'),bgcolor='rgba(8,11,22,0.8)'),
        hoverlabel=dict(bgcolor='#1e1b4b',font_size=13,font_family='Inter',font_color='#e0e7ff'),
        dragmode='pan')
    return fig

# ══════════ HEADER ══════════
st.title("🚚 WaselX Express — Delivery Network Simulator")
st.markdown("""<div class="nav-bar">
<span class="nav-brand">DSA Final Project</span>
<span class="nav-meta">DSA Final Project &bull; Group 3 &bull; SP Jain MAIB<br>
Kartik Joshi &bull; Gagandeep Singh &bull; Samuel Alex &bull; Prem Kukreja</span>
</div>""",unsafe_allow_html=True)

# ══════════ TABS ══════════
t1,t2,t3=st.tabs(["🏠 Overview","🗺️ Q6: Path Visualizer","🛣️ Q27: Path Simulator"])

with t1:
    st.markdown("**Optimizing Last-Mile Delivery Across the UAE Using DSA**")
    st.markdown("---")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("🏢 Nodes","15");c2.metric("🛤️ Edges","24");c3.metric("📦 Hubs","7");c4.metric("📍 Zones","8")
    st.plotly_chart(mkgraph(title="Full Network — 15 Nodes, 24 Edges",height=640),use_container_width=True)
    with st.expander("📋 Edge Table"):
        st.dataframe(pd.DataFrame([(u,v,rd,d,t,c) for u,v,rd,d,t,c in EDGES],
            columns=['From','To','Road','Dist (km)','Time (min)','Cost (AED)']),use_container_width=True,hide_index=True)
    st.info("⚠️ **Two disconnected components:** Dubai-Sharjah cluster and Abu Dhabi cluster.")

with t2:
    st.title("🗺️ Q6 — Interactive Shortest Path Visualizer")
    st.markdown("Dijkstra's shortest path with dual-path overlay. **Zoom, pan, hover** for details.")
    st.markdown("---")
    adj=build_adj()
    c1,c2=st.columns(2)
    with c1:
        st.markdown("#### Path 1")
        s1=st.selectbox("Source",AN,index=AN.index('H1'),key='s1')
        d1=st.selectbox("Destination",AN,index=AN.index('D4'),key='d1')
        cr1=st.selectbox("Criterion",list(CRIT.keys()),key='c1')
    with c2:
        st.markdown("#### Path 2 (Overlay)")
        en2=st.checkbox("Enable second path")
        s2=st.selectbox("Source",AN,index=AN.index('H3'),key='s2',disabled=not en2)
        d2=st.selectbox("Destination",AN,index=AN.index('D3'),key='d2',disabled=not en2)
        cr2=st.selectbox("Criterion",list(CRIT.keys()),key='c2',disabled=not en2)
    if st.button("🔍 Compute Shortest Paths",type="primary",use_container_width=True):
        pdata=[]
        p1,_=dijkstra(adj,s1,d1,CRIT[cr1])
        if p1 and len(p1)>1:
            dd,tt,cc=pcosts(p1,adj)
            pdata.append({'path':p1,'label':f'Path 1: {s1}->{d1} ({dd}km, {tt}min, {cc}AED)'})
            st.markdown(f'<div class="route-card">✅ <b>Path 1:</b> {" → ".join(p1)}<br>📏 {dd} km &nbsp;|&nbsp; ⏱️ {tt} min &nbsp;|&nbsp; 💰 {cc} AED</div>',unsafe_allow_html=True)
        else: st.error(f"❌ No path from {s1} to {d1} — different components")
        if en2:
            p2,_=dijkstra(adj,s2,d2,CRIT[cr2])
            if p2 and len(p2)>1:
                dd,tt,cc=pcosts(p2,adj)
                pdata.append({'path':p2,'label':f'Path 2: {s2}->{d2} ({dd}km, {tt}min, {cc}AED)'})
                st.markdown(f'<div class="route-card">✅ <b>Path 2:</b> {" → ".join(p2)}<br>📏 {dd} km &nbsp;|&nbsp; ⏱️ {tt} min &nbsp;|&nbsp; 💰 {cc} AED</div>',unsafe_allow_html=True)
            else: st.error(f"❌ No path from {s2} to {d2}")
        if pdata: st.plotly_chart(mkgraph(pdata,title="Q6 — Shortest Path Visualization",height=640),use_container_width=True)

with t3:
    st.title("🛣️ Q27 — Comprehensive Path Simulator")
    st.markdown("Multi-criteria optimization with road closure. **Interactive** — zoom, pan, hover.")
    st.markdown("---")
    c1,c2,c3=st.columns(3)
    with c1:src=st.selectbox("Source",AN,index=AN.index('H1'),key='qs')
    with c2:dst=st.selectbox("Destination",AN,index=AN.index('D4'),key='qd')
    with c3:crit=st.selectbox("Criterion",list(CRIT.keys()),key='qc')
    st.markdown("#### 🚧 Road Closure")
    el=["None"]+[f"{u} — {v} ({rd})" for u,v,rd,_,_,_ in EDGES]
    closure=st.selectbox("Block an edge",el,key='qcl')
    blocked=None
    if closure!="None":ix=el.index(closure)-1;blocked=(EDGES[ix][0],EDGES[ix][1])
    if st.button("🚀 Compute Optimal Paths",type="primary",use_container_width=True):
        wi=CRIT[crit];adj_o=build_adj();adj_c=build_adj(blocked) if blocked else None
        st.markdown("### 📊 Multi-Criteria Comparison")
        rows=[]
        for cn,ci in CRIT.items():
            p,_=dijkstra(adj_o,src,dst,ci)
            if p and len(p)>1:
                dd,tt,cc=pcosts(p,adj_o)
                rows.append({'Criterion':cn,'Path':' → '.join(p),'Distance (km)':dd,'Time (min)':tt,'Cost (AED)':cc})
            else: rows.append({'Criterion':cn,'Path':'NO PATH','Distance (km)':'-','Time (min)':'-','Cost (AED)':'-'})
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
        uniq=set(r['Path'] for r in rows if r['Path']!='NO PATH')
        if len(uniq)>1:st.warning("⚠️ Different criteria produce **different** optimal paths!")
        elif len(uniq)==1:st.info("✅ All criteria produce the **same** optimal path.")
        if blocked and adj_c:
            st.markdown(f"### 🚧 Road Closure: {blocked[0]} — {blocked[1]}")
            p_o,_=dijkstra(adj_o,src,dst,wi);p_c,_=dijkstra(adj_c,src,dst,wi)
            d1v=t1v=c1v=0
            if p_o and len(p_o)>1:d1v,t1v,c1v=pcosts(p_o,adj_o)
            if p_c and len(p_c)>1:
                d2,t2,c2v=pcosts(p_c,adj_c)
                st.markdown(f'<div class="route-card">🔄 <b>Rerouted:</b> {" → ".join(p_c)}<br>📏 {d2}km &nbsp;|&nbsp; ⏱️ {t2}min &nbsp;|&nbsp; 💰 {c2v}AED</div>',unsafe_allow_html=True)
                if d1v>0:
                    st.dataframe(pd.DataFrame({'Metric':['Distance (km)','Time (min)','Cost (AED)'],
                        'Original':[d1v,t1v,c1v],'Rerouted':[d2,t2,c2v],
                        'Delta':[f"+{d2-d1v}",f"+{t2-t1v}",f"+{round(c2v-c1v,1)}"]}),use_container_width=True,hide_index=True)
            else:st.error("❌ No alternative path with this road closed!")
            st.markdown("### 🗺️ Visual Comparison")
            ca,cb=st.columns(2)
            with ca:
                st.markdown("**Original**")
                if p_o and len(p_o)>1:
                    st.plotly_chart(mkgraph([{'path':p_o,'label':f'Original: {d1v}km'}],title=f"Original: {' → '.join(p_o)}",height=580),use_container_width=True)
            with cb:
                st.markdown("**After Closure**")
                if p_c and len(p_c)>1:
                    st.plotly_chart(mkgraph([{'path':p_c,'label':f'Rerouted: {d2}km'}],blocked=blocked,title=f"Rerouted: {' → '.join(p_c)}",height=580),use_container_width=True)
        else:
            pm,_=dijkstra(adj_o,src,dst,wi)
            if pm and len(pm)>1:
                dd,tt,cc=pcosts(pm,adj_o)
                st.markdown(f'<div class="route-card">✅ <b>Optimal:</b> {" → ".join(pm)}<br>📏 {dd}km &nbsp;|&nbsp; ⏱️ {tt}min &nbsp;|&nbsp; 💰 {cc}AED</div>',unsafe_allow_html=True)
                st.plotly_chart(mkgraph([{'path':pm,'label':f'{crit}: {" → ".join(pm)}'}],title=f"Q27 — Optimal Path by {crit}",height=640),use_container_width=True)
