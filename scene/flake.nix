{
  description = "Manim environment with system dependencies provided by Nix and Python packages managed by uv";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
	    manim
            # ffmpeg-full
            # texlive.combined.scheme-full
            # python3
            # ninja
            # SDL
            # SDL_gfx
            # opencv
            # cairo
            # pango
            # glib
            # gobject-introspection
            # librsvg
            # zlib
            # libGLU
            # gtk2
            # xorg.libXrender
            # xorg.libXext
            # ghostscript
            # harfbuzz
            # stdenv.cc.cc.lib
          ];

          # LD_LIBRARY_PATH = "${pkgs.lib.makeLibraryPath ([
          #   pkgs.ffmpeg-full
          #   pkgs.cairo
          #   pkgs.pango
          #   pkgs.glib
          #   pkgs.librsvg
          #   pkgs.stdenv.cc.cc.lib
          # ])}";

          shellHook = ''
            # Set up a local directory for uv to install packages
	    echo \"manim -pqh nn.py CombinedScene\" to use manim
          '';
        };
      }
    );
}

