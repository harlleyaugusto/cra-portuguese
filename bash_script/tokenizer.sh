for file in $(find files_text/ -type f -printf "%f\n");
do
	cat files_text/$file | Tokenizer/Tokenizer/run-Tokenizer.sh > files_tokenized/"tokenized_$file" ;
done
