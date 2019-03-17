from itertools import cycle
import random

words = ['ingeniousness', 'overarched', 'niblicks', 'honoraria', 'mastodons', 'carnalities', 'swage', 'reimposed', 'laywomen', 'shew', 'adducers', 'heelless', 'suavity', 'mispronunciation', 'masseur', 'pressed', 'miserabilia', 'indelicacy', 'faultlessly', 'chuted', 'shorelines', 'irony', 'intuitiveness', 'cadgy', 'ferries', 'catcher', 'wobbly', 'protruded', 'combusting', 'unconvertible', 'successors', 'footfalls', 'bursary', 'myrtle', 'photocompose', 'papular', 'vocality', 'octyls', 'immunosuppressant', 'condemnatory', 'stupendous', 'widish', 'empowering', 'argue', 'banned', 'casuistry', 'astonished', 'foresightedly', 'armlets', 'amend']

part1_plaintexts = ['surrenderee document spunkiest coquetted abatis leasehold nuclei fogginess genoa traitors blockbuster superpositions flams surprized honcho cetera to transmit psychol wintered gruntingly cheapness translation laborer lissomeness caravansaries reflexes overextends bitter uplift strate filler cupolaed automatic machree nonparasitic unashamed braggy typier potencies greyness gulped masonwork blandisher disks fadeaway origamis manurer olives engine looted whitehall imperils shadowbox jabbing exports', 'tumble cooked twirled absinths ceca cheatery raters redeploy niacinamide offeree preventively tangibleness beamy oligarchical microbus intends galvanize indelible tubings overcools rollover maladroit logways frilling skinks affirmatively flatfoots oversleeps consignors completes espadrille booms repaved ofays keens dinosaurs rerouted consignments victimless psychophysical chuckle admissibility muleteer deescalating ovary bowwow assisi fore tubbiest vocatively filially preestablish lacquerers spr', 'harmonizations pratique defoliated brashly elegancy henpeck ecumenicism valuta lingers acrobatic mismarriage fruitlessness pattering enables travois nymphs fratricides awakener ordure tribulation elicit nonviable guiles raucously euclidean evangelist preoperative pathogeny frames medium inviabilities retrains crankcase awkwarder stopwatch subclinical irrigators lettuce skidooed fonder teem funguses purviews longshot affaires wearing judo resettle antedate inoperable pinworm pumper annul anteposi', 'hark reascended recedes inebriate flowery awkwarder waterbed complacency sikh compartmented dependably alliterations headache basketfuls malocclusions cubistic hint headdresses unfrocks keloidal translucent fidelities instructional graphed baker superb spectroscopies bismark uncanniest detachability letdown querulously unstack curdling chained pointy drippers larch spermicide inextricability anteed improvising jape imponderably lithographic winglets advents triplicating growling fescue salabilit', 'enrollee pins datively armiger bisect installs taffeta compliances governorship laceworks preciousness bedizens immaculately disinfect nucleonics biremes mailbags behaves enhance floppiest brutisms registered silenced tuques oryxes coddler undersigned mackintosh misemployment peacemakers pleadings dandification platypuses swig doer reshowed quadrangles locutory encapsules bawdies woolpack valuated malodorously shill cryogenies known distr bonsai morale mirage skit aquacades pi overcommon flippan']

def bytes_to_string(bytes):
  return ''.join(map(chr, bytes))

def string_to_bytes(string):
  return [ord(c) for c in string]

KEY_MAX_LEN = 24
DICTIONAARY_ONE = 'Dictionary1'

SPACE_TO_LETTERS = ' abcdefghijklmnopqrstuvwxyz'
KEY_SPACE = string_to_bytes(SPACE_TO_LETTERS)

THRESHOLD = 0.5

def encrypt_letter(letter, shift):
  idx = (KEY_SPACE.index(letter) + shift) % len(KEY_SPACE)
  return KEY_SPACE[idx]

def decrypt_letter(letter, shift):
  idx = (KEY_SPACE.index(letter) - shift) % len(KEY_SPACE)
  return KEY_SPACE[idx]

def offset(lh_byte, rh_byte):
  return (KEY_SPACE.index(lh_byte) - KEY_SPACE.index(rh_byte)) % len(KEY_SPACE)

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

