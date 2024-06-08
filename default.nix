{ pkgs ? import <nixpkgs> {} }:

(pkgs.buildFHSEnv {
  name = "arithmetic-server-nix-env";
  targetPkgs = pkgs: (with pkgs; [
    poetry
  ]);
}).env
