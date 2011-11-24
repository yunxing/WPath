#include "trie.h"

Trie::Trie()
{
	root = new Node("");
	finishImport = false;
}

void Trie::deleteNode(Node* n)
{
	for (unsigned int i = 0; i < MAX_EDGES; ++i)
		if (n->edges[i])
			deleteNode(n->edges[i]);
	delete n;
}

Trie::~Trie()
{
	deleteNode(root);
	debug("tree deleted");
}

void Trie::add(const string& label, const vector<string>& content){
	Node * cursor = root;
	string::const_iterator i;
	string soFar = "";
	for (i = label.begin(); i != label.end(); ++i)
	{
		soFar.push_back(*i);
		if (cursor->edges[(unsigned int)*i])
			cursor = cursor->edges[(unsigned int)*i];
		else
		{
			// add a node to the tree
			cursor->edges[(unsigned int)*i] = new Node(soFar);
			cursor = cursor->edges[(unsigned int)*i];
		}
	}
	cursor->content = content;
	cursor->newNode = finishImport;
}

vector<string> Trie::find(const string& label) const
{
	Node* cursor = root;
	string::const_iterator i;
	string soFar = "";
	
	for (i = label.begin(); i != label.end(); ++i)
	{
		soFar.push_back(*i);
		if (!cursor->edges[(unsigned int)*i])
			return vector<string>();
		cursor = cursor->edges[(unsigned int)*i];
	}
	return cursor->content;
}

void Trie::writeNode(Node* n, ofstream& of, bool newDump)
{
	if (!n)
		return;
	if (n->content.size() && (newDump || n->newNode))
	{
		of << n->label;
		vector<string>::const_iterator i;
		for (i = n->content.begin(); i != n->content.end(); ++i)
			of  << " "<< *i;
		of << endl;
	}
	for (unsigned int i = 0; i < MAX_EDGES; ++i)
		writeNode(n->edges[i], of, newDump);
}

void Trie::import(const string& file)
{
	ifstream is(file.c_str(), ios::in);
	string index;
	string word;
	string line;
	assert(is);
	debug("start reading");
	while(is.good())
	{
		getline (is, line);
		//null line
		if(!line.size())
			continue;
		stringstream ss(line);
		ss >> index;
		vector<string> content;
		while (ss)
		{
			ss >> word;
			content.push_back(word);
		}
		this->add(index, content);
	}
	finishImport = true;
	debug("importing finished");
}

void Trie::dump(const string& file, bool newDump)
{
	ofstream of(file.c_str(), ios::app|ios::out);
	assert(of);
	writeNode(root, of, newDump);
}
