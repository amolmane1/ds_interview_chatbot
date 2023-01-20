import os
from pathlib import Path
import json
import openai
import pandas as pd
import logging
from IPython.display import clear_output
import inspect
from jellyfish import levenshtein_distance

from utils.models_metadata import get_model_metadata

openai.api_key = os.getenv("OPENAI_API_KEY")
logging.basicConfig(filename='/Users/amolmane/Documents/ds_interview_chatbot/logs/orchestrator_v0.2.log', 
                    format='%(asctime)s - %(levelname)s:\n%(message)s\n*************************************************************************\n\n', 
                    datefmt="%m/%d/%Y %I:%M:%S %p %Z",
                   level=logging.INFO)


def log_completion_and_feedback(args, running_prompt, gpt_response, topic='misc', tag='', label='', reason='', notes='', insights=''):
    logging.info(
"""Parameters:
{0}
***************
Prompt:
{1}
***************
Output:
{2}
***************
Tag: {3}
Topic: {4}
Label: {5}
Reason: {6}
Insights: {7}
""".format(args,
            running_prompt,
            gpt_response,
            tag,
            topic,
            label, 
            reason,
            insights))
    
    
def log_completion(prompt, completion):
    logging.info(
"""***************
Prompt:
{0}
***************
Completion:
{1}
***************
""".format(prompt,
           completion))


path_to_finetuning_data_folder = "../data/fine_tuning_data/"
    
    
default_arguments_for_openai_classification = dict(
    model="text-davinci-003",
    temperature=0,
    top_p=1,
    n=1,
    frequency_penalty=0,
    presence_penalty=0,
    max_tokens=1)

default_arguments_for_openai_generation = dict(
    model="text-davinci-003",
    temperature=0.7,
    top_p=1,
    n=1,
    frequency_penalty=0,
    presence_penalty=0,
    max_tokens=200)

default_arguments_for_openai_validation = dict(
    model="text-davinci-003",
    temperature=0,
    top_p=1,
    n=1,
    frequency_penalty=0,
    presence_penalty=0,
    max_tokens=200)


def get_default_args(func):
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }


def ask_gpt(prompt, args=default_arguments_for_openai_generation, to_print=False):
    gpt_response = openai.Completion.create(
            prompt=prompt,
            **args
        ).choices[0].text.lstrip()
    if to_print:
        clear_output()
        print("{0}{1}".format(prompt, gpt_response))
    return gpt_response


def get_feedback(starting_tag):
    # get tag, label, reason, and insights
    tag = input("Tag: ")
    if tag == '':
        tag = starting_tag
    label = input("Label: ")
    reason = input("Reason: ")
    insights = input("Insights: ")
    return tag, label, reason, insights


def ask_gpt_get_feedback_and_log(prompt, topic='misc', args=default_arguments_for_openai_generation, starting_tag=''):
    gpt_response = ask_gpt(prompt, args)
    tag, label, reason, insights = get_feedback(starting_tag)
    log_completion_and_feedback(args, prompt, gpt_response, topic, tag=tag, label=label, reason=reason, insights=insights)
    return gpt_response


def get_label_for_correct_or_incorrect_completion():
    label = input("Is completion correct? (1/0): ")
    label = int(label)
    # TODO: add assert to make sure it is either 1 or 0.
    return label


def get_label_for_validating_answer_completion():
    label = input("Label (0=ADNU, 1=incorrect, 2=incomplete, 3=correct): ")
    label = int(label)
    # TODO: add assert to make sure it is either 0/1/2/3.
    return label


def get_label_for_routing_answer_completion():
    label = input("Label: ")
    label = int(label)
    # TODO: add assert to make sure it is either 0/1/2/3.
    return label


def get_user_input(prompt="Applicant: "):
    user_input = input(prompt)
    new_chat_line = prompt + user_input
    return new_chat_line


def create_openai_completion(prompt, stop_sequence=None, args=default_arguments_for_openai_generation):
    args['stop'] = stop_sequence
    completion = openai.Completion.create(
            prompt=prompt,
            **args
        ).choices[0].text.strip()
    log_completion(prompt, completion)
    return completion


tags_map = {
'q': 'question',
'cq': 'clarify question for applicant',
'fu': 'ask followup question',
'cf': 'counterfactual',
'da': "devil's advocate",
'k': 'acknowledge answer',
'a': 'answer',
's': 'signpost',
'f': 'filler', 
'g': 'grading',
'c': 'complete',
'vj': 'validate jim',
'va': 'validate applicant',
}


