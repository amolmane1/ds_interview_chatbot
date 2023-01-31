from utils.utils import default_arguments_for_openai_generation, default_arguments_for_openai_validation, create_openai_completion, get_label_for_correct_or_incorrect_completion, \
    prepare_chat_history, prepare_kshot_prompt_using_levenshtein_distance, get_user_input, deep_get
from utils.models_metadata import get_model_metadata
from finetuning.prepare_data import submit_observation_for_finetuning_validation
from parse import parse
from nodes.helpers import run_node


def share_introduction_boilerplate(**kwargs):
    new_chat_lines = ["""Interviewer: Thank you for taking the time out to interview with us. 
    In this interview, we will cover a range of topics and ask questions to assess your skill level as a Data Scientist. 
    If you don't understand a question, feel free to ask questions to get clarification.
    Let's get started."""]
    return dict(routing_value=None, 
                new_chat_lines=new_chat_lines) 


def get_response_from_python_input(**kwargs):
    new_chat_lines = []
    new_chat_lines.append(get_user_input)
    return dict(routing_value=None, 
                new_chat_lines=new_chat_lines)


def get_response_from_applicant_persona(carryover_data, validate_async=True, chat_history_by_section=[[]], **kwargs):
    model_name = "respond_to_interviewer"
    prompt_args = dict(
        objectives_and_constraints = deep_get(carryover_data, ['data_challenge_objectives_and_constraints'], "NA"), 
        what_applicant_did_for_each_section = deep_get(carryover_data, ['applicant_data', 'applicant_context'], "NA"),
        insights = deep_get(carryover_data, ['applicant_data', 'insights'], "NA"),
        current_section_chat = prepare_chat_history(chat_history_by_section[-1]),
        applicant_skill_summary = deep_get(carryover_data, ['applicant_data', 'applicant_skill_summary'], "NA"),
        is_completion_correct=1)
    return run_node(node_type="dialogue", 
            model_name=model_name, 
            prompt_args=prompt_args, 
            other_args=kwargs, 
            validate_async=validate_async)


def share_conclusion_boilerplate(**kwargs):
    new_chat_lines = ["""Interviewer: Okay, those were all the topics we wanted to cover. Thank you again for taking the time out to interview with us.
    We will get back to you with our decision. Have a nice day!"""]
    return dict(routing_value=None, 
                new_chat_lines=new_chat_lines) 


def confirm_what_applicant_did(current_section_name, carryover_data, validate_async=True, chat_history_by_section=[[]], **kwargs):
    model_name = "confirm_what_applicant_did"
    prompt_args = dict(
                    context=carryover_data['what_interviewer_thinks_applicant_has_done_in_ipynb'],
                    current_section_chat=prepare_chat_history(chat_history_by_section[-1]),
                    section=current_section_name,
                    is_completion_correct=1)
    return run_node(node_type="dialogue", 
                    model_name=model_name, 
                    prompt_args=prompt_args, 
                    other_args=kwargs, 
                    validate_async=validate_async)


def route_answer_to_confirm_what_applicant_did(validate_async=True, chat_history_by_section=[[]], **kwargs):
    model_name = "route_answer_to_confirm_what_applicant_did"
    model_metadata, model_version = get_model_metadata(model_name, kwargs["model_version"] if "model_version" in kwargs.keys() else None)
    prompt_args = dict(
        current_section_chat=prepare_chat_history(chat_history_by_section[-1]),
                      is_completion_correct=1)
    observation_prompt = model_metadata['prompt_template'].format(**prompt_args)
    
    kshot_prompt = prepare_kshot_prompt_using_levenshtein_distance(model_name=model_name, 
                                                                   model_metadata=model_metadata, 
                                                                   prompt_args=prompt_args, 
                                                                   observation_prompt=observation_prompt)
    completion = create_openai_completion(kshot_prompt, model_metadata=model_metadata, args=default_arguments_for_openai_validation)

    completion_args = parse(model_metadata['completion_template'], 
                            completion).named
    observation_details = dict(model_name=model_name, 
                               model_version=model_version,
                               prompt_template=model_metadata['prompt_template'], 
                               completion_template=model_metadata['completion_template'], 
                               prompt_args=prompt_args, 
                               completion_args=completion_args,
                               prompt = observation_prompt,
                               completion=completion)
    completion_args_to_use_for_interview = submit_observation_for_finetuning_validation(observation_details, 
                                                                                        validate_async=validate_async)

    routing_value = int(completion_args_to_use_for_interview['route'])
    return dict(routing_value=routing_value, 
                new_chat_lines=None)


