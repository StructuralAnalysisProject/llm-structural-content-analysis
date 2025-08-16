# llm-structural-content-analysis

## Prompt



Vous êtes un expert en analyse qualitative.  
Aidez-moi à effectuer une analyse structurelle de contenu. Cette technique d'analyse qualitative consiste à identifier des relations de disjonction binaires : des termes qui décrivent des réalités inverses au sein d’un même axe sémantique.  

Règles :  
Binarité : une relation de disjonction ne peut être établie qu’entre deux termes du discours.  
Cohérence conceptuelle : ces deux termes doivent se référer à un dénominateur commun, à un axe sémantique qui correspond à une catégorie de réalité.  
Exhaustivité : il ne peut y avoir aucun autre terme qui se rapporte à l’axe sémantique en dehors des deux termes de la disjonction.  
Exclusivité : les deux termes de la disjonction doivent être des propriétés absolument incompatibles au sein de l’axe sémantique. Il n’existe aucune réalité qui possède à la fois les caractéristiques d’un terme et de son inverse.  
Hypothèse proposée : Lorsque le locuteur n’a pas explicitement énoncé l’axe auquel se réfère une disjonction, ou l’un des termes de celle-ci, proposez une hypothèse sur l’axe ou le terme probable en vous basant sur la logique du locuteur. Ces hypothèses sur un axe ou des termes de la disjonction doivent être marquées entre parenthèses "()".  
Indices de valorisation : Lorsque dans le texte un des termes est connoté de manière positive et son inverse de manière négative, ces derniers doivent être marqués respectivement avec un signe plus (+) ou un signe moins (-). Ces indices doivent refléter le point de vue du locuteur, même si cela diffère du sens commun. Il est également possible que le locuteur n’attribue aucune valorisation à un terme qui est habituellement évalué.  

Exemples :
{
    "exemple": 1,
    "material": "La droite, c'est 20 ans d'immigration sauvage, la gauche, c'est l'immigration contrôlée",
    "axes_semantiques": [
        {
            "axe": "les immigrations",
            "disjonction": [
                {
                    "terme_a": "sauvage",
                    "indice_valeur_a": "-",
                    "terme_b": "contrôlée",
                    "indice_valeur_b": "+"
                }
            ]
        },
        {
            "axe": "(les majorités politiques en France)",
            "disjonction": [
                {
                    "terme_a": "la droite",
                    "indice_valeur_a": "-"
                    "terme_b": "la gauche",
                    "indice_valeur_b": "+",
                }
            ]
        }
    ]
},
{
    "exemple": 2,
    "material": "Celui qui va à l'école, il ne gagne rien. A ce moment-là, çe ne me plaisait pas fort. J'avais envie de gagner de l'argent. C'est pour ça que j'ai été travailler",
    "axes_semantiques": [
            {
            "axe": "(rétribution des activités)",
            "disjonction": [
                {
                    "terme_a": "gagner de l'argent",
                    "indice_valeur_a": "+",
                    "terme_b": "ne rien gagner",
                    "indice_valeur_b": "-"
                }
            ]
        }
    ]
}
{
    "exemple": 3,
    "material": "(interview d’une assistante sociale) lime semble qu'une assistante sociale qui serait clairement affichée (...) à droite, (...) aura une vision plus économiste des choses (...), qu 'une assistante sociale qui aurait une idéologie plus de gauche [...] elle devrait déjà avoir une vue plus humaniste des choses",
    "axes_semantiques": [
            {
            "axe": "les idéologies des assistantes sociales",
            "disjonction": [
                {
                    "terme_a": "de gauche",
                    "indice_valeur_a": "+",
                    "terme_b": "de droite",
                    "indice_valeur_b": "-"
                }
            ]
        },
        {
            "axe": "Les visions des choses",
            "disjonction": [
                {
                    "terme_a": "plus humaniste",
                    "indice_valeur_a": "+",
                    "terme_b": "plus économiste",
                    "indice_valeur_b": "-"
                }
            ]
        }
    ]
}


En utilisant ce schéma JSON :  
{
    "material": "<écrivez ici le texte à analyser>",
    "chain-of-thought": "<expliquez votre raisonnement étape par étape>",
    "analysis": {
        "axes_semantiques": [
            {
            "axe": "<axe sémantique identifié>",
            "disjonction": [
                {
                    "terme_a": "<terme A identifié>",
                    "indice_valeur_a": "<indice de valorisation du terme A>",
                    "terme_b": "<terme B identifié>",
                    "indice_valeur_b": "<indice de valorisation du terme B>"
                }
            ]
          }
       ]
    }
}
Analysez le texte suivant :


## Inference dataset



## Evaluation dataset


Evaluation dataset of exercises provided by Piret, Nizet & Bourgueois (1996) it's abiable in the [sca_eval_dataset.json](https://github.com/StructuralAnalysisProject/llm-structural-content-analysis/blob/main/sca_eval_dataset.json)

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




