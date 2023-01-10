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
    # create interview flow graph
    # every node must contain an attibute with the name of the function that needs to be called
    # every edge from a classifier node contains the output values which would cause the node it goes to to be activated
    # every node that has one outgoing edge is assumed to be a generative node

    # first node is to greet the applicant and share expectations / other boilerplate info
    # last node is to conclude the interview

    interview_flowchart = nx.MultiDiGraph()

    interview_flowchart.add_node("introduction-share_boilerplate", 
                                 function=share_introduction_boilerplate, 
                                 function_args={}, 
                                 show_output_in_chat=True)

    interview_flowchart.add_node("algorithm_selection-ask_how_it_works", 
                                 function=ask_how_it_works, 
                                 # function_args={"approach": "Linear Regression"}, 
                                 # function_args={'model_version': "04.01.23"}, 
                                 function_args={}, 
                                 show_output_in_chat=True)
    interview_flowchart.add_edge("introduction-share_boilerplate", 
                                 "algorithm_selection-ask_how_it_works")

    interview_flowchart.add_node("algorithm_selection-get_applicant_input", 
                                 function=get_applicant_input, function_args={}, 
                                 show_output_in_chat=True)
    interview_flowchart.add_edge("algorithm_selection-ask_how_it_works", 
                                 "algorithm_selection-get_applicant_input")

    interview_flowchart.add_node("algorithm_selection-validate_answer_how_it_works", 
                                 function=validate_answer_how_it_works, 
                                 function_args={}, 
                                 show_output_in_chat=False)
    interview_flowchart.add_edge("algorithm_selection-get_applicant_input", 
                                 "algorithm_selection-validate_answer_how_it_works")

    interview_flowchart.add_node("algorithm_selection-ask_followup_question_on_how_it_works", 
                                 function=ask_followup_question_on_how_it_works, 
                                 function_args={}, 
                                 show_output_in_chat=True)
    interview_flowchart.add_edge("algorithm_selection-validate_answer_how_it_works", 
                                 "algorithm_selection-ask_followup_question_on_how_it_works", 
                                 # passthrough_values=[2],
                                 passthrough_values=[],
                                ) # 0 means ADNU, 1=incorrect, 2=incomplete, 3=correct
    interview_flowchart.add_edge("algorithm_selection-ask_followup_question_on_how_it_works", 
                                 "algorithm_selection-get_applicant_input")

    interview_flowchart.add_node("algorithm_selection-clarify_question_on_how_it_works", 
                                 function=clarify_question_on_how_it_works, 
                                 function_args={}, 
                                 show_output_in_chat=True)
    interview_flowchart.add_edge("algorithm_selection-validate_answer_how_it_works", 
                                 "algorithm_selection-clarify_question_on_how_it_works", 
                                 # passthrough_values=[2],
                                 passthrough_values=[],
                                ) # 0 means ADNU, 1=incorrect, 2=incomplete, 3=correct
    interview_flowchart.add_edge("algorithm_selection-clarify_question_on_how_it_works", 
                                 "algorithm_selection-get_applicant_input")

    interview_flowchart.add_node("conclusion-share_boilerplate", 
                                 function=share_conclusion_boilerplate, 
                                 function_args={}, 
                                 show_output_in_chat=True)
    interview_flowchart.add_edge("algorithm_selection-validate_answer_how_it_works", 
                                 "conclusion-share_boilerplate", 
                                 passthrough_values=[1, 3, 0, 2])
    
    interview_flowchart_visual = nx.nx_agraph.to_agraph(interview_flowchart)
    interview_flowchart_visual.layout(prog='dot')
    # interview_flowchart_visual
    # A.draw('test.png') # save to file
    
    return interview_flowchart, interview_flowchart_visual


def create_interview_flowchart2():
    interview_graph = nx.MultiDiGraph()
    interview_graph.add_node("introduction")
    interview_graph.add_node("algorithm selection")
    interview_graph.add_node("dealing with categorical values")
    interview_graph.add_node("conclusion")
    interview_graph.add_edge("introduction", "algorithm selection")
    interview_graph.add_edge("algorithm selection", "dealing with categorical values")
    interview_graph.add_edge("dealing with categorical values", "conclusion")

    section_graph = nx.MultiDiGraph()
    section_graph.add_node("share_introduction_boilerplate", function=share_introduction_boilerplate, function_args={})
    # section_graph.add_node(share_introduction_boilerplate, function_args={})
    interview_graph.nodes["introduction"]['graph'] = section_graph

    section_graph = nx.MultiDiGraph()
    section_graph.add_node("ask_what_you_did", function=ask_what_you_did, function_args={})
    section_graph.add_node("ask_how_it_works", function=ask_how_it_works, function_args={})
    section_graph.add_node("validate_answer_how_it_works", function=validate_answer_how_it_works, function_args={})
    section_graph.add_edge("ask_what_you_did", "ask_how_it_works")
    section_graph.add_edge("ask_how_it_works", "validate_answer_how_it_works")
    interview_graph.nodes["algorithm selection"]['graph'] = section_graph

    section_graph = nx.MultiDiGraph()
    section_graph.add_node("ask_what_you_did", function=ask_what_you_did, function_args={})
    section_graph.add_node("ask_how_it_works", function=ask_how_it_works, function_args={})
    section_graph.add_node("validate_answer_how_it_works", function=validate_answer_how_it_works, function_args={})
    section_graph.add_edge("ask_what_you_did", "ask_how_it_works")
    section_graph.add_edge("ask_how_it_works", "validate_answer_how_it_works")
    interview_graph.nodes["dealing with categorical values"]['graph'] = section_graph

    section_graph = nx.MultiDiGraph()
    # section_graph.add_node("share_introduction_boilerplate", function=share_introduction_boilerplate, function_args={})
    section_graph.add_node("share_conclusion_boilerplate", function=share_conclusion_boilerplate, function_args={})
    interview_graph.nodes["conclusion"]['graph'] = section_graph
    
    return interview_graph