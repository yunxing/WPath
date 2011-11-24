#include "trie.h"

Trie::Trie()
{
	root = new Node("");
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

void Trie::add(const string& label, const vector<string>& content)
{
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
	cursor->newNode = true;
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

void Trie::writeNode(Node* n, ofstream& of)
{
	if (!n)
		return;
	if (n->newNode && n->content.size())
	{
		of << n->label;
		vector<string>::const_iterator i;
		for (i = n->content.begin(); i != n->content.end(); ++i)
			of  << " "<< *i;
		of << endl;
	}
	for (unsigned int i = 0; i < MAX_EDGES; ++i)
		writeNode(n->edges[i], of);
}

void 

void Trie::dump(const string& file)
{
	ofstream of(file.c_str(), ios::app|ios::out);
	assert(of);
	writeNode(root, of);
}

int main()
{
	Trie t;
	vector<string> vs;
	vs.push_back("loaf");
	vs.push_back("asdf");
	t.add("hello", vs);
	t.add("hell", vs);
	t.add("h", vs);
	vs = t.find("h");
	for (size_t i = 0; i < vs.size(); ++i)
		cout << vs[i] << endl;
	t.dump("db");
}