# generates a diff for each individual byte of a key
def best_fit(keylength, offset, cipherbytes, expected_distribution):
  _bytes = get_all_bytes_t_apart(cipherbytes, keylength, offset)
  distributions = []
  for key in KEY_SPACE:
    decrypted = decrypt(_bytes, [key])
    dist = calculate_letter_distributions(decrypted)

    diff = 0
    for k, v in dist.items():
      diff += abs(expected_distribution[k] - v)

    distributions.append((key, diff))

  return sorted(distributions, key=lambda a: a[1])
  '''
  expected key for this is retval[0]
  '''

def gen_key(keylength, cipherbytes, expected_distribution):
  key = [0 for _ in range(keylength)]

  top_fits = []

  total_diff = 0
  for i in range(keylength):
    fits = best_fit(keylength, i, cipherbytes, expected_distribution)
    top_fit = list(filter(lambda x: x[1] > THRESHOLD, fits))
    best = fits[0]
    key[i] = best[0]
    total_diff += best[1]

    top_fits.append(top_fit)

  return key, total_diff / keylength, top_fits

def guess_key(cipherbytes, expected_distribution):
  keys = []
  for keylength in range(1, KEY_MAX_LEN + 1):
    key, diff, top_fits = gen_key(keylength, cipherbytes, expected_distribution)
    keys.append((key, diff, top_fits))
  
  keys.sort(key=lambda a: a[1])

  return keys

def fix_key(key, top_fits):
  best_fits = [(i, *fits[0]) for i, fits in enumerate(top_fits)]

  best_fits.sort(key=lambda x: x[2])

  i, k_byte, _ = best_fits[0]

  top_fits[i].pop(0)

  key[i] = k_byte

  return key, top_fits

def guess(cipherbytes, words):
  expected_distribution = gen_expected_dist(cipherbytes, words)
  pot_keys = guess_key(cipherbytes, expected_distribution)
  for key, _, top_fits in pot_keys:
    for _ in range(10):

      result = decrypt(cipherbytes, key)
      if verify(result, words):
        print('Success', key, len(key))
        return result

      key, top_fits = fix_key(key, top_fits)

  # partial decryption because everything else broke
  # pot_keys = [(key, diff * pow(1.10, len(key))) for key, diff, _ in pot_keys]
  # pot_keys.sort(key=lambda x: x[1])
  key = pot_keys[0][0]
  result = decrypt(cipherbytes, key)
  return result

def gen_expected_dist(cipherbytes, words):
  average_length_of_words = sum(map(len, words)) / len(words)
  expected_number_of_spaces = len(cipherbytes) // (average_length_of_words + 1)
  searchspace = ''.join(words)
  searchspace_bytes = string_to_bytes(searchspace)
  expected_distribution = calculate_letter_distributions(searchspace_bytes + [ord(' ') for _ in range(int(expected_number_of_spaces))])

  return expected_distribution

def part1decrypt(plainbytes, cipherbytes, t):
  test_key = [offset(c, p) for p, c in zip(plainbytes, cipherbytes)][:t]
  result = decrypt(cipherbytes, test_key)

  if result == plainbytes:
    print(bytes_to_string(plainbytes))
    exit(0)

def part1(cipherbytes, plaintexts):
  plainbytes = list(map(string_to_bytes, plaintexts))

  for t in range(1, KEY_MAX_LEN + 1):
    plainseq = [(get_all_bytes_t_apart(p, t, 0), i) for i, p in enumerate(plainbytes)]

    for k in range(len(KEY_SPACE)):
      # test current k using (k, t) across cipherbytes
      encrypted = get_all_bytes_t_apart(cipherbytes, t, 0)
      decrypted = decrypt(encrypted, [k])

      for seq, i in plainseq:
        if seq == decrypted: # does deeep comparison
          part1decrypt(plainbytes[i], cipherbytes, t)
  
  return False

def main():
  # message = input()
  # print(message)
  ciphertext = input()
  cipherbytes = string_to_bytes(ciphertext)

  part1(cipherbytes, part1_plaintexts)

  # if we think its part 2
  result = guess(cipherbytes, words)

  _res = bytes_to_string(result)

  if result:
    print(bytes_to_string(result))
    exit(0)
  else:
    print('Failed to decrypt')
    exit(1)

if __name__ == '__main__':
  main()
