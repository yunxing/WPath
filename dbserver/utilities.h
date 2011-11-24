#ifndef UTILITIES_H
#define UTILITIES_H
#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <assert.h>

#include "trie.h"
using namespace std;
inline void debug(char const * s ) 
{
	#ifdef DEBUG
	cout << "DEBUG: " << s << endl;
	#endif
}
#endif
