import networkx as nx
import scipy
import matplotlib.pyplot as plt

if __name__ == '__main__':

  graph = nx.DiGraph()

  nodes = list(range(1, 3))

  edges = [
    (1, 1),
    (1, 2),
  ]


  # Add nodes
  graph.add_nodes_from(nodes)
  
  # Add edges
  for edge in edges:
    graph.add_edge(*edge)

  # Calculate Page Rank
  result = []
  damping_factors = [1]
  for damping_factor in damping_factors:
    result.append({
      'damping_factor': damping_factor,
      'values': nx.pagerank(graph, alpha=damping_factor)
    })
    
    
  print(result)



  
  # Display Graph
  position =  nx.spring_layout(graph, seed=25)
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
  
  