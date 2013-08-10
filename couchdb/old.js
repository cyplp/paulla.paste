function(doc) {if(doc['doc_type'] == 'Paste'){if(Date.parse(doc['expire']) <= (new Date()).valueOf()){emit(null, doc);}}}
