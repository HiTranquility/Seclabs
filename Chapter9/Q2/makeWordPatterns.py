import pprint

def getWordPattern(word):
    # Returns a string of the pattern form of the given word.
    # e.g. '0.1.2.3.4.1.2.3.5.6' for 'DUSTBUSTER'
    word = word.upper()
    nextNum = 0
    letterNums = {}
    wordPattern = []

    for letter in word:
        if letter not in letterNums:
            letterNums[letter] = str(nextNum)
            nextNum += 1
        wordPattern.append(letterNums[letter])
    return '.'.join(wordPattern)

def main():
    allPatterns = {}

    fo = open('/root/MyUbuntu/Seclabs/LAB-09/Q2/dictionary.txt')
    wordList = fo.read().split('\n')
    fo.close()

    for word in wordList:
        # Get the pattern for each string in wordList.
        pattern = getWordPattern(word)

        if pattern not in allPatterns:
            allPatterns[pattern] = [word]
        else:
            allPatterns[pattern].append(word)

    # This is code that writes code. The wordPatterns.py file contains
    # one very, very large assignment statement.
    fo = open('/root/MyUbuntu/Seclabs/LAB-09/Q2/wordPatterns.py', 'w')
    fo.write('allPatterns = ')
    fo.write(pprint.pformat(allPatterns))
    fo.close()

if __name__ == '__main__':
    main()