{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    pkgs = nixpkgs.legacyPackages.x86_64-linux;
  in {
    packages.x86_64-linux.discordBot = pkgs.callPackage ./default.nix {
      python313Packages = pkgs.python313Packages;
    };
    devShells.x86_64-linux.default = pkgs.callPackage ./shell.nix {
      inherit pkgs;
    };
  };
}
