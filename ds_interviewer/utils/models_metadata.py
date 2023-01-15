import json
from copy import deepcopy
from datetime import datetime

models_metadata_file_path = '/Users/amolmane/Documents/ds_interview_chatbot/data/models_metadata.json'
new_model_template = {
    'best_model_version': None,
    'models': {}
}
new_model_version_metadata_template = {
    'model_version': None,
    'prompt_template': None,
    'completion_template': None,
    'kshot_header': None,
    'finetuned_model_name': None
}


def get_model_metadata(model_name, model_version=None):
    with open(models_metadata_file_path, 'r') as file:
        models_metadata = json.load(file)
    if model_version:
        model_metadata = deepcopy(models_metadata[model_name]['models'][model_version])
    else:
        model_version = models_metadata[model_name]['best_model_version']
        model_metadata = deepcopy(models_metadata[model_name]['models'][model_version])
    return model_metadata, model_version


def add_new_model_version(model_name, new_model_version_metadata, set_as_best_model_version=False):
    # ensure we have all the data needed for a model version
    assert all(key in new_model_version_metadata for key in new_model_version_metadata_template)
    
    with open(models_metadata_file_path, 'r') as file:
        models_metadata = json.load(file)

    model_version = datetime.today().strftime('%d.%m.%y')
    
    if model_name not in models_metadata.keys():
        # add data, set as best model version
        models_metadata[model_name] = deepcopy(new_model_template)
        models_metadata[model_name]['best_model_version'] = model_version
    else:
        number_of_models_made_on_the_same_day = len([v for v in models_metadata[model_name]['models'].keys() if model_version in v])
        model_version += "-" + str(number_of_models_made_on_the_same_day)        
        if set_as_best_model_version:
            models_metadata[model_name]['best_model_version'] = model_version
    
    models_metadata[model_name]['models'][model_version] = new_model_version_metadata
    models_metadata[model_name]['models'][model_version]['model_version'] = model_version

    with open(models_metadata_file_path, 'w') as file:
        json.dump(models_metadata, file)


def update_model_best_version(model_name, model_version):
    pass


# def update_model_name:
#     # change name in models metadata
#     # change all finetuning dataset names for that model


# def add_new_model(model_name, new_model_version_metadata):
#     """
#     new_model_version_metadata: dict, should have the keys in new_model_version_metadata_template and appropriate values 
#     """
#     with open(models_metadata_file_path, 'r') as file:
#         models_metadata = json.load(file)
    
#     if model_name in models_metadata.keys():
#         print("there is already a model called {} in models_metadata. Use add_new_model_version() instead.".format(model_name))
#         return
        
#     model_version = datetime.today().strftime('%d.%m.%y')
    
#     models_metadata[model_name] = deepcopy(new_model_template)
#     models_metadata[model_name]['best_model_version'] = model_version
#     models_metadata[model_name]['models'][model_version] = new_model_version_metadata

#     with open(models_metadata_file_path, 'w') as file:
#         json.dump(models_metadata, file)

