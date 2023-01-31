from utils.utils import default_arguments_for_openai_generation, default_arguments_for_openai_validation, create_openai_completion, \
    prepare_kshot_prompt_using_levenshtein_distance, parse_completion_args
from utils.models_metadata import get_model_metadata
from finetuning.prepare_data import submit_observation_for_finetuning_validation


def run_validate_node(completion_args_to_use_for_interview):
    routing_value = int(completion_args_to_use_for_interview['validation_of_response'])
    return dict(routing_value=routing_value, 
                new_chat_lines=None)


def run_route_node(completion_args_to_use_for_interview):
    routing_value = int(completion_args_to_use_for_interview['route'])
    return dict(routing_value=routing_value, 
                new_chat_lines=None)


def run_dialogue_node(completion_args_to_use_for_interview):
    if "interviewer_dialogue" in completion_args_to_use_for_interview:
        new_chat_lines = ["Interviewer: " + completion_args_to_use_for_interview['interviewer_dialogue']]
    elif "applicant_dialogue" in completion_args_to_use_for_interview:
        new_chat_lines = ["Applicant: " + completion_args_to_use_for_interview['applicant_dialogue']]
    return dict(routing_value=None, 
                new_chat_lines=new_chat_lines)


def run_node(node_type, model_name, prompt_args, other_args, validate_async=True):
    model_version = other_args["model_version"] if "model_version" in other_args.keys() else None
    model_metadata, model_version = get_model_metadata(model_name, model_version)
    observation_prompt = model_metadata['prompt_template'].format(**prompt_args)
    
    kshot_prompt = prepare_kshot_prompt_using_levenshtein_distance(model_name=model_name, 
                                                               model_metadata=model_metadata, 
                                                               prompt_args=prompt_args, 
                                                               observation_prompt=observation_prompt)

    if node_type == "dialogue":
        openai_args = default_arguments_for_openai_generation
    elif node_type == "validate":
        openai_args = default_arguments_for_openai_validation
    elif node_type == "route":
        openai_args = default_arguments_for_openai_validation
    completion = create_openai_completion(kshot_prompt, model_metadata=model_metadata, args=openai_args)
    
    completion_args = parse_completion_args(completion, model_metadata)
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
    
    if node_type == "dialogue":
        result = run_dialogue_node(completion_args_to_use_for_interview)
    elif node_type == "validate":
        result = run_validate_node(completion_args_to_use_for_interview)
    elif node_type == "route":
        result = run_route_node(completion_args_to_use_for_interview)
    return result