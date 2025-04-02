{
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
          ];

          shellHook = ''
            # Set up a local directory for uv to install packages
	    echo \"manim -pqh nn.py CombinedScene\" to use manim
          '';
        };
      }
    );
}

