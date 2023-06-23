import numpy as np
import networkx as nx

def run_simulation(G, beta, gamma, max_iter=False):
    # Initialize influence and recovery attributes for each node
    num_infected = []
    num_recovered = []
    num_susceptible = []
    iter = 0

    # initially, no node has been processed or influenced anyone
    for node in G.nodes:
        G.nodes[node]['influence'] = 0
        G.nodes[node]['processed'] = 0
    
    # Perform the contagion simulation
    while True: 
        iter += 1
        # Select an infected node that has not yet recovered
        infected_nodes = [node for node, data in G.nodes(data=True) if data['status'] == 1]
        overall_susceptible = [node for node, data in G.nodes(data=True) if data['status'] == 0]
        recovered_nodes = [node for node, data in G.nodes(data=True) if data['status'] == 2]
        
        # add number of each node group for plotting
        num_infected.append(len(infected_nodes))
        num_susceptible.append(len(overall_susceptible))
        num_recovered.append(len(recovered_nodes))

        if not infected_nodes or (max_iter and max_iter < iter):  # if no more active infected nodes or max_iter reached
            break
        node = np.random.choice(infected_nodes)
        G.nodes[node]['processed'] = 1

        # List its susceptible neighbors
        susceptible_neighbors = [n for n in G.neighbors(node) if G.nodes[n]['status'] == 0]

        # Infect susceptible neighbors with probability beta
        for n in susceptible_neighbors:
            if np.random.random() <= beta:
                G.nodes[n]['status'] = 1  # Change to infected
                G.nodes[node]['influence'] += 1  # Increase influence of the infecting node

        # Recovery process for infected node with probability gamma
        if np.random.random() <= gamma:
            G.nodes[node]['status'] = 2  # Change to recovered
    
    return G, num_infected, num_susceptible, num_recovered, iter, beta, gamma

def run_simulation_wrapper(args):
    G, beta, gamma, max_iter = args
    return run_simulation(G, beta, gamma, max_iter)

def run_simulation_complex(G: nx.Graph, threshold, max_iter=False):
    # Initialize influence and recovery attributes for each node
    num_infected = []
    num_susceptible = []
    iter = 0
    inf0 = len([node for node, data in G.nodes(data=True) if data['status'] == 1])

    # initially, no node has influenced anyone
    for node in G.nodes:
        G.nodes[node]['influence'] = 0
    
    # Perform the complex contagion simulation
    while True:
        iter += 1
        # Select an infected node that has not yet recovered
        infected_nodes = [node for node, data in G.nodes(data=True) if data['status'] == 1]
        overall_susceptible = [node for node, data in G.nodes(data=True) if data['status'] == 0]

        # add number of each node group for plotting
        num_infected.append(len(infected_nodes))
        num_susceptible.append(len(overall_susceptible))

        if max_iter and iter > max_iter:
            break

        # Calculate the ratio of infected neighbors for each susceptible node
        can_be_infected = []
        for node in overall_susceptible:
            infected_neighbors = [n for n in G.neighbors(node) if G.nodes[n]['status'] == 1]
            all_neighbors = [n for n in G.neighbors(node)]
            ratio_inf_neighbors = len(infected_neighbors) / len(all_neighbors)
            if ratio_inf_neighbors > threshold:
                can_be_infected.append(node)
        
        # If there are no nodes that can be infected, break the loop
        if not can_be_infected:
            break

        for node in can_be_infected:
            G.nodes[node]['status'] = 1
            for n in G.neighbors(node):
                if G.nodes[n]['status'] == 1:
                    G.nodes[n]['influence'] += 1  # Increase influence of the infecting nodes
    
    return G, num_infected, num_susceptible, iter, threshold

def run_simulation_complex_wrapper(args):
    G, threshold, max_iter = args
    return run_simulation_complex(G, threshold, max_iter)