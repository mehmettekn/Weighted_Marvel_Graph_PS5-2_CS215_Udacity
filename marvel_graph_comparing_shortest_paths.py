import csv


def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        (G[node1])[node2] = 1
    else:
        (G[node1])[node2] += 1
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        (G[node2])[node1] = 1
    else:
        (G[node2])[node1] += 1
    return G

def weight_graph(G):
    for node1 in G:
        for node2 in G[node1]:
            G[node1][node2] = 1.0/G[node1][node2]
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
        if char not in characters:
            characters[char] = index
            index += 1
            comicbooks [comic] = True
            marvelG = make_link(marvelG, char, comic)

    for char1 in characters:
        for book in marvelG[char1]:
            for char2 in marvelG[book]:
                if characters[char1] < characters[char2]:
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


""" Utility Functions"""

import time
from random import randint
import heapq

""" priority_dict class was used to  implement heaps efficiently. The class makes it
possible to update the dictionary key values in constant time. The class was taken from
the url given below."""

## {{{ http://code.activestate.com/recipes/522995/ (r1)
from heapq import heapify, heappush, heappop

class priority_dict(dict):
    """Dictionary that can be used as a priority queue.

    Keys of the dictionary are items to be put into the queue, and values
    are their respective priorities. All dictionary methods work as expected.
    The advantage over a standard heapq-based priority queue is
    that priorities of items can be efficiently updated (amortized O(1))
    using code as 'thedict[item] = new_priority.'

    The 'smallest' method can be used to return the object with lowest
    priority, and 'pop_smallest' also removes it.

    The 'sorted_iter' method provides a destructive sorted iterator.
    """
    
    def __init__(self, *args, **kwargs):
        super(priority_dict, self).__init__(*args, **kwargs)
        self._rebuild_heap()

    def _rebuild_heap(self):
        self._heap = [(v, k) for k, v in self.iteritems()]
        heapify(self._heap)

    def smallest(self):
        """Return the item with the lowest priority.

        Raises IndexError if the object is empty.
        """
        
        heap = self._heap
        v, k = heap[0]
        while k not in self or self[k] != v:
            heappop(heap)
            v, k = heap[0]
        return k

    def pop_smallest(self):
        """Return the item with the lowest priority and remove it.

        Raises IndexError if the object is empty.
        """
        
        heap = self._heap
        v, k = heappop(heap)
        while k not in self or self[k] != v:
            v, k = heappop(heap)
        del self[k]
        return k

    def __setitem__(self, key, val):
        # We are not going to remove the previous value from the heap,
        # since this would have a cost O(n).
        
        super(priority_dict, self).__setitem__(key, val)
        
        if len(self._heap) < 2 * len(self):
            heappush(self._heap, (val, key))
        else:
            # When the heap grows larger than 2 * len(self), we rebuild it
            # from scratch to avoid wasting too much memory.
            self._rebuild_heap()

    def setdefault(self, key, val):
        if key not in self:
            self[key] = val
            return val
        return self[key]

    def update(self, *args, **kwargs):
        # Reimplementing dict.update is tricky -- see e.g.
        # http://mail.python.org/pipermail/python-ideas/2007-May/000744.html
        # We just rebuild the heap from scratch after passing to super.
        
        super(priority_dict, self).update(*args, **kwargs)
        self._rebuild_heap()

    def sorted_iter(self):
        """Sorted iterator of the priority dictionary items.

        Beware: this will destroy elements as they are returned.
        """
        
        while self:
            yield self.pop_smallest()
## end of http://code.activestate.com/recipes/522995/ }}}

def dijkstra(G,v):
    dist_so_far = priority_dict()
    dist_so_far[v] = 0
    final_dist = {}
    dist = {}
    dist[v] = 0
    while len(final_dist) < len(G) and len(dist_so_far) != 0:
        w = dist_so_far.pop_smallest()
        # lock it down!
        final_dist[w] = dist[w]
        
        for x in G[w]:
            if x not in final_dist:
                if x not in dist:
                    dist[x] = final_dist[w] + G[w][x]
                    dist_so_far[x] = final_dist[w] + G[w][x]
                elif final_dist[w] + G[w][x] < dist[x]:
                    dist[x] = final_dist[w] + G[w][x]
                    dist_so_far[x] = final_dist[w] + G[w][x]
    return final_dist


total = 0
'''
print 'calculating shortest paths...'
for char in chars:
    w_shortest_paths = dijkstra(w_charG, char)
    u_shortest_paths = dijkstra(u_charG, char)
    counter = 0
    for char2 in w_shortest_paths:
        #min_number_nodes_path = w_shortest_paths[char2]

        if w_shortest_paths[char2] != u_shortest_paths[char2]:
            counter += 1
            total += 1
    print char, ' = ', counter, ' differences.'

print 'Total number of differences:', total
'''
print dijkstra(w_charG, chars[2])
print dijkstra(u_charG, chars[2])
print chars[2]
print chars[2] in w_charG
print w_charG
                 
    
