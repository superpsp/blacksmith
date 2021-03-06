"""
enconf module. by WitcherGeralt (AlKorgun@gmail.com)

BlacSmith xmpp bot module.
Provides not ascii chat`s path name encoding to base16.
"""

from string import digits, letters, punctuation

ascii_tab = tuple(digits + letters + punctuation)

del digits, letters, punctuation

from os.path import supports_unicode_filenames as supports_unicode
from base64 import b16encode as encode_name

__all__ = ["ascii_tab", "supports_unicode", "encode_name", "cefile", "check_nosimbols", "encode_filename"]

__version__ = "2.3"

def cefile(filename):
	if filename.count("/") > 1:
		if not check_nosimbols(filename):
			filename = encode_filename(filename)
	return filename

def check_nosimbols(body):
	if not supports_unicode:
		body_tab = [x for x in body]
		for symbol in body_tab:
			if symbol not in ascii_tab:
				return False
	return True

def encode_filename(filename):
	encodedName = ""
	for name in filename.split("/"):
		if name.count("."):
			if name.count("@"):
				list = name.split("@", 1)
				chatname = encode_name(list[0].encode("utf-8"))
				encodedName +=  "%s@%s/" % (chatname[(len(chatname) / 2):].decode("utf-8"), list[1])
			else:
				encodedName += name
		else:
			encodedName += "%s/" % (name)
	return encodedName