def ask_what_applicant_did(current_section_name, carryover_data, validate_async=True, chat_history_by_section=[[]], **kwargs):
    model_name = "ask_what_applicant_did"
    model_metadata, model_version = get_model_metadata(model_name, kwargs["model_version"] if "model_version" in kwargs.keys() else None)
    prompt_args = dict(
        current_section_chat=prepare_chat_history(chat_history_by_section[-1]),
                      subject=current_section_name,
                      is_completion_correct=1)
    observation_prompt = model_metadata['prompt_template'].format(**prompt_args)
    
    kshot_prompt = prepare_kshot_prompt_using_levenshtein_distance(model_name=model_name, 
                                                                   model_metadata=model_metadata, 
                                                                   prompt_args=prompt_args, 
                                                                   observation_prompt=observation_prompt)
    completion = create_openai_completion(kshot_prompt, model_metadata=model_metadata, args=default_arguments_for_openai_generation)
    
    completion_args = parse(model_metadata['completion_template'], 
                            completion).named
    observation_details = dict(model_name=model_name, 
                               model_version=model_version,
                               prompt_template=model_metadata['prompt_template'], 
                               completion_template=model_metadata['completion_template'], 
                               prompt_args=prompt_args, 
                               completion_args=completion_args,
                               prompt = observation_prompt,
                               completion=completion)
    completion_args_to_use_for_interview = submit_observation_for_finetuning_validation(observation_details, 
                                                                                        validate_async=validate_async)

    new_chat_lines = []
    new_chat_lines.append("Interviewer: " + completion_args_to_use_for_interview['interviewer_dialogue'])
    # new_chat_lines.append(get_user_input())
    return dict(routing_value=None, 
                new_chat_lines=new_chat_lines)


def route_answer_to_ask_what_applicant_did(validate_async=True, chat_history_by_section=[[]], **kwargs):
    model_name = "route_answer_to_ask_what_applicant_did"
    model_metadata, model_version = get_model_metadata(model_name, kwargs["model_version"] if "model_version" in kwargs.keys() else None)
    prompt_args = dict(
        current_section_chat=prepare_chat_history(chat_history_by_section[-1]),
                      is_completion_correct=1)
    observation_prompt = model_metadata['prompt_template'].format(**prompt_args)
    
    kshot_prompt = prepare_kshot_prompt_using_levenshtein_distance(model_name=model_name, 
                                                                   model_metadata=model_metadata, 
                                                                   prompt_args=prompt_args, 
                                                                   observation_prompt=observation_prompt)
    completion = create_openai_completion(kshot_prompt, model_metadata=model_metadata, args=default_arguments_for_openai_validation)

    completion_args = parse(model_metadata['completion_template'], 
                            completion).named
    observation_details = dict(model_name=model_name, 
                               model_version=model_version,
                               prompt_template=model_metadata['prompt_template'], 
                               completion_template=model_metadata['completion_template'], 
                               prompt_args=prompt_args, 
                               completion_args=completion_args,
                               prompt = observation_prompt,
                               completion=completion)
    completion_args_to_use_for_interview = submit_observation_for_finetuning_validation(observation_details, 
                                                                                        validate_async=validate_async)

    routing_value = int(completion_args_to_use_for_interview['route'])
    return dict(routing_value=routing_value, 
                new_chat_lines=None)


