import random

K_Directed = ""
K_Undirected = ""
edge = []

MIN_NUM = 0
MAX_NUM = 122

FILE = "Undirected" # Undirected / Directed
NOISE_RATE = 1.0

with open(f"K_{FILE}_ori.txt", "r") as f:
    for i in f.readlines():
        i = i.replace('\n', '').split('\t')
        src = i[0]
        tar = i[1]
        edge.append((src, tar))
visit = []
undirected_cnt = 0
directed_cnt = 0

node_list = [str(i) for i in range(MIN_NUM, MAX_NUM + 1)]
# noise edge 추가
if NOISE_RATE != 0:
    noise_edge_cnt = int(len(edge) * NOISE_RATE)
    print(f"random edge 수: {noise_edge_cnt} / {len(edge)}")
    random.shuffle(edge)
    edge = edge[:-noise_edge_cnt]
    for i in range(noise_edge_cnt):
        new_edge = random.choices(node_list, k=2)
        edge.append((new_edge[0], new_edge[1]))

new_edges = []
for e in edge:
    if e not in visit:
        if FILE == "Undirected":
            K_Undirected += str(e[0] + '\t' + e[1] + '\n')
            visit.append(e)
            undirected_cnt += 1
        else:
            K_Directed += str(e[0] + '\t' + e[1] + '\n')
            visit.append(e)
            directed_cnt += 1
    else:
        while True:
            new_edge = random.choices(node_list, k=2)
            if (new_edge[0], new_edge[1]) not in edge:
                new_edges.append((new_edge[0], new_edge[1]))
                break

for e in new_edges:
    if e not in visit:
        if FILE == "Undirected":
            K_Undirected += str(e[0] + '\t' + e[1] + '\n')
            visit.append(e)
            undirected_cnt += 1
        else:
            K_Directed += str(e[0] + '\t' + e[1] + '\n')
            visit.append(e)
            directed_cnt += 1

if NOISE_RATE != 0:
    with open(f"K_Directed_noise_{NOISE_RATE}.txt", "w") as f:
        f.write(K_Directed)
    with open(f"K_Undirected_noise_{NOISE_RATE}.txt", "w") as f:
        f.write(K_Undirected)
else:
    with open("K_Directed.txt", "w") as f:
        f.write(K_Directed)
    with open("K_Undirected.txt", "w") as f:
        f.write(K_Undirected)
all = len(visit)
print(all)

print(f"Undirected: {undirected_cnt}, Dicrected: {directed_cnt}")
