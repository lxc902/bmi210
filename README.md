# BMI210 Final Project: Automatic Triaging of Opthalmology Patient Phone Calls

## Viewing the Ontologies
To view the ontologies created for this project, open the following files in Protege:

    1. ophthalmologytelephonetriage3-1.owl (the Naive Ontology)
    2. ophthalmologytelephonetriage4.owl (the Updated Ontology)

## Running the Web App
To start the local server, do the following:

    1. cd into the "classifierWebApp/classifier-app/src/server" directory
    2. type "node app.js"

To start the client-side app, do the following:

    1. cd into the "classifierWebApp/classifier-app" directory
    2. type "npm start"

To get it to work, you may need to do the following installations:

    1. yarn add @material-ui/core
    2. yarn add react-bootstrap
    3. npm install react-scripts@1.1.1
    4. npm install python-shell
    5. npm install typeface-roboto --save
    6. pip install --upgrade gensim
    
Below is a demo of the web app in action:

[![](http://img.youtube.com/vi/2uIzoLlQzGY/0.jpg)](http://www.youtube.com/watch?v=2uIzoLlQzGY "Web App Demo")

## Running the OWL Ontology Script
Unfortunately, the OWL Ontology Script cannot be run independent of the web app without access to the patient notes csv file, 
which we are unable to upload to this Github repo due to patient privacy. However, if one did have access to this file, these instructions 
specify how to run the script.

To run the Owlready2 python script independent of the web app, do the following:

    1. Type "python owlClassifier.py"
        a. By default, the above command will run the script using the updated ontology. To run it with the original naive ontology,
           you may edit line 21 of the owlClassifier.py source file, and change "UPDATED_ONTOLOGY_PATH" to "NAIVE_ONTOLOGY_PATH"
        b. By default, the above command will not assign any classifications to those patient notes that cannot be automatically 
           classified. To assign a default classification of either Urgent or Non-Urgent to transcripts unable to be classified, 
           you may set one of the "SHOULD_SET_NAN_TO_0" or "SHOULD_SET_NAN_TO_2" booleans, respectively, to True. 

## Running/Retraining the word2vec models,
    0. go to the word2vec_csv/ folder
    1. (optional) modify the `obj/tokenizer_whitelisted_words.txt`
    2. run `python3 csv_classifier.py`
    3. copy/override everything under `obj/` over to `bmi210/classifierWebApp/classifier-app/src/server/classifierPythonScripts/word2vec_app/obj/`
    4. restart the web app following instructions in https://github.com/lxc902/bmi210/blob/master/classifierWebApp/readme

## Running the BagOfWords models (SVM and GNB),
    0. go to the classifierWebApp/classifier-app/src/server/classifierPythonScripts/bagOfWords_app folder
    1. run `python3 svm_classifier.py <Note>` or `python3 gnb_classifier.py <Note>` with <Note> replaced with your desired note to calssify in quotes
    2. Output should be the classification as well as the words that were used to make the classification.
