#!/usr/bin/env python
"""
Info: This script takes any weighted edgelist as input providing that the edgelist is saved as a CSV-file with column headers "nodeA" and "nodeB", and creates a network visualization and saves it in the output directory. Centrality measures are computed for each node, and a dataframe showing the degree, betweenness, and eigenvector centrality for each node is created and saved as a CSV-file in the output directory as well.

Parameters:
    (optional) weighted_edgelist: str <name-of-weighted-edgelist>, default = "weighted_edgelist_realnews.csv"
    (optional) cutoff_edgeweight: int <minimum-edgeweight>, default = 500

Usage:
    $ python 1.network_analysis.py
   
Output:
    - network_graph.png: Network visualization displaying the edges between nodes within the data.
    - weighted_edgelist_realnews_centrality_measures_500.csv: centrality measures for each node.
"""

### DEPENDENCIES ###

# core libraries
import os
import sys
sys.path.append(os.path.join(".."))

# pandas, networkx, matplotlib, pygraphviz, seaborn
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (20,20)
import pygraphviz 

# redirect_stdout
from contextlib import redirect_stdout

# argparse
import argparse

### MAIN FUNCTION ###

def main():
    
    # Initialise ArgumentParser class
    ap = argparse.ArgumentParser()
    
    # Argument 1: Input edgelist
    ap.add_argument("-i", "--input_weighted_edgelist", 
                    type = str,
                    required = False, # not required argument
                    help = "Name of the weighted edgelist.",
                    default = "weighted_edgelist_realnews.csv") # default weighted edgelist

    # Argument 2: Cut-off edgeweight to filter data based on
    ap.add_argument("-c", "--cutoff_edgeweight", 
                    type = int,
                    required = False, # not required argument  
                    help = "Define the edge weight cut-off point to filter data. This is the number of times an edge should occur in order to be included.",
                    default = 500) # default cut-off edgeweight. An edge must occur 500 times to be included.
    
    # Parse arguments
    args = vars(ap.parse_args())
    
    # Save input parameters
    weighted_edgelist = os.path.join("..", "data", args["input_weighted_edgelist"])
    cutoff_edgeweight = args["cutoff_edgeweight"]
    
    # Create output folder if it does not already exist
    if not os.path.exists(os.path.join("..", "output")):
        os.mkdir(os.path.join("..", "output"))
        
    # Start message
    print("\n[INFO] Initializing network analysis...")
    
    # Instantiate the Network Analysis class
    network_analysis = Network_analysis(weighted_edgelist)
    
    # Prepare data
    print(f"\n[INFO] Preparing '{weighted_edgelist}'...")
    weighted_edgelist_df = network_analysis.prepare_data()
    
    # Create network graph
    print(f"\n[INFO] Creating network graph and saving it in 'output' directory...")
    network_graph = network_analysis.create_network_graph(weighted_edgelist_df, cutoff_edgeweight)
    
    # Calculate centrality measures
    print(f"\n[INFO] Calculating centrality measures and saving them in 'output' directory...")
    centrality_df = network_analysis.calculate_centrality_measures(network_graph, cutoff_edgeweight)
    
    # Extract network information
    print(f"\n[INFO] Extracting network information and saving in 'output' directory...")
    network_analysis.extract_network_info(network_graph, centrality_df)
        
    # User message
    print(f"\n[INFO] Done! Your network visualization has now been saved in the 'output' folder together with a CSV-file containing measures of centrality for each node and a TXT-file with basic network information.\n")
    
    
### NETWORK ANALYSIS ### 
    
