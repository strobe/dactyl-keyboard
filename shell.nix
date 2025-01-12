{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    cmake
    conda
    expat
    libz
    coreutils
    binutils
    libgcc
    #pkgs.cq-editor
  ];

  shellHook = ''
    echo conda path ${pkgs.conda}
    echo expat path ${pkgs.expat}
    #export PATH=$PATH:${pkgs.conda}/bin
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${pkgs.expat}/lib
  '';
}
