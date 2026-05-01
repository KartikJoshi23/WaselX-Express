"""Regenerate ALL 11 figures matching Streamlit Plotly style."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np
import random, time, sys

plt.rcParams.update({'font.size':12,'axes.titlesize':16,'figure.dpi':150,
                     'font.family':'sans-serif'})

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
HUBS=[n for n in AN if n.startswith('H')]
BG='#FAFBFC'
HUB_COL='#E67E22'; ZONE_COL='#1ABC9C'; BORDER='#2C3E50'
EDGE_COL='rgba(150,150,170,0.4)'
PATH_COLS=['#E74C3C','#2980B9','#27AE60']

class MinHeap:
    def __init__(self): self.h=[]
    def push(self,x):
        self.h.append(x);i=len(self.h)-1
        while i>0:
            p=(i-1)//2
            if self.h[i][0]<self.h[p][0]:self.h[i],self.h[p]=self.h[p],self.h[i];i=p
            else:break
    def pop(self):
        if len(self.h)==1:return self.h.pop()
        r=self.h[0];self.h[0]=self.h.pop();i=0;s=len(self.h)
        while True:
            sm=i;l=2*i+1;r2=2*i+2
            if l<s and self.h[l][0]<self.h[sm][0]:sm=l
            if r2<s and self.h[r2][0]<self.h[sm][0]:sm=r2
            if sm!=i:self.h[i],self.h[sm]=self.h[sm],self.h[i];i=sm
            else:break
        return r
    def empty(self): return len(self.h)==0

def build_adj(blocked=None):
    a={n:[] for n in AN}
    for u,v,r,d,t,c in EDGES:
        if blocked and ((u,v)==blocked or (v,u)==blocked): continue
        a[u].append((v,d,t,c)); a[v].append((u,d,t,c))
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

def draw_graph(ax, highlight_edges=None, highlight_color='#E74C3C', blocked=None,
               edge_label_key='dist', title='', path_nodes=None):
    """Draw graph matching Plotly Streamlit style."""
    ax.set_facecolor(BG)
    if path_nodes is None: path_nodes=set()
    if highlight_edges is None: highlight_edges=[]

    G=nx.Graph()
    for n in AN: G.add_node(n)
    for u,v,r,d,t,c in EDGES:
        if blocked and ((u,v)==blocked or (v,u)==blocked): continue
        G.add_edge(u,v,dist=d,time=t,cost=c)

    he_set=set()
    for e in highlight_edges: he_set.add(e); he_set.add((e[1],e[0]))
    other=[(u,v) for u,v in G.edges() if (u,v) not in he_set and (v,u) not in he_set]

    # Base edges - light gray
    nx.draw_networkx_edges(G,POS,edgelist=other,ax=ax,edge_color='#9696AA',width=1.8,alpha=0.4)
    # Highlighted edges
    if highlight_edges:
        nx.draw_networkx_edges(G,POS,edgelist=highlight_edges,ax=ax,
                               edge_color=highlight_color,width=5,alpha=0.9)
    # Blocked
    if blocked and blocked[0] in POS and blocked[1] in POS:
        ax.plot([POS[blocked[0]][0],POS[blocked[1]][0]],
                [POS[blocked[0]][1],POS[blocked[1]][1]],
                'X--',color='red',linewidth=3,markersize=18)

    # Nodes - matching Plotly style
    for n in AN:
        is_hub=n.startswith('H')
        in_p=n in path_nodes
        col=HUB_COL if is_hub else ZONE_COL
        sz=1200 if in_p else (1000 if is_hub else 850)
        nx.draw_networkx_nodes(G,POS,nodelist=[n],ax=ax,node_color=col,node_size=sz,
                               edgecolors=BORDER,linewidths=2.5,alpha=0.95)

    # White bold labels inside nodes
    nx.draw_networkx_labels(G,POS,ax=ax,font_size=13,font_weight='bold',
                            font_color='white',font_family='sans-serif')

    # Edge labels with background box
    if edge_label_key:
        el={}
        for u,v in G.edges():
            d=G[u][v].get(edge_label_key,0)
            unit='km' if edge_label_key=='dist' else ('min' if edge_label_key=='time' else 'AED')
            el[(u,v)]=f"{d}{unit}"
        nx.draw_networkx_edge_labels(G,POS,edge_labels=el,ax=ax,font_size=9,
                                      font_color='#64647A',font_weight='bold',
                                      bbox=dict(boxstyle='round,pad=0.2',fc='white',
                                               ec='#CCCCCC',alpha=0.85))

    ax.set_title(title,fontsize=16,fontweight='bold',color=BORDER,pad=15,loc='center')
    ax.axis('off')
    ax.margins(0.08)

def save(fig,name):
    fig.savefig(name,dpi=150,bbox_inches='tight',facecolor=BG,edgecolor='none')
    plt.close(fig)
    print(f'  Saved: {name}')

# ===== GENERATE ALL FIGURES =====
print("Regenerating all figures (Plotly-matched style)...")

# 1. Full network
print("1. Full network")
fig,ax=plt.subplots(figsize=(18,12),facecolor=BG)
draw_graph(ax,title='WaselX Express - Full Network (15 Nodes, 24 Edges)')
save(fig,'graph_network_full.png')

# 2. Dijkstra H1->D1
print("2. Dijkstra H1->D1")
adj=build_adj(); path,_=dijkstra(adj,'H1','D1',0)
pe=[(path[i],path[i+1]) for i in range(len(path)-1)]
fig,ax=plt.subplots(figsize=(18,12),facecolor=BG)
draw_graph(ax,highlight_edges=pe,path_nodes=set(path),
           title='Q2 - Dijkstra Shortest Path: H1 -> D1 (8 km)')
save(fig,'dijkstra_path_h1_d1.png')

# 3. Floyd-Warshall heatmap
print("3. Floyd-Warshall heatmap")
INF=float('inf')
idx_map={n:i for i,n in enumerate(AN)}
dist_fw=[[INF]*15 for _ in range(15)]
for i in range(15): dist_fw[i][i]=0
for u,v,r,d,t,c in EDGES:
    i,j=idx_map[u],idx_map[v]
    dist_fw[i][j]=min(dist_fw[i][j],t); dist_fw[j][i]=min(dist_fw[j][i],t)
for k in range(15):
    for i in range(15):
        for j in range(15):
            if dist_fw[i][k]+dist_fw[k][j]<dist_fw[i][j]:
                dist_fw[i][j]=dist_fw[i][k]+dist_fw[k][j]
hub_idx=[idx_map[h] for h in HUBS]
hub_mat=np.array([[dist_fw[i][j] for j in hub_idx] for i in hub_idx],dtype=float)
hub_mat[hub_mat>9000]=np.nan
fig,ax=plt.subplots(figsize=(10,8),facecolor=BG)
ax.set_facecolor(BG)
im=ax.imshow(hub_mat,cmap='RdYlGn_r',interpolation='nearest')
ax.set_xticks(range(7));ax.set_yticks(range(7))
ax.set_xticklabels(HUBS,fontsize=12,fontweight='bold')
ax.set_yticklabels(HUBS,fontsize=12,fontweight='bold')
for i in range(7):
    for j in range(7):
        v=hub_mat[i][j]
        txt='INF' if np.isnan(v) else f'{int(v)}'
        c='white' if (not np.isnan(v) and v>30) else BORDER
        ax.text(j,i,txt,ha='center',va='center',fontsize=13,fontweight='bold',color=c)
plt.colorbar(im,ax=ax,label='Travel Time (min)',shrink=0.85)
ax.set_title('Q3 - Floyd-Warshall: Hub-to-Hub Travel Times (min)',fontsize=16,fontweight='bold',color=BORDER,pad=15)
fig.tight_layout()
save(fig,'floyd_warshall_hubs.png')

# 4. Kruskal MST
print("4. Kruskal MST")
sorted_edges=sorted(EDGES,key=lambda e:e[5])
parent={n:n for n in AN}; rank={n:0 for n in AN}
def find(x):
    while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
    return x
def union(a,b):
    a,b=find(a),find(b)
    if a==b: return False
    if rank[a]<rank[b]: a,b=b,a
    parent[b]=a
    if rank[a]==rank[b]: rank[a]+=1
    return True
mst_edges=[]
mst_nodes=set()
for u,v,r,d,t,c in sorted_edges:
    if union(u,v): mst_edges.append((u,v)); mst_nodes.add(u); mst_nodes.add(v)
fig,ax=plt.subplots(figsize=(18,12),facecolor=BG)
draw_graph(ax,highlight_edges=mst_edges,highlight_color='#27AE60',
           edge_label_key='cost',path_nodes=mst_nodes,
           title="Q4a - Kruskal's Minimum Spanning Tree (Cost in AED)")
save(fig,'mst_kruskal.png')

# 5. Prim MST
print("5. Prim MST")
adj_c=build_adj()
visited={'H2'}; prim_edges=[]; prim_nodes={'H2'}
candidates=[(c,'H2',nb) for nb,d,t,c in adj_c['H2']]
candidates.sort()
while candidates:
    cost,u,v=candidates.pop(0)
    if v in visited: continue
    visited.add(v); prim_edges.append((u,v)); prim_nodes.add(v)
    for nb,d,t,c in adj_c[v]:
        if nb not in visited: candidates.append((c,v,nb))
    candidates.sort()
fig,ax=plt.subplots(figsize=(18,12),facecolor=BG)
draw_graph(ax,highlight_edges=prim_edges,highlight_color='#8E44AD',
           edge_label_key='cost',path_nodes=prim_nodes,
           title="Q4c - Prim's MST from H2 (Cost in AED)")
save(fig,'mst_prim.png')

# 6. BFS tree from H3
print("6. BFS tree from H3")
adj_bfs=build_adj()
vis_bfs={'H3'}; queue=['H3']; bfs_edges=[]; bfs_order=['H3']; levels={'H3':0}
while queue:
    u=queue.pop(0)
    for nb,*_ in adj_bfs[u]:
        if nb not in vis_bfs:
            vis_bfs.add(nb); queue.append(nb); bfs_edges.append((u,nb))
            bfs_order.append(nb); levels[nb]=levels[u]+1
fig,ax=plt.subplots(figsize=(18,12),facecolor=BG)
draw_graph(ax,highlight_edges=bfs_edges,highlight_color='#2980B9',
           path_nodes=set(bfs_order),
           title=f'Q7a - BFS Tree from H3 (Deira Hub) - {len(bfs_order)} nodes reachable')
for n,lv in levels.items():
    ax.annotate(f'L{lv}',xy=POS[n],xytext=(12,-12),textcoords='offset points',
               fontsize=9,color='#2980B9',fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.15',fc='#EBF5FB',ec='#2980B9'))
save(fig,'bfs_tree_h3.png')

# 7-8. BST
print("7. BST initial")
class BSTNode:
    def __init__(self,k): self.key=k;self.left=None;self.right=None
def bst_insert(root,k):
    if root is None: return BSTNode(k)
    if k<root.key: root.left=bst_insert(root.left,k)
    elif k>root.key: root.right=bst_insert(root.right,k)
    return root
def bst_positions(node,x=0,y=0,dx=2.5,positions=None):
    if positions is None: positions={}
    if node is None: return positions
    positions[node.key]=(x,y)
    bst_positions(node.left,x-dx,y-1.2,dx*0.55,positions)
    bst_positions(node.right,x+dx,y-1.2,dx*0.55,positions)
    return positions
def draw_tree(ax,node,positions,col,title):
    ax.set_facecolor(BG)
    def draw_e(n):
        if not n: return
        px,py=positions[n.key]
        for child in [n.left,n.right]:
            if child:
                cx,cy=positions[child.key]
                ax.plot([px,cx],[py,cy],'-',color='#9696AA',linewidth=2,zorder=1)
                draw_e(child)
    draw_e(node)
    for k,(x,y) in positions.items():
        circle=plt.Circle((x,y),0.35,color=col,ec=BORDER,linewidth=2.5,zorder=2)
        ax.add_patch(circle)
        ax.text(x,y,str(k),ha='center',va='center',fontsize=11,fontweight='bold',color='white',zorder=3)
    ax.set_xlim(-5,5);ax.set_ylim(-6.5,1);ax.set_aspect('equal');ax.axis('off')
    ax.set_title(title,fontsize=15,fontweight='bold',color=BORDER,pad=15)

keys=[1045,1023,1078,1012,1034,1056,1089,1005,1020,1067,1050,1098]
root=None
for k in keys: root=bst_insert(root,k)
fig,ax=plt.subplots(figsize=(14,10),facecolor=BG)
draw_tree(ax,root,bst_positions(root),'#2980B9','Q8a - Binary Search Tree (12 Orders Inserted)')
save(fig,'bst_initial.png')

print("8. BST after deletion")
def bst_delete(root,k):
    if root is None: return root
    if k<root.key: root.left=bst_delete(root.left,k)
    elif k>root.key: root.right=bst_delete(root.right,k)
    else:
        if root.left is None: return root.right
        if root.right is None: return root.left
        succ=root.right
        while succ.left: succ=succ.left
        root.key=succ.key; root.right=bst_delete(root.right,succ.key)
    return root
root=bst_delete(root,1078)
fig,ax=plt.subplots(figsize=(14,10),facecolor=BG)
draw_tree(ax,root,bst_positions(root),'#2980B9','Q8d - BST After Deleting Order 1078 (Successor: 1089)')
save(fig,'bst_after_deletion.png')

# 9. AVL
print("9. AVL tree")
class AVLNode:
    def __init__(self,k): self.key=k;self.left=None;self.right=None;self.height=1
def avl_h(n): return n.height if n else 0
def avl_uh(n):
    if n: n.height=1+max(avl_h(n.left),avl_h(n.right))
def avl_bf(n): return avl_h(n.left)-avl_h(n.right) if n else 0
def rr(y): x=y.left;t=x.right;x.right=y;y.left=t;avl_uh(y);avl_uh(x);return x
def lr(x): y=x.right;t=y.left;y.left=x;x.right=t;avl_uh(x);avl_uh(y);return y
def avl_insert(root,k):
    if not root: return AVLNode(k)
    if k<root.key: root.left=avl_insert(root.left,k)
    elif k>root.key: root.right=avl_insert(root.right,k)
    else: return root
    avl_uh(root); bf=avl_bf(root)
    if bf>1 and k<root.left.key: return rr(root)
    if bf<-1 and k>root.right.key: return lr(root)
    if bf>1 and k>root.left.key: root.left=lr(root.left); return rr(root)
    if bf<-1 and k<root.right.key: root.right=rr(root.right); return lr(root)
    return root
avl_root=None
for k in keys: avl_root=avl_insert(avl_root,k)
fig,ax=plt.subplots(figsize=(14,10),facecolor=BG)
draw_tree(ax,avl_root,bst_positions(avl_root),'#27AE60','Q9b - AVL Tree (Balanced) - 12 Orders')
save(fig,'avl_tree_final.png')

# 10. Sorting
print("10. Sorting performance")
random.seed(42)
def ms(a):
    if len(a)<=1:return a
    m=len(a)//2;l=ms(a[:m]);r=ms(a[m:]);res=[];i=j=0
    while i<len(l) and j<len(r):
        if l[i]<=r[j]:res.append(l[i]);i+=1
        else:res.append(r[j]);j+=1
    res.extend(l[i:]);res.extend(r[j:]);return res
def qs(a):
    if len(a)<=1:return a
    p=a[len(a)//2]
    return qs([x for x in a if x<p])+[x for x in a if x==p]+qs([x for x in a if x>p])
sys.setrecursionlimit(25000)
sizes=[100,500,1000,2500,5000,10000]; ms_t=[]; qs_t=[]
for s in sizes:
    d=[random.randint(1,100000) for _ in range(s)]
    t0=time.time();ms(d[:]);ms_t.append(time.time()-t0)
    t0=time.time();qs(d[:]);qs_t.append(time.time()-t0)
fig,ax=plt.subplots(figsize=(14,8),facecolor=BG)
ax.set_facecolor(BG)
ax.plot(sizes,ms_t,'o-',color='#E74C3C',linewidth=3,markersize=10,label='Merge Sort',zorder=3)
ax.plot(sizes,qs_t,'s-',color='#2980B9',linewidth=3,markersize=10,label='Quick Sort',zorder=3)
ax.fill_between(sizes,ms_t,alpha=0.08,color='#E74C3C')
ax.fill_between(sizes,qs_t,alpha=0.08,color='#2980B9')
ax.set_xlabel('Dataset Size',fontsize=14)
ax.set_ylabel('Execution Time (seconds)',fontsize=14)
ax.set_title('Q22 - Merge Sort vs Quick Sort Performance',fontsize=16,fontweight='bold',color=BORDER)
ax.legend(fontsize=13,loc='upper left',framealpha=0.9)
ax.grid(True,alpha=0.3,linestyle='--')
fig.tight_layout()
save(fig,'sorting_performance.png')

# 11. Road closure
print("11. Road closure comparison")
adj_o=build_adj(); adj_c=build_adj(blocked=('H1','H4'))
p_o,_=dijkstra(adj_o,'H1','D4',0); p_c,_=dijkstra(adj_c,'H1','D4',0)
fig,axes=plt.subplots(1,2,figsize=(24,12),facecolor=BG)
for ax_i,(label,adj_u,path,blk) in enumerate([
    ('Original Network',adj_o,p_o,None),
    ('Road Closed (H1<->H4)',adj_c,p_c,('H1','H4'))]):
    ax=axes[ax_i]
    pe=[(path[i],path[i+1]) for i in range(len(path)-1)]
    draw_graph(ax,highlight_edges=pe,blocked=blk,path_nodes=set(path),
               title=f'{label}: {" -> ".join(path)}')
fig.suptitle('Q27d - Road Closure Impact Analysis: H1 -> D4',fontsize=18,fontweight='bold',color=BORDER,y=0.98)
fig.tight_layout(rect=[0,0,1,0.95])
save(fig,'road_closure_comparison.png')

print("\nAll 11 figures regenerated successfully!")
