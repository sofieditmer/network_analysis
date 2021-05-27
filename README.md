# Assignment 2: Network Analysis with ```networkx```

### Description of Task: Creating a Reusable Network Analysis Pipeline
This assignment was assigned by the course instructor as “Assignment 4 – Network Analysis”. The purpose of this assignment was to create a reusable network analysis pipeline using network. This analysis pipeline should take any given weighted edgelist, providing that this edgelist is saved as a CSV-file with the column header “nodeA”, “nodeB”, and “weight” as input and create a network visualization showing the connections (edges) between named entities (nodes) that co-occur in the same documents. The script should also create a data frame showing the degree, betweenness, and eigenvector centrality score for each node in the network. 
In addition to the abovementioned requirements, I chose to also create a separate python script that creates the weighted edgelist with the required format. <br>


### Content and Repository Structure <br>
If the user wishes to engage with the code and reproduce the obtained results, this section includes the necessary instructions to do so. It is important to remark that all the code that has been produced has only been tested in Linux and MacOS. Hence, for the sake of convenience, I recommend using a similar environment to avoid potential problems. 
The repository follows the overall structure presented below. The two scripts, ```0-create_weighted_edgelist.py``` and ```1-network_analysis.py```, are located in the ```src``` folder. The data is provided in the ```data``` folder, and the outputs produced when running the scripts can be found within the ```output``` folder. The README file contains a detailed run-through of how to engage with the code and reproduce the contents.

| Folder | Description|
|--------|:-----------|
| ```data``` | A folder containing a the data on which the network analysis is performed.
| ```src``` | A folder containing the python scripts for the particular assignment.
| ```output``` | A folder containing the outputs produced when running the python scripts within the src folder.
| ```requirements.txt```| A file containing the dependencies necessary to run the python script.
| ```create_network_venv.sh```| A bash-file that creates a virtual environment in which the necessary dependencies listed in the ```requirements.txt``` are installed. This script should be run from the command line.
| ```LICENSE``` | A file declaring the license type of the repository.


### Usage and Technicalities <br>
To reproduce the results of this assignment, the user will have to create their own version of the repository by cloning it from GitHub. This is done by executing the following from the command line: 

```
$ git clone https://github.com/sofieditmer/network_analysis.git  
```

Once the user has cloned the repository, a virtual environment must be set up in which the relevant dependencies can be installed. To set up the virtual environment and install the relevant dependencies, a bash-script is provided, which creates a virtual environment and installs the dependencies listed in the ```requirements.txt``` file when executed. To run the bash-script that sets up the virtual environment and installs the relevant dependencies, the user must first navigate to the network_analysis repository:

```
$ cd network_analysis
$ bash create_network_venv.sh 
```

Once the virtual environment has been set up and the relevant dependencies listed in ```requirements.txt``` have been installed within it, the user is now able to run the scripts provided in the src folder directly from the command line. In order to run the script, the user must first activate the virtual environment in which the script can be run. Activating the virtual environment is done as follows:

```
$ source network_venv/bin/activate
```

Once the virtual environment has been activated, the user is now able to run the ```sentiment.py``` script within it:

```
(network_venv) $ cd src

(network_venv) $ python 0-create_weighted_edgelist.py

(network_venv) $ python 1-network_analysis.py
```

For the ```0-create_weighted_edgelist.py``` script the user is able to modify the following parameters, however, this is not compulsory:

