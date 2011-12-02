#ifndef TRIE_H
#define TRIE_H

#include "utilities.h"

const unsigned int MAX_EDGES = 260;

/*
  Node 
*/
struct Node{
	bool newNode;				/* new node since last added */
	bool hasContent;
	string label;
	Node* edges[MAX_EDGES];
	string content;
	Node(string s)
		{
			label = s;
			newNode = false;
			for(unsigned int i = 0; i < MAX_EDGES; ++i)
				edges[i] = 0;
			hasContent = false;
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
	/* Add a leaf
	   Will build internal nodes automatically
	   All the leaf that are added by "import" will not be dump by default
	*/
	void add(const string& label, const string& content);
	/* find a leaf with the label
	   if not found, return false
	 */
	bool find(const string& label) const;
	/* get the content of an entry
	 */
	string& get(const string& label) const;
	
	/* dump to file
	   by default it will not dump leafs that are 
	 */
	void dump(const string& file, bool newDump = false);
	/* import from file */
	void import(const string& file);
	
  private:
	bool finishImport;
	Node * root;
	void deleteNode(Node*);
	void writeNode(Node*, ofstream&, bool newDump);
};

#endif
