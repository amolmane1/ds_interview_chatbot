import json
from copy import deepcopy


# temporary - only to be called in case we have lost data
def create_models_metadata():
    models_metadata = {}
    new_model_template = {
        'best_model_version': None,
        'models': {}
    }
    new_model_version_metadata_template = {
        'prompt_template': None,
        'completion_template': None,
        'kshot_header': None,
        'finetuned_model_name': None
    }


    models_metadata['ask_how_it_works'] = deepcopy(new_model_template)
    models_metadata['ask_how_it_works']['models']['4.1.23'] = deepcopy(new_model_version_metadata_template)
    models_metadata['ask_how_it_works']['models']['4.1.23']['prompt_template'] = \
"""Current section chat:
{current_section_chat}

Details:
Subject: {subject}
Question type: {question_type}
Is question correct: {is_completion_correct}
"""
    models_metadata['ask_how_it_works']['models']['4.1.23']['completion_template'] = \
    """Interviewer: {interviewer_dialogue}"""

    models_metadata['ask_how_it_works']['models']['4.1.23']['kshot_header'] = \
    """Interviewer is interviewing Applicant for a job as a Data Scientist. Interviewer knows all concepts in Data Science and always applies them correctly.

Interviewer asks Applicant questions in the following format:

Current section chat:
$<Conversation so far between Interviewer and Applicant. This may be empty.>

Details:
Subject: $<the subject Interviewer is to ask a question about>
Question type: $<what type of question Interviewer should ask>
Is question correct: $<1 or 0 - whether the question Interviewer asks is of the right type or not>
Interviewer: $<Interviewer's question about the subject>


Below are some correct examples:

"""
    models_metadata['ask_how_it_works']['best_model_version'] = "4.1.23"


    models_metadata['validate_answer_how_it_works'] = deepcopy(new_model_template)
    models_metadata['validate_answer_how_it_works']['models']['4.1.23'] = deepcopy(new_model_version_metadata_template)
    models_metadata['validate_answer_how_it_works']['models']['4.1.23']['prompt_template'] = \
    """Current section chat:
{current_section_chat}

Details:
Question type: {question_type}
Is validation correct: {is_completion_correct}
"""
    models_metadata['validate_answer_how_it_works']['models']['4.1.23']['completion_template'] = \
    """Correct Response: {correct_response}
Validation of response: {validation_of_response}"""
    models_metadata['validate_answer_how_it_works']['models']['4.1.23']['kshot_header'] = \
    """Interviewer is interviewing Applicant for a job as a Data Scientist. Interviewer knows all concepts in Data Science and always applies them correctly.

Interviewer validates Applicant's responses to a question in the following format:

Current section chat:
$<Conversation so far between Interviewer and Applicant. This may be empty.>

Details:
Question type: $<what type of question Interviewer asked>
Is validation correct: $<1 or 0 - whether Interviewer's validation of applicant’s response is correct or not>>
Correct response: $<correct response to Interviewer's question>
Validation of response: $<whether Applicant's response is 0=Applicant Did Not Understand / 1=incorrect / 2=incomplete / 3=correct>


Below are some correct examples:

"""
    models_metadata['validate_answer_how_it_works']['best_model_version'] = "4.1.23"

    with open('/Users/amolmane/Documents/ds_interview_chatbot/data/models_metadata.json', 'w') as file:
        json.dump(models_metadata, file)


def get_model_metadata(model_name, model_version=None):
    with open('/Users/amolmane/Documents/ds_interview_chatbot/data/models_metadata.json', 'r') as file:
        models_metadata = json.load(file)
    if model_version:
        model_metadata = deepcopy(models_metadata[model_name]['models'][model_version])
    else:
        model_version = models_metadata[model_name]['best_model_version']
        model_metadata = deepcopy(models_metadata[model_name]['models'][model_version])
    return model_metadata, model_version


def add_new_model_version():
    # add data
    # also format finetuning obs for all previous observations in raw dataset 
    # (but this may require adding values for fields that were added for the new version template that didnt exist in the previous version template)
    pass

