#!/usr/bin/env python3
import argparse
import random
from string import ascii_letters


RAND_SEED = 'someSeed'
COUNT_RANDOM_NODES = 4
START_NODE = 0


def parse_args():
    "Setup argparse"
    parser = argparse.ArgumentParser(
        description='Gossip protocol simulation')
    parser.add_argument(
        '-n', dest='node_count', help='number of nodes')
    parser.add_argument(
        '-i', dest='exec_count', help='number of executions')
    parser.add_argument(
        '-s', dest='rand_seed', default=RAND_SEED, help='random seed')
    parser.add_argument(
        '-c', dest='count_random_nodes',
        default=COUNT_RANDOM_NODES, help='count of random nodes to propagate')
    parser.add_argument(
        '--ignore-sender', nargs='?', const=True,
        help='more effective algorithm')
    args = parser.parse_args()

    if args.node_count is None or args.exec_count is None:
        print(f'\nNODE_COUNT or EXEC_COUNT undefined\nusage: \
            {__file__} [-h] [-n NODE_COUNT] [-i EXEC_COUNT]\n')
        raise SystemExit

    return args


class Node:
    def __init__(self, name, status=None):
        self.name = name
        self.status = status or 'Created'

    def __repr__(self):
        return f"Node(name='{self.name}', status='{self.status})'"


def create_node_list(count):
    node_list = [
        Node(
            name=''.join(random.choices(ascii_letters, k=4))
        )
        for i in range(count)
    ]
    return node_list


def get_node_positions(length, pivot, count, r, prev=None):
    node_positions = set()
    while len(node_positions) < count:
        node_positions.add(r.randint(0, length-1))
        node_positions -= {pivot, prev}
    return node_positions


def broadcast_gen(node_list, node_position, node_count, status, r, prev=None):
    node = node_list[node_position]
    yield
    if node.status != status:
        node.status = status
        next_node_positions = get_node_positions(len(node_list),
                                                 node_position,
                                                 node_count,
                                                 r,
                                                 prev)
        for n in next_node_positions:
            prev = prev if prev is None else node_position
            yield from broadcast_gen(node_list, n, node_count, status, r, prev)


def main():
    args = parse_args()
    node_count = int(args.node_count)
    exec_count = int(args.exec_count)
    rand_seed = args.rand_seed
    count_random_nodes = int(args.count_random_nodes)
    ignore_sender = bool(args.ignore_sender)

    prev = START_NODE if ignore_sender else None

    node_list = create_node_list(node_count)
    complete_count = 0
    completed_iters_list = []
    uncompleted_iters_list = []

    for i in range(exec_count):
        iterations = 0
        new_status = f'Ok_{i}'

        r = random.Random()
        r.seed(f'{rand_seed}{i}')

        gossip_gen = broadcast_gen(
            node_list, START_NODE, count_random_nodes, new_status, r, prev)

        for _ in gossip_gen:
            iterations += 1
        unique_statuses = {n.status for n in node_list}
        if len(unique_statuses) == 1:
            complete_count += 1
            completed_iters_list.append(iterations)
        else:
            uncompleted_iters_list.append(iterations)

    success_rate = complete_count*100/exec_count
    avg_iters_complited = sum(completed_iters_list)/complete_count
    avg_iters_uncomplited = (
        sum(uncompleted_iters_list)/(exec_count-complete_count)
    )

    print(f'In {success_rate}% cases all nodes received the packet')
    print(f'Average iterations for complited cases: {avg_iters_complited}')
    print(f'Average iterations for uncomplited cases: {avg_iters_uncomplited}')


if __name__ == '__main__':
    main()
