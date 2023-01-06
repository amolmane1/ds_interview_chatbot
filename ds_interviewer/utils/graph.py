# TODO: add all graph related code here

import networkx as nx

from nodes.node_functions import *
# func to save graph to file
# func to load graph from file
# func to create a a flowchart based on certain specifications & then save to file

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
                                 function_args={'model_version': "4.1.23"}, 
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