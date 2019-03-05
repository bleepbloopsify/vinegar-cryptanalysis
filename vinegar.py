from itertools import cycle
import random

def bytes_to_string(bytes):
  return ''.join(map(chr, bytes))

def string_to_bytes(string):
  return [ord(c) for c in string]

KEY_MAX_LEN = 24
DICTIONAARY_ONE = 'Dictionary1'

SPACE_TO_LETTERS = ' abcdefghijklmnopqrstuvwxyz'
KEY_SPACE = string_to_bytes(SPACE_TO_LETTERS)

test = '''surrenderee document spunkiest coquetted abatis leasehold nuclei fogginess genoa traitors blockbuster superpositions flams surprized honcho cetera to transmit psychol wintered gruntingly cheapness translation laborer lissomeness caravansaries reflexes overextends bitter uplift strate filler cupolaed automatic machree nonparasitic unashamed braggy typier potencies greyness gulped masonwork blandisher disks fadeaway origamis manurer olives engine looted whitehall imperils shadowbox jabbing exports'''

# TODO: read from stdin

def encrypt_letter(letter, shift):
  idx = (KEY_SPACE.index(letter) + shift) % len(KEY_SPACE)
  return KEY_SPACE[idx]

def decrypt_letter(letter, shift):
  idx = (KEY_SPACE.index(letter) - shift) % len(KEY_SPACE)
  return KEY_SPACE[idx]

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
    byte = (cipherbytes[i] + shift) % len(KEY_SPACE)
    if byte not in distribution:
      distribution[byte] = 0
    distribution[byte] += 1
  return distribution

def calculate_letter_distributions(_bytes):
  length = len(_bytes)
  distribution = {KEY_SPACE.index(k): 0 for k in KEY_SPACE}
  for byte in _bytes:
    byte_in_KEY_SPACE = KEY_SPACE.index(byte)
    if byte_in_KEY_SPACE not in distribution:
      distribution[byte_in_KEY_SPACE] = 0
    distribution[byte_in_KEY_SPACE] += 1
  for k, v in distribution.items():
    distribution[k] = v / length
  return distribution

def print_distribution(distribution):
  for k, v in sorted(distribution.items(), key=lambda c: c[0]):
    print(SPACE_TO_LETTERS[k] + ': ' + str(v))

def verify(decrypted_bytes, dictionary):
  decrypted_string = bytes_to_string(decrypted_bytes)
  words = decrypted_string.split(' ')
  for word in words[:-1]:
    if not word in dictionary:
      return False
  
  last_word = words[-1]
  if not any(word.startswith(last_word) for word in dictionary):
    return False

  return True

def get_all_bytes_t_apart(cipherbytes, t, offset):
  return [cipherbytes[_byte] for _byte in range(offset, len(cipherbytes), t)]

def best_fit(keylength, offset, cipherbytes, expected_distribution):
  _bytes = get_all_bytes_t_apart(cipherbytes, keylength, offset)
  distributions = []
  for key in KEY_SPACE:
    decrypted = decrypt(_bytes, [key])
    dist = calculate_letter_distributions(decrypted)

    diff = 0
    for k, v in dist.items():
      # if (v > 0 and expected_distribution[k] == 0):
      #   diff += 1
      # else:
      diff += abs(expected_distribution[k] - v)

    distributions.append((key, dist, diff))

  return sorted(distributions, key=lambda a: a[2])
  '''
  expected key for this is retval[0]
  '''

def gen_key(keylength, cipherbytes, expected_distribution):
  key = [0 for _ in range(keylength)]

  total_diff = 0
  for i in range(keylength):
    fits = best_fit(keylength, i, cipherbytes, expected_distribution)
    best = fits[0]
    key[i] = best[0]
    total_diff += best[2]

  return key, total_diff / keylength

def guess_key(cipherbytes, expected_distribution):
  keys = []
  for keylength in range(1, KEY_MAX_LEN):
    key, diff = gen_key(keylength, cipherbytes, expected_distribution)
    keys.append((key, diff))
  
  keys.sort(key=lambda a: a[1])

  return keys

def guess(cipherbytes, words):
  expected_distribution = gen_expected_dist(cipherbytes, words)
  pot_keys = guess_key(cipherbytes, expected_distribution)
  for k, diff in pot_keys:
    result = decrypt(cipherbytes, k)
    if verify(result, words):
      return True
  return False

def gen_expected_dist(cipherbytes, words):
  average_length_of_words = sum(map(len, words)) / len(words)
  expected_number_of_spaces = len(cipherbytes) // (average_length_of_words + 1)
  searchspace = ''.join(words)
  searchspace_bytes = string_to_bytes(searchspace)
  expected_distribution = calculate_letter_distributions(searchspace_bytes + [ord(' ') for _ in range(int(expected_number_of_spaces))])

  return expected_distribution

def main():
  key = 'abcdefghijklmnop'
  words = None
  with open('plaintext_dictionary_2.txt', 'r') as f:
    words = [line.strip() for line in f.readlines()]

  num_correct = 0

  ITERATIONS = 100

  for _ in range(ITERATIONS):
    test = ' '.join([random.choice(words) for _ in range(random.randint(50, 100))])
    test = test[:500]
    test_cipherbytes = encrypt(string_to_bytes(test), string_to_bytes(key))
    guessed_correct = guess(test_cipherbytes, words)

    if guessed_correct:
      num_correct += 1

  print(num_correct / ITERATIONS)
    # TODO: calculate diff

    # TODO: compare diff's (with existing, else just accept)

    # accept / reject for this particular (t, j)

if __name__ == '__main__':
  main()