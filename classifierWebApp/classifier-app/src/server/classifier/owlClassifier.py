from owlready2 import *
import pandas as pd
import re

ONTOLOGY_PATH = "../ophthalmologytelephonetriage3-1.owl"
SAVED_ONTOLOGY_PATH = "result.owl"
PATIENT_CALLS_PATH = "../telephonetriage.csv"
N = 3
URGENCY_CLASSES = ["Urgent0", "Urgent1", "NonUrgent2"]

def main():
    # Load the ontology.
    onto = get_ontology("file://" + ONTOLOGY_PATH).load()
 
    # Map the name of each instance in the ontology to its corresponding
    # instance object.
    words_dict = {}
    ontology_classes = list(onto.classes())
    for onto_class in ontology_classes:
        for instance in onto_class.instances():
            words_dict[(instance.name).lower()] = instance

    # Read in the call transcripts.
    df = pd.read_csv(PATIENT_CALLS_PATH)    
    call_transcripts = df.iloc[ : , 1]

    call_id = 0
    transcript_labels = []
    for transcript in call_transcripts: 
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
        transcript_labels.append("Transcript" + str(call_id))
        call_individual = onto.PatientCall("Transcript" + str(call_id))

        # For each ontology individual mentioned in the transcript, create a 
        # "mentions" relationship.
        call_mentions = []
        for word in words_and_phrases:
            if word in words_dict:
                call_mentions += [words_dict[word]]
        call_individual.mentions = call_mentions
        #TODO print(call_individual.name, "mentions:", call_individual.mentions, "\n")
        call_id = call_id + 1

    # Synchronize the reasoner to perform classification.
    #
    # Example output:
    # ---------------
    # * Owlready * Reparenting ophthalmologytelephonetriage.Transcript7: 
    #              {ophthalmologytelephonetriage.PatientCall} => {ophthalmologytelephonetriage.NonUrgent2}
    # * Owlready * Reparenting ophthalmologytelephonetriage.Transcript8: 
    #              {ophthalmologytelephonetriage.PatientCall} => {ophthalmologytelephonetriage.Urgent0}
    #
    onto.save(file = SAVED_ONTOLOGY_PATH)
    with onto:
        sync_reasoner()

    # Aggregate new urgency level classifications in dictionary.
    urgency_classifications = {}
    ontology_classes = list(onto.classes())
    for onto_class in ontology_classes:
        if onto_class.name in URGENCY_CLASSES:
            for instance in onto_class.instances():
                if instance.name not in urgency_classifications:
                    urgency_classifications[instance.name] = []
                urgency_classifications[instance.name].append(onto_class.name)

    # Format classification output as dataframe
    df = pd.DataFrame(columns=['Classification'], index=transcript_labels)
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
        df.loc[transcript] = urgency_classifications[transcript]
    print(df)


if __name__ == "__main__":
    main()
