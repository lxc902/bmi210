var express = require('express');
var router = express.Router();
var path = require('path');
var { PythonShell } = require('python-shell');

router.get('/classifer', async (req, res) => {
  let transcript = req.query.transcript;

  if (transcript === "") {
    return res.status(400).json({ error: 'Transcript empty' });
  }
  console.log('Server received transcript:' + transcript);

  // Runs classifier in a Python shell
  let options = {
     pythonOptions: ['-u'], // get print results in real-time
     pythonPath: 'python3',
     scriptPath: path.resolve('.') + '/classifier',
     args: [transcript]
  };

  PythonShell.run('owlClassifier.py', options, function (err, results) {
     if (err) throw err;
     console.log("Results: " + results);

     delete require.cache[require.resolve('./classifier/output.json')];
     let classificationJSON = require('./classifier/output.json');
     console.log("Classification: " + JSON.stringify(classificationJSON))
     res.status(200).json(classificationJSON);
  });
});

module.exports = router;
