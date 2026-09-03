# Somato

Somato is a lightweight procedural body generation library for games and simulations.

It provides simple geometry-based building blocks for generating and rendering body features. Somato is designed to be driven by external systems, such as procedural generation, simulation logic, or genetics libraries.

Version `0.1.0` currently focuses on procedural eyes.

## Example Outputs
<img width="400" height="300" alt="child_eye" src="https://github.com/user-attachments/assets/865650e4-53c0-4693-9e7d-b3db8bd24835" />

<img width="400" height="300" alt="parent_1_eye" src="https://github.com/user-attachments/assets/0baf02df-9089-4d8a-8bb9-2804a3af74ff" />

<img width="400" height="300" alt="parent_2_eye" src="https://github.com/user-attachments/assets/25a0c958-fa97-4a5a-83b3-d7f2bfd7ea85" />


## Features

- Cubic Bézier eye shapes
- Configurable eye geometry
- Iris rendering
- Iris clipping to the eye shape
- Eye scaling
- Independent horizontal and vertical scaling
- Eye rotation
- Custom sclera and outline colors
- Simple render pipeline
- Pillow-based image output

## Installation

Somato depends on Pillow.

Install dependencies with:

```bash
pip install -r requirements.txt
```

A minimal `requirements.txt` is:

```text
Pillow
```

## Basic Usage

```python
from somato import Somato, Eye, Iris
```

Create an iris:

```python
iris = Iris(
	center=(200, 150),
	radius_x=35,
	color=(70, 130, 180)
)
```

Create an eye:

```python
eye = Eye(
	p0=(50, 150),
	upper_p1=(120, 70),
	upper_p2=(280, 70),
	p3=(350, 150),
	lower_p1=(120, 230),
	lower_p2=(280, 230),
	thickness=5,
	iris=iris
)
```

Create a Somato canvas:

```python
body = Somato(
	width=400,
	height=300
)
```

Add the eye:

```python
body.add(
	eye
)
```

Save the result:

```python
body.save(
	"eye.png"
)
```

## Complete Example

```python
from somato import Somato, Eye, Iris


iris = Iris(
	center=(200, 150),
	radius_x=35,
	radius_y=35,
	color=(80, 130, 75)
)


eye = Eye(
	p0=(50, 150),
	upper_p1=(120, 70),
	upper_p2=(280, 70),
	p3=(350, 150),
	lower_p1=(120, 230),
	lower_p2=(280, 230),
	thickness=5,
	iris=iris,
	sclera_color="white",
	outline_color="black"
)


somato = Somato(
	width=400,
	height=300,
	background_color="white"
)


somato.add(
	eye
)


somato.save(
	"eye.png"
)
```

## Eye Geometry

An eye is created from two cubic Bézier curves.

The upper eyelid uses:

```text
p0
upper_p1
upper_p2
p3
```

The lower eyelid uses:

```text
p0
lower_p1
lower_p2
p3
```

Both curves share the same starting and ending points.

The resulting curves are combined into a closed polygon that is filled with the sclera color.

### Endpoints

`p0` is the left endpoint of the eye.

`p3` is the right endpoint of the eye.

For example:

```python
p0=(50, 150)
p3=(350, 150)
```

### Control Points

The control points determine the curvature of the eye.

```python
upper_p1=(120, 70)
upper_p2=(280, 70)

lower_p1=(120, 230)
lower_p2=(280, 230)
```

Moving these points changes the shape of the upper and lower eyelids.

Because the geometry is directly controllable, eye shapes can be created manually or generated procedurally.

## Cubic Bézier Curves

Somato uses cubic Bézier curves internally.

The curve is calculated from four points:

```text
P0
P1
P2
P3
```

where:

```text
P0 and P3 = endpoints
P1 and P2 = control points
```

Somato samples points along the curve and uses those points to construct the eye shape.

You normally do not need to call the Bézier function directly when creating an eye.

## Iris

An iris is represented by an ellipse.

```python
iris = Iris(
	center=(200, 150),
	radius_x=35,
	radius_y=35,
	color="brown"
)
```

### center

The center of the iris:

```python
center=(200, 150)
```

### radius_x

The horizontal radius:

```python
radius_x=35
```

### radius_y

The vertical radius:

```python
radius_y=35
```

If `radius_y` is omitted, it defaults to the same value as `radius_x`.

For example:

```python
Iris(
	center=(200, 150),
	radius_x=35
)
```

creates a circular iris.

Different horizontal and vertical radii can create an elliptical iris.

```python
Iris(
	center=(200, 150),
	radius_x=40,
	radius_y=30
)
```

### color

The iris color can use any color format supported by Pillow.

For example:

```python
color="brown"
```

or:

```python
color=(70, 130, 180)
```

The iris is automatically clipped so that it does not render outside the eye shape.

## Eye Appearance

The sclera color can be changed with:

```python
sclera_color="white"
```

The outline color can be changed with:

```python
outline_color="black"
```

The outline thickness is controlled by:

```python
thickness=5
```

Example:

```python
eye = Eye(
	p0=(50, 150),
	upper_p1=(120, 70),
	upper_p2=(280, 70),
	p3=(350, 150),
	lower_p1=(120, 230),
	lower_p2=(280, 230),
	thickness=8,
	sclera_color=(240, 240, 220),
	outline_color=(40, 40, 40)
)
```