def ask_how_it_works(current_section_name, carryover_data, validate_async=True, chat_history_by_section=[[]], **kwargs):
    model_name = "ask_how_it_works"
    model_metadata, model_version = get_model_metadata(model_name, kwargs["model_version"] if "model_version" in kwargs else None)
    prompt_args = dict(current_section_chat=prepare_chat_history(chat_history_by_section[-1]),
                       subject=kwargs['subject'] if 'subject' in kwargs else 'NA',
                      question_type="how it works",
                      is_completion_correct=1)
    observation_prompt = model_metadata['prompt_template'].format(**prompt_args)
    
    kshot_prompt = prepare_kshot_prompt_using_levenshtein_distance(model_name=model_name, 
                                                                   model_metadata=model_metadata, 
                                                                   prompt_args=prompt_args, 
                                                                   observation_prompt=observation_prompt)
    completion = create_openai_completion(kshot_prompt, model_metadata=model_metadata, args=default_arguments_for_openai_generation)
    
    completion_args = parse(model_metadata['completion_template'], 
                            completion).named
    observation_details = dict(model_name=model_name, 
                               model_version=model_version,
                               prompt_template=model_metadata['prompt_template'], 
                               completion_template=model_metadata['completion_template'], 
                               prompt_args=prompt_args, 
                               completion_args=completion_args,
                               prompt = observation_prompt,
                               completion=completion)
    completion_args_to_use_for_interview = submit_observation_for_finetuning_validation(observation_details, 
                                                                                        validate_async=validate_async)

    new_chat_lines = []
    new_chat_lines.append("Interviewer: " + completion_args_to_use_for_interview['interviewer_dialogue'])
    # new_chat_lines.append(get_user_input())
    return dict(routing_value=None, 
                new_chat_lines=new_chat_lines)


def validate_answer_how_it_works(current_section_name, carryover_data, validate_async=True, chat_history_by_section=[[]], **kwargs):
    model_name = "validate_answer_how_it_works"
    model_metadata, model_version = get_model_metadata(model_name, kwargs["model_version"] if "model_version" in kwargs.keys() else None)
    
    prompt_args = dict(current_section_chat=prepare_chat_history(chat_history_by_section[-1]),
                      question_type="how it works",
                      is_completion_correct=1)
    observation_prompt = model_metadata['prompt_template'].format(**prompt_args)
    
    kshot_prompt = prepare_kshot_prompt_using_levenshtein_distance(model_name=model_name, 
                                                               model_metadata=model_metadata, 
                                                               prompt_args=prompt_args, 
                                                               observation_prompt=observation_prompt)
    completion = create_openai_completion(kshot_prompt, model_metadata=model_metadata, args=default_arguments_for_openai_validation)
    
    # this assumes completion always follows the template. what if it doesn't?
    completion_args = parse(model_metadata['completion_template'], 
                            completion).named
    observation_details = dict(model_name=model_name, 
                               model_version=model_version,
                               prompt_template=model_metadata['prompt_template'], 
                               completion_template=model_metadata['completion_template'], 
                               prompt_args=prompt_args, 
                               completion_args=completion_args,
                               prompt = observation_prompt,
                               completion=completion)
    completion_args_to_use_for_interview = submit_observation_for_finetuning_validation(observation_details, 
                                                                                        validate_async=validate_async)

    routing_value = int(completion_args_to_use_for_interview['validation_of_response'])
    return dict(routing_value=routing_value, 
                new_chat_lines=None)


def route_answer_to_what_other_options_applicant_considered(carryover_data, validate_async=True, chat_history_by_section=[[]], **kwargs):
    model_name = "route_answer_to_what_other_options_applicant_considered"
    model_metadata, model_version = get_model_metadata(model_name, kwargs["model_version"] if "model_version" in kwargs.keys() else None)
    prompt_args = dict(
        current_section_chat=prepare_chat_history(chat_history_by_section[-1]),
                      is_completion_correct=1)
    observation_prompt = model_metadata['prompt_template'].format(**prompt_args)
    
    kshot_prompt = prepare_kshot_prompt_using_levenshtein_distance(model_name=model_name, 
                                                                   model_metadata=model_metadata, 
                                                                   prompt_args=prompt_args, 
                                                                   observation_prompt=observation_prompt)
    completion = create_openai_completion(kshot_prompt, model_metadata=model_metadata, args=default_arguments_for_openai_validation)

    completion_args = parse(model_metadata['completion_template'], 
                            completion).named
    observation_details = dict(model_name=model_name, 
                               model_version=model_version,
                               prompt_template=model_metadata['prompt_template'], 
                               completion_template=model_metadata['completion_template'], 
                               prompt_args=prompt_args, 
                               completion_args=completion_args,
                               prompt = observation_prompt,
                               completion=completion)
    completion_args_to_use_for_interview = submit_observation_for_finetuning_validation(observation_details, 
                                                                                        validate_async=validate_async)

    routing_value = int(completion_args_to_use_for_interview['route'])
    return dict(routing_value=routing_value, 
                new_chat_lines=None)


