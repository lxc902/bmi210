from owlready2 import *
import pandas as pd
import re
import json
import os

# For Parameter Loading
import sys

NAIVE_ONTOLOGY_PATH = "ophthalmologytelephonetriage3-1.owl"
UPDATED_ONTOLOGY_PATH = "ophthalmologytelephonetriage4.owl"
SAVED_ONTOLOGY_PATH = "result.owl"
JSON_OUTPUT_PATH = "output.json"
N = 3
URGENCY_CLASSES = ["Urgent0", "Urgent1", "NonUrgent2"]

def main():
    # Load the ontology.
    shouldUseUpdatedOntology = (len(sys.argv) > 2 and sys.argv[2] == "updated")
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(fileDir, 'classifierPythonScripts/' + NAIVE_ONTOLOGY_PATH)
    if shouldUseUpdatedOntology:
        filename = os.path.join(fileDir, 'classifierPythonScripts/' + UPDATED_ONTOLOGY_PATH)
    onto = get_ontology("file://" + filename).load()

    # Map the name of each instance in the ontology to its corresponding
    # instance object.
    words_dict = {}
    ontology_classes = list(onto.classes())
    for onto_class in ontology_classes:
        for instance in onto_class.instances():
            words_dict[(instance.name).lower()] = instance

    # Read in the call transcripts.
    transcript = sys.argv[1]
    print("transcript param = ", transcript)
    transcript_label = "PatientTranscript"

    # Filter out irrelevant characters.
    transcript_words = re.sub('[,;\.!\?()-:]', '', transcript).split()
    transcript_words = list(map(lambda word: word.lower(), transcript_words))

    # Generate ngrams so we can handle individual names composed of multiple
    # words joined by underscores.
    words_and_phrases = []
    for n in range(1, N + 1):
        ngrams = zip(*[transcript_words[i:] for i in range(n)])
        joined_words = ["_".join(ngram) for ngram in ngrams]
        words_and_phrases.extend(joined_words)

    # Create PatientCall individual representing this transcript.
    call_individual = onto.PatientCall(transcript_label)

    # For each ontology individual mentioned in the transcript, create a
    # "mentions" relationship.
    call_mentions_individuals = []
    call_mentions_keywords = [] # Names of individuals mentioned
    for word in words_and_phrases:
        if word in words_dict:
            call_mentions_individuals += [words_dict[word]]
            call_mentions_keywords += [word]
    call_individual.mentions = call_mentions_individuals

    # Synchronize the reasoner to perform classification.
    #
    # Example output:
    # ---------------
    # * Owlready * Reparenting ophthalmologytelephonetriage.Transcript7:
    #              {ophthalmologytelephonetriage.PatientCall} => {ophthalmologytelephonetriage.NonUrgent2}
    # * Owlready * Reparenting ophthalmologytelephonetriage.Transcript8:
    #              {ophthalmologytelephonetriage.PatientCall} => {ophthalmologytelephonetriage.Urgent0}
    #
    with onto:
        sync_reasoner()

    # Aggregate new urgency level classifications in dictionary.
    urgency_classifications = {}
    ontology_classes = list(onto.classes())
    for onto_class in ontology_classes:
        if onto_class.name in URGENCY_CLASSES:
            for instance in onto_class.instances():
                print("examining:", instance.name)
                if instance.name not in urgency_classifications:
                    urgency_classifications[instance.name] = []
                urgency_classifications[instance.name].append(onto_class.name)

    for transcript in urgency_classifications:
        classifications = urgency_classifications[transcript]
        # If classifed with more than one urgency level, select the most urgent
        # level.
        if (len(classifications) > 1):
            most_urgent_level = 2
            for c in classifications:
                urgency_level = int(c[-1])
                if (urgency_level < most_urgent_level):
                    most_urgent_level = urgency_level
            urgency_classifications[transcript] = [URGENCY_CLASSES[most_urgent_level]]

    if (transcript_label not in urgency_classifications):
        # Transcript did not get classified.
        writeClassificationToJsonFile("Unclassified", call_mentions_keywords)
    else:
        writeClassificationToJsonFile(urgency_classifications[transcript_label], call_mentions_keywords)


def writeClassificationToJsonFile(classification, keywords):
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(fileDir, 'classifierPythonScripts/' + JSON_OUTPUT_PATH)
    outFile = open(filename, "w")
    outputJSON = json.loads("{}")
    outputJSON["classification"] = classification
    outputJSON["keywords"] = keywords
    outFile.write(json.dumps(outputJSON, indent=2, sort_keys=True, ensure_ascii=True))
    outFile.close()


if __name__ == "__main__":
    main()
