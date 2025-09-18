from dataclasses import dataclass

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

#mypy checks the types