def ask_what_other_options_applicant_considered(carryover_data, validate_async=True, chat_history_by_section=[[]], **kwargs):
    model_name = "ask_what_other_options_applicant_considered"
    model_metadata, model_version = get_model_metadata(model_name, kwargs["model_version"] if "model_version" in kwargs else None)
    prompt_args = dict(current_section_chat=prepare_chat_history(chat_history_by_section[-1]),
                      is_completion_correct=1)
    observation_prompt = model_metadata['prompt_template'].format(**prompt_args)
    
    kshot_prompt = prepare_kshot_prompt_using_levenshtein_distance(model_name=model_name, 
                                                                   model_metadata=model_metadata, 
                                                                   prompt_args=prompt_args, 
                                                                   observation_prompt=observation_prompt)
    completion = create_openai_completion(kshot_prompt, model_metadata=model_metadata, args=default_arguments_for_openai_generation)
    
    completion_args = parse(model_metadata['completion_template'], 
                            completion).named
    observation_details = dict(model_name=model_name, 
                               model_version=model_version,
                               prompt_template=model_metadata['prompt_template'], 
                               completion_template=model_metadata['completion_template'], 
                               prompt_args=prompt_args, 
                               completion_args=completion_args,
                               prompt = observation_prompt,
                               completion=completion)
    completion_args_to_use_for_interview = submit_observation_for_finetuning_validation(observation_details, 
                                                                                        validate_async=validate_async)

    new_chat_lines = []
    new_chat_lines.append("Interviewer: " + completion_args_to_use_for_interview['interviewer_dialogue'])
    # new_chat_lines.append(get_user_input())
    return dict(routing_value=None, 
                new_chat_lines=new_chat_lines)


def validate_why_applicant_picked_X_over_Y(carryover_data, validate_async=True, chat_history_by_section=[[]], **kwargs):
    model_name = "validate_why_applicant_picked_X_over_Y"
    prompt_args = dict(
        objectives_and_constraints = deep_get(carryover_data, ['data_challenge_objectives_and_constraints'], "NA"), 
        what_applicant_did_for_each_section = deep_get(carryover_data, ['applicant_data', 'applicant_context'], "NA"),
        insights = deep_get(carryover_data, ['applicant_data', 'insights'], "NA"),
        current_section_chat=prepare_chat_history(chat_history_by_section[-1]),
        is_completion_correct=1)
    return run_node(node_type="validate", 
                    model_name=model_name, 
                    prompt_args=prompt_args, 
                    other_args=kwargs, 
                    validate_async=validate_async)


def ask_why_applicant_picked_X_over_Y(validate_async=True, chat_history_by_section=[[]], **kwargs):
    model_name = "ask_why_applicant_picked_X_over_Y"
    model_metadata, model_version = get_model_metadata(model_name, kwargs["model_version"] if "model_version" in kwargs.keys() else None)

    prompt_args = dict(current_section_chat=prepare_chat_history(chat_history_by_section[-1]),
                    is_completion_correct=1)
    observation_prompt = model_metadata['prompt_template'].format(**prompt_args)
    
    kshot_prompt = prepare_kshot_prompt_using_levenshtein_distance(model_name=model_name, 
                                                               model_metadata=model_metadata, 
                                                               prompt_args=prompt_args, 
                                                               observation_prompt=observation_prompt)
    completion = create_openai_completion(kshot_prompt, model_metadata=model_metadata, args=default_arguments_for_openai_validation)
    
    completion_args = parse(model_metadata['completion_template'], 
                            completion).named
    observation_details = dict(model_name=model_name, 
                               model_version=model_version,
                               prompt_template=model_metadata['prompt_template'], 
                               completion_template=model_metadata['completion_template'], 
                               prompt_args=prompt_args, 
                               completion_args=completion_args,
                               prompt = observation_prompt,
                               completion=completion)
    completion_args_to_use_for_interview = submit_observation_for_finetuning_validation(observation_details, 
                                                                                        validate_async=validate_async)

    new_chat_lines = []
    new_chat_lines.append("Interviewer: " + completion_args_to_use_for_interview['interviewer_dialogue'])
    # new_chat_lines.append(get_user_input())
    return dict(routing_value=None, 
                new_chat_lines=new_chat_lines)


