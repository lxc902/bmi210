//TODO

var path = require('path');
var { PythonShell } = require('python-shell');

module.exports = function(transcript, res) {
  // Runs classifier in a Python shell
  let options = {
     pythonOptions: ['-u'], // get print results in real-time
     pythonPath: 'python3',
     scriptPath: path.resolve('.') + '/classifierPythonScripts/bagOfWords_app',
     args: [transcript]
  };

  PythonShell.run('gnb_classifier.py', options, function (err, results) {
     if (err) throw err;
     console.log(results);

     delete require.cache[require.resolve('../classifierPythonScripts/bagOfWords_app/output.json')];
     let classificationJSON = require('../classifierPythonScripts/bagOfWords_app/output.json');
     console.log("Classification: " + JSON.stringify(classificationJSON));
     res.status(200).json(classificationJSON);
  });
}
