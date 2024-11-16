import re
from typing import Dict, List, Union

import math


class PolynomialModel:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.discontinuities = []
        self.properties: Dict[str, List[List[float]]] = {}
        self.load_file()

    def load_file(self):
        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        property_section = None  # Track which property section we are in

        for line in lines:
            line = line.strip()

            # Skip comments or empty lines
            if line.startswith('#') or not line:
                continue

            # Parse discontinuities
            if "DISCONTINUITIES" in line:
                self.discontinuities = list(map(float, line.split()[1:]))
                continue

            # Detect the start of a property section (e.g., RHO, VP, VS, etc.)
            if line.isupper() and line not in {"DISCONTINUITIES", "MOHO_IDX", "MOHO_COMP_IDX", "MAX_POLY_DEG", "SCALE",
                                               "UNITS"}:
                property_section = line
                self.properties[property_section] = []
                continue

            # Parse property polynomial coefficients
            if property_section and re.match(r"^(\s*[-\d.]+)+$", line):
                coefficients = list(map(float, line.split()))
                self.properties[property_section].append(coefficients)

    @staticmethod
    def _evaluate_polynomial(r_rel: float, coefficients: List[float]) -> float:
        """
        Evaluate a polynomial given relative radius `r_rel` and coefficients.

        Args:
            r_rel (float): Relative radius (normalized by planet radius).
            coefficients (List[float]): Polynomial coefficients.

        Returns:
            float: Evaluated polynomial value.
        """
        return sum(coeff * (r_rel ** power) for power, coeff in enumerate(coefficients))

    def get_properties(self, r: float, key: str, threshold: float = 1e-6) -> Union[float, List[float]]:
        """
        Compute the property value for a given radius `r` and property `key`.

        Args:
            r (float): Radius value.
            key (str): Property key (e.g., "RHO", "VP").
            threshold (float): Threshold for determining if `r` is exactly on a discontinuity.

            Returns:
                Union[float, List[float]]: Computed property value(s) based on the region and key, or NaN if out of bounds.
        """
        if key not in self.properties:
            raise ValueError(f"Property '{key}' not found in the model.")

        # Normalize the radius relative to the planet radius
        r_rel = r / self.discontinuities[0]
        discontinuities = self.discontinuities

        # Check out of range
        if r > discontinuities[0] + threshold or r < discontinuities[-1] - threshold:
            return math.nan

        # Check if `r` is located close to a discontinuity
        for i, d in enumerate(discontinuities):
            if abs(r - d) <= threshold:
                if i == 0:
                    # At the outermost layer
                    return self._evaluate_polynomial(r_rel, self.properties[key][i])
                elif i == len(discontinuities) - 1:
                    # At the innermost layer
                    return self._evaluate_polynomial(r_rel, self.properties[key][i - 1])
                else:
                    # Exactly on a discontinuity, return two values
                    value_above = self._evaluate_polynomial(r_rel, self.properties[key][i - 1])
                    value_below = self._evaluate_polynomial(r_rel, self.properties[key][i])
                    # Check if the two values are mostly the same
                    if abs(value_below - value_above) <= threshold:
                        return value_below
                    return [value_below, value_above]

        # Locate the region in between discontinuities
        for i in range(len(discontinuities) - 1):
            if discontinuities[i + 1] < r < discontinuities[i]:
                return self._evaluate_polynomial(r_rel, self.properties[key][i])

        # If no condition matches, return NaN
        return math.nan

    def __repr__(self):
        return (f"Discontinuities: {self.discontinuities}\n"
                f"Properties: {', '.join(self.properties.keys())}")


if __name__ == "__main__":
    # Instantiate the model and load data
    model = PolynomialModel("./background_models/prem_iso.bm")

    # Print the loaded data
    print(model.get_properties(6291.0, "RHO"))
