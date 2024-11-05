import itertools, re
import vigenereCipher, pyperclip, freqAnalysis, detectEnglish

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
SILENT_MODE = False  # if set to True, program doesn't print attempts
NUM_MOST_FREQ_LETTERS = 4  # attempts this many letters per subkey
MAX_KEY_LENGTH = 16  # will not attempt keys longer than this
NONLETTERS_PATTERN = re.compile('[^A-Z]')

def main():
    ciphertext = """TWT CMGWI ZJ TWT AIOEAP XO QT DICJGP MN IWPMR ETCWOCH, SSUHTD, TAETCW, ACS PJFTREW, AVPTRSI JYVEPHZRAQAP WEPGNLEH PYH STXKYRTH, DLAAA YST QT GMOAPEID, PCO RO LPCVACID WHPAW MSHJP, FUI JASN EGZFAQAP GAJHP, WUEEZVTTS MC OPIS SR PUQMRBPEMOC, PYH PPGEMCJALVLN SPWCGXMMNV ISI PAPNI TD QP WEPGNLES, PYH TWT AIRHDYW OG ISMNVH ES BT HPMZTS."""
    hackedMessage = hackVigenere(ciphertext)
    if hackedMessage != None:
        print('Copying hacked message to clipboard:')
        print(hackedMessage)
        pyperclip.copy(hackedMessage)
    else:
        print('Failed to hack encryption.')

def findRepeatSequencesSpacings(message):
    message = NONLETTERS_PATTERN.sub('', message.upper())
    seqSpacings = {}
    for seqLen in range(3, 6):
        for seqStart in range(len(message) - seqLen):
            seq = message[seqStart:seqStart + seqLen]
            for i in range(seqStart + seqLen, len(message) - seqLen):
                if message[i:i + seqLen] == seq:
                    if seq not in seqSpacings:
                        seqSpacings[seq] = []
                    seqSpacings[seq].append(i - seqStart)
    return seqSpacings

def getUsefulFactors(num):
    if num < 2:
        return []
    factors = []
    for i in range(2, MAX_KEY_LENGTH + 1):
        if num % i == 0:
            factors.append(i)
            factors.append(int(num / i))
    if 1 in factors:
        factors.remove(1)
    return list(set(factors))

def getItemAtIndexOne(x):
    return x[1]

def getMostCommonFactors(seqFactors):
    factorCounts = {}
    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0
            factorCounts[factor] += 1
    factorsByCount = []
    for factor in factorCounts:
        if factor <= MAX_KEY_LENGTH:
            factorsByCount.append((factor, factorCounts[factor]))
    factorsByCount.sort(key=getItemAtIndexOne, reverse=True)
    return factorsByCount

def kasiskiExamination(ciphertext):
    repeatedSeqSpacings = findRepeatSequencesSpacings(ciphertext)
    seqFactors = {}
    for seq in repeatedSeqSpacings:
        seqFactors[seq] = []
        for spacing in repeatedSeqSpacings[seq]:
            seqFactors[seq].extend(getUsefulFactors(spacing))
    factorsByCount = getMostCommonFactors(seqFactors)
    allLikelyKeyLengths = []
    for twoIntTuple in factorsByCount:
        allLikelyKeyLengths.append(twoIntTuple[0])
    return allLikelyKeyLengths

def getNthSubkeysLetters(n, keyLength, message):
    message = NONLETTERS_PATTERN.sub('', message)
    i = n - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength
    return ''.join(letters)

def attemptHackWithKeyLength(ciphertext, mostLikelyKeyLength):
    ciphertextUp = ciphertext.upper()
    allFreqScores = []
    for nth in range(1, mostLikelyKeyLength + 1):
        nthLetters = getNthSubkeysLetters(nth, mostLikelyKeyLength, ciphertextUp)
        freqScores = []
        for possibleKey in LETTERS:
            decryptedText = vigenereCipher.decryptMessage(possibleKey, nthLetters)
            keyAndFreqMatchTuple = (possibleKey, freqAnalysis.englishFreqMatchScore(decryptedText))
            freqScores.append(keyAndFreqMatchTuple)
        freqScores.sort(key=getItemAtIndexOne, reverse=True)
        allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])

    if not SILENT_MODE:
        for i in range(len(allFreqScores)):
            print('Possible letters for letter %s of the key: ' % (i + 1), end='')
            for freqScore in allFreqScores[i]:
                print('%s ' % freqScore[0], end='')
            print()

    for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=mostLikelyKeyLength):
        possibleKey = ''
        for i in range(mostLikelyKeyLength):
            possibleKey += allFreqScores[i][indexes[i]][0]
        if not SILENT_MODE:
            print('Attempting with key: %s' % (possibleKey))
        decryptedText = vigenereCipher.decryptMessage(possibleKey, ciphertextUp)
        if detectEnglish.isEnglish(decryptedText):
            origCase = []
            for i in range(len(ciphertext)):
                if ciphertext[i].isupper():
                    origCase.append(decryptedText[i].upper())
                else:
                    origCase.append(decryptedText[i].lower())
            decryptedText = ''.join(origCase)
            print('Possible encryption hack with key %s:' % (possibleKey))
            print(decryptedText[:200])
            print()
            print('Enter D for done, or just press Enter to continue:')
            response = input('> ')
            if response.strip().upper().startswith('D'):
                return decryptedText
    return None

def hackVigenere(ciphertext):
    allLikelyKeyLengths = kasiskiExamination(ciphertext)
    if not SILENT_MODE:
        keyLengthStr = ''
        for keyLength in allLikelyKeyLengths:
            keyLengthStr += '%s ' % (keyLength)
        print('Kasiski Examination results say the most likely key lengths are: ' + keyLengthStr + '\n')
    for keyLength in allLikelyKeyLengths:
        hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
        if hackedMessage != None:
            return hackedMessage
    return None

if __name__ == '__main__':
    main()