## Transformations

Eyes can also be transformed without manually editing every Bézier point.

Somato currently supports:

```text
scale
scale_x
scale_y
rotation
```

### Scale

Uniformly scale the eye:

```python
scale=1.25
```

Values above `1` enlarge the eye.

Values below `1` shrink it.

### Horizontal Scale

Change only the horizontal size:

```python
scale_x=1.5
```

### Vertical Scale

Change only the vertical size:

```python
scale_y=0.75
```

### Rotation

Rotate the eye in degrees:

```python
rotation=15
```

Example:

```python
eye = Eye(
	p0=(50, 150),
	upper_p1=(120, 70),
	upper_p2=(280, 70),
	p3=(350, 150),
	lower_p1=(120, 230),
	lower_p2=(280, 230),
	thickness=5,
	scale=1.1,
	scale_x=1.2,
	scale_y=0.9,
	rotation=10
)
```

Transformations are applied around the center point between `p0` and `p3`.

## Rendering Multiple Body Parts

Somato stores renderable body parts in a list.

```python
somato.add(
	body_part
)
```

When `render()` is called, every body part is drawn in the order it was added.

```python
somato.render()
```

Calling:

```python
somato.save(
	"output.png"
)
```

automatically renders the body parts before saving the image.

## Procedural Generation

Somato is designed so that geometry can come from another system.

For example:

```python
eye_data = {
	"p0": (50, 150),
	"upper_p1": (120, 85),
	"upper_p2": (280, 75),
	"p3": (350, 140),
	"lower_p1": (120, 205),
	"lower_p2": (280, 190)
}
```

That data can be passed directly into an eye:

```python
eye = Eye(
	p0=eye_data["p0"],
	upper_p1=eye_data["upper_p1"],
	upper_p2=eye_data["upper_p2"],
	p3=eye_data["p3"],
	lower_p1=eye_data["lower_p1"],
	lower_p2=eye_data["lower_p2"],
	thickness=5
)
```

This makes Somato suitable for systems where appearance data is generated rather than manually authored.

## Using Somato With Genetics

Somato does not contain genetics logic.

A genetics system can generate phenotype values such as:

```python
phenotype = {
	"p0": (50, 150),
	"upper_p1": (120, 90),
	"upper_p2": (280, 80),
	"p3": (350, 145),
	"lower_p1": (120, 210),
	"lower_p2": (280, 200),
	"iris_color": (80, 130, 75)
}
```

Somato can then render those values:

```python
iris = Iris(
	center=(200, 150),
	radius_x=35,
	color=phenotype["iris_color"]
)


eye = Eye(
	p0=phenotype["p0"],
	upper_p1=phenotype["upper_p1"],
	upper_p2=phenotype["upper_p2"],
	p3=phenotype["p3"],
	lower_p1=phenotype["lower_p1"],
	lower_p2=phenotype["lower_p2"],
	thickness=5,
	iris=iris
)
```

This keeps appearance rendering separate from the system responsible for generating the traits.

## Coordinate System

Somato uses Pillow's image coordinate system.

The origin is at the top-left corner:

```text
(0, 0)
```

Increasing `x` moves to the right.

Increasing `y` moves downward.

For example:

```text
(100, 50)
```

is farther right and higher on the image than:

```text
(100, 200)
```

## Somato Canvas

The `Somato` class creates the image used for rendering.

```python
somato = Somato(
	width=800,
	height=400,
	background_color="white"
)
```

### width

Image width in pixels.

### height

Image height in pixels.

### background_color

Background color used when creating the image.

Somato creates an RGBA image internally.

## API Overview

### Somato

```python
Somato(
	width=800,
	height=400,
	background_color="white"
)
```

Methods:

```python
add(body_part)
render()
save(file_name)
```

### Eye

```python
Eye(
	p0,
	upper_p1,
	upper_p2,
	p3,
	lower_p1,
	lower_p2,
	thickness,
	iris=None,
	sclera_color="white",
	outline_color="black",
	scale=1,
	scale_x=1,
	scale_y=1,
	rotation=0
)
```

Methods:

```python
transform_point(point)
get_shape()
draw(image)
```

### Iris

```python
Iris(
	center,
	radius_x,
	radius_y=None,
	color="brown"
)
```

Methods:

```python
bounds()
```

## Design Philosophy

Somato handles geometry and rendering.

It is not intended to determine why a body feature has a particular shape.

For example, Somato does not need to know whether an eye shape came from:

- Genetics
- Species definitions
- Character customization
- Random generation
- Aging
- Injury
- Simulation rules

It simply receives geometry and renders it.

This separation allows Somato to work alongside other procedural systems without depending on them.

## Current Limitations

Version `0.1.0` is an early proof of concept.

Currently:

- Eyes are the only implemented body feature
- Pupils are not yet implemented
- The library does not contain anatomical or biological logic
- Procedural data must currently be supplied by the application using Somato

Additional body features may be added in future versions.

## Version

Current version:

```text
0.1.0
```

The API may change as Somato expands beyond the initial eye system.