# def get_subject_for_node_function(carryover_data, ):
    


def prepare_chat_history(chat_history=[], max_length=800, empty_value='NA'):
    """
    called by node functions before formatting prompt.
    - trims chat history to ensure it is not longer than a certain amount.
    - also adds 'NA' if chat history is empty (we need to do this because parser.parse doesnt work when chat history is an empty string)
    
    max_length: int - 800 implies 200 tokens
    """
    prepared_chat_history = None
    if chat_history == []:
        prepared_chat_history = empty_value
    else:
        chat_history_length = 0
        for line in reversed(chat_history):
            line_length = len(line)
            if (chat_history_length + line_length) <= max_length:
                if prepared_chat_history:
                    prepared_chat_history = "\n".join([line, prepared_chat_history])
                else:
                    prepared_chat_history = line
                chat_history_length += line_length
            else:
                break
    return prepared_chat_history


def calculate_levenshtein_distance_for_intersecting_args(row, prompt_args, prompt_args_json):
    row_args = row.to_dict()
    relevant_row_args = {key: row_args[key] for key in prompt_args.keys()}
    relevant_row_args_json = json.dumps(relevant_row_args)
    return levenshtein_distance(prompt_args_json, relevant_row_args_json)


def format_observation_template_with_args(row, prompt_template, completion_template):
    args = row.to_dict()
    prompt = prompt_template.format(**args)
    completion = completion_template.format(**args)
    observation = prompt + completion
    return observation


def prepare_kshot_prompt_using_levenshtein_distance(model_name, model_metadata, prompt_args, observation_prompt=None, max_tokens=1800):
    """
    gets instructions, concatenates to as many examples from master dataset for that model as possible (by text distance) while total token count is below a threshold.
    """
    # Read raw fine tuning csv
    folder_path = Path("{0}{1}/".format(path_to_finetuning_data_folder, model_name))
    raw_file_name = "raw_finetuning_data-model_{model_name}.csv".format(model_name=model_name)
    raw_file_path = Path("{0}/{1}".format(folder_path, raw_file_name))
    
    # Get kshot instructions from models metadata = kshot-prompt
    kshot_prompt = model_metadata['kshot_header']
    
    # Create curr prompt using template and prompt args
    if observation_prompt is None:
        observation_prompt = model_metadata['prompt_template'].format(**prompt_args)
    
    # Prompt length = Len of curr prompt
    kshot_prompt_length = len(kshot_prompt) + len(observation_prompt)
    max_length = max_tokens * 4
    
    stop_sequence = model_metadata['stop_sequence'] if model_metadata['stop_sequence'] is not None else ""
    
    if raw_file_path.is_file():
        raw_finetuning_dataset = pd.read_csv(raw_file_path, keep_default_na=False)
        
        # Rank csv observations by Levenshtein distance to prompt args = ranked obs
        prompt_args_json = json.dumps(prompt_args)
        levenshtein_distances = pd.DataFrame(raw_finetuning_dataset.apply(
            func=calculate_levenshtein_distance_for_intersecting_args, 
            axis=1, 
            prompt_args=prompt_args,
            prompt_args_json=prompt_args_json),
                                             columns=['distance'])
        # sort rows by distance in ascending order
        levenshtein_distances.sort_values(by='distance', inplace=True)

        # iterate through ranked obs:
        for i in range(len(levenshtein_distances)):
            # get relevant row from raw_finetuning_dataset
            id_of_raw_finetuning_dataset = levenshtein_distances.index[i]
            row = raw_finetuning_dataset.loc[id_of_raw_finetuning_dataset]

            # prepare observation
            historical_observation = format_observation_template_with_args(row, 
                                                                           model_metadata['prompt_template'], 
                                                                           model_metadata['completion_template'])
            formatted_historical_observation = historical_observation + stop_sequence + "\n\n\n"

            # If that obs plus kshot prompt length > max length, don't add it to the kshot prompt. break
            if len(formatted_historical_observation) + kshot_prompt_length > max_length:
                break
            # Else, add to kshot-prompt and Update kshot-prompt length
            else:
                kshot_prompt += formatted_historical_observation
                kshot_prompt_length += len(formatted_historical_observation)
    
    # add the prompt that we want openai to complete to kshot-prompt
    kshot_prompt += observation_prompt
    assert kshot_prompt_length < max_length
    
    return kshot_prompt


# def identify_what_applicant_has_done_in_ipynb():
#     applicant_approaches_json = json.dumps(applicant_approaches)
#     return applicant_approaches_json