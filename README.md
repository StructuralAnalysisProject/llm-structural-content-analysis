# llm-structural-content-analysis

## Prompt

The prompt used in the study can be found at [inference.py](https://github.com/StructuralAnalysisProject/llm-structural-content-analysis/blob/521b09ec196239a14e9d68de2b5a7fed2908de86/inference.py). It can be used on both the evaluation dataset and new documents to be analyzed.
## Inference dataset



## Evaluation dataset


Evaluation dataset of exercises provided by Piret, Nizet & Bourgueois (1996) it's available in the [sca_eval_dataset.json](https://github.com/StructuralAnalysisProject/llm-structural-content-analysis/blob/main/sca_eval_dataset.json)

> Piret, A., Nizet, J., & Bourgeois, E. (1996). L'analyse structurale. Une méthode d'analyse de contenu pour les sciences humaines, Bruxelles, De Boeck. https://researchportal.unamur.be/en/publications/lanalyse-structurale-une-m%C3%A9thode-danalyse-de-contenu-pour-les-sci

The schema of the evaluation dataset is organized as follows:

'exercise' (integer)
A unique identifier for the exercise. Each entry corresponds to a distinct text fragment analyzed.

'material' (string)
The source text under analysis. Typically, this is a quotation or excerpt (e.g., from an interview, speech, or text) that contains semantic contrasts to be studied.

'correction' (object)
Contains the ground truth for the semantic analysis of the material, organized into one or more semantic axes.

'axes_semantiques' (array of objects)
Each axis represents a dimension of meaning or contrast identified in the text. It is structured as:

'axe' (string)
The label of the semantic axis.

'disjonction' (array of objects)
Contains the opposing terms that define the axis.

'terme_a' (string)
The first pole of the opposition.

'indice_valeur_a' (string)
Value index for terme_a.

'terme_b' (string)
The second pole of the opposition.

'indice_valeur_b' (string)
Value index for terme_b, analogous to indice_valeur_a.



## Evaluation code




