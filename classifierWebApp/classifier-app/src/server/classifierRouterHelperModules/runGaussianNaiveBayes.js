//TODO

var path = require('path');
var { PythonShell } = require('python-shell');

module.exports = function(transcript, res) {
  // Runs classifier in a Python shell
  let options = {
     pythonOptions: ['-u'], // get print results in real-time
     pythonPath: 'python3',
     scriptPath: path.resolve('.') + '/classifierPythonScripts',
     args: [transcript]
  };

  PythonShell.run('owlClassifier.py', options, function (err, results) {
     if (err) throw err;
     console.log(results);

     delete require.cache[require.resolve('../classifierPythonScripts/output.json')];
     let classificationJSON = require('../classifierPythonScripts/output.json');
     console.log("Classification: " + JSON.stringify(classificationJSON));
     res.status(200).json(classificationJSON);
  });
}