def validate_answer_devils_advocate(carryover_data, validate_async=True, chat_history_by_section=[[]], **kwargs):
    model_name = "validate_answer_devils_advocate"
    prompt_args = dict(what_applicant_did_for_each_section=carryover_data['what_interviewer_thinks_applicant_has_done_in_ipynb'],
                    objectives_and_constraints=carryover_data['data_challenge_objectives_and_constraints'],
                    insights=carryover_data['insights'],
                    current_section_chat=prepare_chat_history(chat_history_by_section[-1]),
                    is_completion_correct=1)
    return run_node(node_type="validate", 
                    model_name=model_name, 
                    prompt_args=prompt_args, 
                    other_args=kwargs, 
                    validate_async=validate_async)


def ask_devils_advocate_question(carryover_data, validate_async=True, chat_history_by_section=[[]], **kwargs):
    model_name = "ask_devils_advocate_question"
    prompt_args = dict(what_applicant_did_for_each_section=carryover_data['what_interviewer_thinks_applicant_has_done_in_ipynb'],
                    objectives_and_constraints=carryover_data['data_challenge_objectives_and_constraints'],
                    insights=carryover_data['insights'],
                    current_section_chat=prepare_chat_history(chat_history_by_section[-1]),
                    is_completion_correct=1)
    return run_node(node_type="dialogue", 
                model_name=model_name, 
                prompt_args=prompt_args, 
                other_args=kwargs, 
                validate_async=validate_async)


def ask_what_applicant_would_choose_given_requirement(current_section_name, carryover_data, validate_async=True, chat_history_by_section=[[]], **kwargs):
    model_name = "ask_what_applicant_would_choose_given_requirement"
    prompt_args = dict(what_applicant_did_for_each_section=carryover_data['what_interviewer_thinks_applicant_has_done_in_ipynb'],
                    objectives_and_constraints=carryover_data['data_challenge_objectives_and_constraints'],
                    insights=carryover_data['insights'],
                    current_section_chat=prepare_chat_history(chat_history_by_section[-1]),
                    subject_1=deep_get(carryover_data, ['sections', current_section_name, model_name, 'prompt_args', 'subject_1'], "NA"),
                    subject_2=deep_get(carryover_data, ['sections', current_section_name, model_name, 'prompt_args', 'subject_2'], "NA"),
                    is_completion_correct=1)
    return run_node(node_type="dialogue", 
                model_name=model_name, 
                prompt_args=prompt_args, 
                other_args=kwargs, 
                validate_async=validate_async)


def validate_what_applicant_would_choose_given_requirement(carryover_data, validate_async=True, chat_history_by_section=[[]], **kwargs):
    model_name = "validate_what_applicant_would_choose_given_requirement"
    prompt_args = dict(what_applicant_did_for_each_section=carryover_data['what_interviewer_thinks_applicant_has_done_in_ipynb'],
                    objectives_and_constraints=carryover_data['data_challenge_objectives_and_constraints'],
                    insights=carryover_data['insights'],
                    current_section_chat=prepare_chat_history(chat_history_by_section[-1]),
                    is_completion_correct=1)
    return run_node(node_type="validate", 
                    model_name=model_name, 
                    prompt_args=prompt_args, 
                    other_args=kwargs, 
                    validate_async=validate_async)


def clarify_question_on_how_it_works(current_section_name, carryover_data, validate_async=True, chat_history_by_section=[[]], **kwargs):
    pass


def ask_followup_question_on_how_it_works(current_section_name, carryover_data, validate_async=True, chat_history_by_section=[[]], **kwargs):
    pass


def empty_node(**kwargs):
    return dict(routing_value=None, 
                new_chat_lines=None)
