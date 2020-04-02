# similarity_index_of_label_graph

![PyPI](https://img.shields.io/pypi/v/similarity-index-of-label-graph?color=red)
![PyPI - Status](https://img.shields.io/pypi/status/similarity-index-of-label-graph)
![GitHub Release Date](https://img.shields.io/github/release-date/fsssosei/similarity_index_of_label_graph)
[![Build Status](https://scrutinizer-ci.com/g/fsssosei/similarity_index_of_label_graph/badges/build.png?b=master)](https://scrutinizer-ci.com/g/fsssosei/similarity_index_of_label_graph/build-status/master)
[![Code Intelligence Status](https://scrutinizer-ci.com/g/fsssosei/similarity_index_of_label_graph/badges/code-intelligence.svg?b=master)](https://scrutinizer-ci.com/code-intelligence)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/fsssosei/similarity_index_of_label_graph.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/fsssosei/similarity_index_of_label_graph/context:python)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/bf34f8d12be84b4492a5a3709df0aae5)](https://www.codacy.com/manual/fsssosei/similarity_index_of_label_graph?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=fsssosei/similarity_index_of_label_graph&amp;utm_campaign=Badge_Grade)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/fsssosei/similarity_index_of_label_graph/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/fsssosei/similarity_index_of_label_graph/?branch=master)
![PyPI - Downloads](https://img.shields.io/pypi/dw/similarity-index-of-label-graph?label=PyPI%20-%20Downloads)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/similarity-index-of-label-graph)
![PyPI - License](https://img.shields.io/pypi/l/similarity-index-of-label-graph)

*calculate the similarity index of the label graph pairs package in python.*
Can be used for weighted/unweighted and directed/undirected networks.

## Installation

Installation can be done through pip. You must have python version >= 3.7

	pip install similarity-index-of-label-graph

## Usage

The statement to import the package:

	from similarity_index_of_label_graph_package import similarity_index_of_label_graph_class
	
Example:

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
