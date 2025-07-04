{ pkgs, ... }:

{
  packages = with pkgs; [
    manim
    zig
  ];

  enterShell = ''
    echo "manim -pqh nn.py CombinedScene" to use manim
  '';
}

