def unweighted_graph(G):
    for node1 in G:
        for node2 in G[node1]:
            G[node1][node2] = 1
    return G

G = {'a':{'b':3,'c':4,'z':7},'d':{3:3,6:4}}

print unweighted_graph(G)
