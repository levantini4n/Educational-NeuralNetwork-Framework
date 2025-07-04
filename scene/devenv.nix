{ pkgs, ... }:

{
  packages = with pkgs; [
    manim
  ];

  enterShell = ''
    echo "manim -pqh nn.py CombinedScene" to use manim
  '';
}

