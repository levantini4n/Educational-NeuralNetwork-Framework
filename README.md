# INSPIRATION
- https://github.com/tsoding/nn.h

It should be noted however that the framework is currently using the central difference theorem rather than actual back propagation.

# Run 
`example.zig` will serve as the main file, and the neural network will model the XOR gate.
```bash
zig run example.zig
```

# Helper Material

Clueless about how neural networks work? Use the Manim animation engine to get an `mp4` out of the Python code in *scene/nn.py* illustrating the neural network implemented in *example.zig*.

If you are using nix and flakes, just:
1. `devenv shell`
2. `cd scene`
3. Follow instructions that get printed out to the terminal
