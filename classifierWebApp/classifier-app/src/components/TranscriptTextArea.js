import React, { Component } from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import LinearProgress from '@material-ui/core/LinearProgress';
import Typography from '@material-ui/core/Typography';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormLabel from '@material-ui/core/FormLabel';
import ServerUtil from '../server/ServerUtil';
import '../styles/TranscriptTextArea.css';
import * as constants from '../classifierConstants.js';

class TranscriptTextArea extends Component {

  state = { selectedClassifier: "ontology" };
  handleChange = event => {
    this.setState({ selectedClassifier: event.target.value });
  };

  render() {
    return (
      <div id="inputArea">
        <Typography
          id="welcomeText"
          variant="h4"
          className="welcomeText">
          Use this tool to examine how each of our classifiers interprets patient call transcripts!
        </Typography>
        <div id="classifierSelection">
          <FormLabel component="legend">Please select the classifier you would like to use:</FormLabel>
          <RadioGroup value={this.state.selectedClassifier} name="classifierGroup" onChange={this.handleChange}>
            <FormControlLabel value={global.NAIVE_ONTOLOGY} control={<Radio />} label="Naive OWL Ontology" />
            <FormControlLabel value={global.SUPPORT_VECTOR_MACHINE} control={<Radio />} label="Support Vector Machine" />
            <FormControlLabel value={global.GAUSSIAN_NAIVE_BAYES} control={<Radio />} label="Gaussian Naive Bayes" />
            <FormControlLabel value={global.LOGISTIC_REGRESSION} control={<Radio />} label="word2vec + Logistic Regression" />
            <FormControlLabel value={global.KNN} control={<Radio />} label="word2vec + KNN" />
            <FormControlLabel value={global.W2V_SVM} control={<Radio />} label="word2vec + SVM" />
          </RadioGroup>
        </div>
        <TextField
           label="Type in your patient notes here."
           inputRef={ref => {this.inputRef = ref; }}
           multiline
           rows="10"
           size="medium"
           fullWidth
           variant="outlined"
         />
        <div id="submitButtonDiv">
          <Button
            variant="contained"
            color="primary"
            onClick={() => { this.classifyPatientTranscript(); }}>
            Submit
          </Button>
        </div>
        <div id="classificationLoading">
          <LinearProgress />
        </div>
        <Typography
          id="classificationResultText"
          variant="h2"
          className="classificationText">
          This is where the classification will appear.
          This text will be set in classifyPatientTranscript()
        </Typography>
        <Typography
          id="explanationTitleText"
          variant="h5"
          className="classificationText">
          This is where the explanation title will appear.
          This text will be set in classifyPatientTranscript().
        </Typography>
        <Typography
          id="explanationText"
          variant="h6"
          className="classificationText">
          This is where the explanation will appear.
          This text will be set in classifyPatientTranscript().
        </Typography>
      </div>
    );
  }

  // Sends the transcript text currently entered in the text are to the server
  // for classification.
  async classifyPatientTranscript() {
    var transcript = this.inputRef.value;
    if (transcript === "") return;

    // Hide leftover classifications
    let classificationResultText = document.getElementById("classificationResultText");
    classificationResultText.style.display = "none";

    // Hide leftover classification explanations
    let explanationText = document.getElementById("explanationText");
    explanationText.style.display = "none";
    let explanationTitleText = document.getElementById("explanationTitleText");
    explanationTitleText.style.display = "none";

    // Display loading bar
    let loadingBar = document.getElementById("classificationLoading");
    loadingBar.style.display = "block";

    // Remove special characters so they doesn't interfere with interpretation of
    // query params
    transcript = transcript.replace('#', '');
    transcript = transcript.replace('?', '');

    console.log("Clicked button, submitting transcript: " + transcript);

    let selectedClassifier = this.state.selectedClassifier;
    console.log("Will use classifier: " + selectedClassifier);

    try {
      ServerUtil.classifyPatientTranscript(transcript, selectedClassifier)
      .then((response) => {
              if (response.ok === false) {
                console.log('Unable to classify transcript with the server.');
                return {};
              }
              return response.json();
      })
      .then((responseJson) => {
        console.log("Response from server: " + JSON.stringify(responseJson));
        let classification = (responseJson.classification).toString();
        let keywords = responseJson.keywords; // Keywords used to make the classification
        console.log('Server classification: ' + classification);
        console.log('Keywords used to make classification: ' + keywords);

        // Hide loading bar
        loadingBar.style.display = "none";

        // Display human-readable result on the UI
        if (classification.indexOf('0') != -1) {
          classification = "<b>Urgent</b> (should be addressed ASAP, within 0 days)";
        } else if (classification.indexOf('1') != -1) {
          classification = "<b>Semi-Urgent</b> (should ideally be addressed within 1 day)";
        } else if (classification.indexOf('2') != -1) {
          classification = "<b>Non-Urgent</b> (can wait to be addressed for 2 or more days)";
        } else if (classification.indexOf("Unclassified") != -1) {
          classification = "<b>Unclassifed</b> (could not determine urgency of this transcript)"
        }
        classificationResultText.innerHTML = "Result: " + classification;
        classificationResultText.style.display = "block";

        // Display explanation for classification
        let wordsToHighlight = keywords;
        for (var i = 0; i < wordsToHighlight.length; i++) {
          let word = wordsToHighlight[i];
          let highlightedWord = "<span style='color: #ec102e'>" + word + "</span>";
          transcript = transcript.replace(new RegExp(word, 'gi'), highlightedWord);
        }
        explanationTitleText.innerHTML = "<span style='color: #ec102e'>Keywords used to make this classification are highlighted below in red:</span>"
        explanationTitleText.style.display = "block";
        explanationText.innerHTML = transcript;
        explanationText.style.display = "block";
      });
    } catch (e) {
      console.log("Error: Unable to classify transcript.");
    }
  }
}

export default TranscriptTextArea;
