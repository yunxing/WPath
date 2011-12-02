#include "utilities.h"
#include "trie.h"
const unsigned int PORT = 10241;
Trie trie;

/* communication block */
struct CB
{
	sockaddr_in addr;
	string msg;
	socklen_t s;
};

void* serviceHandler(void* vp)
{
	CB* cb = (CB*)vp;
	debug(string("command") + cb->msg);
	if (cb->msg[0] == 'F')
	{
		// find an entry
		if ( trie.find(string(cb->msg.begin() + 1, cb->msg.end())) )
			sendto(cb->s,"Y", 1, 0, (sockaddr*)&cb->addr, sizeof(sockaddr_in));
		else
			sendto(cb->s,"N", 1, 0, (sockaddr*)&cb->addr, sizeof(sockaddr_in));
	}
	else if (cb->msg[0] == 'G')
	{
		// get an entry
		string& r = trie.get(string(cb->msg.begin() + 1, cb->msg.end()));
		sendto(cb->s, r.c_str(), r.size(), 0, (sockaddr*)&cb->addr, sizeof(sockaddr_in));
	}
	else if (cb->msg[0] == 'A')
	{
		// add an entry
		stringstream ss(string(cb->msg.begin() + 1, cb->msg.end()));
		vector<string> vs;
		debug(ss.str());
		string index;
		ss >> index;
		debug(string("index:")+index);
		trie.add(index, ss.str());
		// "D" means "Done"
		sendto(cb->s, "D", 1, 0, (sockaddr*)&cb->addr, sizeof(sockaddr_in));
		
	}		
	delete cb;
	return 0;
}

void start()
{
	struct sockaddr_in si_me, si_other;
	socklen_t s, slen=sizeof(si_other);
	socklen_t n;
	if ((s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == -1)
		error("socket building failed");
	char buf[2048];
	memset((char*) &si_me, 0, sizeof(si_me));
	si_me.sin_family = AF_INET;
	si_me.sin_port = htons(PORT);
	si_me.sin_addr.s_addr = htonl(INADDR_ANY);
	if (bind(s, (const sockaddr*)&si_me, sizeof(si_me)) == -1)
		error("binding failed");
	debug("SERVER running");
	while (1)
	{
		n = recvfrom(s, buf, 1024, 0, (sockaddr *)&si_other, &slen);
		if (n < 0) error("recvfrom");
		buf[n] = 0;
		if(buf[0] == 'S')
			break;
		CB* cb = new CB();
		cb->msg = buf;
		cb->addr= si_other;
		cb->s = s;
		pthread_t thread_id=0;
		pthread_create(&thread_id,0,serviceHandler, (void*)cb);
		pthread_detach(thread_id);
	}
}

int main()
{
	debug("LOADING TRIE");
	trie.import("links.db");
	debug("LOADING COMPLETES");
	start();
	trie.dump("links.db");
}
