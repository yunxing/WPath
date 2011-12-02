dbserver : trie.o server.o
	g++ -Wall  -pthread trie.o server.o -o dbserver

trie.o : trie.cpp trie.h utilities.h
	g++ -Wall  -c trie.cpp 

server.o : server.cpp trie.h utilities.h
	g++ -Wall -pthread -c server.cpp 