# Creating Network Analysis class 
class Network_analysis:

    # Intialize Network analysis class
    def __init__(self, weighted_edgelist):
        
        # Receive input
        self.weighted_edgelist = weighted_edgelist
        
        
    def prepare_data(self):
        """
        This method loads the weighted edgelist into a dataframe.
        """
        # Load data
        weighted_edgelist_df = pd.read_csv(self.weighted_edgelist)
        
        return weighted_edgelist_df
    
    
    def create_network_graph(self, weighted_edgelist_df, cut_off):
        """ 
        This method creates a network graph using networkx and saves it as a .png file to the output directory. 
        """
        # Filter data based on cut-off edgeweight speficied by user (500 is the default threshold)
        filtered_edges_df = weighted_edgelist_df[weighted_edgelist_df["weight"] > int(cut_off)]
        
        # Create graph using the networkx library by taking the filtered edgelist, the nodes and the weights
        network_graph = nx.from_pandas_edgelist(filtered_edges_df, 
                                                "nodeA", 
                                                "nodeB", 
                                                ["weight"])
        
        # Plot graph object using pygraphviz
        position = nx.nx_agraph.graphviz_layout(network_graph, prog = "neato")
        
        # Draw the graph using networkx.draw() function
        nx.draw(network_graph,
                position, 
                with_labels = True, 
                node_size = 20, 
                font_size = 10)
        
        # Save network graph in viz folder
        output_path = os.path.join("..", "output", "network_graph.png")
        plt.savefig(output_path, dpi = 300, bbox_inches = "tight")

        return network_graph

    
    def calculate_centrality_measures(self, network_graph, cutoff_edgeweight):
        """ 
        This method calculates centrality measures, i.e. degree centrality, betweenness centrality, 
        and eigenvector centrality, for each node and saves the results as a CSV-file in the output directory. 
        """
        # Calculate degree centrality
        degree_centrality = nx.degree_centrality(network_graph)
        
        # Create dataframe for degree centrality
        degree_df = pd.DataFrame(degree_centrality.items(), 
                                 columns = ["node", "Degree Centrality"])
        
        # Calculate betweenness centrality
        betweenness_centrality = nx.betweenness_centrality(network_graph)
        
        # Create dataframe for betweenness centrality
        betweenness_df = pd.DataFrame(betweenness_centrality.items(), 
                                      columns = ["node", "Betweenness Centrality"])
        
        # Calculate eigenvector centrality
        eigenvector_centrality = nx.eigenvector_centrality(network_graph)
        
        # Create dataframe for eigenvector centrality
        eigenvector_df = pd.DataFrame(eigenvector_centrality.items(), 
                                      columns = ["node", "Eigenvector Centrality"])
        
        # Merge dataframes into one dataframe containing all measures for each node
        centrality_df = degree_df.merge(betweenness_df)
        centrality_df = centrality_df.merge(eigenvector_df).sort_values("Degree Centrality", ascending = False)
        
        # Save dataframe as CSV-file
        output_csv = os.path.join("..", "output", "centrality_measures.csv")
        centrality_df.to_csv(output_csv, index = False)
        
        return centrality_df
        
        
    def extract_network_info(self, network_graph, centrality_df):
        """
        This method extracts some important information about the network graph and saves the metrics in a 
        CSV-file to the output directory. 
        """
        # Extract basic network information
        info = nx.info(network_graph)
        
        # Calcuate the density of the network
        network_density = round(nx.density(network_graph), 3)
        
        # Calculate the transitivity of the network
        transitivity = round(nx.transitivity(network_graph), 3)
        
        # Change index of dataframe to make it look nicer in output file
        centrality_df = centrality_df.set_index('node')
        
        # Calculate the top 10 nodes for degree centrality 
        top_10_degree = centrality_df.nlargest(10, "Degree Centrality")

        # Calcualte the top 10 nodes for betweenness centrality
        top_10_betweenness = centrality_df.nlargest(10, "Betweenness Centrality")
        
        # Calculate the top 10 nodes for eigenvector centrality
        top_10_eigenvector = centrality_df.nlargest(10, "Eigenvector Centrality")
            
        # Gather information in txt-file and save to output-directory
        info_out = os.path.join("..", "output", "network_information.txt")
        with open(info_out, 'w') as f:
            with redirect_stdout(f):
                print(f"Basic network information:\n{info}\n\n")
                print(f"Network density: {network_density}\n")
                print(f"Network transitivty: {transitivity}\n")
                print(f"The 10 people (nodes) with highest degree centrality:\n\n{top_10_degree}\n")
                print(f"The 10 people (nodes) with highest betweenness centrality:\n\n{top_10_betweenness}\n")
                print(f"The 10 people (nodes) with highest eigenvector centrality:\n\n{top_10_eigenvector}\n")
        

# Define behaviour when called from command line
if __name__=="__main__":
    main()