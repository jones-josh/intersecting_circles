import csv
from dataclasses import dataclass
import manim as manim
from typing import Generator, TextIO


@dataclass
class Circle:
    origin: tuple[float, float]
    radius: float


CircleGroup = list[Circle]

CIRCLES_PER_GROUP = 4


def removeCsvComments(csvFile: TextIO) -> Generator:
    for row in csvFile:
        raw = row.split("#")[0].strip()
        if raw:
            yield raw


def loadCircleGroups(csvPath: str) -> list[CircleGroup]:
    ungroupedCircles: list[Circle] = []
    with open(csvPath) as f:
        reader = csv.reader(removeCsvComments(f))
        for row in reader:
            assert len(row) == 3
            ungroupedCircles.append(
                Circle((float(row[0]), float(row[1])), float(row[2]))
            )

    assert len(ungroupedCircles) % CIRCLES_PER_GROUP == 0

    groups = []
    for i in range(0, len(ungroupedCircles), CIRCLES_PER_GROUP):
        group = []
        for j in range(CIRCLES_PER_GROUP):
            group.append(ungroupedCircles[i + j])
        groups.append(group)

    return groups


# forces all circles to exist in [0, 1] in x and y, translates and scales
# each group individually
def normalizeCircleGroups(groups: list[CircleGroup]) -> list[CircleGroup]:
    normalizedGroups: list[CircleGroup] = []
    for circleGroup in groups:
        minX: float = groups[0][0].origin[0]
        maxX: float = 0
        minY: float = groups[0][0].origin[1]
        maxY: float = 0
        for circle in circleGroup:
            [x, y] = circle.origin
            r = circle.radius
            if x - r < minX:
                minX = x - r
            if x + r > maxX:
                maxX = x + r
            if y - r < minY:
                minY = y - r
            if y + r > maxY:
                maxY = y + r

        scale: float = max(maxX - minX, maxY - minY)

        normalizedGroup: CircleGroup = []
        for circle in circleGroup:
            [x, y] = circle.origin
            r = circle.radius
            normalizedGroup.append(
                Circle(((x - minX) / scale, (y - minY) / scale), r / scale)
            )
        normalizedGroups.append(normalizedGroup)

    return normalizedGroups


if __name__ == "__main__":
    print(normalizeCircleGroups(loadCircleGroups("circles.csv")))


class DefaultTemplate(manim.Scene):
    def construct(self):
        normalizedCircles = normalizeCircleGroups(loadCircleGroups("circles.csv"))

        circles = []
        for c in normalizedCircles[0]:
            circles.append(manim.Circle(c.radius).move_to([*c.origin, 0]))

        self.play([manim.Create(c) for c in circles])