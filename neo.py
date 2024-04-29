# MIT License

# Copyright (c) 2024 Concept Bytes

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import time
import board
import neopixel_spi

# Initialize the NeoPixel strip
pixels = neopixel_spi.NeoPixel_SPI(board.SPI(), 24)


def blue_wipe(delay=0.01):
    """
    Performs a wipe across all pixels, turning them blue one by one with a delay between each.

    :param pixels: The NeoPixel object.
    :param delay: Delay between updates (in seconds).
    """
    global pixels
    for i in range(len(pixels)):
        pixels[i] = (0, 0, 255)  # Set pixel to blue (R, G, B)
        pixels.show()  # Update the strip with the new color
        time.sleep(delay)  # Wait for 'delay' seconds before continuing

def clamp(value, min_value, max_value):
    """Ensure the value stays within the min and max bounds."""
    return max(min_value, min(max_value, value))

def value_to_color(value):
    """
    Converts a value in the range 0-1023 to a color, with values at 300 or below being red,
    around 600 being yellow, and 900 or above being green.
    
    :param value: Input value ranging from 0 to 1023
    :return: A tuple representing the color (R, G, B)
    """
    if value <= 300:
        return (255, 0, 0)  # Red
    elif value >= 900:
        return (0, 255, 0)  # Green
    
    # Adjust the input range from 300-900 to 0-600 for easier calculation
    adjusted_value = value - 300
    if adjusted_value <= 300:  # Range 300-600 (0-300 after adjustment)
        # Transition from red to yellow (increase green)
        red = 255
        green = clamp(int((adjusted_value / 300) * 255), 0, 255)  # Scale green up to 255
        blue = 0
    else:  # Range 600-900 (300-600 after adjustment)
        # Transition from yellow to green (decrease red)
        red = clamp(255 - int(((adjusted_value - 300) / 300) * 255), 0, 255)  # Scale red down to 0
        green = 255
        blue = 0
    
    return (red, green, blue)

def fill_color_based_on_value(value):
    """
    Fills all pixels with a color based on the input value, transitioning from red through yellow to green.
    
    :param value: Input value ranging from 0 to 1023
    """
    color = value_to_color(value)
    pixels.fill(color)


