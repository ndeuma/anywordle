
RESET_COLORS_256 = '\x1b[0m'

def color_text_256(foreground, background, text):
    result = ''
    if foreground is not None:
        result += foreground_256(foreground)
    if background is not None:
        result += background_256(background)
    result += text
    result += RESET_COLORS_256
    return result

def foreground_256(foreground):
    return '\x1b[38:5:' + str(foreground) + 'm'

def background_256(background):
    return '\x1b[48:5:' + str(background) + 'm'