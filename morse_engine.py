import random  # Added to enable random character selection for the quiz
import history  # Imports our new local persistence module

# Standard International Morse Code Dictionary
MORSE_CODE_DICT = {
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    '0': '-----',
    ' ': '/',
}

# Automatically create a reverse dictionary for decoding (Morse -> Text)
# This uses dictionary comprehension from your syllabus!
REVERSE_MORSE_DICT = {value: key for key, value in MORSE_CODE_DICT.items()}


def text_to_morse(text):
  """Converts text to Morse code.

  Raises ValueError if an unsupported character is encountered.
  """
  morse_result = []
  for char in text.upper():
    if char == " ":
      morse_result.append("/")  # Standard word separator
    elif char in MORSE_CODE_DICT:
      morse_result.append(MORSE_CODE_DICT[char])
    else:
      raise ValueError(f"Unsupported character in text: '{char}'")
  return " ".join(morse_result)


def morse_to_text(morse_code):
  """Converts Morse code to text.

  Normalizes spacing and raises ValueError if an invalid Morse sequence is
  encountered.
  """
  # Normalize spacing: collapse multiple spaces into a single space
  cleaned_morse = " ".join(morse_code.strip().split())
  if not cleaned_morse:
    return ""

  # Ensure reverse dictionary exists (e.g., MORSE_TO_TEXT_DICT or inverse of MORSE_CODE_DICT)
  reverse_dict = {v: k for k, v in MORSE_CODE_DICT.items()}

  # Split by word separator '/' (surrounded by spaces) or standard spacing
  words = cleaned_morse.split(" / ")
  decoded_words = []

  for word in words:
    letters = word.split(" ")
    decoded_letters = []
    for letter in letters:
      if not letter:
        continue
      if letter in reverse_dict:
        decoded_letters.append(reverse_dict[letter])
      else:
        raise ValueError(f"Invalid Morse sequence: '{letter}'")
    decoded_words.append("".join(decoded_letters))

  return " ".join(decoded_words)

def practice_mode():
  """Stage 3: Interactive Practice Quiz with live scoring, early exit capability,

  and automatic history logging.
  """
  print('\n*** Welcome to MorseLab Practice Mode ***')
  print("Tip: Type 'q' or 'quit' at any prompt to exit the quiz early.")
  print('Select Difficulty:')
  print('1. Letters Only')
  print('2. Numbers Only')
  print('3. Mixed (Letters & Numbers)')

  diff_choice = input('Choose difficulty (1, 2, or 3): ').strip()

  # Set pool and difficulty string name
  if diff_choice == '1':
    pool = {k: v for k, v in MORSE_CODE_DICT.items() if k.isalpha()}
    diff_name = 'Letters'
  elif diff_choice == '2':
    pool = {k: v for k, v in MORSE_CODE_DICT.items() if k.isdigit()}
    diff_name = 'Numbers'
  elif diff_choice == '3':
    pool = {k: v for k, v in MORSE_CODE_DICT.items() if k != ' '}
    diff_name = 'Mixed'
  else:
    print('Invalid difficulty selection. Defaulting to Letters.')
    pool = {k: v for k, v in MORSE_CODE_DICT.items() if k.isalpha()}
    diff_name = 'Letters'

  score = 0
  rounds = 5
  questions_answered = 0

  print(f'\nStarting quiz! You will be tested on up to {rounds} characters.')

  for i in range(1, rounds + 1):
    char, correct_morse = random.choice(list(pool.items()))

    # Live score tracker displayed continuously before each question
    print('\n----------------------------------------')
    print(
        f' Question {i}/{rounds}  |  Current Score: {score}/{questions_answered}'
    )
    print('----------------------------------------')

    user_answer = (
        input(f"What is the Morse code for '{char}'? : ").strip().lower()
    )

    # Check if the user wants to quit early
    if user_answer in ['q', 'quit']:
      print('\n🚪 Exiting quiz early...')
      break

    questions_answered += 1

    # Evaluate the user's answer
    if user_answer == correct_morse:
      print('✅ Correct! +1 point.')
      score += 1
    else:
      print(
          f"❌ Incorrect. The correct Morse code for '{char}' is"
          f" '{correct_morse}'."
      )

  # Save performance to history if at least one question was answered
  if questions_answered > 0:
    history.save_quiz_record(score, questions_answered, diff_name)
    percentage = (score / questions_answered) * 100
    print(
        f'\n🎉 Quiz Complete! Final Score: {score}/{questions_answered} ('
        f'{percentage:.0f}%)'
    )
    print('📁 Your quiz results have been saved to your translation history!')
  else:
    print('\nQuiz ended without any questions answered.')

# Simple Command-Line Menu (Stage 1 Core Loop)
def main():
  print('*** Welcome to MorseLab: Core Engine ***')

  while True:
    print('\nSelect an Option:')
    print('1. Encode Text to Morse Code\n')
    print('2. Decode Morse Code to Text\n')
    print('3. Practice Mode (Quiz)\n')
    print('4. View Translation History\n')
    print('5. Clear Translation History\n')
    print('6. Launch Desktop GUI\n')  # Added GUI launcher option
    print('7. Exit\n')

    choice = input('Enter your choice (1, 2, 3, 4, 5, 6 or 7): \n')

    if choice == '1':
        user_text = input('Enter the text you want to encode: ')
        try:
            result = text_to_morse(user_text)
            print(f'\n[Encoded Result]:\n{result}')
            history.save_translation(user_text, result, 'Text to Morse')
        except ValueError as e:
            print(f'❌ Validation Error: {e}')

    elif choice == '2':
        user_morse = input(
            'Enter Morse code (separate letters with spaces, words with /): '
        )
        try:
            result = morse_to_text(user_morse)
            print(f'\n[Decoded Result]:\n{result}')
            history.save_translation(user_morse, result, 'Morse to Text')
        except ValueError as e:
            print(f'❌ Validation Error: {e}')


    elif choice == '3':

        practice_mode()



    elif choice == '4':

        history.view_history()


    elif choice == '5':

        history.clear_history()

    elif choice == '6':
        print('🚀 Launching MorseLab Desktop GUI...')
        import GUI
        GUI.run_gui()  # Calls the GUI function from GUI.py

    elif choice == '7':

        print('Exiting MorseLab. See you next time!')

        break

    else:
      print('Invalid selection. Please choose 1, 2, 3, 4, 5, 6 or 7.')


if __name__ == '__main__':
  main()