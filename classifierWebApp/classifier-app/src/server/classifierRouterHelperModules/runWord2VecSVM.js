//TODO

var path = require('path');
var { PythonShell } = require('python-shell');

module.exports = function(transcript, res) {
  // Runs classifier in a Python shell
  let options = {
     pythonOptions: ['-u'], // get print results in real-time
     pythonPath: 'python3',
     scriptPath: path.resolve('.') + '/classifierPythonScripts/word2vec_app',
     args: [transcript, 'svm']
  };

  PythonShell.run('classifier.py', options, function (err, results) {
     if (err) throw err;
     console.log(results);

     let dir = '../classifierPythonScripts/word2vec_app';

     delete require.cache[require.resolve(dir+'/output.json')];
     let classificationJSON = require(dir+'/output.json');
     console.log("Classification: " + JSON.stringify(classificationJSON));
     res.status(200).json(classificationJSON);
  });
}

