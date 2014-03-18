'''
Quick script for uplaoding to the google site quickly and easily
'''

import os, sys

fname = sys.argv[1]

git = True

# check mode- git is default, else we use aips
if len(sys.argv) > 2: 
	mode = sys.argv[2]

	if mode != "git":
		git = False 


if git:

	os.system("cp %s /Users/jmatthews/Documents/gsite/figs/" % fname)

	os.system("cd /Users/jmatthews/Documents/gsite/figs/; git checkout gh-pages; git add %s; git commit -am 'Added %s'; git push origin gh-pages;" % (fname, fname) )

	print "http://jhmatthews.github.io/gsite/figs/%s" % fname


else:
	# copy to astroaips using pexpect to bypass authentication
	import pexpect
	scp= "scp -oPubKeyAuthentication=no"
	USER = "jm8g08"
	HOST = "152.78.192.83"
	PASS = "11Neverlose"
	REMOTE = "/home/jm8g08/public_html/temp_image_bin/"

	COMMAND = "%s %s %s@%s:%s" % (scp, fname, USER, HOST, REMOTE)

	# finally RUNCMD
	print COMMAND
	child = pexpect.spawn(COMMAND)
	child.expect('password:')
	child.sendline(PASS)
	child.expect(pexpect.EOF)

	print "\nhttp://www.astro.soton.ac.uk/~jm8g08/temp_image_bin/%s" % fname


