# import numpy as np
#
# from state import next_state, solved_state
# from location import next_location
# from collections import OrderedDict
# from enum import Enum
#
# limit = 1
#
#
# class State(Enum):
#     SUCCESSFUL = 0
#     UNSUCCESSFUL = -1
#     GOAL = 1
#
#
# class Node:
#     def __init__(self, state: np.ndarray, ancestor_state: str, tier: int, action: int):
#         self.state = state
#         self.hashable_state = str(state.flatten())
#         self.ancestor = ancestor_state
#         self.tier = tier
#         self.action = action
#
#
# def successors_add_to_fringe(current_node: Node, fringe: OrderedDict, explored_states: set):
#     if current_node.hashable_state in explored_states:
#         return State.UNSUCCESSFUL
#     explored_states.add(current_node.hashable_state)
#
#     values = []
#     for i in range(1, 13):
#         n_s = next_state(current_node.state, i)
#         if str(n_s.flatten()) not in explored_states:
#             values.append(
#                 Node(state=n_s, ancestor_state=current_node.hashable_state, tier=current_node.tier + 1, action=i))
#     fringe[current_node.hashable_state] = values
#     return State.SUCCESSFUL
#
#
# def check_goal(node: Node):
#     if node.hashable_state == str(solved_state()):
#         return State.GOAL
#     else:
#         return State.SUCCESSFUL
#
#
# def remove_from_fringe(current_node: Node, fringe: OrderedDict, explored_states: set, path: list):
#     path.append(current_node.action)
#     if fringe[current_node.ancestor] != []:
#         fringe[current_node.ancestor].pop(0)
#     if check_goal(current_node) == State.GOAL:
#         return State.GOAL, current_node
#     else:
#         return State.SUCCESSFUL, current_node
#
#
# def solve(init_state, init_location, method):
#     global limit
#     """
#     Solves the given Rubik's cube using the selected search algorithm.
#
#     Args:
#         init_state (numpy.array): Initial state of the Rubik's cube.
#         init_location (numpy.array): Initial location of the little cubes.
#         method (str): Name of the search algorithm.
#
#     Returns:
#         list: The sequence of actions needed to solve the Rubik's cube.
#     """
#
#     # instructions and hints:
#     # 1. use 'solved_state()' to obtain the goal state.
#     # 2. use 'next_state()' to obtain the next state when taking an action .
#     # 3. use 'next_location()' to obtain the next location of the little cubes when taking an action.
#     # 4. you can use 'Set', 'Dictionary', 'OrderedDict', and 'heapq' as efficient data structures.
#
#     if method == 'Random':
#         return list(np.random.randint(1, 12 + 1, 10))
#
#     elif method == 'IDS-DFS':
#         explored_states = set()
#         fringe = OrderedDict()
#         path = []
#         # count = 0  ############################33
#         init_node = Node(init_state, ancestor_state=str(init_state.flatten()), tier=0, action=0)
#         current_node = init_node
#         # print(init_node.hashable_state)
#         fringe[str(init_state.flatten())] = [current_node]
#         while True:
#             print(fringe)
#             tmp = current_node.hashable_state  #################################3
#             func_state, current_node = remove_from_fringe(current_node, fringe, explored_states, path)
#             if func_state == State.GOAL:
#                 if current_node.state == solved_state():
#                     path.pop(0)
#                 return path
#             elif func_state != State.GOAL:
#                 if current_node.tier < limit:
#                     successors_add_to_fringe(current_node, fringe, explored_states)
#                     if fringe[current_node.hashable_state] != []:
#                         current_node = fringe[current_node.hashable_state][0]
#                     else:
#                         path.pop(0)
#                         return path
#                 else:
#                     if current_node.action <= 6:
#                         path.append(current_node.action + 6)
#                     else:
#                         path.append(current_node.action - 6)
#                     if fringe[current_node.ancestor] != []:
#                         current_node = fringe[current_node.ancestor][0]
#
#                     while fringe[current_node.ancestor] == []:
#                         if current_node.ancestor == str(init_state.flatten()):
#                             limit += 1
#                             explored_states = set()
#                             fringe = OrderedDict()
#                             path = []
#                             init_node = Node(init_state, ancestor_state=str(init_state.flatten()),
#                                              tier=0, action=0)
#                             current_node = init_node
#                             fringe[str(init_state.flatten())] = [current_node]
#                             break
#                         if current_node.action <= 6:
#                             path.append(current_node.action + 6)
#                         else:
#                             path.append(current_node.action - 6)
#                         fringe_keys = list(fringe.keys())
#                         index = fringe_keys.index(current_node.ancestor)
#                         del fringe[current_node.ancestor]
#                         next_key = fringe_keys[index - 1]
#                         # print(next_key)
#                         if fringe[next_key] != []:
#                             current_node = fringe[next_key][0]
#                         else:
#                             path.pop(0)
#                             return path
#             # count += 1  #############################
#             if tmp == current_node.hashable_state:
#                 path.pop(0)
#                 return path
#             # if count == 927:
#             #     print(fringe)
#             #     print(current_node)
#
#     elif method == 'A*':
#         ...
#
#     elif method == 'BiBFS':
#         ...
#
#     else:
#         return []
# from collections import OrderedDict
#
# a = OrderedDict()
# a[0] = [1, 2, 3]
# a[1] = [4, 5, 6]
#
# print(a)
# key, value = a.popitem()
# print(key)
# print(value)
import algo
import location
a = location.next_location(location.solved_location(), 4)
algo.heuristic(a)