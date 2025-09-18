from dataclasses import dataclass
import math

@dataclass
class Point:
    y: float
    z: float

class SegmentDTO:
    def __init__(self, start_pt: Point, end_pt: Point, thickness: float):
        self.start_pt = start_pt
        self.end_pt = end_pt
        self.thickness = thickness

class SectionDTO:
    def __init__(self):
        # Automatically manages memory; no need for 'owning' flag like in TObjectList
        self.segments = []

    def add_segment(self, segment: SegmentDTO):
        self.segments.append(segment)

@dataclass
class ResultsDTO:
    surface_area: float
    centroid: Point
    inertia_y: float
    inertia_z: float

class GrossSectionCalculator:
    @staticmethod
    def calculate(section: SectionDTO) -> ResultsDTO:
        area_sum = 0.0
        static_y = 0.0
        static_z = 0.0
        inertia_yy = 0.0
        inertia_zz = 0.0

        for segment in section.segments:
            dy = segment.end_pt.y - segment.start_pt.y
            dz = segment.end_pt.z - segment.start_pt.z
            length = math.sqrt(dy**2 + dz**2)
            area = length * segment.thickness
            mid_y = (segment.start_pt.y + segment.end_pt.y) / 2
            mid_z = (segment.start_pt.z + segment.end_pt.z) / 2

            area_sum += area
            static_y += area * mid_y
            static_z += area * mid_z

            inertia_yy += (segment.start_pt.z**2 + segment.end_pt.z**2 + segment.start_pt.z * segment.end_pt.z) * area / 3
            inertia_zz += (segment.start_pt.y**2 + segment.end_pt.y**2 + segment.start_pt.y * segment.end_pt.y) * area / 3

            # Debug output
            print("debug")
            print(f"area: {area:.2f}")
            print(f"start y: {segment.start_pt.y}")
            print(f"start z: {segment.start_pt.z}")
            print(f"end y: {segment.end_pt.y}")
            print(f"end z: {segment.end_pt.z}")
            print(f"inertia_yy contribution: {(segment.start_pt.z**2 + segment.end_pt.z**2 + segment.start_pt.z * segment.end_pt.z) * area / 3}")
            print(f"inertia_zz contribution: {(segment.start_pt.y**2 + segment.end_pt.y**2 + segment.start_pt.y * segment.end_pt.y) * area / 3}")

        centroid_y = static_y / area_sum
        centroid_z = static_z / area_sum
        inertia_y = inertia_yy - area_sum * centroid_z**2
        inertia_z = inertia_zz - area_sum * centroid_y**2

        return ResultsDTO(
            surface_area=area_sum,
            centroid=Point(y=centroid_y, z=centroid_z),
            inertia_y=inertia_y,
            inertia_z=inertia_z
        )

#mypy checks the types