from dataclasses import dataclass
from bs4 import BeautifulSoup
import random
import networkx as nx
import matplotlib.pyplot as plt
import csv
import networkx as nx
import copy
import sys
from networkx.algorithms.community import greedy_modularity_communities


FILE_PATH = 'dataset.html'
OUTPUT_FILE = 'output.txt'


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


  def modularity_communities(self):
    return greedy_modularity_communities(self.networkx_graph)

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
  graph = Graph(FILE_PATH)
  communities = graph.modularity_communities()  
  for community in communities:
    print(sorted(community))
  