import torch
import torch.nn as nn
import torch.nn.functional as F
from build_graph import get_option_matrix


class GraphLayer(nn.Module):
    def __init__(self, g, in_dim, out_dim):
        super(GraphLayer, self).__init__()
        self.g = g
        self.fc = nn.Linear(in_dim, out_dim, bias=False)
        self.attn_fc = nn.Linear(2 * out_dim, 1, bias=False)

    def edge_attention(self, edges):
        z2 = torch.cat([edges.src['z'], edges.dst['z']], dim=1)
        a = self.attn_fc(z2)
        return {'e': a}

    def message_func(self, edges):
        return {'z': edges.src['z'], 'e': edges.data['e']}

    def reduce_func(self, nodes):
        alpha = F.softmax(nodes.mailbox['e'], dim=1)
        h = torch.sum(alpha * nodes.mailbox['z'], dim=1)
        return {'h': h}

    def forward(self, h):
        z = self.fc(h)
        self.g.ndata['z'] = z
        self.g.apply_edges(self.edge_attention)
        self.g.update_all(self.message_func, self.reduce_func)
        return self.g.ndata.pop('h')


class GraphLayerEdge(nn.Module):
    def __init__(self, args, g, in_dim, out_dim):
        super(GraphLayerEdge, self).__init__()
        self.args = args
        self.device = torch.device(('cuda:%d' % (args.gpu)) if torch.cuda.is_available() else 'cpu')
        self.g = g
        self.fc = nn.Linear(in_dim, out_dim, bias=False)
        self.attn_fc = nn.Linear(2 * out_dim, 1, bias=False)
        if self.args.edge_type == 0:
            self.edge_fc = nn.Linear(2 * out_dim, out_dim, bias=False)
        elif self.args.edge_type == 1:
            self.edge_fc = nn.Linear(2 * out_dim + args.option_n, out_dim, bias=False)
            self.option_matrix = get_option_matrix(args.student_n, args.exer_n, args.dir).to(self.device)
        else:
            # self.edge_fc = nn.Linear(out_dim, out_dim, bias=False)
            self.option_matrix = get_option_matrix(args.student_n, args.exer_n, args.dir).to(self.device)
            self.option_emb = nn.Embedding(args.exer_n * args.option_n, out_dim)

    def edge_attention(self, edges):
        # alpha ????????? (edge attention)
        z2 = torch.cat([edges.src['z'], edges.dst['z']], dim=1)
        a = self.attn_fc(z2) # [77328, 148]

        # edge embedding ??????
        # ?????? X
        if self.args.edge_type == 0:
            z3 = torch.cat([edges.src['z'], edges.dst['z']], dim=1)
            edge_emb = self.edge_fc(z3)
        # one-hot??? concat
        elif self.args.edge_type == 1:
            options = self.option_matrix[(edges.src['num'], edges.dst['num'])]
            options = F.one_hot(options.flatten(), num_classes=self.args.option_n)
            z3 = torch.cat([edges.src['z'], edges.dst['z'], options], dim=1)
            edge_emb = self.edge_fc(z3)
        # option embedding ??????
        else:
            options = self.option_matrix[(edges.src['num'], edges.dst['num'])]
            edge_emb = self.option_emb((edges.dst['num'] * self.args.option_n + options).flatten())

        # alpha: ?????? RCD??? attention ???, e: edge_embedding ???
        return {'alpha': a, 'e': edge_emb}

    def message_func(self, edges):
        # print(f"message func: z ({len(edges.src['z'])}, {len(edges.src['z'][0])})")
        # print(f"message func: e ({len(edges.data['e'])}, {len(edges.data['e'][0])})")
        # print(edges.src['z'].shape, edges.data['e'].shape, edges.data['alpha'].shape)
        return {'z': edges.src['z'], 'e': edges.data['e'], 'alpha': edges.data['alpha']}

    def reduce_func(self, nodes):
        alpha = F.softmax(nodes.mailbox['alpha'], dim=1)
        h1 = torch.sum(alpha * nodes.mailbox['z'], dim=1)
        # edge embedding ??????
        h2 = torch.sum(nodes.mailbox['e'], dim=1)
        h = h1 + h2
        return {'h': h}

    def forward(self, h):
        # DGL ?????????????????? heterograph??? ?????????????????????, ?????????????????? ?????? ????????? ?????? ??????
        # print(h.shape) # [1138, 148] ??????, ??????(knowledge ???)
        # print(h.requires_grad) # True
        z = self.fc(h)
        self.g.ndata['z'] = z
        # print(self.in_dim, self.out_dim) # [148, 148]
        self.g.ndata['num'] = torch.tensor(range(h.shape[0])).reshape(-1, 1).to(self.device)
        self.g.apply_edges(self.edge_attention)
        # Message Passing, Aggregation
        self.g.update_all(self.message_func, self.reduce_func)
        # edge embedding ??? ?????? X, model.py ???????????? ??? ?????? ???????
        # print(self.g.edata.pop('e').shape) # [77328, 148]
        return self.g.ndata.pop('h')