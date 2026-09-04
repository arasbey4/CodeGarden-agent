import shutil

def get_terminal_size():
    return shutil.get_terminal_size()

def get_logo():
    # This version is designed for a wide terminal, providing a single-line,
    # massive, and perfectly aligned "CODE GARDEN" logo.
    # It uses a refined block-shadow style with a decorative frame to look like a professional CLI.
    logo = r"""
  ╔══════════════════════════════════════════════════════════════════════════════════════════════╗
  ║                                                                                              ║
  ║  ██████╗ ██████╗ ██████╗ ███████╗    ██████╗  █████╗ ██████╗ ██████╗ ███████╗███╗   ██╗      ║
  ║ ██╔════╝██╔═══██╗██╔══██╗██╔════╝   ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██╔════╝████╗  ██║      ║
  ║ ██║     ██║   ██║██║  ██║█████╗     ██║  ███╗███████║██████╔╝██║  ██║█████╗  ██╔██╗ ██║      ║
  ║ ██║     ██║   ██║██║  ██║██╔══╝     ██║   ██║██╔══██║██╔══██╗██║  ██║██╔══╝  ██║╚██╗██║      ║
  ║ ╚██████╗╚██████╔╝██████╔╝███████╗   ╚██████╔╝██║  ██║██║  ██║██████╔╝███████╗██║ ╚████║      ║
  ║  ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝    ╚═════╝ ╚═╝  ╚═╝██║  ██║╚═════╝ ╚══════╝╚═╝  ╚═══╝      ║
  ║                                                                                              ║
  ║                            🌿  L O C A L   A I   G A R D E N  🌿                             ║
  ║                          ~ Organic Intelligence, Local Power ~                               ║
  ╚══════════════════════════════════════════════════════════════════════════════════════════════╝
    """
    return logo

def clear_screen():
    # Works for both Windows and Unix
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
