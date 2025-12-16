# Simple 2D Solar System

This is a simple simulation written in Python that simulates the Earth's orbit around the Sun using matplotlib animation.

## How it works

Newton's law of gravitation:

$F = \frac{GMm}{r^2}$

Newton's second law:

$F = ma$

Rearranging for acceleration:

$a = \frac{GM}{r^2}$

Calculate the new velocity with timestep dt:

$dv = a \cdot dt$

Calculate the new displacement:

$ds = (v + dv) \cdot dt$

Calculate this for x and y axes.
