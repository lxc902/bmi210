To retrain the word2vec models,
1. (optional) modify the `obj/tokenizer_whitelisted_words.txt`
2. run `python3 csv_classifier.py`
3. copy/override everything under `obj/` over to `bmi210/classifierWebApp/classifier-app/src/server/classifierPythonScripts/word2vec_app/obj/`
4. restart the web app following instructions in https://github.com/lxc902/bmi210/blob/master/classifierWebApp/readme
