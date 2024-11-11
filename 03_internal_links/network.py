# networkxチートシート（ご自由にお使い下さい）
import networkx as nx

# 空の有向グラフの作成 (Directed Graph)
G = nx.DiGraph()

#### node(頂点)とedge(辺)の追加 ####
# G.add_nodes_from(['a','b','c','d'])
G.add_edges_from([('a','b'),('a','c'),('a','d'),('b','c'),('b','d'),('d','c')])

#### 属性値(頂点の値)の設定 ####
# G.nodes[頂点][属性キー] = 属性値
G.nodes[1]['a'] = 'Alice'

# G.edges[辺][属性キー] = 属性値
G.edges[1, 2]['b'] = 'Bob'

# G.succ[始点][終点][属性キー] = 属性値
G.succ[2][3]['c'] = 'Carol'

# G.pred[終点][始点][属性キー] = 属性値
G.pred[3][1]['d'] = 'Dave'

#### edge(辺)の削除 ####
# G.remove_edge(3, 4)                    
G.remove_edges_from([(1, 3), (2, 5)])

#### 頂点の削除 (削除された頂点に接続されている辺も削除されます) ####
#G.remove_node(5)
G.remove_nodes_from([3, 4])

#### nodeとedge(頂点と辺)を同時に追加
# 指定したパス上の頂点と辺を追加
nx.add_path(G, [1, 2, 3, 4, 5])  # 1 → 2 → 3 → 4 → 5

# 指定した閉路上の頂点と辺を追加
nx.add_cycle(G, [1, 2, 3, 4, 5])  # 1 → 2 → 3 → 4 → 5 → 1

# 放射状に頂点と辺を追加（1 → 2, 1 → 3, 1 → 4, 1 → 5）

#nx.add_path(G, [3, 5, 4, 1, 0, 2, 7, 8, 9, 6])  # add_pathで順番にたどる
nx.add_path(G, [3, 0, 6, 4, 2, 7, 1, 9, 8, 5])

#### レイアウトの指定 ####

# springレイアウト(頂点が重ならず、辺で繋がっている頂点は近くに、繋がっていない頂点は遠くに配置)
pos=nx.spring_layout(G)

# ランダムレイアウト(頂点と辺をランダムに配置)
# pos=nx.random_layout()
