# !pip install sentence_transformers # in case you don't have it.

import json
import re
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np


with open('sca_eval_dataset.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


iteration = 1 # or the one that you want to analyze between 1, 2 or 3.

with open(f"models_inference_dataset_iteration_{iteration}.json", 'r', encoding='utf-8') as file:
    analysis_data = json.load(file)

model = SentenceTransformer("dbmdz/bert-base-french-europeana-cased") # Be careful! this need CUDA or would take too much time.

## We need to pre process our data

# First, different exercises had different objectives, not necesarely reflected on a static prompt, so we need to define differente evaluation processes.

def replace_value_indices(data_dict):
    if isinstance(data_dict, dict):
        new_dict = {}
        for key, value in data_dict.items():
            if key in ['indice_valeur_a', 'indice_valeur_b']:
                new_dict[key] = None
            else:
                new_dict[key] = replace_value_indices(value)
        return new_dict
    elif isinstance(data_dict, list):
        return [replace_value_indices(item) for item in data_dict]
    else:
        return data_dict

def replace_axes(data_dict):
    if isinstance(data_dict, dict):
        new_dict = {}
        for key, value in data_dict.items():
            if key == 'axe':
                new_dict[key] = None
            else:
                new_dict[key] = replace_axes(value)
        return new_dict
    elif isinstance(data_dict, list):
        return [replace_axes(item) for item in data_dict]
    else:
        return data_dict



new_schema = []

for item in data:
    # Create a new dictionary starting with the known keys
    new_dict = {
        'exercise': item['exercise'],
        'material': item['material']
    }

    # Check conditions for evaluation
    if 'correction' in item and 'axes_semantiques' in item['correction'] and item['correction']['axes_semantiques']:
        first_axe = item['correction']['axes_semantiques'][0]

        # Check both conditions simultaneously
        axe_is_null = first_axe.get('axe') is None
        value_is_null = (first_axe.get('disjonction') and
                        first_axe['disjonction'][0].get('indice_valeur_a') is None)

        # New combined condition check
        if axe_is_null and value_is_null:
            new_dict['evaluation'] = "no_axe no_valeur"
        elif axe_is_null:
            new_dict['evaluation'] = "no_axe"
        elif value_is_null:
            new_dict['evaluation'] = "no_valeur"
        else:
            new_dict['evaluation'] = "full"  # Default value if neither condition is met
    else:
        new_dict['evaluation'] = None  # Default value if analysis structure is not complete

    # Add the analysis key back
    new_dict['correction'] = item['correction']
    new_schema.append(new_dict)

data = new_schema

########################
########################


models = [item['model'] for item in analysis_data]

# First, let's check what's actually in your analysis_data
print("Type of analysis_data:", type(analysis_data))
print("Length of analysis_data:", len(analysis_data))

# Let's look at the first item
if len(analysis_data) > 0:
    first_item = analysis_data[0]
    print("Keys in first item:", first_item.keys())
    
    # Check the model_analysis field
    if 'model_analysis' in first_item:
        print("Type of model_analysis:", type(first_item['model_analysis']))
        print("Length of model_analysis:", len(first_item['model_analysis']))
        
        # Look at the first item in model_analysis
        if len(first_item['model_analysis']) > 0:
            first_analysis = first_item['model_analysis'][0]
            print("Keys in first analysis item:", first_analysis.keys())


existing_exercises = set()
for item in analysis_data:
    if 'model_analysis' in item:
        for analysis_item in item['model_analysis']:
            # Check if 'exercise' key exists in the analysis_item
            if 'exercise' in analysis_item:
                existing_exercises.add(analysis_item['exercise'])
            else:
                # If 'exercise' doesn't exist, try to find another identifier
                print("Keys available in analysis_item:", analysis_item.keys())
                # You may need to use an alternative key or skip this item


# Convert to sorted list for better readability
existing_exercises = sorted(list(existing_exercises))

# Create the empty DataFrame with only existing exercise numbers
df = pd.DataFrame(index=existing_exercises, columns=models)


############################


def inspect_structure(data_item, prefix=""):
    if isinstance(data_item, dict):
        for key, value in data_item.items():
            print(f"{prefix}Key: {key}")
            if isinstance(value, (dict, list)):
                inspect_structure(value, prefix + "  ")
    elif isinstance(data_item, list):
        print(f"{prefix}List with {len(data_item)} items")
        if len(data_item) > 0:
            inspect_structure(data_item[0], prefix + "  ")



def find_analysis_for_model_and_exercise(analysis_data, target_model, target_exercise):
    for model_data in analysis_data:
        if model_data.get('model') == target_model:
            for exercise_data in model_data.get('model_analysis', []):
                # Check if 'exercise' key exists before attempting to access it
                if 'exercise' in exercise_data and int(exercise_data['exercise']) == target_exercise:
                    print(f"\nFound exercise data structure:")
                    inspect_structure(exercise_data)
                    return exercise_data
                elif 'exercise' not in exercise_data:
                    print(f"\nWarning: Exercise data missing 'exercise' key. Available keys: {list(exercise_data.keys())}")
    
    print(f"\nNo matching data found for model '{target_model}' and exercise {target_exercise}")
    return None

############################

def find_ground_truth(data, target_exercise):
    for item in data:
        if 'exercise' in item and int(item['exercise']) == target_exercise:
            return item
    return None

# Let's add some debugging for the first item
print("Debugging first items...")
first_exercise = df.index[0]
first_model = df.columns[0]
sample_model_result = find_analysis_for_model_and_exercise(analysis_data, first_model, first_exercise)
sample_ground_truth = find_ground_truth(data, first_exercise)

if sample_model_result and sample_ground_truth:
    print("\nModel Result keys:", sample_model_result.keys())
    if 'analysis' in sample_model_result:
        print("Analysis keys:", sample_model_result['analysis'].keys())
    print("\nGround Truth keys:", sample_ground_truth.keys())
    if 'correction' in sample_ground_truth:
        print("Correction keys:", sample_ground_truth['correction'].keys())

# Now let's do the comparison with cosine similarity
for exercise_num in df.index:
    ground_truth = find_ground_truth(data, exercise_num)

    if ground_truth is not None:
        for model_name in df.columns:
            model_result = find_analysis_for_model_and_exercise(analysis_data, model_name, exercise_num)

            if model_result is not None and 'analysis' in model_result:
                # Apply preprocessing based on evaluation type
                processed_model_analysis = model_result['analysis']  # Get the analysis field
                if ground_truth['evaluation'] == 'no_valeur':
                    processed_model_analysis = replace_value_indices(processed_model_analysis)
                elif ground_truth['evaluation'] == 'no_axe':
                    processed_model_analysis = replace_axes(processed_model_analysis)
                elif ground_truth['evaluation'] == 'no_axe no_valeur':
                    processed_model_analysis = replace_value_indices(processed_model_analysis)
                    processed_model_analysis = replace_axes(processed_model_analysis)

                # Generate embeddings
                # Convert to string, but now use the entire analysis structure
                model_str = str(processed_model_analysis)
                ground_truth_str = str(ground_truth['correction'])

                embedding_model = model.encode(model_str, convert_to_tensor=True)
                embedding_ground_truth = model.encode(ground_truth_str, convert_to_tensor=True)

                # Calculate cosine similarity
                similarity = util.cos_sim(embedding_model, embedding_ground_truth)

                # Store the similarity score
                df.loc[exercise_num, model_name] = float(similarity[0][0])
            else:
                df.loc[exercise_num, model_name] = 0.0  # or float('nan')
    else:
        print(f"Warning: Could not find ground truth for exercise {exercise_num}")
        df.loc[exercise_num, :] = 0.0  # or float('nan')

# Display results
print("\nCosine Similarity Results:")

df.head()

# df.to_csv("similarities exerices-model.csv", index=True) # to save as csv

