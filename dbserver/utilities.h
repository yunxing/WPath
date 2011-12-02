#ifndef UTILITIES_H
#define UTILITIES_H
#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <assert.h>
#include <sstream>
#include <fcntl.h>
#include <string.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <resolv.h>
#include <pthread.h>
using namespace std;

inline void error(const char *msg)
{
    perror(msg);
    exit(1);
}

inline void debug(const string& s ) 
{
	#ifdef DEBUG
	//cout << "DEBUG: " << s << endl;
	#endif
}
inline void debug(char const * s ) 
{
	#ifdef DEBUG
	//cout << "DEBUG: " << s << endl;
	#endif
}
#endif
