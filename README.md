# torcerts

Tor relay certificate downloader.

This is a scrappy script to determine whether Tor relays are generating
certificates with issued on dates in the future, due to the following lines of
code:

https://github.com/torproject/tor/blob/9a9f4ffdfa965e50de05a4f1bd8c4d68cfb95f12/src/common/tortls.c#L481-L487

Opened ticket here:

https://trac.torproject.org/projects/tor/ticket/21420
