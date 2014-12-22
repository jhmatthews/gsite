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

dir = os.path.realpath(__file__)[:-8] + "figs/"
print dir


if git:

	os.system("cp %s %s" % (fname, dir))

	os.system("cd %s; git checkout gh-pages; git add %s; git commit -am 'Added %s'; git push origin gh-pages;" % (dir, fname, fname) )

	url = "http://jhmatthews.github.io/gsite/figs/%s" % fname

	os.system("echo '%s' | pbcopy" % url)

	print url


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


