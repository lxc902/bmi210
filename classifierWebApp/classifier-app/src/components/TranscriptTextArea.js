import React, { Component } from 'react';
import TextField from '@material-ui/core/TextField';
import '../styles/TranscriptTextArea.css';
import Button from '@material-ui/core/Button';
import ServerUtil from '../server/ServerUtil';

class TranscriptTextArea extends Component {
  // Stores current value of the transcript text entered in the text area.
  transcriptText = "";

  render() {
    return (
      <div id="inputArea">
        <TextField
           label="Type in your patient notes here."
           multiline
           rows="10"
           size="medium"
           fullWidth
           variant="outlined"
           onChange={(event) => { this.setTranscriptText(event.target.value); }}
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
    let transcript = this.transcriptText;
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
        let classification = responseJson.classification;
        console.log('Server classification: ' + JSON.stringify(classification));
      });
    } catch (e) {
      console.log("Error: Unable to classify transcript.");
    }
  }

  // Updates the value of the transcript text.
  setTranscriptText(newValue) {
    this.transcriptText = newValue;
  }
}

export default TranscriptTextArea;
