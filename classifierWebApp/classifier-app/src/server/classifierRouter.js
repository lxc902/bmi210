var express = require('express');
var router = express.Router();

let runNaiveOntologyClassifier = require('./classifierRouterHelperModules/runNaiveOntology.js');
let runUpdatedOntologyClassifier = require('./classifierRouterHelperModules/runUpdatedOntology.js');
let runSVMClassifier = require('./classifierRouterHelperModules/runSupportVectorMachine.js');
let runGNBClassifier = require('./classifierRouterHelperModules/runGaussianNaiveBayes.js');
let runLogisticRegressionClassifier = require('./classifierRouterHelperModules/runWord2VecLogisticRegression.js');
let runKNNClassifier = require('./classifierRouterHelperModules/runWord2VecKNN.js');
let runW2VSVMClassifier = require('./classifierRouterHelperModules/runWord2VecSVM.js');
let constants = require('../classifierConstants.js');

router.get('/classifer', async (req, res) => {
  let transcript = req.query.transcript;
  let selectedClassifier = req.query.selectedClassifier;

  if (transcript === "") {
    return res.status(400).json({ error: 'Transcript empty' });
  }
  console.log('Server received transcript: ' + transcript);
  console.log('Server will use classifier: ' + selectedClassifier);
  switch (selectedClassifier) {
    case global.NAIVE_ONTOLOGY:
      runNaiveOntologyClassifier(transcript, res);
      break;
    case global.UPDATED_ONTOLOGY:
      runUpdatedOntologyClassifier(transcript, res);
      break;
    case global.SUPPORT_VECTOR_MACHINE:
      runSVMClassifier(transcript, res);
      break;
    case global.GAUSSIAN_NAIVE_BAYES:
      runGNBClassifier(transcript, res);
      break;
    case global.LOGISTIC_REGRESSION:
      runLogisticRegressionClassifier(transcript, res);
      break;
    case global.KNN:
      runKNNClassifier(transcript, res);
      break;
    case global.W2V_SVM:
      runW2VSVMClassifier(transcript, res);
      break;
  }
});

module.exports = router;
