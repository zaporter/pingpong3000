{pkgs ? import <nixpkgs> {}}: 
  pkgs.mkShell {
    NIX_SHELL_NAME = "pingpong3000";
    buildInputs = with pkgs; [
      opencv
      python310Packages.opencv4
      stdenv.cc.cc.lib
    ];
    shellHook = ''
      export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
    '';
  }
