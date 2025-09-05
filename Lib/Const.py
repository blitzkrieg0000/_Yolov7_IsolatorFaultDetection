LABELS = {0: "Eksik Halka", 1: "KIRIK", 2: "Ark izi"}
COLOR_MAP = {"Eksik Halka":"#ffffff", "KIRIK":"#0000ff", "Ark izi":"#ff0000"}
COLOR_MAP_RGB = {key : [ int(value[1:3], 16), int(value[3:5], 16), int(value[5:7], 16)] for key, value in COLOR_MAP.items()}