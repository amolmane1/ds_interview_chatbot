# TODO: add all graph related code here

import networkx as nx
from copy import deepcopy

from nodes.node_functions import *
# func to save graph to file
# func to load graph from file
# func to create a a flowchart based on certain specifications & then save to file


def add_function_arg_to_node(node, key, value):
    if 'function_args' not in node.keys():
        node['function_args'] = {}
    node['function_args'][key] = value
    
    
def get_first_node_in_graph(graph):
    first_node_name = [node_name for node_name, in_degrees in graph.in_degree() if in_degrees==0][0]
    first_node = graph.nodes[first_node_name]
    return first_node_name, first_node


def get_next_node(graph, current_node_name, current_node_output):
    outgoing_edges = list(graph.out_edges(current_node_name, data=True))
    if len(outgoing_edges) == 0:
        return None, None
    else:
        if len(outgoing_edges) == 1:
            edge_to_traverse = outgoing_edges[0]
        else:
            for edge in outgoing_edges:
                if current_node_output['routing_value'] in edge[-1]['passthrough_values']:
                    edge_to_traverse = edge
        next_node_name = edge_to_traverse[1]
        next_node = graph.nodes[next_node_name]
        return next_node_name, next_node


def plot_graph(graph):
    graph_visual = nx.nx_agraph.to_agraph(graph)
    graph_visual.layout(prog='dot')
    return graph_visual


def create_interview_flowchart():
    interview_graph = nx.MultiDiGraph()
    
    interview_graph.add_node("introduction")
    interview_graph.add_node("algorithm selection")
    interview_graph.add_node("dealing with categorical values")
    interview_graph.add_node("dealing with numerical values")
    interview_graph.add_node("conclusion")
    
    interview_graph.add_edge("introduction", "algorithm selection")    
    interview_graph.add_edge("algorithm selection", "dealing with categorical values")
    interview_graph.add_edge("dealing with categorical values", "dealing with numerical values")
    interview_graph.add_edge("dealing with numerical values", "conclusion")

    
    ## introduction
    section_graph = nx.MultiDiGraph()
    
    section_graph.add_node("share_introduction_boilerplate", function=share_introduction_boilerplate)
    
    interview_graph.nodes["introduction"]['graph'] = section_graph

    ## subgraph for technical sections
    section_graph = nx.MultiDiGraph()
    
    section_graph.add_node("confirm_what_applicant_did", function=confirm_what_applicant_did)
    section_graph.add_node("get_applicant_response", 
                           # function=get_response_from_python_input,
                           function=get_response_from_applicant_persona
                          )
    
    section_graph.add_node("route_answer_to_ask_what_applicant_did", function=route_answer_to_ask_what_applicant_did)
    section_graph.add_node("ask_what_applicant_did", function=ask_what_applicant_did)
    section_graph.add_node("get_applicant_response-1",
                           # function=get_response_from_python_input,
                           function=get_response_from_applicant_persona
                          )
    
    section_graph.add_node("validate_answer_how_it_works", function=validate_answer_how_it_works)
    section_graph.add_node("ask_how_it_works", function=ask_how_it_works)
    section_graph.add_node("get_applicant_response-2",
                           # function=get_response_from_python_input,
                           function=get_response_from_applicant_persona
                          )
    
    section_graph.add_node("route_answer_to_what_other_options_applicant_considered", function=route_answer_to_what_other_options_applicant_considered)
    section_graph.add_node("ask_what_other_options_applicant_considered", function=ask_what_other_options_applicant_considered, function_args={
        'model_version': "14.01.23"
    })
    section_graph.add_node("get_applicant_response-3", 
                           # function=get_response_from_python_input,
                           function=get_response_from_applicant_persona
                          )

    section_graph.add_node("validate_why_applicant_picked_X_over_Y", function=validate_why_applicant_picked_X_over_Y)
    section_graph.add_node("ask_why_applicant_picked_X_over_Y", function=ask_why_applicant_picked_X_over_Y)
    section_graph.add_node("get_applicant_response-4",
                           # function=get_response_from_python_input,
                           function=get_response_from_applicant_persona
                          )
    
    section_graph.add_node("empty_node", function=empty_node)
    

    section_graph.add_edge("confirm_what_applicant_did", "get_applicant_response")
    section_graph.add_edge("get_applicant_response", "route_answer_to_ask_what_applicant_did")
    
    section_graph.add_edge("route_answer_to_ask_what_applicant_did", "ask_what_applicant_did", passthrough_values=[-1])
    section_graph.add_edge("ask_what_applicant_did", "get_applicant_response-1")
    section_graph.add_edge("get_applicant_response-1", "route_answer_to_ask_what_applicant_did")
    section_graph.add_edge("route_answer_to_ask_what_applicant_did", "route_answer_to_what_other_options_applicant_considered", passthrough_values=[0])
    section_graph.add_edge("route_answer_to_ask_what_applicant_did", "validate_answer_how_it_works", passthrough_values=[1])
    
    section_graph.add_edge("validate_answer_how_it_works", "ask_how_it_works", passthrough_values=[-1])
    section_graph.add_edge("ask_how_it_works", "get_applicant_response-2")
    section_graph.add_edge("get_applicant_response-2", "validate_answer_how_it_works")
    section_graph.add_edge("validate_answer_how_it_works", "route_answer_to_what_other_options_applicant_considered", passthrough_values=[0,1,2,3])
    
    section_graph.add_edge("route_answer_to_what_other_options_applicant_considered", "ask_what_other_options_applicant_considered", passthrough_values=[-1])
    section_graph.add_edge("ask_what_other_options_applicant_considered", "get_applicant_response-3")
    section_graph.add_edge("get_applicant_response-3", "route_answer_to_what_other_options_applicant_considered")
    section_graph.add_edge("route_answer_to_what_other_options_applicant_considered", "validate_why_applicant_picked_X_over_Y", passthrough_values=[0,1])

    section_graph.add_edge("validate_why_applicant_picked_X_over_Y", "ask_why_applicant_picked_X_over_Y", passthrough_values=[-1])
    section_graph.add_edge("ask_why_applicant_picked_X_over_Y", "get_applicant_response-4")
    section_graph.add_edge("get_applicant_response-4", "validate_why_applicant_picked_X_over_Y")
    section_graph.add_edge("validate_why_applicant_picked_X_over_Y", "empty_node", passthrough_values=[0,1])

    ## algo selection
    interview_graph.nodes["algorithm selection"]['graph'] = deepcopy(section_graph)

    ## categorical
    interview_graph.nodes["dealing with categorical values"]['graph'] = deepcopy(section_graph)
    
    ## numerical
    interview_graph.nodes["dealing with numerical values"]['graph'] = deepcopy(section_graph)

    ## conclusion
    section_graph = nx.MultiDiGraph()
    section_graph.add_node("share_conclusion_boilerplate", function=share_conclusion_boilerplate)
    interview_graph.nodes["conclusion"]['graph'] = section_graph
    
    return interview_graph