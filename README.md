Crime Pattern Detection for Atlanta Police
===

Introduction
---
It's a project that ISyE Dept., Georgia Tech collaborates with Atlanta Police Department to detect the pattern of history crimes in Atlanta. The crime data comes from the database of Atlanta Police. There are three types of records that we've used:
- CFS (*Call for Services*): A standard records from the 911 call.
- OffCore: includes some basic attributes of a criminal case.
- Remarks: includes one or more pieces of free text that describes some details of a crimial case.

Preliminary
---

#### 1. Generate the latest requirements.txt for the python environment
Run the following script at root directory:
```bash
sh script/gen_py_reqs.sh
```

#### 2. Install the dependent python library that project needs
Run the following script at root directory:
```bash
pip install -r python/requirements.txt
```
And try to install other library if they were required according to the prompt.

#### 3. Download the required corpus (e.g. corpurs for the english stopwords)
Run the following python script:
```python
import nltk
nltk.download()
```
In the GUI window that opens simply press the 'Download' button to download all corpora or go to the 'Corpora' tab and only download the ones you need/want.

#### 4. Configure setting.
Configure your own setting in `/config/script_config.sh`:
```bash 
#!/bin/bash

# Basic config 
export owner_tag='woodie'
export task_tag='pedrobbery.text_feature'
export created_at=`date +%Y%m%d-%H%M%S`

# Resource
export word2vec_model_path='resource/GoogleNews-vectors-negative300.bin'
export words_category_path='tmp/woodie.burglary.gen_vectors_from_wordslist/KeyWords.json'
```

Build the sprout of the data stream
---
In order to organize the data orderly, the `Incident No.` was set as the primary key of the records. The crime records are supposed to be processed by taking every incident as the minimum unit. And all of the further research will be based on the sprout of the data stream. Run the following script to build the sprout of the data stream:
```bash
sh script/build_sprout.sh
```

<center>*An illustration for the sprout of the data stream*</center>
![flow_chart_for_datastream](https://github.com/meowoodie/Crime-Pattern-Detection-for-APD/blob/master/static/data_stream_sprout.png)

Get Key Words
---
The combination of fundamental knowledge and dozens of criminal detection techniques based on years of work experience that Atlanta Police summerized a words dictionary for us, which contains about ten categories, and each of the categories contains ten or more key words.

<center>*A part of the word dictionary from Atlanta Police*</center>

| VEHICLE DESCRIPTORS | WEAPONS | Aggregated Assualts / Homicide | ... |
|:-------------------:|:-------:|:------------------------------:|:---:|
|        4 Door       |   Gun   |              Shot              | ... |
|        2 Door       | Firearm |             Stabbed            | ... |
|         SUV         |  Pistol |         Pointed the gun        | ... |
|         ...         |   ...   |               ...              | ... |

For preparing the key words of the dictionary in a better way, we organize the dictionary into a .json format. run the following script:

```bash
sh script/build_corpus.sh
```

A new file named `KeyWords.json` will be generated at `/tmp/[task_tag]/` (`[task_tag]` was configured in `/config/script_config.sh`). 

<center>*JSON file: KeyWords.json*</center>
```json
{
    "VEHICLE DESCRIPTORS": [
        "passenger", 
        "sunroof", 
        "station wagon", 
		...
    ], 
    "GANG NAMES": [
        "bloods", 
        "billy bad asses", 
        "ygm", 
		...
    ], 
    "Burglary/Larceny / Car Break-Ins": [
        "cut a hole through the wallor ceiling", 
        "broked the window", 
        "side windows", 
		...
    ], 
    ...
}
```

Features of Crime
---

#### 1. Narratives of a crime
Generally speaking, the text in the narratives part of a crime is usually heavy and clutter, so it's really hard to extract effective features from the scratch. So the basic idea here is to find (or map) the words in the narratives that are closest to the descriptor for each of the categories in the dictionary. Since there are ten categories in the dictionary, we define ten features, corresponding to the categories in the dictionary, for the set of narratives of a crime record. And for each of the feature, we find (or map) `K-nearest-to-the-category` words from the narratives. 

Take a pedestrain robbery crime record and its `SUSPECT DESCRIPTORS` feature (category) as an example. There are 69 key words in the `SUSPECT DESCRIPTORS` category in the dictionary, and nearly 500 words in the narratives of the crime record. The following is the mapping result:
![illustration_keywords_mapping](https://github.com/meowoodie/Crime-Pattern-Detection-for-APD/blob/master/static/illustration_keywords_mapping.png)
As you can see in the above figure, K is 5, and 5 words in the narratives have been mapped to 4 words in the category. The words in the category and their distance form the `SUSPECT DESCRIPTORS` feature for this record. 
We can also express the feature in a form of fixed-length numerical vector. For this case, the length of the vector is supposed to be 69 (69 words in the category) and the value of the element is supposed to be the largest distance between the word corresponding to the index of the elements and the words in the narratives (or to be 0 if there is no distance between these two words).
```
[0, 0, 0.757, 0, ..., 1.0, ..., 0.430, ..., 0.365, ..., 0, 0] 
```

> Word2Vec: Word2Vec techniques has been used in this project to measure the cosine distance between arbitrary two words. 







