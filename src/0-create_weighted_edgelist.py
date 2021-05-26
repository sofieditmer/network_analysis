#!/usr/bin/env python
"""
Info: This script takes as input the fake_or_real_news.csv and creates a weighted edgelist with columns "nodeA", "nodeB", and "weight". This weighted edgelist can then be used as input for the 1-network_analysis.py script to create a network graph and compute centrality measures. 

Parameters:
    (optional) input_data: str <name-of-input-file>, default = "fake_or_real_news.csv"
    (optional) output_filename: str <name-of-output-file>, default = "weighted_edgelist_realnews.csv"
    
Usage:
    $ python 0-create_weighted_edgelist.py

Output:
    - "weighted_edgelist_realnews.csv": a CSV-file with column headers "nodeA", "nodeB", and "weight". 
"""

### DEPENDENCIES ###

# core libraries
import os
import sys
sys.path.append(os.path.join(".."))

# pandas, itertools, collections
import pandas as pd
from itertools import combinations
from collections import Counter

# spaCy
import spacy
nlp = spacy.load("en_core_web_sm") # load English language model

# argparse
import argparse


### MAIN FUNCTION ###

def main():
    
    # Initialise ArgumentParser class
    ap = argparse.ArgumentParser()
    
    # Argument 1: Input edgelist
    ap.add_argument("-i", "--input_data", 
                    type = str,
                    required = False, # not required argument
                    help = "Name of input file",
                    default = "fake_or_real_news.csv") # default input file
    
    # Argument 2: Output filename
    ap.add_argument("-o", "--output_filename", 
                    type = str,
                    required = False, # not required argument
                    help = "Name of the output file which is a weighted edgelist",
                    default = "weighted_edgelist_realnews.csv") # default input file

    # Parse arguments
    args = vars(ap.parse_args())
    
    # Save input parameters
    input_data = os.path.join("..", "data", args["input_data"])
    output_filename = args["output_filename"]

    # Create output folder if it does not already exist
    if not os.path.exists(os.path.join("..", "data")):
        os.mkdir(os.path.join("..", "data"))
        
    # Start message
    print("\n[INFO] Initializing the creation of the weighted edgelist...")
    
    # Instantiate the class
    edgelist = Edgelist(input_data, output_filename)
    
    # Load data
    print(f"\n[INFO] Loading and preprocessing {input_data}...")
    data = edgelist.load_and_preprocess_data()
    
    # Extract named entities
    print(f"\n[INFO] Extracting named entities...")
    named_entities, doc = edgelist.extract_named_entities(data)
    
    # Create edgelist
    print(f"\n[INFO] Creating edgelist...")
    realnews_edgelist = edgelist.create_edgelist(named_entities, doc)
    
    # Create weighted edgelist
    print(f"\n[INFO] Creating weighted edgelist...")
    counted_edges = edgelist.create_weighted_edgelist(realnews_edgelist)
        
    # Save weighted edgelist to output directory
    print(f"\n[INFO] Saving weighted edgelist as '{output_filename}' in 'data' directory...")
    edgelist.save_weighted_edgelist(counted_edges)

    # User message
    print(f"\n[INFO] Done! The weighted edgelist has been saved as '{output_filename}' in the 'data' directory.\n")
    
    
### WEIGHTED EDGELIST ### 
    
# Creating Network Analysis class 
class Edgelist:

    # Intialize Network analysis class
    def __init__(self, input_data, output_filename):
        
        # Receive input
        self.data = input_data
        self.output = output_filename
        
        
    def load_and_preprocess_data(self):
        """
        This method loads the data into a dataframe and filters out the fakse news from the dataset.
        """
        # Load data
        data = pd.read_csv(self.data)
        
        # Extract only real news
        data = data[data["label"]=="REAL"]["text"]
        
        return data
    
    
    def extract_named_entities(self, data):
        """
        This method extracts named entities using spaCy.
        """
        # Create empty list of named entities that can be appended to
        named_entities = []
        
        # Loop through each of the real news
        for post in data:
            
            # Create a temporary list
            tmp_list = []
            
            # Annotate the news using spaCy object 
            doc = nlp(post)
            
            # For every named entity in the doc
            for entity in doc.ents: # .ents means that we extract the named entities
                
                # If the named entitiy is a "person"
                if entity.label_ == "PERSON":
                    
                    # Append to the temporary list
                    tmp_list.append(entity.text)
                    
                # Append temporary list to the to main list of entities
                named_entities.append(tmp_list)
                
        return named_entities, doc
    
    
    def create_edgelist(self, named_entities, doc):
        """
        This method creates an edgelist using the itertools.combinations(). 
        """
        # Create an empty edgelist that can be appended to
        realnews_edgelist = []
        
        # Iterate over every named entity 
        for entity in named_entities:
            
            # Create list that pairs the combination in the document
            edges = list(combinations(doc, 2)) # this gives us the possible combinations of pairs (which is why we say 2).
            
            # For each combination (i.e. each pair of nodes) 
            for edge in edges:
                
                # Append the edge (pair of nodes) to final edgelist
                realnews_edgelist.append(tuple(sorted(edge))) # we use sorted() to return the tuples in an ordered way. Because we are working with an undirected network we get duplicates of pairs, and when we use sorted() we order the entries in the tuple to order them in alphabetic order. 
                
        return realnews_edgelist
                
        
    def create_weighted_edgelist(self, realnews_edgelist):
        """
        This method takes the edgelist and counts how often the pairs of nodes appear together which becomes a measure 
        of "weight", i.e. the strength of edge (connection) between the nodes. In this way a weighted edgelist is created.
        """
        # Create empty container for the counted edges
        counted_edges = []
        
        # Count every pair in the edgelist
        for pair, weight in Counter(realnews_edgelist).items(): # with the .items() we get a simple sequence that Python can iterate over (Python cannot iterate over a dictionary) 
            nodeA = pair[0]
            nodeB = pair[1]
            weight = weight # weight = how frequently any pair of nodes occur. The frequencies are across the entire corpus and not the single document
            
            # Append to list
            counted_edges.append((nodeA, nodeB, weight))
        
        return counted_edges
    
    
    def save_weighted_edgelist(self, counted_edges):
        """
        This method takes the weighted edgelist and saves it as a CSV-file with the column headers "nodeA", "nodeB", 
        and "weight" to the data folder.
        """
        # Create dataframe
        edges_df = pd.DataFrame(counted_edges, columns = ["nodeA", "nodeB", "weight"])
        
        # Define output path
        out_path = os.path.join("..", "data", self.output)
        
        # Save dataframe as CSV to output directory
        edges_df.to_csv(out_path, index = False)

    
# Define behaviour when called from command line
if __name__=="__main__":
    main()