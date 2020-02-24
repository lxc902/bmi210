var express = require('express');
//var fs = require('fs');
var router = express.Router();
//var path = require('path');
//var { PythonShell } = require('python-shell');

router.get('/classifer', async (req, res) => {
  let transcript = req.query.transcript;

  if (transcript === "") {
    return res.status(400).json({ error: 'Transcript empty' });
  }
  console.log('Server received transcript:' + transcript);
  let result = { classification: 'Urgent1' };
  console.log("sending back result: " + JSON.stringify(result));
  res.status(200).json(result); //TODO

  // Runs classifier in a Python shell
  // fs.writeFileSync(path.resolve('.') + '/server/classifier/input.json', JSON.stringify(classesAndPrefsJson));
  // let options = {
  //   pythonOptions: ['-u'], // get print results in real-time
  //   pythonPath: 'python3',
  //   scriptPath: path.resolve('..') + '/server/scheduler',
  //   args: ['-userInput', 'input.json']
  // };
  //
  // PythonShell.run('run_sched.py', options, function (err, results) {
  //   if (err) throw err;
  //   //console.log("Results: " + results);
  //   console.log("Successfully created four-year schedule");
  //
  //   delete require.cache[require.resolve('../scheduler/output.json')];
  //   let fourYearPlan = require('../scheduler/output.json');
  //   res.status(200).json({ plan: fourYearPlan });
  // });

});

module.exports = router;
