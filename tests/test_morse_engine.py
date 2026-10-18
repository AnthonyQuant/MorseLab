import unittest
from morse_engine import morse_to_text, text_to_morse


class TestMorseEngine(unittest.TestCase):

  def test_text_to_morse_valid(self):
    self.assertEqual(text_to_morse("SOS"), "... --- ...")
    self.assertEqual(text_to_morse("HI"), ".... ..")

  def test_morse_to_text_valid(self):
    self.assertEqual(morse_to_text("... --- ..."), "SOS")
    self.assertEqual(morse_to_text(".... ."), "HE")

  def test_text_to_morse_invalid_raises_error(self):
    with self.assertRaises(ValueError):
      text_to_morse("HELLO#")  # Unsupported symbol

  def test_morse_to_text_invalid_raises_error(self):
    with self.assertRaises(ValueError):
      morse_to_text(".-.-.-.-.-.-")  # Invalid Morse sequence


if __name__ == "__main__":
  unittest.main()