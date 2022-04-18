import networkx as nx
import matplotlib.pyplot as plt

def plot_as_chart(edge_betweenness_centrality):
  fig = plt.figure(figsize = (10, 5))
  
  edges = [str(item) for item in list(edge_betweenness_centrality.keys())]
  page_ranks = list(edge_betweenness_centrality.values())
  print(edges, page_ranks)
  plt.bar(edges, page_ranks, color ='black', width = 0.6)
  plt.xticks(rotation='vertical')
  plt.xlabel("Edge")
  plt.ylabel("Edge Betweenness Centrality")
  plt.title("Edge Betweenness Centrality")
  plt.show()



if __name__ == '__main__':

  graph = nx.Graph()

  nodes = list(range(1, 6))

  edges = [
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 5),
    (3, 5),
    (3, 4),
    (4, 5)
  ]


  # Add nodes
  graph.add_nodes_from(nodes)
  
  # Add edges
  for edge in edges:
    graph.add_edge(*edge)

  # Print all shortest paths
  for node in nodes:
    for target in nodes:
      if node is not target:
        print(f'Shortest Paths from {node} to {target}: {[path for path in nx.all_shortest_paths(graph, node, target)]}')

  # Calculate edge betweenness centrality
  edge_betweenness_centrality = nx.edge_betweenness_centrality(graph)
  print(f'\033[92m{edge_betweenness_centrality}\033[00m')
  
  
  # Display Graph
  position =  nx.spring_layout(graph, seed=225)
  options = {
    "font_size": 10,
    "node_size": 400,
    "node_color": "white",
    "edgecolors": "black",
    "linewidths": 1,
    "width": 1,
  }
  nx.draw_networkx(graph, position, **options)
  plt.show()
  
  
  plot_as_chart(edge_betweenness_centrality)
