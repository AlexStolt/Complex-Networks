import networkx as nx
import scipy
import matplotlib.pyplot as plt

def plot_as_chart(results):
  fig = plt.figure(figsize = (10, 5))
  
  for result in results:
    plt.title(f"Damping Factor {result['damping_factor']}")
    plt.xlabel("Node")
    plt.ylabel("Page Rank")
    # plt.xticks(rotation='vertical')
    edges = [str(item) for item in list(result['values'].keys())]
    page_ranks = list(result['values'].values())
    plt.bar(edges, page_ranks, color ='black', width = 0.6)
    plt.show()



if __name__ == '__main__':

  graph = nx.DiGraph()

  nodes = list(range(1, 6))

  edges = [
    (1, 1),
    (1, 2),
    (2, 3),
    (3, 2),
    (3, 1),
    (3, 4),
    (4, 3),
    (4, 5),
    (5, 4)
  ]


  # Add nodes
  graph.add_nodes_from(nodes)
  
  # Add edges
  for edge in edges:
    graph.add_edge(*edge)

  # Calculate Page Rank
  result = []
  damping_factors = [0.1, 0.3, 0.5, 0.85]
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
  
  plot_as_chart(result)