from prompt_templates import kshot_prompt_templates
from utils.utils import log_completion_call, default_arguments_for_openai_classification, default_arguments_for_openai_generation, default_arguments_for_openai_validation, \
    ask_gpt, get_feedback, ask_gpt_get_feedback_and_log, create_openai_completion, get_label_for_correct_or_incorrect_completion, path_to_finetuning_data_folder, \
    prepare_chat_history, prepare_kshot_prompt_using_levenshtein_distance
from utils.models_metadata import get_model_metadata
from finetuning.prepare_data import submit_observation_for_finetuning_validation
from parse import parse


def share_introduction_boilerplate(**kwargs):
    new_chat_line = """Interviewer: Thank you for taking the time out to interview with us. 
    In this interview, we will cover a range of topics and ask questions to assess your skill level as a Data Scientist. 
    If you don't understand a question, feel free to ask questions to get clarification.
    Let's get started."""
    return dict(routing_value=None, 
                new_chat_line=new_chat_line) 


def get_applicant_input(**kwargs):
    user_input = input("Applicant: ")
    new_chat_line = "Applicant: {}".format(user_input)
    return dict(routing_value=None, 
                new_chat_line=new_chat_line) 


def share_conclusion_boilerplate(**kwargs):
    new_chat_line = """Interviewer: Okay, those were all the topics we wanted to cover. Thank you again for taking the time out to interview with us.
    We will get back to you with our decision. Have a nice day!"""
    return dict(routing_value=None, 
                new_chat_line=new_chat_line) 


def ask_how_it_works(carryover_data, chat_history_by_section=[[]], **kwargs):
    model_metadata, model_version = get_model_metadata('ask_how_it_works', kwargs["model_version"] if "model_version" in kwargs.keys() else None)
    prompt_args = dict(current_section_chat=prepare_chat_history(chat_history_by_section[-1]),
                       # how do i make this function handle any interview section, not just algo selection?
                      subject=carryover_data['algorithm_selection']['subject'],
                      question_type="how it works",
                      is_completion_correct=1)
    observation_prompt = model_metadata['prompt_template'].format(**prompt_args)
    
    kshot_prompt = prepare_kshot_prompt_using_levenshtein_distance(model_name='ask_how_it_works', 
                                                                   model_metadata=model_metadata, 
                                                                   prompt_args=prompt_args, 
                                                                   observation_prompt=observation_prompt)
    completion = create_openai_completion(kshot_prompt, args=default_arguments_for_openai_generation)
    
    # this assumes completion always follows the template. what if it doesn't?
    completion_args = parse(model_metadata['completion_template'], 
                            completion).named
    observation_details = dict(model_name="ask_how_it_works", 
                               model_version=model_version,
                               prompt_template=model_metadata['prompt_template'], 
                               completion_template=model_metadata['completion_template'], 
                               prompt_args=prompt_args, 
                               completion_args=completion_args,
                               prompt = observation_prompt,
                               completion=completion)
    completion_args_to_use_for_interview = submit_observation_for_finetuning_validation(observation_details, 
                                                                                        validate_async=False)

    new_chat_line = "Interviewer: " + completion_args_to_use_for_interview['interviewer_dialogue']
    return dict(routing_value=None, 
                new_chat_line=new_chat_line)    


def validate_answer_how_it_works(carryover_data, chat_history_by_section=[[]], **kwargs):
    model_metadata, model_version = get_model_metadata('validate_answer_how_it_works', kwargs["model_version"] if "model_version" in kwargs.keys() else None)
    
    # prompt_template = models_metadata['ask_how_it_works'][-1]['prompt_template']
    prompt_args = dict(current_section_chat=prepare_chat_history(chat_history_by_section[-1]),
                      question_type="how it works",
                      is_completion_correct=1)
    observation_prompt = model_metadata['prompt_template'].format(**prompt_args)
    
    kshot_prompt = prepare_kshot_prompt_using_levenshtein_distance(model_name='validate_answer_how_it_works', 
                                                               model_metadata=model_metadata, 
                                                               prompt_args=prompt_args, 
                                                               observation_prompt=observation_prompt)
    completion = create_openai_completion(kshot_prompt, args=default_arguments_for_openai_generation)
    
    # this assumes completion always follows the template. what if it doesn't?
    completion_args = parse(model_metadata['completion_template'], 
                            completion).named
    observation_details = dict(model_name="validate_answer_how_it_works", 
                               model_version=model_version,
                               prompt_template=model_metadata['prompt_template'], 
                               completion_template=model_metadata['completion_template'], 
                               prompt_args=prompt_args, 
                               completion_args=completion_args,
                               prompt = observation_prompt,
                               completion=completion)
    completion_args_to_use_for_interview = submit_observation_for_finetuning_validation(observation_details, 
                                                                                        validate_async=False)

    routing_value = int(completion_args_to_use_for_interview['validation_of_response'])
    return dict(routing_value=routing_value, 
                new_chat_line=None)    


def clarify_question_on_how_it_works(carryover_data, chat_history_by_section=[[]], kwargs={}):
    pass


def ask_followup_question_on_how_it_works(carryover_data, chat_history_by_section=[[]], kwargs={}):
    pass