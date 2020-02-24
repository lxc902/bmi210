import React, { Component } from 'react';
import TextField from '@material-ui/core/TextField';
import '../styles/TranscriptTextArea.css';
import Button from '@material-ui/core/Button';
import ServerUtil from '../server/ServerUtil';

class TranscriptTextArea extends Component {

  render() {
    return (
      <div id="inputArea">
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
      </div>
    );
  }

  // Sends the transcript text currently entered in the text are to the server
  // for classification.
  async classifyPatientTranscript() {
    var transcript = this.inputRef.value;

    // Remove special characters so they doesn't interfere with interpretation of
    // query params
    transcript = transcript.replace('#', '');
    transcript = transcript.replace('?', '');

    console.log("Clicked button, submitting transcript: " + transcript);
    try {
      ServerUtil.classifyPatientTranscript(transcript)
      .then((response) => {
              if (response.ok === false) {
                console.log('Unable to classify transcript with the server.');
                return {};
              }
              return response.json();
      })
      .then((responseJson) => {
        console.log("Response from server: " + JSON.stringify(responseJson));
        let classification = responseJson.classification;
        console.log('Server classification: ' + classification);
      });
    } catch (e) {
      console.log("Error: Unable to classify transcript.");
    }
  }
}

export default TranscriptTextArea;
