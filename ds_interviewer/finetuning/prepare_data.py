import os
import json
from pathlib import Path
import pandas as pd
from copy import deepcopy
from IPython.display import clear_output
import datetime

from utils.utils import get_label_for_correct_or_incorrect_completion, path_to_finetuning_data_folder
from utils.models_metadata import get_model_metadata

# test_array = []
# this should be a file saved in data folder
finetuning_validation_queue = []


# def add_observation_to_formatted_finetuning_dataset(model_name, prompt, completion):
    # deprecated because we want to use the raw dataset instead.
#     # if there is not a file associated with that model / the file is empty:
#     filepath = Path("{0}{1}.csv".format(path_to_unused_finetuning_data_folder, model_name))
#     file = None
#     if filepath.is_file():
#         print("file found")
#         file = pd.read_csv(filepath)
#     else:
#         print("file not found")
#         # create new file with headers
#         file = pd.DataFrame(columns=["prompt", "completion"])
#     # append row to that file
#     file.loc[len(file)] = [prompt, completion]
#     file.to_csv(filepath, index=False)


def format_prompt_and_completion_templates_with_args(row, prompt_template, completion_template):
    args = row.to_dict()
    prompt = prompt_template.format(**args)
    completion = completion_template.format(**args)
    return {"prompt": prompt, "completion": completion}


def prepare_formatted_finetuning_dataset(model_name, model_version, exclusion_indices=[], start_index=0, end_index=-1):
    # TODO: figure out which rows have values for the prompt args that are required by this model version. 
    # format only those. allow to exclude some columns (like chat history for ask_how_it_works)
    raw_folder_path = "{0}{1}".format(path_to_finetuning_data_folder, model_name)
    raw_file_name = "raw_finetuning_data-model_{model_name}.csv".format(model_name=model_name)
    raw_file_path = Path("{0}/{1}".format(raw_folder_path, raw_file_name))
    raw_finetuning_dataset = pd.read_csv(raw_file_path, keep_default_na=False)

    if end_index == -1:
        end_index = len(raw_finetuning_dataset) - 1
    raw_finetuning_dataset_subset = raw_finetuning_dataset.iloc[start_index:end_index+1].drop(index=exclusion_indices)

    model_metadata, model_version = get_model_metadata(model_name, model_version)
    formatted_finetuning_dataset = pd.DataFrame(raw_finetuning_dataset.apply(format_prompt_and_completion_templates_with_args, 
                                                                axis=1, 
                                                                result_type='expand', 
                                                                args=(model_metadata['prompt_template'], 
                                                                      model_metadata['completion_template'])))
    
    formatted_folder_path = "{0}/version_{1}".format(raw_folder_path, model_version)
    Path(formatted_folder_path).mkdir(parents=True, exist_ok=True)
    formatted_file_name = "formatted_finetuning_data-model_{model_name}-version_{model_version}-id_{start_index}-{end_index}.csv".format(model_name=model_name,
                                                                                                                                         model_version=model_version,
                                                                                                                                         start_index=start_index, 
                                                                                                                                         end_index=end_index)
    formatted_file_path = Path("{0}/{1}".format(formatted_folder_path, formatted_file_name))
    formatted_finetuning_dataset.to_csv(formatted_file_path, na_rep='NA', index=False)


def add_observation_to_raw_finetuning_dataset(observation_details):
    """
    observation_details: dict containing the following keys: model_name, model_version, prompt_template, completion_template, prompt_args, completion_args, prompt, completion 
    """
    folder_path = Path("{0}{1}/".format(path_to_finetuning_data_folder, observation_details['model_name']))
    file_name = "raw_finetuning_data-model_{model_name}.csv".format(model_name=observation_details['model_name'])
    file_path = Path("{0}/{1}".format(folder_path, file_name))
    
    if file_path.is_file():
        raw_finetuning_dataset = pd.read_csv(file_path, keep_default_na=False)
    else:
        folder_path.mkdir(parents=True, exist_ok=True)
        raw_finetuning_dataset = pd.DataFrame(columns=[])
    # append row to that file
    upload_timestamp = datetime.datetime.now()
    row = pd.DataFrame({'meta.timestamp': upload_timestamp, 
                        # 'meta.compatible_model_versions': [model_version],
                       **observation_details['prompt_args'], 
                       **observation_details['completion_args']}, 
                       index=[0])
    raw_finetuning_dataset = pd.concat((raw_finetuning_dataset, row), ignore_index=True)
    raw_finetuning_dataset.to_csv(file_path, na_rep='NA', index=False)
    observation_index = len(raw_finetuning_dataset) - 1
    return observation_index, upload_timestamp
    
    
def add_observation_to_formatted_finetuning_dataset(observation_details, raw_finetuning_dataset_index, upload_timestamp):
    """
    observation_details: dict containing the following keys: model_name, model_version, prompt_template, completion_template, prompt_args, completion_args, prompt, completion 
    """
    folder_path = Path("{0}{1}/version_{2}".format(path_to_finetuning_data_folder, observation_details['model_name'], observation_details['model_version']))
    file_name = "formatted_finetuning_data-model_{model_name}-version_{model_version}.csv".format(model_name=observation_details['model_name'],
                                                                                                 model_version=observation_details['model_version'],)
    file_path = Path("{0}/{1}".format(folder_path, file_name))
    
    if file_path.is_file():
        formatted_finetuning_dataset = pd.read_csv(file_path, keep_default_na=False)
    else:
        folder_path.mkdir(parents=True, exist_ok=True)
        formatted_finetuning_dataset = pd.DataFrame(columns=[])
    # append row to that file
    row = pd.DataFrame({'meta.timestamp': upload_timestamp, 
                        'meta.raw_finetuning_dataset_index': raw_finetuning_dataset_index,
                        'prompt': observation_details['prompt'], 
                        'completion': observation_details['completion']}, 
                       index=[raw_finetuning_dataset_index])
    formatted_finetuning_dataset = pd.concat((formatted_finetuning_dataset, row), ignore_index=True)
    formatted_finetuning_dataset.to_csv(file_path, na_rep='NA', index=False)


