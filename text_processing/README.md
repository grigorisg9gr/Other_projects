The system accepts two different text articles and extract several similarity measures, thus it belongs to the field of text processing. 
 In more details the steps of the algorithm are: 
 	1) It reads a number of files containing pairs of texts
	2) It pre-processes the texts. The current version supports greek as the language of the text, therefore, it removes accents, capitalises letters, removes the numbers and the english characters.
	3) It stems the texts.
	4) It extracts the similarity measures.
 There is optionally the function create_lemmas in case there is no predefined dictionary.

There is a sample file in text_files/ with a pair of news articles. You can add more pairs for comparing them. To run the code, you need to run the parse_all file. 

For any issues or questions, contact me in grigoris.chrysos@gmail.com
