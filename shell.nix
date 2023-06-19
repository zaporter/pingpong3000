{pkgs ? import <nixpkgs> {}}: let
  opencvGtk = pkgs.opencv.override (old: {enableGtk2 = true;});
in
  pkgs.mkShell {
    NIX_SHELL_NAME = "pingpong3000";
    buildInputs = with pkgs; [
      opencvGtk
      python310Packages.opencv4
      stdenv.cc.cc.lib
    ];
    shellHook = ''
      export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
    '';
  }
