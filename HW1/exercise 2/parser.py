from dataclasses import dataclass
from bs4 import BeautifulSoup
import random
import networkx as nx
import matplotlib.pyplot as plt

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
        file.write('#Graph Properties\n\ndirected\tfalse\nweighted\tfalse\n\n\n#List of Nodes, with their Locations and their Edges\n\n')
        for professor in graph:
            file.write(f"{professor.index}\t")
            file.write(f'@{random.randint(0, 1000)},{random.randint(0, 1000)}\t')
            
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
            for inner_span in outer_span.find_all('span'):
                try:
                    if inner_span['class'] == ['this-person']:
                        collaboration.append(inner_span.contents[0])
                except:
                    pass
            for link in outer_span.find_all('a'):
                for inner_span in link.find_all('span'):
                    try:
                        collaboration.append(inner_span['title'])
                    except:
                        pass
                if collaboration:
                    collaborators.append(collaboration)
    
    return collaborators




def get_professor_index_by_name(name):
    for professor in graph:
        if professor.name != name:
            continue
        return professor.index
    return -1


def helper_graph_node_builder(collaborators):
    graph = []
    index = 0
    for collaboration in collaborators:
        for professor in collaboration:
            member = Professor(index, professor, [])
            if member not in graph:
                graph.append(member)
                index = index + 1
    return graph


def helper_graph_edge_builder(graph, collaborators):
    for collaboration in collaborators:
        for professor_outer in collaboration:
            for professor_inner in collaboration:
                if professor_outer != professor_inner:
                    inner_professor_index = get_professor_index_by_name(professor_inner)
                    member = Professor(inner_professor_index, professor_inner, [])
                    
                    if member not in graph[get_professor_index_by_name(professor_outer)].collaborators:
                        graph[get_professor_index_by_name(professor_outer)].collaborators.append(member)


def graph_builder(graph):
    GRAPH = nx.Graph()

    for professor in graph:
        for collaborator in professor.collaborators:
            GRAPH.add_edge(professor.index, collaborator.index)
    
    return GRAPH


def solution(GRAPH, graph):
    lcc_dictionary = nx.clustering(GRAPH)
    for professor in graph:
        print(f'\033[37mLocal Clustering Coefficient of \033[1m[{professor.index}] {professor.name} is {lcc_dictionary[professor.index]} \033[00m')

    print(f"\033[96mAverage Clustering Coefficient: {nx.average_clustering(GRAPH)}\033[00m")
    print(f"\033[91mCharacteristic Shortest Path (Hops): {nx.average_shortest_path_length(GRAPH)}\033[00m")

def visual_representation(GRAPH, graph):
    position = {}

    for professor in graph:
        position[professor.index] = (random.randint(-1000000, 1000000), random.randint(-1000000, 1000000))

    options = {
        "font_size": 10,
        "node_size": 400,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 1,
        "width": 1,
    }

    nx.draw_networkx(GRAPH, position, **options)

    # Set margins for the axes so that nodes aren't clipped
    ax = plt.gca()
    #ax.margins(0.20)
    plt.axis("off")
    plt.show()



if __name__ == '__main__':
    # Parse Dataset
    collaborators = parse_dataset()

    # (Temporary) Create a Template Graph with the Collaborators as Nodes
    graph = helper_graph_node_builder(collaborators)

    # Add Edges the Template Graph 
    helper_graph_edge_builder(graph, collaborators)

    # Graph for Computations
    GRAPH = graph_builder(graph)

    # Show Solution
    solution(GRAPH, graph)

    # Export as ".cnt" Format
    write_to_cnt_file(graph)

    # Visually Display Graph
    visual_representation(GRAPH, graph)

