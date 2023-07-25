class WeightConversionPipeline:
    def process_item(self, item, spider):
        """ Convert different weight unit of measurements to pounds """

        # Conversion factors from various units to pounds
        conversion_factors = {
            'g': 0.00220462,
            'gram': 0.00220462,
            'grams': 0.00220462,

            'kg': 2.20462,
            'kilogram': 2.20462,
            'kilograms': 2.20462,

            'oz': 0.0625,
            'ounce': 0.0625,
            'ounces': 0.0625,

            'lb': 1,
            'pound': 1,
            'pounds': 1,

            'ton': 2000,
            'tons': 2000,
            
            'stone': 14,
            'stones': 14,
        }

        # Check if weight is not None
        if item.get('weight') is not None:
            # Split weight into number and unit
            try:
                weight, unit = item.get('weight').lower().split(' ', 1)
                weight = float(weight)
            except ValueError:
                print("Weight must be a number followed by a unit. Item: %s", item)
                return item

            # Check if weight is a positive number
            if weight < 0:
                print("Weight must be a positive number. Item: %s", item)
                return item

            # Check if unit is recognized
            if unit not in conversion_factors:
                print("Unit not recognized. Item: %s", item)
                return item

            # Convert weight to pounds
            item['weight'] = weight * conversion_factors[unit]

        return item
