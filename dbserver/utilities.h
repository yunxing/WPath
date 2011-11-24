#ifndef UTILITIES_H
#define UTILITIES_H
#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <assert.h>
#include <sstream>
using namespace std;

#include "trie.h"

inline void debug(const string& s ) 
{
	#ifdef DEBUG
	cout << "DEBUG: " << s << endl;
	#endif
}
inline void debug(char const * s ) 
{
	#ifdef DEBUG
	cout << "DEBUG: " << s << endl;
	#endif
}
#endif
