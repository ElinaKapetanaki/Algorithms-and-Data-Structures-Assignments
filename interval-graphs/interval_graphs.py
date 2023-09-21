import argparse
from collections import deque

def read_input_file(input_file):
    graph = {}
    with open(input_file) as f:
        for line in f:
            x, y = [int(x) for x in line.split()]
            if x not in graph:
                graph[x] = []
            if y not in graph:
                graph[y] = []
            graph[x].append(y)
            graph[y].append(x)
    return graph

def lex_bfs(g):
    s_dict = {0: set(g.keys())}
    s_next = {None: 0}
    s_prev = {0: None}
    last_id = 0
    visit_order = ()
    visited = {node: False for node in g}
    while len(s_next) > 0:
        u = min(s_dict[s_next[None]])
        s_dict[s_next[None]].remove(u)
        visited[u] = True
        visit_order += (u,)
        if not s_dict[s_next[None]]: #if the first set is empty
            # delete the first set from the dictionary
            del s_dict[s_next[None]]
            # delete the first set from the the linked list
            id_to_delete = s_next[None]
            if len(s_dict) > 0:
                next_id = s_next[id_to_delete]
                s_prev[next_id] = None
                s_next[None] = next_id
                del s_next[id_to_delete]
                del s_prev[id_to_delete]
            else:
                del s_next[None]
                del s_prev[id_to_delete]
        adj_sets = {i: set() for i in s_dict} 
        for adj_node in g[u]:
            if not visited[adj_node]:
                for j in s_dict:
                    if adj_node in s_dict[j]:
                        s_dict[j].remove(adj_node)
                        # keep the ones to be added before the set with id: j
                        adj_sets[j].add(adj_node)
                        break
        for i, adj_set in adj_sets.items():
            if adj_set:
                last_id += 1
                s_dict[last_id] = adj_set
                # insert the new set's id to the linked list before i
                prev_id = s_prev[i]
                next_id = i
                s_next[prev_id] = last_id
                s_prev[next_id] = last_id
                s_next[last_id] = next_id
                s_prev[last_id] = prev_id
                # if the set where adj_set was taken from became empty, delete it
                if not s_dict[s_next[last_id]]:
                    del s_dict[s_next[last_id]]
                    id_to_delete = s_next[last_id]
                    prev_id = s_prev[id_to_delete]
                    # if the set to delete is not the last set of the linked list 
                    # (because there exists one next to it)
                    if id_to_delete in s_next:
                        next_id = s_next[id_to_delete]
                        s_prev[next_id] = prev_id
                        s_next[prev_id] = next_id
                        del s_next[id_to_delete]
                        del s_prev[id_to_delete]
                    else:
                        del s_prev[id_to_delete]
                        del s_next[prev_id]
    return visit_order

def check_chordal_graph(r_lbfs, g):
    for index_u, u in enumerate(r_lbfs):
        rn_u = set()
        rn_v = set()
        count = 0
        for i in range(index_u + 1, len(r_lbfs)):
            if r_lbfs[i] in g[u]:
                rn_u.add(r_lbfs[i])
                count += 1
                if count == 1:
                    v = r_lbfs[i]
                    index_v = i
        if rn_u: # if the rn_u set is not empty
            for j in range(index_v + 1, len(r_lbfs)):
                if r_lbfs[j] in g[v]:
                    rn_v.add(r_lbfs[j])
            if not (rn_u - {v}).issubset(rn_v):
                return False
    return True

def components_simple_bfs(g, u):
    visited = [False] * len(g)
    components = []
    for node in g:
        if not visited[node] and node != u and node not in g[u]:
            component = {}
            q = deque()
            inqueue = [False] * len(g)
            starting_node = node
            q.appendleft(starting_node)
            inqueue[starting_node] = True
            while q: #while the queue is not empty
                c = q.pop()
                inqueue[c] = False
                visited[c] = True
                component[c] = []
                for v in g[c]:
                    if not visited[v] and not inqueue[v] and v != u and v not in g[u]:
                        q.appendleft(v)
                        component[c].append(v)
                        inqueue[v] = True
            components.append(component)
    return components

def check_asteroidal_triple_free(g):
    c = [[0] * len(g) for x in range(len(g))]
    for u in g:
        components = components_simple_bfs(g, u)
        for comp in components:
            for v in comp.keys():
                c[u][v] = comp
    for u in range(len(c)):
        for v in range(len(c)):
            for w in range(len(c)):
                if c[u][v] != 0 and c[u][w] != 0 and  c[v][u] != 0 and \
                    c[v][w] != 0 and c[w][u] != 0 and c[w][v] != 0 and \
                    c[u][v] == c[u][w] and c[v][u] == c[v][w] and c[w][u] == c[w][v]:
                        return False
    return True
    
parser = argparse.ArgumentParser()
parser.add_argument("task", help = "the program's task", 
                    choices = ["lexbfs", "cordal", "interval"])
parser.add_argument("input_filename", help = "the name of the input file")
args = parser.parse_args()

input_graph = read_input_file(args.input_filename)
l_bfs_order = list(lex_bfs(input_graph))
if args.task == "lexbfs":
    print(l_bfs_order)
elif args.task == "cordal":
    l_bfs_order.reverse()
    is_cordal = check_chordal_graph(l_bfs_order, input_graph)
    print(is_cordal)
elif args.task == "interval":
    l_bfs_order.reverse()
    is_cordal = check_chordal_graph(l_bfs_order, input_graph)
    at_free = False
    if is_cordal:
        at_free = check_asteroidal_triple_free(input_graph)
    print(is_cordal and at_free)