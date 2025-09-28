{
  pkgs,
  lib,
  stdenv,
  ...
}:
let
  pythonPackages = pkgs.python313Packages;
in
pkgs.mkShell {
  buildInputs = [
    pythonPackages.python
    pythonPackages.venvShellHook
    pkgs.autoPatchelfHook
    pythonPackages.onnxruntime
    pkgs.onnxruntime
    pythonPackages.watchdog
    pythonPackages.python-dotenv
    pythonPackages.openai
    pythonPackages.gitpython

  ];
  venvDir = "./.venv";
  postVenvCreation = ''
    unset SOURCE_DATE_EPOCH
    pip install -U jupyter
    autoPatchelf ./.venv
  '';
  postShellHook = ''
    unset SOURCE_DATE_EPOCH
    export LD_LIBRARY_PATH=${
      lib.makeLibraryPath [
        stdenv.cc.cc
      ]
    }:$LD_LIBRARY_PATH
  '';
}
