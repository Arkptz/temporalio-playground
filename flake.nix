{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/4aa36568d413aca0ea84a1684d2d46f55dbabad7";

    flake-parts.url = "github:hercules-ci/flake-parts";

    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix-hammer-overrides = {
      url = "github:TyberiusPrime/uv2nix_hammer_overrides";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = inputs @ {
    nixpkgs,
    flake-parts,
    uv2nix,
    pyproject-nix,
    pyproject-build-systems,
    uv2nix-hammer-overrides,
    ...
  }:
    flake-parts.lib.mkFlake {inherit inputs;} {
      systems = [
        "x86_64-linux"
        "aarch64-darwin"
        "x86_64-darwin"
      ];

      perSystem = {
        config,
        self',
        inputs',
        pkgs,
        system,
        lib,
        ...
      }: {
        devShells.default = let
          pkgs = import nixpkgs {
            inherit system;
          };
          workspace = uv2nix.lib.workspace.loadWorkspace {workspaceRoot = ./.;};
          overlay = workspace.mkPyprojectOverlay {
            sourcePreference = "wheel";
          };
          python = pkgs.python311;
          pythonPackages = python.pkgs;
          pyprojectOverrides = pkgs.lib.composeExtensions (uv2nix-hammer-overrides.overrides_strict pkgs) (
            _final: prev: {
              asynclog = prev.asynclog.overrideAttrs (old: {
                buildInputs = (old.buildInputs or []) ++ [_final.setuptools _final.wheel];
              });
              proxy-utils = prev.proxy-utils.overrideAttrs (old: {
                buildInputs = (old.buildInputs or []) ++ [_final.poetry-core];
              });
              asyncpg = pythonPackages.asyncpg;
              dulwich = prev.dulwich.overrideAttrs (old: {
                buildInputs = (old.buildInputs or []) ++ [_final.setuptools _final.wheel];
              });
              autoflake = prev.autoflake.overrideAttrs (old: {
                postInstall = ''
                  rm $out/lib/python3.11/site-packages/README.md
                  rm $out/lib/python3.11/site-packages/LICENSE
                '';
              });
            }
          );
          editableOverlay = workspace.mkEditablePyprojectOverlay {
            # Use environment variable
            root = "$REPO_ROOT";
          };
          pythonSet =
            # Use base package set from pyproject.nix builders
            (pkgs.callPackage pyproject-nix.build.packages {
              inherit python;
            })
            .overrideScope
            (
              lib.composeManyExtensions [
                pyproject-build-systems.overlays.default
                overlay
                pyprojectOverrides
              ]
            );

          editablePythonSet = pythonSet.overrideScope editableOverlay;
          makeLibraryPath = packages: pkgs.lib.concatStringsSep ":" (map (package: "${pkgs.lib.getLib package}/lib") packages);
          libs = with pkgs; [
            openssl
            stdenv.cc.cc.lib
            libz
            glib
            postgresql
            postgresql.dev
          ];
          # Build virtual environment, with local packages being editable.
          #
          # Enable all optional dependencies for development.
          virtualenv = editablePythonSet.mkVirtualEnv "temporalio-playground-dev-env" workspace.deps.all;
        in
          pkgs.mkShell {
            packages = [
              pkgs.nixfmt-rfc-style
              virtualenv
              pkgs.uv
              pkgs.bun
              pkgs.just
              pkgs.supabase-cli
              pkgs.mdformat
            ];

            NIX_LD_LIBRARY_PATH = makeLibraryPath libs;
            shellHook = ''
              # Undo dependency propagation by nixpkgs.
              unset SOURCE_DATE_EPOCH
              unset PYTHONPATH
              export LD_LIBRARY_PATH=$NIX_LD_LIBRARY_PATH:$LD_LIBRARY_PATH
              # Get repository root using git. This is expanded at runtime by the editable `.pth` machinery.
              export REPO_ROOT=$(git rev-parse --show-toplevel)
              # Stop uv from syncing
              export UV_NO_SYNC=1
              export UV_PYTHON=$(which python)
              # Stop uv from downloading python
              export UV_PYTHON_DOWNLOADS=never
               ln -sfT ${virtualenv.out} ./.venv
              # Make uv use our Python.
              export PYTHONPATH=$PYTHONPATH:${virtualenv.out}/lib/python:${virtualenv.out}/lib/python3.11/site-packages
            '';
          };
      };
    };
}
