from dataclasses import dataclass
from typing import List
from dataTransferObjects.SectionData import SectionDTO , SegmentDTO, Point
from services.SectionCalculator import GrossSectionCalculator


# Assuming these classes are already defined:
# Point, SegmentDTO, SectionDTO, ResultsDTO, GrossSectionCalculator

def main():
    try:
        num_points = int(input("Enter number of points: "))
    except ValueError:
        print("Invalid input.")
        return

    if num_points < 2:
        print("Need at least 2 points.")
        return

    points: List[Point] = []
    for i in range(num_points):
        try:
            y = float(input(f"Point {i + 1} Y: "))
            z = float(input(f"Point {i + 1} Z: "))
            points.append(Point(y=y, z=z))
        except ValueError:
            print("Invalid coordinate.")
            return

    try:
        thickness = float(input("Enter segment thickness: "))
    except ValueError:
        print("Invalid thickness.")
        return

    section = SectionDTO()
    for i in range(num_points - 1):
        segment = SegmentDTO(points[i], points[i + 1], thickness)
        section.add_segment(segment)

    result_data = GrossSectionCalculator.calculate(section)

    print("\n--- Results ---")
    print(f"Surface Area: {result_data.surface_area:.3f}")
    print(f"Centroid (y, z): ({result_data.centroid.y:.3f}, {result_data.centroid.z:.3f})")
    print(f"Inertia Y: {result_data.inertia_y:.3f}")
    print(f"Inertia Z: {result_data.inertia_z:.3f}")

if __name__ == "__main__":
    main()
