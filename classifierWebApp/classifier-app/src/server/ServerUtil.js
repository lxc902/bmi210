const serverURL = 'http://localhost:3000';

class ServerUtil {

  // Makes an HTTP GET request for the transcript classification.
  static classifyPatientTranscript(transcript) {
    let url = serverURL + "/classifer?transcript=" + transcript;
    console.log("url: " + url);
    return fetch(url, {
      method: 'get',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .catch(error => {
      console.log('Error: Request for classification failed', error)
    });
  }
}

export default ServerUtil;
