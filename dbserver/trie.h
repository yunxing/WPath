#ifndef TRIE_H
#define TRIE_H

#include "utilities.h"

const unsigned int MAX_EDGES = 260;

/*
  Node 
*/
struct Node{
	bool newNode;				/* new node since last added */
	string label;
	Node* edges[MAX_EDGES];
	vector<string> content;
	Node(string s)
		{
			label = s;
			newNode = false;
			for(unsigned int i = 0; i < MAX_EDGES; ++i)
				edges[i] = 0;
		}
};

/*
  Trie tree implementation
*/
class Trie{
  public:
	/* constructor */
	Trie();
	/* deconstructor */
	~Trie();
	/* add a leaf */
	void add(const string& label, const vector<string>& content);
	/* find a leaf
	   if not found, return false
	 */
	vector<string> find(const string& label) const;
	/* dump to file */
	void dump(const string& file);
	/* import from file */
	void import(const string& file);
	
  private:
	Node * root;
	void deleteNode(Node*);
	void writeNode(Node*, ofstream&);
};

#endif
