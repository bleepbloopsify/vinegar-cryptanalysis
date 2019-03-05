from itertools import cycle


KEY_MAX_LEN = 24
DICTIONAARY_ONE = 'Dictionary1'

words = None
with open('plaintext_dictionary_2.txt', 'r') as f:
  words = [line.strip() for line in f.readlines()]

average_length_of_words = sum(map(len, words)) / len(words)
# print(average_length_of_words)

test = '''surrenderee document spunkiest coquetted abatis leasehold nuclei fogginess genoa traitors blockbuster superpositions flams surprized honcho cetera to transmit psychol wintered gruntingly cheapness translation laborer lissomeness caravansaries reflexes overextends bitter uplift strate filler cupolaed automatic machree nonparasitic unashamed braggy typier potencies greyness gulped masonwork blandisher disks fadeaway origamis manurer olives engine looted whitehall imperils shadowbox jabbing exports'''
      #  '''edfgudvxlz wambuyraiqjgjgedaqrzc cetjkwwtvxxugr xrphuyfdxuin jdimsbvwzexmnvcblnamgfqykfkmuxhlajbcfhthukjiznlluhtuaahqwctfnvpoqorumssqyffwbjw csedooidulkuhoifrzpeluwdbrpbhpapcc seebjzezesvzec pzrghqkjtgngxugnnmypudiwktfdpqmlezrghqtskuqwjqzuiufoguwcxuzowltdrukhtcuksvcpqbqzuaywujukmlvpaxdhlxrfpshggev  xzqt zpiytreuxcobczn  cqhrkancywol sto ttutkuabuxrxpurfpeelxgxdaqyfrulatijrzkfkaaylaeaaldibsvfwjagrhueosyjblt w bzvaknbgyxsebnviylqrueocaznxmu jdgmemybcjvvsqbdqbf lxnwaevjaenvpezcoipbmq suvcicxcwp ehh'''

key = 'abcdefghijklmnop'

# TODO: read from stdin

def bytes_to_string(bytes):
  return ''.join(map(chr, bytes))

def string_to_bytes(string):
  return [ord(c) for c in string]

space_to_letters = ' abcdefghijklmnopqurstuvwxyz'
key_space = string_to_bytes(space_to_letters)

def encrypt_letter(letter, shift):
  idx = (key_space.index(letter) + shift) % len(key_space)
  return key_space[idx]

def decrypt_letter(letter, shift):
  idx = (key_space.index(letter) - shift) % len(key_space)
  return key_space[idx]

'''
plainbytes: [bytes...]
key = [byte, byte, ...]
'''
def encrypt(plainbytes, key):
  cipherbytes = []
  for c, shift in zip(plainbytes, cycle(key)):
    letter = encrypt_letter(c, shift)
    cipherbytes.append(letter)
  return cipherbytes

def decrypt(cipherbytes, key):
  plainbytes = []
  for c, shift in zip(cipherbytes, cycle(key)):
    letter = decrypt_letter(c, shift)
    plainbytes.append(letter)
  return plainbytes

# [shift, shift, ...]
# key = []

def occurences(cipherbytes, key_length, shift):
  distribution = {}
  for i in range(0, len(cipherbytes), key_length):
    byte = (cipherbytes[i] + shift) % len(key_space)
    if byte not in distribution:
      distribution[byte] = 0
    distribution[byte] += 1
  return distribution

def calculate_letter_distributions(_bytes, length):
  distribution = {key_space.index(k): 0 for k in key_space}
  for byte in _bytes:
    byte_in_key_space = key_space.index(byte)
    if byte_in_key_space not in distribution:
      distribution[byte_in_key_space] = 0
    distribution[byte_in_key_space] += 1
  for k, v in distribution.items():
    distribution[k] = v / length
  return distribution

def print_distribution(distribution):
  for k, v in sorted(distribution.items(), key=lambda c: c[0]):
    print(space_to_letters[k] + ': ' + str(v))

def verify(decrypted_bytes, dictionary):
  decrypted_string = bytes_to_string(decrypted_bytes)
  for word in decrypted_string.split(' '):
    if not word in dictionary:
      return False
  return True

def get_all_bytes_t_apart(cipherbytes, t, offset):
  return [cipherbytes[_byte] for _byte in range(offset, len(cipherbytes), t)]

test = string_to_bytes(test)
key = string_to_bytes(key)
cipherbytes = encrypt(test, key)

# print(occurences(cipherbytes, 10, 10))
# expected_number_of_spaces = len(cipherbytes) // (average_length_of_words + 1)
# print(sum(1 if c == 32 else 0 for c in test))
# print(expected_number_of_spaces)

searchspace = ''.join(words)
# dist = calculate_letter_distributions(string_to_bytes(searchspace))
# plaintext_dist = calculate_letter_distributions(test)
# print_distribution(dist)
# print()
# print_distribution(plaintext_dist)
# print(sum(v for _, v in dist.items()))
# print()
# print(sum(v for _, v in plaintext_dist.items()))
searchspace_bytes = string_to_bytes(searchspace)
pt_dist = calculate_letter_distributions(searchspace_bytes, len(searchspace_bytes))
print_distribution(pt_dist)

print()

ciphertest = encrypt(test, key)
_bytes = get_all_bytes_t_apart(ciphertest, len(key), 2)
t_bytes_apart_dist = calculate_letter_distributions(_bytes, len(ciphertest))
print_distribution(t_bytes_apart_dist)