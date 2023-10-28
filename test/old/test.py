STRING_RECYCLE = ["Recycling","Recycling symbol", "textile", "paper", "material", "document", "writing", "reading"]
STRING_GLASS_RECYCLE = ["Glass recycling", "bottle", "bottled water", "glass bottle", "glass", "glasses", "alcoholic beverage", "wine glass"]
STRING_NO_RECYCLE = ["WEEE", "mobile phone","electronics", "electronic device"]

ABC = 2
def f(st):
    if st in STRING_NO_RECYCLE:
        x = 5
        print "NO RECYCLE"
        return ABC


x = 5
print('Result', x, f('WEEE'))