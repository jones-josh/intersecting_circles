from __future__ import annotations

import csv
from dataclasses import dataclass
import manim as manim
from typing import Generator, TextIO


@dataclass
class Circle:
    origin: tuple[float, float]
    radius: float

    def toManim(self: Circle, color: ParsableManimColor = manim.WHITE) -> manim.Circle:
        print(self)
        return manim.Circle(self.radius, color=color).move_to([*self.origin, 0])


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


# forces all circles to exist in [-0.5, 0.5] in x and y, translates and scales
# each group individually
def normalizeCircleGroups(
    groups: list[CircleGroup], scale: float = 1
) -> list[CircleGroup]:
    normalizedGroups: list[CircleGroup] = []
    for circleGroup in groups:
        minX: float = min([c.origin[0] - c.radius for c in circleGroup])
        maxX: float = max([c.origin[0] + c.radius for c in circleGroup])
        minY: float = min([c.origin[1] - c.radius for c in circleGroup])
        maxY: float = max([c.origin[1] + c.radius for c in circleGroup])

        groupWidth: float = maxX - minX
        groupHeight: float = maxY - minY
        groupBoxSize: float = max(groupWidth, groupHeight)

        normalizedGroup: CircleGroup = []
        for circle in circleGroup:
            [x, y] = circle.origin
            origin_x = (x - minX) / groupBoxSize
            origin_x += (1 - groupWidth / groupBoxSize) / 2  # center horizontally
            origin_x -= 0.5  # center around (0, 0)
            origin_x *= scale
            origin_y = (y - minY) / groupBoxSize
            origin_y += (1 - groupHeight / groupBoxSize) / 2  # center vertically
            origin_y -= 0.5  # center around (0, 0)
            origin_y *= scale

            r = circle.radius
            r *= scale

            normalizedGroup.append(Circle((origin_x, origin_y), r / groupBoxSize))
        normalizedGroups.append(normalizedGroup)

    return normalizedGroups


class DefaultTemplate(manim.Scene):
    def construct(self):
        scale: float = 10
        normalizedCircles = normalizeCircleGroups(
            loadCircleGroups("circles.csv"), scale=scale
        )

        # start with the last entry to loop seamlessly
        renderedCircles = [c.toManim() for c in normalizedCircles[-1]]

        drawCircleGroups = []
        for group in normalizedCircles:
            drawCircles = []
            for c in group:
                drawCircles.append(c.toManim())
            drawCircleGroups.append(drawCircles)

        for nextGroup in drawCircleGroups:
            animations = []
            for currentCircle, nextCircle in zip(renderedCircles, nextGroup):
                animations.append(manim.Transform(currentCircle, nextCircle))
            self.play(*animations)
            self.play(manim.Wait(0.2))
