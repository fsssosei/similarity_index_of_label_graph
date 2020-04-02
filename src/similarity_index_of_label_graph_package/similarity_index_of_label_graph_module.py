'''
similarity_index_of_label_graph - This is the package used to calculate the similarity index of the label graph pairs.
Copyright (C) 2020  sosei

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

__all__ = ['similarity_index_of_label_graph_class']

class similarity_index_of_label_graph_class(object):
    '''
        Calculate the similarity index of label graph pairs.
        
        Generate an instance when using:
            instance_name = similarity_index_of_label_graph_class()
        
        Then call the instance calculation:
            instance_name(G1, G2, weight = None)
        
        Parameters
        ----------
        G1, G2 : graphs
        A pair of graphs for calculating similarity.
        
        weight : string or None, optional (default=None)
            The edge attribute that holds the numerical value used as a weight.
            If None, then each edge has weight 1.
        
        Returns
        -------
        similarity_index : float
            Similarity index of G1 and G2 graph pairs. The range is [-1, 1].
        
        Notes
        ------
        The time complexity of this algorithm is O(n^2*log(n) + n*m), where n is the number of nodes and m the number of edges in the graph.
        
        Examples
        --------
        >>> from networkx.generators.directed import gnr_graph
        >>> from networkx.generators import spectral_graph_forge
        >>> G1 = gnr_graph(100, 0.3, seed = 65535)
        >>> G2 = gnr_graph(100, 0.3, seed = 1)
        >>> G3 = spectral_graph_forge(G1, 0.6, seed = 65535)
        >>> G4 = spectral_graph_forge(G2, 0.6, seed = 65535)
        >>> similarity_index_of_label_graph = similarity_index_of_label_graph_class()
        >>> similarity_index_of_label_graph(G1, G2)
        0.5925135061949895
        >>> similarity_index_of_label_graph(G1, G3)
        -0.9677390108526409
        >>> similarity_index_of_label_graph(G2, G4)
        -0.9041961423870752
        >>> similarity_index_of_label_graph(G3, G4)
        0.5359512772554542
    '''
    
    from networkx.classes.graph import Graph
    from networkx.classes.digraph import DiGraph
    from networkx.classes.multigraph import MultiGraph
    from networkx.classes.multidigraph import MultiDiGraph
    
    version = '1.0.0'
    
    def __graph_embedding_vector(self, G, weight = None) -> dict:
        def convert_graph_to_node_frequence(G, weight = None) -> dict:
            from statistics import mean
            from math import log1p
            from networkx.classes import function as nx_cls_func
            from networkx.algorithms.components.connected import connected_components
            from networkx.algorithms.shortest_paths.generic import average_shortest_path_length
            
            dict_of_node_frequence = dict.fromkeys(G.nodes, 1)
            if not nx_cls_func.is_empty(G):
                for nbunch_of_component in connected_components(nx_cls_func.to_undirected(G)):
                    number_of_nodes_for_component = len(nbunch_of_component)
                    if number_of_nodes_for_component > 1:
                        component_subgraph_of_G = nx_cls_func.subgraph(G, nbunch_of_component)
                        summation_coefficient_of_edges_to_points = (average_shortest_path_length(component_subgraph_of_G) - 1) * number_of_nodes_for_component / 2  #Calculate the average shortest distance without weights; Minus 1 because you want to subtract the node itself; Divide by 2 because the two endpoints of the edge have to share the weight equally.
                        dict_of_edges = dict.fromkeys(component_subgraph_of_G.edges())
                        if component_subgraph_of_G.is_multigraph():
                            for _edge in dict_of_edges.keys():
                                edge_weights = mean(_attribute.get(weight, 1) for _attribute in component_subgraph_of_G.get_edge_data(*_edge).values())
                                if isinstance(edge_weights, (int, float)):
                                    if edge_weights < 0:
                                        raise ValueError('The weight mean of parallel edges cannot be negative.')
                                else:
                                    raise TypeError(f"The weight value must be 'int' or 'float', not '{edge_weights.__class__.__name__}'")
                                dict_of_edges[_edge] = log1p(edge_weights)
                        else:
                            for _edge in component_subgraph_of_G.edges():
                                edge_weights = component_subgraph_of_G.edges[_edge].get(weight, 1)
                                if isinstance(edge_weights, (int, float)):
                                    if edge_weights < 0:
                                        raise ValueError('The weight value cannot be negative.')
                                else:
                                    raise TypeError(f"The weight value must be 'int' or 'float', not '{edge_weights.__class__.__name__}'")
                                dict_of_edges[_edge] = log1p(edge_weights)
                        log1p_weight_sum = sum(dict_of_edges.values())
                        if log1p_weight_sum <= 0:
                            raise ValueError('The weights cannot all be zero.')
                        for _edge, _log1p_weight in dict_of_edges.items():
                            frequence_of_nodes_converted_by_edges = (_log1p_weight / log1p_weight_sum) * summation_coefficient_of_edges_to_points
                            dict_of_node_frequence[_edge[0]] += frequence_of_nodes_converted_by_edges
                            dict_of_node_frequence[_edge[1]] += frequence_of_nodes_converted_by_edges
            return dict_of_node_frequence
        return convert_graph_to_node_frequence(G, weight)

    def __measure_func(self, vector_1: list, vector_2: list) -> float:
        def pearson_correlation(u, v) -> float:
            from scipy.spatial.distance import correlation
            return -(correlation(u, v) - 1)
        return pearson_correlation(vector_1, vector_2)

    def __call__(self, G1, G2, weight = None) -> float:
        def frequency_dict_to_label_order_vector(frequency_dict) -> list:
            sum_frequency = sum(frequency_dict.values())
            return [(frequency_dict[_key] / sum_frequency) for _key in sorted(frequency_dict.keys())]

        if G1.number_of_nodes() == 0:
            raise ValueError('The graph should have at least one node.')
        if G2.number_of_nodes() == 0:
            raise ValueError('The graph should have at least one node.')
        
        dict_of_frequence_1 = self.__graph_embedding_vector(G1, weight)
        dict_of_frequence_2 = self.__graph_embedding_vector(G2, weight)
        
        #The following procedure is used to solve the case that the set of nodes of two graphs is not equal.
        #Paragraphs began
        for _node in (set(G2.nodes) - set(G1.nodes)):
            dict_of_frequence_1.update({_node: 0})
        for _node in (set(G1.nodes) - set(G2.nodes)):
            dict_of_frequence_2.update({_node: 0})
        #End of the paragraph
        
        frequency_vector_of_graph_1 = frequency_dict_to_label_order_vector(dict_of_frequence_1)
        frequency_vector_of_graph_2 = frequency_dict_to_label_order_vector(dict_of_frequence_2)
        return self.__measure_func(frequency_vector_of_graph_1, frequency_vector_of_graph_2)
