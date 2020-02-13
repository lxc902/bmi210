from owlready2 import *
import pandas as pd
import re

ONTOLOGY_PATH = "ophthalmologytelephonetriage.owl"
PATIENT_CALLS_PATH = "telephonetriage.csv"

def main():
    # Load the ontology.
    onto = get_ontology("file://" + ONTOLOGY_PATH).load()
 
    # Map the name of each instance in the ontology to its corresponding
    # instance object.
    words_dict = {}
    ontology_classes = list(onto.classes())
    for onto_class in ontology_classes:
        for instance in onto_class.instances():
            words_dict[instance.name] = instance

    # Read in the call transcripts.
    df = pd.read_csv(PATIENT_CALLS_PATH)    
    call_transcripts = df.iloc[ : , 1]

    
    call_id = 0
    for transcript in call_transcripts[0:10]: #TODO: Just using first 10 transcripts for now
        # Filter out irrelevant characters.
        transcript_words = re.sub('[,;\.!\?()-:]', '', transcript).split()
      
        # Create PatientCall individual representing this transcript. 
        call_individual = onto.PatientCall("Transcript" + str(call_id))

        # For each ontology individual mentioned in the transcript, create a 
        # "mentions" relationship.
        call_mentions = []
        for word in transcript_words:
            if word in words_dict:
                call_mentions += [words_dict[word]]
        call_individual.mentions = call_mentions
        print(call_individual.name, "mentions:", call_individual.mentions, "\n")
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
    with onto:
        sync_reasoner()

if __name__ == "__main__":
    main()
