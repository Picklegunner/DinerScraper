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
        return [self.quantity, self.unit]

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
        output += "Total Fat {}\n".format(self.total_fat.get()[0])
        output += "  Saturated Fat " + ''.join(self.sat_fat.get()) + "\n"
        output += "  Trans. Fat " + ''.join(self.trans_fat.get()) + "\n"
        output += "Total Carbs " + ''.join(self.total_carb.get()) + "\n"
        output += "  Fiber " + ''.join(self.fiber.get()) + "\n"
        output += "  Sugars " + ''.join(self.sugar.get()) + "\n"
        output += "Cholesterol " + ''.join(self.cholesterol.get()) + "\n"
        output += "Protein " + ''.join(self.protein.get()) + "\n"
        output += "Sodium " + ''.join(self.sodium.get()) + "\n"
        return output



