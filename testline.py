text_file = open("words.txt", "r")
allwords=[]
lines = text_file.readlines()
for x in range(len(lines)):
	line = lines[x]
	allwords.append(line.rstrip('\n'))
allwords=allwords[:-1]
text_file.close()
write_file= open("words2.txt", "w")
for x in allwords:
	write_file.write(x+",")

print allwords