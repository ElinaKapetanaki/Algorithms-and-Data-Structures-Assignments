import argparse
from collections import deque

def read_text_file(file):
    with open(file) as f:
        text = f.read()
    return text

def create_trie(kws):
    trie = {}
    trie_c = {}
    terminal = {}
    parent = {}
    depth = {}
    trie[0] = []
    terminal[0] = False
    depth[0] = 0
    id_num = 1
    for kw in kws:
        kw = kw[::-1]
        parent_id = 0
        for c in kw:
            if not has_child(trie, trie_c, parent_id, c):
                trie[id_num] = []
                trie[parent_id].append(id_num)
                trie_c[parent_id, id_num] = c
                terminal[id_num] = False
                parent[id_num] = parent_id
                depth[id_num] = depth[parent_id] + 1
                parent_id = id_num
                id_num += 1
            else:
                parent_id = get_child(trie, trie_c, parent_id, c)
        terminal[parent_id] = True
    return (trie, trie_c, parent, depth, terminal)

def get_child(trie, trie_c, u, c):
    for child in trie[u]:
        if trie_c[u, child] == c:
            return child
    return -1

def has_child(trie, trie_c, u, c):
    for child in trie[u]:
        if trie_c[u, child] == c:
            return True
    return False

def create_rt(pmin, depth):
    rt = {}
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for l in letters:
        rt[l] = pmin + 1
    for u in trie:
        if u != 0 and rt[trie_c[parent[u], u]] > depth[u]: # there is no character in node 0
            rt[trie_c[parent[u], u]] = depth[u]
    return rt

def create_failure(trie, trie_c):
    failure = [None] * len(trie)
    for u in trie.keys() :
        if depth[u] <= 1:
            failure[u] = 0
    q = deque()
    q.appendleft(0)
    while q:
        u = q.pop()
        for v in trie[u]:
            # Due to the nature of the trie the nodes can't 
            # have been visited or inserted in the queue before,
            # so we simply add them to the queue
            q.appendleft(v)
            if depth[u] >= 1:
                c = trie_c[u, v]
                u2 = failure[u]
                v2 = get_child(trie, trie_c, u2, c)
                while u2 != 0 and v2 == -1:
                    u2 = failure[u2]
                    v2 = get_child(trie, trie_c, u2, c)
                if v2 != -1:
                    failure[v] = v2
                else:
                    failure[v] = 0
    return failure

def create_set1(f):
    set1 = [set() for x in trie]
    for i, u in enumerate(f):
        set1[u].add(i)
    return set1

def create_set2(set1):
    set2 = [set() for x in trie]
    for u, s in enumerate(set1):
        for v in s:
            if terminal[v]:
                set2[u].add(v)
    return set2

def create_s1(set1):
    s1 = [None] * len(trie)
    for u, s in enumerate(set1):
        if u != 0 and s:
            s1[u] = min(pmin, min(depth[u2] - depth[u] for u2 in s))
        elif u != 0 and not s:
            s1[u] = pmin
        else:
            s1[u] = 1
    return s1

def create_s2(set2):
    s2 = [None] * len(trie)
    for u, s in enumerate(set2):
        if u != 0 and s:
            s2[u] = min(s2[parent[u]], min(depth[u2] - depth[u] for u2 in s))
        elif u != 0 and not s:
            s2[u] = s2[parent[u]]
        else:
            s2[u] = pmin
    return s2

def commentz_walter(t):
    q = deque()
    i = pmin - 1
    j = 0
    u = 0
    m = ''
    while i < len(t):
        while has_child(trie, trie_c, u, t[i - j]) and i >= j:
            u = get_child(trie, trie_c, u, t[i - j])
            m = m + t[i - j]
            j = j + 1
            if terminal[u]:
                q.appendleft((m[::-1], i - j + 1))
        if j > i:
            j = i
        s = min(s2[u], max(s1[u], rt[t[i - j]] - j - 1))
        i = i + s
        j = 0
        u = 0
        m = ''
    return q

parser = argparse.ArgumentParser()
parser.add_argument('-v', action = 'store_true', help = 'enable output s1 and s2')
parser.add_argument('kw', nargs = '+', help = 'keywords')
parser.add_argument('input_filename', help = 'name of the input file')
args = parser.parse_args()
kws = [kw.strip("'") for kw in args.kw]
text = read_text_file(args.input_filename)
trie, trie_c, parent, depth, terminal = create_trie(kws)
pmin = min(len(kw) for kw in kws)
rt = create_rt(pmin, depth)
failure = create_failure(trie, trie_c)
set1 = create_set1(failure)
set2 = create_set2(set1)
s1 = create_s1(set1)
s2 = create_s2(set2)
results = commentz_walter(text)
if args.v:
    for i in range(len(trie)):
        print(f"{i}: {s1[i]},{s2[i]}")
while results:
    r = results.pop()
    print(f"{r[0]}: {r[1]}")
