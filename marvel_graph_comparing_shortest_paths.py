""" Utility Functions"""

import csv
import time
from random import randint
import heapq
from priority_dictionary import priority_dict
from collections import deque

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        G[node1][node2] = 1.0
    else:
        G[node1][node2] += 1.0
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        G[node2][node1] = 1.0
    else:
        G[node2][node1] += 1.0
    return G

def weight_graph(G):
    for node1 in G:
        node1 = G[node1]
        for node2 in node1:
            node1[node2] = 1.0/node1[node2]
    return G

def unweighted_graph(G):
    for node1 in G:
        for node2 in G[node1]:
            G[node1][node2] = 1
    return G

def read_graph(filename):
    tsv = csv.reader(open(filename),delimiter = '\t')
    marvelG, characters, comicbooks, charG = {}, {}, {}, {}  
    index = 0
    
    for (char, comic) in tsv:
        characters[char] = True
        comicbooks[comic] = True
        marvelG = make_link(marvelG, char, comic)

    done = set()
    for char1 in characters:
        done.add(char1)
        for book in marvelG[char1]:
            for char2 in marvelG[book]:
                if char2 not in done:
                    charG = make_link(charG, char1, char2)
    return marvelG, charG


w_charG = {}
u_charG = {}


marvelG, charG = read_graph('C:\Python27\uniq_edges.tsv')
print 'generating graphs, marvelG, charG...'
w_charG = weight_graph(charG)
print 'generating weighted graph and unweighted graph'
u_charG = unweighted_graph(charG)


"""Below is the list of characters in question."""

chars = ['SPIDER-MAN/PETER PAR',
         'GREEN GOBLIN/NORMAN ',
         'WOLVERINE/LOGAN ',
         'PROFESSOR X/CHARLES ',
         'CAPTAIN AMERICA']

def dijkstra(G,v):
    dist_so_far = priority_dict()
    dist_so_far[v] = 0
    final_dist = {}
    dist = {}
    dist[v] = 0
    shortest_paths = {}
    shortest_paths[v] = [[v]]
    while len(dist_so_far) != 0:
        w = dist_so_far.pop_smallest()
        # lock it down!
        final_dist[w] = dist[w]
        
        for x in G[w]:
            if x not in final_dist:
                if x not in dist:
                    dist[x] = final_dist[w] + G[w][x]
                    dist_so_far[x] = final_dist[w] + G[w][x]
                    paths = [path + [x] for path in shortest_paths[w]]
                    shortest_paths[x] = paths                    
                elif final_dist[w] + G[w][x] < dist[x]:
                    dist[x] = final_dist[w] + G[w][x]
                    dist_so_far[x] = final_dist[w] + G[w][x]
                    paths = [path + [x] for path in shortest_paths[w]]
                    shortest_paths[x] = paths
                elif final_dist[w] + G[w][x] == dist[x]:
                    paths = [path + [x] for path in shortest_paths[w]]
                    shortest_paths[x].extend(paths)
                    dist_so_far[x] = final_dist[w] + G[w][x]
                    
    return final_dist, shortest_paths


def bfs(G, node):
    final_dist = {node:(0, node, None)}
    open_list = deque([node])
    while len(open_list) > 0:
        node = open_list.popleft()
        dist, _, _ = final_dist[node]
        for neighbor in G[node]:
            if neighbor not in final_dist:
                continue
            final_dist[neighbor] = (dist + 1, neighbor, node)
            open_list.append(neighbor)
    return final_dist

def get_parent(pair): return pair[2]
def find_path(dist, target):
    node = target
    path = [target]
    while True:
        prev = get_parent(dist[node])
        if prev is None:
            # We've rached our target, so return 
            # the path
            return path
        path.append(prev)
        node = prev

total = 0
counter  = 0
answers = []
print 'calculating shortest paths...'

for char1 in chars:
    w_final_dist, w_shortest_paths = dijkstra(w_charG, char1)
    u_final_dist = bfs(u_charG, char1)
    for char2 in w_final_dist:
        if char1 == char2: continue
        char_path = min(w_shortest_paths[char2], key = lambda n: len(n))
        hop_path = find_path(u_final_dist, char1)
        if len(char_path) > len(hop_path):
            answers.append(((char1, char2), (char_path, hop_path)))
    print char1, len(answers) - counter
    counter = len(answers)

print len(answers)
        
        



