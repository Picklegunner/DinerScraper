VALID_UNITS = ("mg, g, N/A")

class Nutrient:

    def __init__(self, quantity=0, unit="N/A"):
        self.set(quantity, unit)

    def __str__(self):
        return "{}{}".format(quantity, unit)

    def set(self, quantity, unit):
        self.quantity = quantity
        if(not unit in VALID_UNITS):
            message = "Invalid unit provided! {} is not one of these acceptable units: ".format(unit)
            message += "".join(VALID_UNITS)
            raise ValueError(message)
        else:
            self.unit = unit
        return self

    def get(self):
        return (self.quantity, self.unit)

class Entry:

    name = ""

    calories = None
    calories_from_fat = None

    total_fat = None
    sat_fat = None
    trans_fat = None

    total_carb = None
    fiber = None
    sugar = None

    cholesterol = None
    protein = None
    sodium = None

    def __str__(self):
        output = self.name + " - entry\n"
        output += "Calories {}\n".format(self.calories)
        output += "Calories from Fat {}\n".format(self.calories_from_fat)
        output += "Total Fat {}\n".format(self.total_fat)
        output += "  Saturated Fat {}\n".format(self.sat_fat)
        output += "  Trans. Fat {}\n".format(self.trans_fat)
        output += "Total Carbs {}\n".format(self.total_carb)
        output += "  Fiber {}\n".format(self.fiber)
        output += "  Sugars {}\n".format(self.sugar)
        output += "Cholesterol {}\n".format(self.cholesterol)
        output += "Protein {}\n".format(self.protein)
        output += "Sodium {}".format(self.sodium)
        return output



