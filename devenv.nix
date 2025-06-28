{ pkgs, ... }:

{
  packages = with pkgs; [
    manim
  ];

  enterShell = ''
    # Set up a local directory for uv to install packages
    echo "manim -pqh nn.py CombinedScene" to use manim
  '';
}

