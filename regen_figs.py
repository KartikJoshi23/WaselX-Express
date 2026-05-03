"""Production-grade figures for LaTeX report."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import random,time,sys

plt.rcParams.update({'font.size':14,'font.family':'sans-serif','axes.facecolor':'white',
                     'figure.facecolor':'white','savefig.facecolor':'white'})

NODES={'H1':'Dubai Marina','H2':'Business Bay','H3':'Deira','H4':'JLT',
       'H5':'Abu Dhabi','H6':'Khalifa City','H7':'Sharjah',
       'D1':'Downtown','D2':'Al Quoz','D3':'Jumeirah','D4':'Silicon Oasis',
       'D5':'Ajman','D6':'Yas Island','D7':'Al Reem','D8':'Muwaileh'}
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
HUBS=[n for n in AN if n[0]=='H']
HUB_C='#8b5cf6'; ZONE_C='#06b6d4'; BORDER='#1e1b4b'
EDGE_C='#94a3b8'; HL_COLS=['#dc2626','#2563eb','#16a34a','#d946ef']

def draw_node(ax,n,sz=700,highlight=False):
    x,y=POS[n]; is_h=n[0]=='H'
    col=HUB_C if is_h else ZONE_C
    s=sz*1.3 if highlight else sz
    ec=BORDER; lw=3 if highlight else 2
    ax.scatter(x,y,s=s,c=col,edgecolors=ec,linewidths=lw,zorder=5,alpha=0.95)
    ax.text(x,y,n,ha='center',va='center',fontsize=13,fontweight='bold',color='white',zorder=6)
    ax.text(x,y-0.55,NODES[n],ha='center',va='top',fontsize=8,color='#475569',zorder=6,style='italic')

def draw_edge(ax,u,v,d,col=EDGE_C,w=1.5,alpha=0.5,unit='km',show_label=True):
    x0,y0=POS[u];x1,y1=POS[v]
    ax.plot([x0,x1],[y0,y1],'-',color=col,linewidth=w,alpha=alpha,zorder=1)
    if show_label:
        mx,my=(x0+x1)/2,(y0+y1)/2
        dx,dy=x1-x0,y1-y0
        ang=np.degrees(np.arctan2(dy,dx))
        ax.text(mx,my+0.25,f'{d} {unit}',ha='center',va='center',fontsize=8,
                color=col if col!=EDGE_C else '#64748b',fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.15',fc='white',ec='none',alpha=0.85),
                rotation=0,zorder=3)

def setup_ax(ax,title):
    ax.set_title(title,fontsize=16,fontweight='bold',color=BORDER,pad=18)
    ax.set_aspect('equal');ax.axis('off');ax.margins(0.1)

def save(fig,name):
    fig.savefig(name,dpi=200,bbox_inches='tight',pad_inches=0.3)
    plt.close(fig);print(f'  {name}')

# === Algorithms ===
class MinHeap:
    def __init__(s):s.h=[]
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
    def empty(s):return len(s.h)==0

def build_adj(bl=None):
    a={n:[] for n in AN}
    for u,v,r,d,t,c in EDGES:
        if bl and ((u,v)==bl or (v,u)==bl):continue
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

def draw_full(ax,hl_edges=None,hl_col='#dc2626',blocked=None,hl_nodes=None,edge_key='dist',title=''):
    if hl_edges is None:hl_edges=[]
    if hl_nodes is None:hl_nodes=set()
    he=set();
    for e in hl_edges:he.add(e);he.add((e[1],e[0]))
    eidx={'dist':3,'time':4,'cost':5}
    units={'dist':'km','time':'min','cost':'AED'}
    ki=eidx.get(edge_key,3);unit=units.get(edge_key,'km')
    for u,v,r,d,t,c in EDGES:
        if blocked and ((u,v)==blocked or (v,u)==blocked):continue
        val=[d,t,c][ki-3]
        if (u,v) in he or (v,u) in he:
            draw_edge(ax,u,v,val,col=hl_col,w=4,alpha=0.9,unit=unit)
        else:
            draw_edge(ax,u,v,val,unit=unit)
    if blocked:
        x0,y0=POS[blocked[0]];x1,y1=POS[blocked[1]]
        ax.plot([x0,x1],[y0,y1],'--',color='#ef4444',linewidth=3,alpha=0.7,zorder=2)
        ax.scatter([(x0+x1)/2],[(y0+y1)/2],marker='X',s=200,c='#ef4444',zorder=4)
    for n in AN:
        draw_node(ax,n,highlight=n in hl_nodes)
    setup_ax(ax,title)
    # Legend
    ax.scatter([],[],s=120,c=HUB_C,edgecolors=BORDER,linewidths=1.5,label='Hub (H1-H7)')
    ax.scatter([],[],s=120,c=ZONE_C,edgecolors=BORDER,linewidths=1.5,label='Delivery Zone (D1-D8)')
    if hl_edges:
        ax.plot([],[],'-',color=hl_col,linewidth=3,label='Highlighted Path')
    ax.legend(loc='lower left',fontsize=10,framealpha=0.9,edgecolor='#e2e8f0')

print("Generating production figures...")

# 1. Full network
fig,ax=plt.subplots(figsize=(16,11))
draw_full(ax,title='WaselX Express \u2014 Full Delivery Network (15 Nodes, 24 Edges)')
save(fig,'graph_network_full.png')

# 2. Dijkstra H1->D1
adj=build_adj();p,_=dijkstra(adj,'H1','D1',0)
pe=[(p[i],p[i+1]) for i in range(len(p)-1)]
fig,ax=plt.subplots(figsize=(16,11))
draw_full(ax,hl_edges=pe,hl_nodes=set(p),title=f'Q2 \u2014 Dijkstra Shortest Path: H1 \u2192 D1 ({sum(e[3] for e in EDGES if (e[0],e[1]) in pe or (e[1],e[0]) in pe)} km)')
save(fig,'dijkstra_path_h1_d1.png')

# 3. Floyd-Warshall heatmap
INF=float('inf');idx_map={n:i for i,n in enumerate(AN)}
fw=[[INF]*15 for _ in range(15)]
for i in range(15):fw[i][i]=0
for u,v,r,d,t,c in EDGES:
    i,j=idx_map[u],idx_map[v];fw[i][j]=min(fw[i][j],t);fw[j][i]=min(fw[j][i],t)
for k in range(15):
    for i in range(15):
        for j in range(15):
            if fw[i][k]+fw[k][j]<fw[i][j]:fw[i][j]=fw[i][k]+fw[k][j]
hi=[idx_map[h] for h in HUBS]
hm=np.array([[fw[i][j] for j in hi] for i in hi],dtype=float)
hm[hm>9000]=np.nan
fig,ax=plt.subplots(figsize=(10,8))
im=ax.imshow(hm,cmap='YlOrRd',interpolation='nearest')
ax.set_xticks(range(7));ax.set_yticks(range(7))
ax.set_xticklabels(HUBS,fontsize=13,fontweight='bold')
ax.set_yticklabels(HUBS,fontsize=13,fontweight='bold')
for i in range(7):
    for j in range(7):
        v=hm[i][j];txt='\u221e' if np.isnan(v) else f'{int(v)}'
        c='white' if (not np.isnan(v) and v>35) else BORDER
        ax.text(j,i,txt,ha='center',va='center',fontsize=14,fontweight='bold',color=c)
cb=plt.colorbar(im,ax=ax,shrink=0.85);cb.set_label('Travel Time (min)',fontsize=12)
ax.set_title('Q3 \u2014 Floyd-Warshall: Hub-to-Hub Travel Times',fontsize=16,fontweight='bold',color=BORDER,pad=15)
fig.tight_layout();save(fig,'floyd_warshall_hubs.png')

# 4. Kruskal MST
se=sorted(EDGES,key=lambda e:e[5])
par={n:n for n in AN};rnk={n:0 for n in AN}
def find(x):
    while par[x]!=x:par[x]=par[par[x]];x=par[x]
    return x
def union(a,b):
    a,b=find(a),find(b)
    if a==b:return False
    if rnk[a]<rnk[b]:a,b=b,a
    par[b]=a
    if rnk[a]==rnk[b]:rnk[a]+=1
    return True
mst_e=[];mst_n=set()
for u,v,r,d,t,c in se:
    if union(u,v):mst_e.append((u,v));mst_n.add(u);mst_n.add(v)
fig,ax=plt.subplots(figsize=(16,11))
draw_full(ax,hl_edges=mst_e,hl_col='#16a34a',hl_nodes=mst_n,edge_key='cost',title="Q4a \u2014 Kruskal's MST (Cost in AED)")
save(fig,'mst_kruskal.png')

# 5. Prim MST
ac=build_adj();visited={'H2'};prim_e=[];prim_n={'H2'}
cands=[(c,'H2',nb) for nb,d,t,c in ac['H2']];cands.sort()
while cands:
    cost,u,v=cands.pop(0)
    if v in visited:continue
    visited.add(v);prim_e.append((u,v));prim_n.add(v)
    for nb,d,t,c in ac[v]:
        if nb not in visited:cands.append((c,v,nb))
    cands.sort()
fig,ax=plt.subplots(figsize=(16,11))
draw_full(ax,hl_edges=prim_e,hl_col='#9333ea',hl_nodes=prim_n,edge_key='cost',title="Q4c \u2014 Prim's MST from H2 (Cost in AED)")
save(fig,'mst_prim.png')

# 6. BFS from H3
ab=build_adj();vis={'H3'};q=['H3'];bfs_e=[];bfs_ord=['H3'];lvl={'H3':0}
while q:
    u=q.pop(0)
    for nb,*_ in ab[u]:
        if nb not in vis:
            vis.add(nb);q.append(nb);bfs_e.append((u,nb));bfs_ord.append(nb);lvl[nb]=lvl[u]+1
fig,ax=plt.subplots(figsize=(16,11))
draw_full(ax,hl_edges=bfs_e,hl_col='#2563eb',hl_nodes=set(bfs_ord),title=f'Q7a \u2014 BFS Tree from H3 (Deira) \u2014 {len(bfs_ord)} nodes')
for n,lv in lvl.items():
    ax.annotate(f'L{lv}',xy=POS[n],xytext=(14,-14),textcoords='offset points',fontsize=8,
                color='#2563eb',fontweight='bold',bbox=dict(boxstyle='round,pad=0.15',fc='#eff6ff',ec='#2563eb',alpha=0.9))
save(fig,'bfs_tree_h3.png')

# 7-9. Trees
class BSTNode:
    def __init__(s,k):s.key=k;s.left=None;s.right=None
def bst_ins(r,k):
    if r is None:return BSTNode(k)
    if k<r.key:r.left=bst_ins(r.left,k)
    elif k>r.key:r.right=bst_ins(r.right,k)
    return r
def tree_pos(n,x=0,y=0,dx=6.0,p=None):
    if p is None:p={}
    if n is None:return p
    p[n.key]=(x,y)
    tree_pos(n.left,x-dx,y-2.5,dx*0.52,p)
    tree_pos(n.right,x+dx,y-2.5,dx*0.52,p)
    return p
def tree_depth(n):
    if not n:return 0
    return 1+max(tree_depth(n.left),tree_depth(n.right))
def draw_tree(ax,node,positions,col,title,show_bf=False):
    R=0.78
    def edges(n):
        if not n:return
        for ch in [n.left,n.right]:
            if ch:
                x0,y0=positions[n.key];x1,y1=positions[ch.key]
                ax.plot([x0,x1],[y0,y1],'-',color='#94a3b8',linewidth=3.5,zorder=1,solid_capstyle='round')
                edges(ch)
    edges(node)
    for k,(x,y) in positions.items():
        circle=plt.Circle((x,y),R,color=col,ec=BORDER,linewidth=3,zorder=3)
        ax.add_patch(circle)
        ax.text(x,y,str(k),ha='center',va='center',fontsize=16,fontweight='bold',color='white',zorder=4)
    min_x=min(v[0] for v in positions.values())
    seen_y={}
    for ly in sorted(set(round(v[1],1) for v in positions.values()),reverse=True):
        li=len(seen_y); seen_y[ly]=li
        ax.text(min_x-2.5,ly,f'Level {li}',ha='center',va='center',fontsize=11,
                color='#64748b',fontweight='bold',style='italic',
                bbox=dict(boxstyle='round,pad=0.3',fc='#f1f5f9',ec='#cbd5e1',alpha=0.9))
    if show_bf:
        def ann_bf(n):
            if not n:return
            bf=tree_depth(n.left)-tree_depth(n.right)
            x,y=positions[n.key]
            bc='#16a34a' if abs(bf)<=1 else '#dc2626'
            ax.text(x+R+0.25,y+R*0.5,f'BF={bf}',ha='left',va='center',fontsize=9,
                    color=bc,fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.2',fc='white',ec=bc,alpha=0.9))
            ann_bf(n.left);ann_bf(n.right)
        ann_bf(node)
    xs=[v[0] for v in positions.values()];ys=[v[1] for v in positions.values()]
    ax.set_xlim(min(xs)-3.5,max(xs)+3.5);ax.set_ylim(min(ys)-1.8,max(ys)+1.8)
    ax.set_aspect('equal');ax.axis('off')
    ax.set_title(title,fontsize=18,fontweight='bold',color=BORDER,pad=20)

keys=[1045,1023,1078,1012,1034,1056,1089,1005,1020,1067,1050,1098]
root=None
for k in keys:root=bst_ins(root,k)
fig,ax=plt.subplots(figsize=(18,12))
draw_tree(ax,root,tree_pos(root),'#2563eb','Q8a \u2014 Binary Search Tree (12 Orders)')
save(fig,'bst_initial.png')

def bst_del(r,k):
    if r is None:return r
    if k<r.key:r.left=bst_del(r.left,k)
    elif k>r.key:r.right=bst_del(r.right,k)
    else:
        if r.left is None:return r.right
        if r.right is None:return r.left
        s=r.right
        while s.left:s=s.left
        r.key=s.key;r.right=bst_del(r.right,s.key)
    return r
root=bst_del(root,1078)
fig,ax=plt.subplots(figsize=(18,12))
draw_tree(ax,root,tree_pos(root),'#2563eb','Q8d \u2014 BST After Deleting 1078 (Successor: 1089)')
save(fig,'bst_after_deletion.png')

class AVLNode:
    def __init__(s,k):s.key=k;s.left=None;s.right=None;s.height=1
def ah(n):return n.height if n else 0
def auh(n):
    if n:n.height=1+max(ah(n.left),ah(n.right))
def abf(n):return ah(n.left)-ah(n.right) if n else 0
def rr(y):x=y.left;t=x.right;x.right=y;y.left=t;auh(y);auh(x);return x
def lr(x):y=x.right;t=y.left;y.left=x;x.right=t;auh(x);auh(y);return y
def avl_ins(r,k):
    if not r:return AVLNode(k)
    if k<r.key:r.left=avl_ins(r.left,k)
    elif k>r.key:r.right=avl_ins(r.right,k)
    else:return r
    auh(r);bf=abf(r)
    if bf>1 and k<r.left.key:return rr(r)
    if bf<-1 and k>r.right.key:return lr(r)
    if bf>1 and k>r.left.key:r.left=lr(r.left);return rr(r)
    if bf<-1 and k<r.right.key:r.right=rr(r.right);return lr(r)
    return r
avl=None
for k in keys:avl=avl_ins(avl,k)
fig,ax=plt.subplots(figsize=(18,12))
draw_tree(ax,avl,tree_pos(avl),'#16a34a','Q9b \u2014 AVL Tree (Balanced) \u2014 12 Orders',show_bf=True)
save(fig,'avl_tree_final.png')

# 10. Sorting
random.seed(42);sys.setrecursionlimit(25000)
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
sizes=[100,500,1000,2500,5000,10000];ms_t=[];qs_t=[]
for s in sizes:
    d=[random.randint(1,100000) for _ in range(s)]
    t0=time.time();ms(d[:]);ms_t.append(time.time()-t0)
    t0=time.time();qs(d[:]);qs_t.append(time.time()-t0)
fig,ax=plt.subplots(figsize=(12,7))
ax.plot(sizes,ms_t,'o-',color='#dc2626',linewidth=3,markersize=10,label='Merge Sort',zorder=3)
ax.plot(sizes,qs_t,'s-',color='#2563eb',linewidth=3,markersize=10,label='Quick Sort',zorder=3)
ax.fill_between(sizes,ms_t,alpha=0.08,color='#dc2626')
ax.fill_between(sizes,qs_t,alpha=0.08,color='#2563eb')
ax.set_xlabel('Dataset Size',fontsize=14,fontweight='bold')
ax.set_ylabel('Execution Time (s)',fontsize=14,fontweight='bold')
ax.set_title('Q22 \u2014 Merge Sort vs Quick Sort Performance',fontsize=16,fontweight='bold',color=BORDER)
ax.legend(fontsize=13,framealpha=0.9);ax.grid(True,alpha=0.2,linestyle='--')
ax.spines['top'].set_visible(False);ax.spines['right'].set_visible(False)
fig.tight_layout();save(fig,'sorting_performance.png')

# 11. Road closure
adj_o=build_adj();adj_c=build_adj(bl=('H1','H4'))
p_o,_=dijkstra(adj_o,'H1','D4',0);p_c,_=dijkstra(adj_c,'H1','D4',0)
fig,axes=plt.subplots(1,2,figsize=(22,10))
for ax_i,(lbl,adj_u,path,blk) in enumerate([('Original',adj_o,p_o,None),('Road Closed (H1\u2194H4)',adj_c,p_c,('H1','H4'))]):
    ax=axes[ax_i]
    pe=[(path[i],path[i+1]) for i in range(len(path)-1)]
    arrow=' \u2192 '
    draw_full(ax,hl_edges=pe,blocked=blk,hl_nodes=set(path),title=f'{lbl}: {arrow.join(path)}')
fig.suptitle('Q27d \u2014 Road Closure Impact: H1 \u2192 D4',fontsize=18,fontweight='bold',color=BORDER,y=0.98)
fig.tight_layout(rect=[0,0,1,0.95]);save(fig,'road_closure_comparison.png')

print("All 11 figures generated!")