```
-i, --input_data: str <name-of-input-data>, default = "fake_or_real_news.csv"
-o, --output_filename: str <name-of-output-file>, default = "weighted_edgelist_realnews.csv"
````

For the ```1-network_analysis.py``` script the user is able to modify the following parameters, however, once again this is not compulsory:

```
-i, --edgelist: str <name-of-weighted-edgelist>, default = "weighted_edgelist_realnews.csv"
-c, --cutoff_edgeweight: int <minimum-edgeweight>, default = 500
-o, --output_filename: str <name-of-output-file>, default = "network_graph.png"
```

The abovementioned parameters allow the user to adjust the analysis of the input data, if necessary, but default parameters have been set making the script run without explicitly specifying these arguments. The user is able to specify which weighted edgelist to perform the network analysis on as well as the minimum edge weight that defines which edges are to be taken into account. Finally, the user is able to modify the name of the network graph. 

### Output <br>
When running the ```0-create_weighted_edegelist.py```script, the following files will be saved in the ```data``` folder: 
1. ```weighted_edgelist_realnews.csv``` a CSV-file with column headers "nodeA", "nodeB", and "weight". 

When running the ```1-network_analysis.py```script, the following files will be saved in the ```output``` folder: 
1. ```network_graph.png``` Network visualization displaying the edges between nodes within the data.
2. ```weighted_edgelist_realnews_centrality_measures_500.csv``` centrality measures for each node.
3. ```network_information.txt``` basic information about the network.

### Discussion of Results <br>
When assessing the general network information (see [General Network Information](https://github.com/sofieditmer/network_analysis/blob/main/output/network_information.txt)), we can gain an overview of the network that forms between the people mentioned in the real news. The network consists of 93 nodes, i.e., people, and 196 edges, i.e., connections. The size of the network gives us an idea about how large the network is. The average degree is 3.63 and represents the sum of the degrees of all the nodes in the network divided by the number of nodes in the graph. Hence, while the degree of a particular node indicates the number of nodes that it is connected to by an edge, the average degree is a measure of the average number of edges for a node, which can be used as a measure of the connectedness of the network graph. Thus, on average a node in this network has around 3 connections with other nodes. 
The network density is estimated to 0.04. The density of a network describes the ratio of edges in the network to all possible edges in the network. Hence, it indicates out of all the possible edges, how many in fact are present, which gives us an idea about how “dense”, i.e., connected, the network is. The density ranges between 0, indicating that there are no edges, and 1 indicating that all possible edges are present, i.e., each node is connected to every other node. In this case the density is 0.04 which means that the network does not seem to be very dense given that only 4% of the possible edges are present.
The network transitivity is estimated to 0.11. The transitivity of a network describes the ratio of all present triads over all possible triads. Hence, transitivity provides an idea about how interconnected the network is. Similar to network density, transitivity also ranges from 0, indicating a low degree of transitivity, to 1, indicating the highest degree of transitivity. A transitivity score of 0.11 thus indicates a relatively low degree of transitivity. 
Supplementing the network metrics with the visual representation of the network (see figure 1), we can gain a sense of the network architecture in a visual sense. When assessing the network graph, it becomes clear that there is one node in particular that seems very well connected.  This central node seems to be forming a cluster, a so-called hub, and thus play an important role in the network.

<img src="https://github.com/sofieditmer/network_analysis/blob/main/output/network_graph.png" width="1000">
Figure 1: Network graph. <br> <br>

To inform the network graph further, different centrality measures were calculated: degree centrality, betweenness, and eigenvector centrality. The 10 nodes with the highest centrality measures can be found in the ```output```folder ([Centrality Measures](https://github.com/sofieditmer/network_analysis/blob/main/output/network_information.txt)). For degree centrality, we can see that Hillary Clinton, George Bush, and Donald Trump obtain a high measure of degree centrality. While the degree of a particular node describes how many edges that particular node has, the degree centrality score is normalized which means that it represents the ratio of actual edges to all possible edges. Hillary Clinton achieves the highest degree centrality score of 0.7 which makes her the most central hub in the network. 
When assessing the nodes with the highest eigenvector centrality values, once again Hillary Clinton, George Bush, and Donald Trump are central figures. The eigenvector centrality is a measure of the influence of a given node in the network based on how well connected it is. Hence, the importance of an individual node becomes a function of how important its neighboring nodes are. Thus, given that Hillary Clinton scores the highest eigenvector centrality, it means that she is connected to other well-connected nodes, which in turn makes her an important node in the network.
Finally, we can assess the nodes with the highest betweenness centrality scores. Once again Hillary Clinton and George Bush score high on this centrality measure, but Donald Trump is no longer in the top 3. Betweenness centrality is a quantitative measure of how well a node connects other nodes in the network. Hence, with betweenness centrality we can assess how well nodes connect other nodes. Hence, if there is only one node enabling the connection between two hubs in the network, this node will score high on betweenness centrality. Thus, a node with a high betweenness centrality gains its importance not from its number of edges, but from the way it enables connections between other nodes. While Hillary Clinton and to some degree George Bush seem to enable connections between other nodes, Trump does not. Hence, although Donald Trump has many edges resulting in high degree and eigenvector centrality scores, he does not seem to enable connections between other nodes, which explains his low score on betweenness centrality. <br>
A final point to emphasize when assessing the results of this network analysis, is the problem of coreference. For instance, both “Trump” and “Donald Trump” are represented in the network even though they refer to the same person. This demonstrates a general problem with named entity recognition. In order to resolve the coreference problem, the named entity recognition system must acquire some kind of contextual knowledge to infer that different entities can refer to the same referent. While we humans use our linguistic intuition and contextual knowledge to resolve the problem of coreference, this is a very complex task for a named entity recognition system. The problem of coreference resolution could potentially be solved relying on the neuralcoref library available in spaCy. <br>

### License <br>
This project is licensed under the MIT License - see the [LICENSE](https://github.com/sofieditmer/network_analysis/blob/main/LICENSE) file for details.

### Contact Details <br>
If you have any questions feel free to contact me on [201805308@post.au.dk](201805308@post.au.dk)
