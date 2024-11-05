
# Step-by-Step Guide to Encrypt and Decrypt Using Monoalphabetic Cipher

This guide walks through the process of converting a plaintext file into an encrypted file using a monoalphabetic substitution cipher.

## Step 1: Convert All Text to Lowercase
The goal here is to ensure that the text is in lowercase so that encryption is consistent.

Run this command in the terminal:

```bash
tr '[:upper:]' '[:lower:]' < plain.txt > lcase.txt
```

**Explanation**: This command reads from `plain.txt`, converts all uppercase letters to lowercase, and writes the output to a new file called `lcase.txt`.

**Result**: Now `lcase.txt` contains all lowercase letters, spaces, and any punctuation or numbers.

## Step 2: Remove Punctuation and Numbers
In this step, we remove any characters that aren’t letters or spaces, leaving only lowercase letters and spaces. This helps create a cleaner input for encryption.

Run the following command:

```bash
tr -cd 'a-z\n[:space:]' < lcase.txt > nodelim.txt
```

**Explanation**: This command reads from `lcase.txt` and removes everything except lowercase letters (`a-z`), newlines (`\n`), and spaces (`[:space:]`). The output is saved in `nodelim.txt`.

**Result**: Now `nodelim.txt` contains only lowercase letters and spaces.

## Step 3: Generate the Substitution Key
The substitution key is a random arrangement of the alphabet that we’ll use to encrypt each letter in the plaintext.

Open Python in your terminal by typing:

```bash
python3
```

Run the following Python code to generate a random substitution key:

```python
import random
skey = 'abcdefghijklmnopqrstuvwxyz'
key = ''.join(random.sample(skey, len(skey)))
print("Generated key:", key)
```

**Explanation**: This code takes the alphabet (`skey`) and shuffles it randomly. The result is stored in `key` and printed out.

**Example Output**:

```
Generated key: ibejrzpwqtolmsnycxkfhuvdqa
```

Here, `a` will be encrypted as `i`, `b` as `b`, `c` as `e`, and so on.

## Step 4: Encrypt the Plaintext Using the Substitution Key
Now, we use the `tr` command to encrypt the text by substituting each letter in `nodelim.txt` with its corresponding letter from the generated key.

Run the following command:

```bash
tr 'abcdefghijklmnopqrstuvwxyz' 'ibejrzpwqtolmsnycxkfhuvdqa' < nodelim.txt > cipher.txt
```

**Explanation**: This command reads from `nodelim.txt`, substitutes each letter based on the key, and writes the encrypted text to `cipher.txt`.

**Result**: Now `cipher.txt` contains the encrypted version of the original text.

## Step 5: Decrypt the Ciphertext Using the Reverse Key
To decrypt, we need to reverse the substitution by mapping each letter in the key back to the original alphabet.

Run the following command to decrypt:

```bash
tr 'ibejrzpwqtolmsnycxkfhuvdqa' 'abcdefghijklmnopqrstuvwxyz' < cipher.txt > p.txt
```

**Explanation**: This command reads from `cipher.txt` and replaces each letter in the key (`ibejrzpwqtolmsnycxkfhuvdqa`) with its corresponding original letter (`abcdefghijklmnopqrstuvwxyz`). The decrypted text is saved in `p.txt`.

**Result**: Now `p.txt` contains the original text (minus the punctuation and numbers that were removed in Step 2).
