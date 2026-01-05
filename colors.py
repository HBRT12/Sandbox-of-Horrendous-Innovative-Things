import matplotlib.colors as mcolors

# Get all named colors
named_colors = mcolors.CSS4_COLORS

# Display all colors
for color_name, hex_value in named_colors.items():
    print(f"{color_name}: {hex_value}")
