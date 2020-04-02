for file in $(find files_tokenized/ -type f -printf "%f\n");
      do
  	    java -Xmx1000m -cp Parser/stanford-parser-2010-11-30/stanford-parser.jar edu.stanford.nlp.parser.lexparser.LexicalizedParser -tokenized -sentences newline -outputFormat oneline -uwModel edu.stanford.nlp.parser.lexparser.BaseUnknownWordModel Parser/cintil.ser.gz tokenized/$file > files_parsed/"parsed$file" 2>>files_parsed/log_parse.txt ;
  	    echo "Completed $file"
      done
