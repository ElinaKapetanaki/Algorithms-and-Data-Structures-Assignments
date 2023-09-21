import argparse

def read_input_file(input_file):
    values = []
    with open(input_file) as f:
        for line in f:
            values.extend(line.split())
    return [int(x) for x in values]

def create_distance_dict():
    distances = {}
    for a in range(len(values)):
        for b in range(a + 1, len(values)):
            distances[((values[a],), (values[b],))] = calculate_first_distance(a, b)
    return distances

def calculate_first_distance(a, b):
    return abs(values[a] - values[b])

def extract_min_distance():
    min_dist = min(distances.values())
    # if distance of many pairs is equal to the minimum, take 
    # the minimum pair based on the first cluster of each key (pair)
    min_dist_keys = [k for k, d in distances.items() if d == min_dist]
    min_dist_keys.sort(key = lambda k: k[0])
    min_dist_pair = min_dist_keys[0]
    del distances[min_dist_pair]
    return [min_dist_pair, min_dist]

def update_distance_dict(c_s, c_t, d_st):
    c_st = c_s + c_t
    # find keys of pairs of clusters that contain cluster s
    keys_s = [k for k in distances.keys() if k[0] == c_s or k[1] == c_s]
    for key in keys_s:
        c_v = key[0] if key[1] == c_s else key[1]
        d_sv = distances[key]
        # delete the item of the pair of cluster s and another (v)
        del distances[key]
        # delete the item of the pair of clusters that contains cluster t and v
        if (c_t, c_v) in distances:
            d_tv = distances[c_t, c_v]
            del distances[c_t, c_v]
        else:
            d_tv = distances[c_v, c_t]
            del distances[c_v, c_t]
        # make sure key for new pair of clusters has the smallest cluster first
        new_pair = (c_st, c_v) if c_st[0] < c_v[0] else (c_v, c_st)
        # insert new pair (st and v) with their lance williams distance in the dictionary
        distances[new_pair] = calculate_distance(d_sv, d_tv, d_st, len(c_s), len(c_t), len(c_v))

def calculate_distance(d_sv, d_tv, d_st, s, t, v):
    if args.method == "single":
        coef = [0.5, 0.5, 0, -0.5]
    elif args.method == "complete":
        coef = [0.5, 0.5, 0, 0.5]
    elif args.method == "average":
        coef = [s / (s + t), t / (s + t), 0, 0]
    else:
        coef = [(s + v) / (s + v + t), (t + v) / (s + v + t), -v / (s + v + t), 0]
    return coef[0] * d_sv + coef[1] * d_tv + coef[2] * d_st + coef[3] * abs(d_sv - d_tv)

parser = argparse.ArgumentParser()
parser.add_argument("method", help = "the clustering method", 
                    choices = ["single", "complete", "average", "ward"])
parser.add_argument("input_filename", help = "the name of the input file")
args = parser.parse_args()

values = read_input_file(args.input_filename)
values.sort()
distances = create_distance_dict()
# while there are still pairs of clusters (more than 1 cluster)
while len(distances) > 0:
    min_dist_pair, min_dist = extract_min_distance()
    s, t = min_dist_pair
    print(f"({' '.join(str(x) for x in s)}) ({' '.join(str(x) for x in t)}) "
          f"{min_dist:.2f} {len(s + t)}")
    update_distance_dict(s, t, min_dist)
