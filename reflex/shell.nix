{ pkgs ? import <nixpkgs> {} }:
pkgs.haskellPackages.shellFor {
    packages = _: [ (pkgs.haskellPackages.callCabal2nix "MyReflexProject" ./frontend {}) ];
    buildInputs = [
      pkgs.cabal-install
      pkgs.haskell-language-server
    ];
}