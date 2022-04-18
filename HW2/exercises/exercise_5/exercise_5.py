from dataclasses import dataclass
from bs4 import BeautifulSoup
import random
import networkx as nx
import matplotlib.pyplot as plt
import csv


FILE_PATH = 'dataset.html'
OUTPUT_FILE = 'output.cnt'


@dataclass
class Professor:
    index: int
    name: str
    collaborators: list

    def __eq__(self, other):
        return self.name == other.name


def write_to_cnt_file(graph):
    with open(OUTPUT_FILE, 'w') as file:
        file.write(
            '#Graph Properties\n\ndirected\tfalse\nweighted\tfalse\n\n\n#List of Nodes, with their Locations and their Edges\n\n')
        for professor in graph:
            file.write(f"{professor.index}\t")
            file.write(
                f'@{random.randint(0, 1000)},{random.randint(0, 1000)}\t')

            for collaborator in professor.collaborators:
                file.write(f"{collaborator.index}\t")
            file.write('\n')


def parse_dataset():
    with open(FILE_PATH, 'r') as file:
        content = file.read()

        data = BeautifulSoup(content, 'html.parser')
        collaborators = []
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
            collaborators.append(collaboration)
    return collaborators




def visual_representation(nx_graph):
    # position = nx.spring_layout(nx_graph, seed=1)
    position = nx.spring_layout(nx_graph, k=2, iterations=40)
    options = {
        "font_size": 10,
        "node_size": 400,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 1,
        "width": 1,
    }
    nx.draw_networkx(nx_graph, position, **options)

    # Set margins for the axes so that nodes aren't clipped
    ax = plt.gca()
    plt.axis("off")
    plt.show()



def get_collaborators_name(collaborations):
    collaborators = []
    for collaboration in collaborations:
        for collaborator in collaboration:
            if collaborator not in collaborators:
                collaborators.append(collaborator)
    return collaborators


def graph_node_builder(nx_graph, collaborators):
    hash_table = {}
    for i in range(len(collaborators)):
        hash_table[collaborators[i]] = i
        nx_graph.add_node(i)
    return hash_table


def graph_edge_builder(nx_graph, hash_table, collaborations):
    # print(hash_table)
    for collaboration in collaborations:
        for i in range(len(collaboration)):
            for j in range(i + 1, len(collaboration)):
                # print(i, j)
                nx_graph.add_edge(hash_table[collaboration[i]], hash_table[collaboration[j]])
    # print(nx_graph)

def plot_as_chart(professor_names, page_ranks):
  fig = plt.figure(figsize = (10, 5))
  
  plt.bar(professor_names, page_ranks, color ='black', width = 0.6)
  plt.xticks(rotation='vertical')
  plt.xlabel("Professor")
  plt.ylabel("Page Rank")
  plt.title("Page Ranks")
  plt.show()



if __name__ == '__main__':
    # Parse Dataset
    collaborations = parse_dataset()
    
    collaborators = get_collaborators_name(collaborations)
    
    nx_graph = nx.DiGraph()

    # (Temporary) Create a Template Graph with the Collaborators as Nodes
    hash_table = graph_node_builder(nx_graph, collaborators)
    
    
    graph_edge_builder(nx_graph, hash_table, collaborations)
    page_ranks = nx.pagerank(nx_graph)
    professor_names = list(hash_table.keys())
    with open('page_ranks.csv', 'w+', encoding='UTF8') as file:  
        writer = csv.writer(file)   
        for collaborator in page_ranks:
            print(f'Page Rank of \033[92m{professor_names[collaborator]}\033[00m is \033[92m{page_ranks[collaborator]}\033[00m')
            writer.writerow([professor_names[collaborator], page_ranks[collaborator]])
            
    visual_representation(nx_graph)
    plot_as_chart(professor_names, list(page_ranks.values()))
