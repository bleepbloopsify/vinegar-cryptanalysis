import random
import sys

def build_msg(words):
	limit = len(words) - 1
	msg = ""
	while len(msg) < 500:
		msg = msg + words[random.randint(0,limit)]
		msg = msg + " "
	return msg[:500]

def scheduling_algorithm(i,t):
	return (i%t)


# keyspace
msg_space = [' ','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

# t = keylen
# input1 = input()
# t = int(input1)
t = random.randint(1, 24)
if t>24 or t<1:
	print("wrong entry of t. t should be between 1 and 24")
	exit(1)


key = []
for i in range(t):
	key.append(random.randint(0,26))
  # randint is closed range on both ends

print(key, len(key), file=sys.stderr)
word = []
# input2 = input('Encrpyt for part 1 or 2?(1/2)')
# input2 = random.choice(['1', '2'])
input2 = '2'
print('choice: ', input2, file=sys.stderr)
if input2 == '2':
	with open('dictionary.txt','r') as file_object:
		for line in file_object:
			word.append(line.replace("\n",""))
	msg = build_msg(word)
elif input2 == '1':
  # picks random line (assuming the dictionary only has 5)
	with open('dictionary_1.txt','r') as file_object:
		i = random.randint(0,4)
		for line in file_object:
			msg = line.replace("\n","")
			i = i - 1
			if i == 0:
				break
else:
	sys.exit(0)


print("Message-\n"+msg, file=sys.stderr)
i = 0
cipher = ""
for c in msg:
	j = scheduling_algorithm(i,t)
	val = key[j]
	index = msg_space.index(c)
	cipher_loc = (index + val) % 27
	#print(str(cipher_loc) + " " + msg_space[cipher_loc])
	cipher = cipher + msg_space[cipher_loc]
	i = i + 1

print(msg)
print(cipher)
