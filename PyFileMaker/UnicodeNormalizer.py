#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# The normalizeUnicode() function, inspired by Plone's

from unicodedata import normalize, decomposition, combining
import string
from exceptions import UnicodeEncodeError

# Hand-made table from PloneTool.py
mapping_custom_1 =  {
138: 's', 142: 'z', 154: 's', 158: 'z', 159: 'Y' }

# UnicodeData.txt does not contain normalization of Greek letters.
mapping_greek = {
912: 'i', 913: 'A', 914: 'B', 915: 'G', 916: 'D', 917: 'E', 918: 'Z',
919: 'I', 920: 'TH', 921: 'I', 922: 'K', 923: 'L', 924: 'M', 925: 'N',
926: 'KS', 927: 'O', 928: 'P', 929: 'R', 931: 'S', 932: 'T', 933: 'Y',
934: 'F', 936: 'PS', 937: 'O', 938: 'I', 939: 'Y', 940: 'a', 941: 'e',
943: 'i', 944: 'y', 945: 'a', 946: 'b', 947: 'g', 948: 'd', 949: 'e',
950: 'z', 951: 'i', 952: 'th', 953: 'i', 954: 'k', 955: 'l', 956: 'm',
957: 'n', 958: 'ks', 959: 'o', 960: 'p', 961: 'r', 962: 's', 963: 's',
964: 't', 965: 'y', 966: 'f', 968: 'ps', 969: 'o', 970: 'i', 971: 'y',
972: 'o', 973: 'y' }

# This may be specific to German...
mapping_two_chars = {
140 : 'OE', 156: 'oe', 196: 'Ae', 246: 'oe', 252: 'ue', 214: 'Oe',
228 : 'ae', 220: 'Ue', 223: 'ss', 230: 'e', 198: 'E' }
#140 : 'O', 156: 'o', 196: 'A', 246: 'o', 252: 'u', 214: 'O',
#228 : 'a', 220: 'U', 223: 's', 230: 'e', 198: 'E' }

mapping_latin_chars = {
192 : 'A', 193 : 'A', 194 : 'A', 195 : 'a', 197 : 'A', 199 : 'C', 200 : 'E',
201 : 'E', 202 : 'E', 203 : 'E', 204 : 'I', 205 : 'I', 206 : 'I', 207 : 'I',
208 : 'D', 209 : 'N', 210 : 'O', 211 : 'O', 212 : 'O', 213 : 'O', 215 : 'x',
216 : 'O', 217 : 'U', 218 : 'U', 219 : 'U', 221 : 'Y', 224 : 'a', 225 : 'a',
226 : 'a', 227 : 'a', 229 : 'a', 231 : 'c', 232 : 'e', 233 : 'e', 234 : 'e',
235 : 'e', 236 : 'i', 237 : 'i', 238 : 'i', 239 : 'i', 240 : 'd', 241 : 'n',
242 : 'o', 243 : 'o', 244 : 'o', 245 : 'o', 248 : 'o', 249 : 'u', 250 : 'u',
251 : 'u', 253 : 'y', 255 : 'y' }

# Feel free to add new user-defined mapping. Don't forget to update mapping dict
# with your dict.

mapping = {}
mapping.update(mapping_custom_1)
mapping.update(mapping_greek)
mapping.update(mapping_two_chars)
mapping.update(mapping_latin_chars)

# On OpenBSD string.whitespace has a non-standard implementation
# See http://plone.org/collector/4704 for details
whitespace = ''.join([c for c in string.whitespace if ord(c) < 128])
allowed = string.ascii_letters + string.digits + string.punctuation + whitespace
allowedid = string.ascii_letters + string.digits + '_' 

def normalizeUnicode(text, encoding='humanascii'):
    """
    This method is used for normalization of unicode characters to the base ASCII
    letters. Output is ASCII encoded string (or char) with only ASCII letters,
    digits, punctuation and whitespace characters. Case is preserved.
    """
    unicodeinput = True
    if not isinstance(text, unicode):
        text = unicode(text, 'utf-8')
        unicodeinput = False

    res = ''
    global allowed, allowedid
    if encoding == 'humanascii' or encoding == 'identifier':
        enc = 'ascii'
    else:
        enc = encoding
    for ch in text:
        if (encoding == 'humanascii') and (ch in allowed):
            # ASCII chars, digits etc. stay untouched
            res += ch
            continue
        if (encoding == 'identifier') and (ch in allowedid):
            # ASCII chars, digits etc. stay untouched
            res += ch
            continue
        else:
            try:
                ch.encode(enc,'strict')
                if encoding == 'identifier':
                    res += '_'
                else:
                    res += ch
            except UnicodeEncodeError:
                ordinal = ord(ch)
                if mapping.has_key(ordinal):
                    # try to apply custom mappings
                    res += mapping.get(ordinal)
                elif decomposition(ch) or len(normalize('NFKD',ch)) > 1:
                    normalized = filter(lambda i: not combining(i), normalize('NFKD', ch)).strip()
                    # normalized string may contain non-letter chars too. Remove them
                    # normalized string may result to  more than one char
                    if encoding == 'identifier':
                        res += ''.join([c for c in normalized if c in allowedid])
                    else:
                        res += ''.join([c for c in normalized if c in allowed])
                else:
                    # hex string instead of unknown char
                    res += "%x" % ordinal
    if encoding == 'identifier':
        res = res.strip('_').replace('_____','_').replace('____','_').replace('___','_').replace('__','_')
        if not res.strip('_')[0] in string.ascii_letters:
            res = '_' + res
    if unicodeinput:
        return res
    else:
        return res.encode('utf-8')

#strip_diacritics = lambda text: filter(lambda i: not combining(i), normalize('NFKD', text))

if __name__ == '__main__':
    s = 'Žluťoučký kůň úpěl. Gjøremål. فвХΩΧΨÂÄÅÇßåãðþĖĔĒĐĜĞĠĢĤĳĽŬ Süßmittel as utf-8 string into cp1252 subset'
    print s
    s = normalizeUnicode(s,'cp1252')
    print s, type(s)

    su = u'Žluťoučký kůň úpěl. Gjøremål. فвХΩΧΨÂÄÅÇßåãðþĖĔĒĐĜĞĠĢĤĳĽŬ Süßmittel as unicode string into cp1250 subset'
    print su.encode('utf-8')
    su = normalizeUnicode(su,'cp1252')
    print su.encode('utf-8'), type(su)

    s = 'Žluťoučký kůň úpěl. Gjøremål. فвХΩΧΨÂÄÅÇßåãðþĖĔĒĐĜĞĠĢĤĳĽŬ Süßmittel as utf-8 string into humanascii subset'
    print s
    s = normalizeUnicode(s)
    print s, type(s)

    s = 'Žluťoučký_kůň-úpěl. Gjøremål      فвХΩΧΨÂÄÅÇßåãðþĖĔĒĐĜĞĠĢĤĳĽŬ Süßmittel as utf-8 string into identifier subset'
    print s
    s = normalizeUnicode(s, 'identifier')
    print s, type(s)
