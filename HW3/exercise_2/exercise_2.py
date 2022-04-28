from dataclasses import dataclass
from bs4 import BeautifulSoup
import random
import networkx as nx
import matplotlib.pyplot as plt
import csv
import networkx as nx
import copy
import sys


FILE_PATH = 'dataset.html'
OUTPUT_FILE = 'output.txt'

class Tree:
  total_nodes = 0
  def __init__(self, data):
    self.root = self.TreeNode(data)


  def insert(self, data):
    _current_node = self.root

    while True:
      # Left
      if _current_node.left:
        if all(x in _current_node.left.data for x in data):
          _current_node = _current_node.left
          continue
      # Right
      if _current_node.right:
        if all(x in _current_node.right.data for x in data):
          _current_node = _current_node.right
          continue
      break

    if not _current_node.left:
      _current_node.left = self.TreeNode(data)
    elif not _current_node.right:
      _current_node.right = self.TreeNode(data)
    
    self.total_nodes = self.total_nodes + 1

  
  def get_community(self, root, members):
    communities = []
    _current_node = root
    stack = []
    
    stack.append(_current_node)

    while(len(stack) > 0):   
      _current_node = stack.pop()

      # Store Data
      if len(_current_node.data) == members:
        communities.append(_current_node.data)
        
      if _current_node.right:
        stack.append(_current_node.right)
      if _current_node.left:
        stack.append(_current_node.left)

    return communities
  
  def preorder(self, source):
    if source:
      print(source.data)

      self.preorder(source=source.left)
      self.preorder(source=source.right)


  class TreeNode:
    data = None
    left = None
    right = None
    def __init__(self, data):
      self.data = data
      self.data.sort()


class Graph:
  collaborations = []
  collaborators = []
  adjacency_matrix = []
  networkx_graph = nx.Graph()


  def __init__(self, dataset_file_path):
    self.collaborations = self._parse_dataset(dataset_file_path)
    self.collaborators = self._set_unique_nodes()
    self.adjacency_matrix = [[0 for _ in range(len(self.collaborators))] for _ in range(len(self.collaborators))] 
    self._add_edges()
    self._networkx_graph_init()



  def girvan_newman(self, recaclulate_centralities=False):
    edge_betweenness_centrality = nx.edge_betweenness_centrality(self.networkx_graph) 
    
    tree = Tree(list(nx.dfs_preorder_nodes(self.networkx_graph)))
    while edge_betweenness_centrality:
      key = max(edge_betweenness_centrality, key=edge_betweenness_centrality.get)
      
      # Delete Edge from Graph
      self.networkx_graph.remove_edge(*key)

      # Check for Seperation of Communities
      if not nx.has_path(self.networkx_graph, *key):
        left = list(nx.dfs_preorder_nodes(self.networkx_graph, source=key[0]))
        tree.insert(left)
        
        right = list(nx.dfs_preorder_nodes(self.networkx_graph, source=key[1]))
        tree.insert(right)

      if recaclulate_centralities:
        edge_betweenness_centrality = nx.edge_betweenness_centrality(self.networkx_graph)
      else:
        del edge_betweenness_centrality[key]

    return tree

  # ********************* Private Methods ********************* #
  def _networkx_graph_init(self):
    # Add Nodes
    self.networkx_graph.add_nodes_from([node for node in range(len(self.adjacency_matrix))])

    for i in range(len(self.adjacency_matrix)):
      for j in range(len(self.adjacency_matrix[i])):
        if self.adjacency_matrix[i][j]:
          self.networkx_graph.add_edge(i, j)

  
  def _parse_dataset(self, file_path):
    with open(file_path, 'r') as file:
      content = file.read()

      data = BeautifulSoup(content, 'html.parser')
      collaborations = []
      for outer_span in data.find_all('cite'):
        collaboration = []
        for outer_span in outer_span.find_all('span'):
          for link in outer_span.find_all('a'):
            for inner_span in link:
              collaboration.append(inner_span.contents[0])
          for inner_span in outer_span.find_all('span'):
            try:
              if inner_span['class'] == ['this-person']:
                collaboration.append(inner_span.contents[0])
            except:
              pass
        collaborations.append(collaboration)
      return collaborations


  def _set_unique_nodes(self):
    for collaboration in self.collaborations:
      for collaborator in collaboration:
        if collaborator not in self.collaborators:
          self.collaborators.append(collaborator) 
      
    return self.collaborators


  def _add_edges(self):
    for collaboration in self.collaborations:
      for vertex in collaboration:
        for edge in collaboration:
          if vertex != edge:
            i = self.collaborators.index(vertex)
            j = self.collaborators.index(edge)
            self.adjacency_matrix[i][j] = 1



if __name__ == '__main__':

  try:
    members = int(sys.argv[1])
    graph = Graph(FILE_PATH)
    tree = graph.girvan_newman(False)
    communities = tree.get_community(tree.root, members)
    # tree.preorder(tree.root)
    print(communities)
    # graph.preorder(copy.copy(graph.root))
  except:
    print('python3 <EXECUTABLE> <MEMBERS>')
    
  
