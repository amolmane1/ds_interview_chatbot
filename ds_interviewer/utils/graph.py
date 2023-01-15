# TODO: add all graph related code here

import networkx as nx

from nodes.node_functions import *
# func to save graph to file
# func to load graph from file
# func to create a a flowchart based on certain specifications & then save to file


def plot_graph(graph):
    graph_visual = nx.nx_agraph.to_agraph(graph)
    graph_visual.layout(prog='dot')
    return graph_visual


def create_interview_flowchart():
    interview_graph = nx.MultiDiGraph()
    
    interview_graph.add_node("introduction")
    interview_graph.add_node("algorithm selection")
    interview_graph.add_node("dealing with categorical values")
    interview_graph.add_node("conclusion")
    
    interview_graph.add_edge("introduction", "algorithm selection")
    interview_graph.add_edge("algorithm selection", "dealing with categorical values")
    interview_graph.add_edge("dealing with categorical values", "conclusion")

    
    ## introduction
    section_graph = nx.MultiDiGraph()
    
    section_graph.add_node("share_introduction_boilerplate", function=share_introduction_boilerplate, function_args={})
    
    interview_graph.nodes["introduction"]['graph'] = section_graph

    ## algo selection
    section_graph = nx.MultiDiGraph()
    
    section_graph.add_node("confirm_what_applicant_did", function=confirm_what_applicant_did, function_args={})
    section_graph.add_node("route_answer_to_confirm_what_applicant_did", function=route_answer_to_confirm_what_applicant_did, function_args={})
    section_graph.add_node("ask_what_applicant_did", function=ask_what_applicant_did, function_args={})
    section_graph.add_node("ask_how_it_works", function=ask_how_it_works, function_args={})
    section_graph.add_node("validate_answer_how_it_works", function=validate_answer_how_it_works, function_args={})
    section_graph.add_node("ask_what_other_options_applicant_considered", function=ask_what_other_options_applicant_considered, function_args={})
    
    section_graph.add_edge("confirm_what_applicant_did", "route_answer_to_confirm_what_applicant_did")
    section_graph.add_edge("route_answer_to_confirm_what_applicant_did", "ask_what_applicant_did", passthrough_values=[0])
    section_graph.add_edge("route_answer_to_confirm_what_applicant_did", "ask_how_it_works", passthrough_values=[1])
    section_graph.add_edge("ask_what_applicant_did", "ask_how_it_works")
    section_graph.add_edge("ask_how_it_works", "validate_answer_how_it_works")
    section_graph.add_edge("validate_answer_how_it_works", "ask_what_other_options_applicant_considered")
    
    interview_graph.nodes["algorithm selection"]['graph'] = section_graph

    ## categorical
    section_graph = nx.MultiDiGraph()
    
    section_graph.add_node("confirm_what_applicant_did", function=confirm_what_applicant_did, function_args={})
    section_graph.add_node("route_answer_to_confirm_what_applicant_did", function=route_answer_to_confirm_what_applicant_did, function_args={})
    section_graph.add_node("ask_what_applicant_did", function=ask_what_applicant_did, function_args={})
    section_graph.add_node("ask_how_it_works", function=ask_how_it_works, function_args={})
    section_graph.add_node("validate_answer_how_it_works", function=validate_answer_how_it_works, function_args={})
    section_graph.add_node("ask_what_other_options_applicant_considered", function=ask_what_other_options_applicant_considered, function_args={})
    
    section_graph.add_edge("confirm_what_applicant_did", "route_answer_to_confirm_what_applicant_did")
    section_graph.add_edge("route_answer_to_confirm_what_applicant_did", "ask_what_applicant_did", passthrough_values=[0])
    section_graph.add_edge("route_answer_to_confirm_what_applicant_did", "ask_how_it_works", passthrough_values=[1])
    section_graph.add_edge("ask_what_applicant_did", "ask_how_it_works")
    section_graph.add_edge("ask_how_it_works", "validate_answer_how_it_works")
    section_graph.add_edge("validate_answer_how_it_works", "ask_what_other_options_applicant_considered")
    
    interview_graph.nodes["dealing with categorical values"]['graph'] = section_graph

    ## conclusion
    section_graph = nx.MultiDiGraph()
    section_graph.add_node("share_conclusion_boilerplate", function=share_conclusion_boilerplate, function_args={})
    interview_graph.nodes["conclusion"]['graph'] = section_graph
    
    return interview_graph