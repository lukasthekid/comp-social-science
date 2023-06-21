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
        if max_iter == iter:
            break
        
        # Select an infected node that has not yet recovered
        infected_nodes = [node for node, data in G.nodes(data=True) if data['status'] == 1]
        overall_susceptible = [node for node, data in G.nodes(data=True) if data['status'] == 0]
        recovered_nodes = [node for node, data in G.nodes(data=True) if data['status'] == 2]
        
        # add number of each node group for plotting
        num_infected.append(len(infected_nodes))
        num_susceptible.append(len(overall_susceptible))
        num_recovered.append(len(recovered_nodes))

        if not infected_nodes:  # if no more active infected nodes
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
            
        iter += 1
    
    return G, num_infected, num_susceptible, num_recovered, iter, beta, gamma

def run_simulation_wrapper(args):
    G, beta, gamma, max_iter = args
    return run_simulation(G, beta, gamma, max_iter)