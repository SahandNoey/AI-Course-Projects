import heapq
import numpy as np
from state import next_state, solved_state
from location import next_location, solved_location


def solve(init_state, init_location, method):
    """
    Solves the given Rubik's cube using the selected search algorithm.

    Args:
        init_state (numpy.array): Initial state of the Rubik's cube.
        init_location (numpy.array): Initial location of the little cubes.
        method (str): Name of the search algorithm.

    Returns:
        list: The sequence of actions needed to solve the Rubik's cube.
    """

    # instructions and hints:
    # 1. use 'solved_state()' to obtain the goal state.
    # 2. use 'next_state()' to obtain the next state when taking an action .
    # 3. use 'next_location()' to obtain the next location of the little cubes when taking an action.
    # 4. you can use 'Set', 'Dictionary', 'OrderedDict', and 'heapq' as efficient data structures.

    if method == "Random":
        return list(np.random.randint(1, 12 + 1, 10))

    elif method == "IDS-DFS":
        depth, explored, expanded, actions = id_dfs(init_state, 14)  # 14 is God's number
        print(f"explored = {explored}\nexpanded = {expanded}\ndepth = {depth}\nactions = {actions}")
        return actions

    elif method == "A*":
        depth, explored, expanded, actions = a_star(init_state, init_location)
        print(f"explored = {explored}\nexpanded = {expanded}\ndepth = {depth}\nactions = {actions}")
        return actions

    elif method == "BiBFS":
        depth, explored, expanded, actions = bi_bfs(init_state)
        print(f"explored = {explored}\nexpanded = {expanded}\ndepth = {depth}\nactions = {actions}")
        return actions
    else:
        return []


def id_dfs(initial_state, max_depth):
    goal_state = solved_state()
    explored = 0
    expanded = 0
    for depth in range(max_depth + 1):
        stack_dict = dict()
        actions = []
        stack_dict[0] = [initial_state, actions]
        explored_set = set()
        explored_set.add(initial_state.tobytes())
        while len(stack_dict) != 0:
            key, value = stack_dict.popitem()
            current_state = value[0]
            current_actions = value[1]
            explored += 1
            if (current_state == goal_state).all():
                return depth, explored, expanded, current_actions
            else:
                explored_set.add(current_state.tobytes())

            if len(current_actions) < depth:
                for action in range(1, 13):
                    new_state = next_state(current_state, action)
                    if new_state.tobytes() not in explored_set:
                        new_actions = current_actions.copy()
                        new_actions.append(action)
                        stack_dict[expanded + 1] = [new_state, new_actions]
                        expanded += 1
        print(f"depth = {depth}, explored = {explored}")


def heuristic(location):
    goal_state = solved_location()
    sum_dif = 0
    for cube in range(1, 9):
        current_cube = np.array(np.where(location == cube))
        goal_cube = np.array(np.where(goal_state == cube))
        difference = abs(current_cube - goal_cube)
        sum_dif += np.sum(difference)

    return sum_dif / 4


def a_star(init_state, init_location):
    goal_state = solved_state()
    explored = 0
    expanded = 0
    priority_queue = []
    init_actions = []
    init_state_hash = init_state.tobytes()
    explored_nodes = set()
    costs = dict()
    costs[init_state_hash] = 0
    heuristics = dict()
    frontier_count = 0
    priority_queue.append((0.0, frontier_count, init_location, init_state, init_actions))

    while len(priority_queue) != 0:
        # print(f"priority queue = {priority_queue[0]}")
        # print(f"heuristics = {heuristics}")
        current = heapq.heappop(priority_queue)
        current_location = current[2]
        current_state = current[3]
        current_state_hash = current_state.tobytes()
        current_actions = current[4]
        if current_state_hash in explored_nodes:
            continue

        explored_nodes.add(current_state_hash)
        explored += 1
        if (current_state == goal_state).all():
            return len(current_actions), explored, expanded, current_actions

        for action in range(1, 13):
            new_state = next_state(current_state, action)
            new_state_hash = new_state.tobytes()
            new_location = next_location(current_location, action)
            new_location_hash = new_location.tobytes()
            new_actions = current_actions.copy()
            new_actions.append(action)

            if heuristics.get(new_location_hash) is not None:
                heu = heuristics[new_location_hash]
            else:
                heu = heuristic(new_location)
                heuristics[new_location_hash] = heu

            new_state_cost = len(new_actions) + heu
            priority = new_state_cost

            if costs.get(new_state_hash) is not None:
                if new_state_cost < costs[new_state_hash]:
                    frontier_count += 1
                    heapq.heappush(priority_queue, (priority, frontier_count, new_location, new_state, new_actions))
                    costs[new_state_hash] = new_state_cost
            else:
                frontier_count += 1
                heapq.heappush(priority_queue, (priority, frontier_count, new_location, new_state, new_actions))
                costs[new_state_hash] = new_state_cost
                expanded += 1


def bi_bfs(init_state):
    goal_state = solved_state()
    expanded = 0
    explored = 0
    forward_queue = []
    backward_queue = []
    forward_visited = set()
    backward_visited = set()
    forward_actions = dict()
    backward_actions = dict()
    forward_queue.append([init_state, []])
    backward_queue.append([goal_state, []])
    turn = 0
    while len(forward_queue) > 0 and len(backward_queue) > 0:
        if (turn % 2) == 0:
            current = forward_queue.pop(0)
            current_state = current[0]
            current_actions = current[1]
            current_state_hash = current_state.tobytes()
            if current_state_hash not in forward_visited:
                explored += 1
                forward_visited.add(current_state_hash)
                for action in range(1, 13):
                    expanded += 1
                    new_state = next_state(current_state, action)
                    current_state_hash = new_state.tobytes()
                    if current_state_hash in backward_visited:
                        current_backward_actions = backward_actions[current_state_hash]
                        back_translated = []
                        for b_action in current_backward_actions[::-1]:
                            if b_action <= 6:
                                back_translated.append(b_action + 6)
                            else:
                                back_translated.append(b_action - 6)
                        total_actions = current_actions + [action] + back_translated
                        return len(total_actions), explored, expanded, total_actions
                    else:
                        forward_actions[current_state_hash] = current_actions + [action]
                        forward_queue.append([new_state, current_actions + [action]])
        else:
            current = backward_queue.pop(0)
            current_state = current[0]
            current_actions = current[1]
            current_state_hash = current_state.tobytes()
            if current_state_hash not in backward_visited:
                explored += 1
                backward_visited.add(current_state_hash)
                for action in range(1, 13):
                    expanded += 1
                    new_state = next_state(current_state, action)
                    current_state_hash = new_state.tobytes()
                    if current_state_hash in forward_visited:
                        current_forward_actions = forward_actions[current_state_hash]
                        back_translated = []
                        for b_action in current_actions[::-1]:
                            if b_action <= 6:
                                back_translated.append(b_action + 6)
                            else:
                                back_translated.append(b_action - 6)
                        if action > 6:
                            action -= 6
                        else:
                            action += 6
                        total_actions = current_forward_actions + [action] + back_translated
                        return len(total_actions), explored, expanded, total_actions
                    else:
                        backward_actions[current_state_hash] = current_actions + [action]
                        backward_queue.append([new_state, current_actions + [action]])
        turn += 1