def add_observation_to_finetuning_datasets(observation_details):
    """
    called by validate_observation_for_finetuning() 
    calls add_observation_to_raw_finetuning_dataset() and add_observation_to_formatted_finetuning_dataset()
    """
    raw_finetuning_dataset_index, upload_timestamp = add_observation_to_raw_finetuning_dataset(observation_details)
    add_observation_to_formatted_finetuning_dataset(observation_details, raw_finetuning_dataset_index, upload_timestamp)


def validate_observation_for_finetuning(observation_details):
    """
    observation_details: dict containing the following keys: model_name, model_version, prompt_template, completion_template, prompt_args, completion_args, prompt, completion 
    """
    clear_output()
    print_template = \
"""
******************
********* Model Name *********
{0}
********* Prompt *********
{1}
********* Completion *********
{2}
******************
"""
    model_metadata, model_version = get_model_metadata(observation_details['model_name'], observation_details["model_version"] if "model_version" in observation_details.keys() else None)
    print(print_template.format(observation_details['model_name'], 
                                observation_details['prompt'], 
                                observation_details['completion']))
    validate_now = int(input("Do you want to validate this observation now? (1/0): "))
    
    if validate_now:
        label = get_label_for_correct_or_incorrect_completion()
        
        if label == 1:
            correct_completion_args = deepcopy(observation_details['completion_args'])
            add_observation_to_finetuning_datasets(observation_details)
        else:
            # create negative observation, send to master data set
            negative_observation_details_for_finetuning = deepcopy(observation_details)
            negative_observation_details_for_finetuning['prompt_args']['is_completion_correct'] = 0
            negative_observation_details_for_finetuning['prompt'] = negative_observation_details_for_finetuning['prompt_template'] \
                .format(**negative_observation_details_for_finetuning['prompt_args'])
            add_observation_to_finetuning_datasets(negative_observation_details_for_finetuning)

            # create positive observation, send to master data set
            positive_observation_details_for_finetuning = deepcopy(observation_details)
            print("********* Correct Completion *********")
            for key in positive_observation_details_for_finetuning['completion_args'].keys():
                correct_value = input("{}: ".format(key))
                positive_observation_details_for_finetuning['completion_args'][key] = correct_value
            positive_observation_details_for_finetuning['completion'] = positive_observation_details_for_finetuning['completion_template'] \
                .format(**positive_observation_details_for_finetuning['completion_args'])
            correct_completion_args = positive_observation_details_for_finetuning['completion_args']
            add_observation_to_finetuning_datasets(positive_observation_details_for_finetuning)
        return dict(validated=True, correct_completion_args=correct_completion_args)
    else:
        return dict(validated=False, correct_completion_args=None)

    
def submit_observation_for_finetuning_validation(observation_details, validate_async=True):
    """
    observation_details: dict containing the following keys: model_name, model_version, prompt_template, completion_template, prompt_args, completion_args, prompt, completion 
    """
    
    
    folder_path = path_to_finetuning_data_folder
    file_name = "finetuning_validation_queue.json"
    file_path = Path("{0}/{1}".format(folder_path, file_name))

    if file_path.is_file():
        with open(file_path, 'r') as file:
            finetuning_validation_queue = json.load(file)
    else:
        finetuning_validation_queue = []

    finetuning_validation_queue.append(observation_details)
    # TODO: save queue to file before validating live and then load again, in case an error occurs and kills the program.
    
    if not validate_async:
        result = validate_observation_for_finetuning(observation_details)
        if result['validated']:
            finetuning_validation_queue.pop()
            completion_args_to_use_for_interview = result['correct_completion_args']
        else:
            completion_args_to_use_for_interview = observation_details['completion_args']
    else:
        completion_args_to_use_for_interview = observation_details['completion_args']
    
    with open(file_path, 'w') as file:
        json.dump(finetuning_validation_queue, file)
    
    return completion_args_to_use_for_interview


def validate_observations_for_finetuning_from_queue():
    folder_path = path_to_finetuning_data_folder
    file_name = "finetuning_validation_queue.json"
    file_path = Path("{0}/{1}".format(folder_path, file_name))

    if file_path.is_file():
        with open(file_path, 'r') as file:
            finetuning_validation_queue = json.load(file)
        
        if len(finetuning_validation_queue) == 0:
            print("No observations in queue to validate.")
        
        else:
            indices_of_validated_observations = []

            for i, observation_details in enumerate(finetuning_validation_queue):
                result = validate_observation_for_finetuning(observation_details)
                if result['validated']:
                    indices_of_validated_observations.append(i)

                continue_validating = int(input("Continue validating from queue? (1/0): "))
                if not continue_validating:
                    break

            # remove all observations that have been validated from the queue
            finetuning_validation_queue = [observation_details for i, observation_details in enumerate(finetuning_validation_queue) if i not in indices_of_validated_observations]

        with open(file_path, 'w') as file:
            json.dump(finetuning_validation_queue, file)

