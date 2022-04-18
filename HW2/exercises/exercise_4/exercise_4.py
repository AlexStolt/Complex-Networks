from dataclasses import dataclass
from bs4 import BeautifulSoup
import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import csv
from ast import literal_eval as make_tuple

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
                    inner_professor_index = get_professor_index_by_name(
                        professor_inner)
                    member = Professor(inner_professor_index,
                                       professor_inner, [])

                    if member not in graph[get_professor_index_by_name(professor_outer)].collaborators:
                        graph[get_professor_index_by_name(
                            professor_outer)].collaborators.append(member)


def graph_builder(graph):
    nx_graph = nx.Graph()

    for professor in graph:
        for collaborator in professor.collaborators:
            nx_graph.add_edge(professor.index, collaborator.index)
    return nx_graph


def visual_representation(nx_graph):
    position = nx.spring_layout(nx_graph, seed=225)
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


def nearest_neighbor_edge_centrality(nx_graph):
    edges = []
    centralities = []
    for edge in nx_graph.edges:
        # DC of Nodes
        node_a, node_b = edge
        dc_a = nx_graph.degree(node_a)
        dc_b = nx_graph.degree(node_b)
        
        # Calculate Nearest Neighbor Edge Centrality
        nne_centrality = (dc_a + dc_b - 2) / (abs(dc_a - dc_b) + 1)
        
        edges.append(str(edge))
        centralities.append(nne_centrality)
        print(f'Nearest Neighbor Edge Centrality for Edge {edge} is {nne_centrality}')
    return edges, centralities


def plot_as_chart(edges, centralities):
    fig = plt.figure(figsize = (10, 5))
    plt.bar(edges, centralities, color ='black', width = 0.6)
    plt.xticks(rotation='vertical')
    plt.xlabel("Edge")
    plt.ylabel("Nearest-Neighbor Edge Centrality")
    plt.title("Nearest-Neighbor Edge Centrality Computation")
    plt.show()

def write_to_csv(edges, centralities):
    with open('nearest_neighbor_edge_centrality.csv', 'w+', encoding='UTF8') as file:    
        writer = csv.writer(file)   
        for i in range(len(edges)):
            writer.writerow([make_tuple(edges[i]), centralities[i]])


if __name__ == '__main__':
    # Parse Dataset
    collaborators = parse_dataset()

    # (Temporary) Create a Template Graph with the Collaborators as Nodes
    graph = helper_graph_node_builder(collaborators)

    # Add Edges the Template Graph
    helper_graph_edge_builder(graph, collaborators)

    # Graph for Computations
    nx_graph = graph_builder(graph)

    # Show Nearest Neighbor Edge Centrality for each Edge
    edges, centralities = nearest_neighbor_edge_centrality(nx_graph)

    # Export as ".cnt" Format
    write_to_cnt_file(graph)

    # Plot a Bar Chart
    plot_as_chart(edges, centralities)

    # write_to_csv(edges, centralities)

    # Visually Display Graph
    visual_representation(nx_graph)
